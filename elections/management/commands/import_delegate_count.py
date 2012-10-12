"""
This script is used to create and update delegate counter tables. Command arguments 
are required
"""
from cStringIO import StringIO
import os
from ftplib import FTP
from xml.dom.minidom import parseString

from django.core.management.base import BaseCommand, CommandError
from elections.models import DelegateElection, CandidateDelegateCount, \
                            Candidate, State, ElectionEvent, DelegateStateElection
from elections.settings import FTP_USER, FTP_PASSWORD, FTP_HOST
from elections import to_bool

class Command(BaseCommand):
    def handle(self, *a,**kw):
        """ Sending the the correct year and race if very important. Once AP switches exporting
        the delegate report based on another election. These variables must be changed so as
        not to override older elections """
        if len(a) < 2:
            raise CommandError('Command arguments (year and race) type are required. [force, path to file]')
        year = int(a[0])
        race_type = a[1]
        if len(a)>3:
            force = to_bool(a[2])
        else:
            force = None
        if len (a)==4:
            ftp_dir = a[3]
        else:
            ftp_dir = '/Delegate_Tracking/Reports'
        created_delegate_count = 0
        updated_delegate_count = 0
        skipped_delegate_count = 0
        buffer_ = StringIO()
        
        full_path = os.path.join(ftp_dir, 'delstate.xml')
        # Craft an FTP command that can pull the file
        cmd = 'RETR %s' % full_path
        # Connect to the FTP server, issue the command and catch the data
        # in our buffer file object.
        try:
            ftp = FTP(FTP_HOST, FTP_USER, FTP_PASSWORD)
            ftp.retrbinary(cmd, buffer_.write)
        except Exception, e:
            print cmd
            if "550 The system cannot find the" in e.message:
                raise FileDoesNotExistError("The file you've requested does not exist." +
                    " If you're looking for data about a state, make sure you" +
                    " input valid postal codes. If you're looking for a date," +
                    " make sure it's correct.")
            elif "530 User cannot log in" in e.message:
                raise BadCredentialsError("The username and password you submitted" +
                " are not accepted by the AP's FTP.")
            else:
                raise e
        
        # Now go through the file and extract data from it
        dom = parseString(buffer_.getvalue()).getElementsByTagName('delState')[0]
        
        # For each delegate eleciton. In the case of primaries, Both Democrat and 
        # Republicans have records
        for node in dom.getElementsByTagName('del'):
            delegates_needed = int(node.getAttribute('dNeed'))
            total_delegates = int(node.getAttribute('dVotes'))
            party_id = node.getAttribute('pId')
            
            if race_type=='primary':
                de_race_type = '%sPrim' % party_id
            elif race_type=='caucus':
                de_race_type = '%sCauc' % party_id
            else:
                de_race_type = 'General'
            try:
               
                delegate_election = DelegateElection.objects.get(year=year,
                                                                     race_type=de_race_type)
                # This is a double check once AP switches the fiole to report on a different
                # race/year. We don't want to overwrite data that we shouldn't be
                if delegate_election.delegates_needed != delegates_needed or \
                       total_delegates !=  delegate_election.total_delegates:
                    if force:
                        delegate_election.delegates_needed = delegates_needed
                        delegate_election.total_delegates = total_delegates
                        delegate_election.save()
                    else:
                        raise CommandError('Looking up the Delegate Election using year, race type and party.'
                                       'Delegates needed and or Total Delegates changed. Thus implying '
                                       'that AP has started running a new race with this report. Please '
                                       'double check and either change race_type and year or send in force '
                                       '= True attribute. Note sending in True for force and if your not positive '
                                       'these values are supposed to change might destroy all past data.')
            except DelegateElection.DoesNotExist:
                delegate_election = DelegateElection()
                delegate_election.race_type = de_race_type
                delegate_election.year = year
                delegate_election.delegates_needed = delegates_needed
                delegate_election.total_delegates = total_delegates
                delegate_election.save()
                print "Creating delegate election %s %s - %s" %(year, party_id, race_type)
            
            # For each state create a state election
            for node in node.getElementsByTagName('State'):
                state_id = node.getAttribute('sId')

                try:
                    delegate_state_election = DelegateStateElection.objects.get(
                                                  delegate_election=delegate_election,
                                                  state=state_id)
                    if not delegate_state_election.event_date:
                        # calendar might have been updated therefore just to make sure
                        # we can't populate it now
                        set_election_event_date(delegate_state_election)
                        delegate_state_election.save()
                except DelegateStateElection.DoesNotExist:
                    try:
                        state = State.objects.get(state_id=state_id)
                    except State.DoesNotExist:
                        state = State()
                        state.state_id = state_id
                        state.name = state_id
                        state.postal = state_id
                        state.save()
                    delegate_state_election = DelegateStateElection()
                    delegate_state_election.state = state
                    delegate_state_election. delegate_election=delegate_election
                    set_election_event_date(delegate_state_election)
                    delegate_state_election.save()
                    
                for node in node.getElementsByTagName('Cand'):
                    candidate_id = node.getAttribute('cId')
                    candidate_name = node.getAttribute('cName')
                    delegate_count = node.getAttribute('dTot')
                    
                    try:
                        delegate_count_obj = CandidateDelegateCount.objects.get(
                                                          candidate=candidate_id,
                                                          delegate_state_election=delegate_state_election)
                        if delegate_count_obj.delegate_count != int(delegate_count):
                            delegate_count_obj.delegate_count = delegate_count
                            delegate_count_obj.save()
                            updated_delegate_count += 1
                        else:
                            skipped_delegate_count += 1
                    except CandidateDelegateCount.DoesNotExist:
                        delegate_count_obj = CandidateDelegateCount()
                        try:
                            candidate = Candidate.objects.get(politician_id=candidate_id)
                        except Candidate.DoesNotExist:
                            # Create a blank candidate if needed
                            candidate = Candidate()
                            candidate.politician_id = candidate_id
                            candidate.ap_candidate_id = candidate_id
                            candidate.candidate_number = candidate_id
                            candidate.last_name = candidate_name
                            candidate.save()
                        delegate_count_obj.candidate = candidate
                        delegate_count_obj.delegate_count = delegate_count
                        delegate_count_obj.delegate_state_election = delegate_state_election
                        delegate_count_obj.save()
                        created_delegate_count += 1
                        
        print "Summary"
        print 'Added %d candidate delegate count(s).' % created_delegate_count
        print "Updated %d candidate delegate count(s)." % updated_delegate_count
        print 'Skipped %d candidate delegate count(s)' % skipped_delegate_count
        
def set_election_event_date(delegate_state_election):
    """ Set the event date based on some algorithms. Note this algorithm probably won't
    work for the general eleciton. But thats ok because it doesn't matter because all 
    races are on the same day """
    election_events = ElectionEvent.objects.filter(
                event_date__year=delegate_state_election.delegate_election.year, 
                state=delegate_state_election.state.state_id)
    count = election_events.count()
    
    if count > 1:
        # We need to filter it even more. Try to get it by party
        election_events_by_party = election_events.filter(
            description__icontains=delegate_state_election.delegate_election.get_party_display())
        count = election_events_by_party.count()
        if count == 0:
            # If that didn't work try to get it by race
            election_events = election_events.filter(
                description__icontains=delegate_state_election.delegate_election.get_race_type_display())
            count = election_events.count()
        else:
            election_events = election_events_by_party
    # If there are still more then 1. Leave the date blank, might need to find a better 
    # way to find it
    if count==1:
        delegate_state_election.event_date = election_events[0].event_date
    else:
        delegate_state_election.event_date = None
        
class FileDoesNotExistError(Exception):
    
   def __init__(self, value):
       self.parameter = value
    
   def __str__(self):
       return repr(self.parameter)
   
class BadCredentialsError(Exception):
    
   def __init__(self, value):
       self.parameter = value
    
   def __str__(self):
       return repr(self.parameter)