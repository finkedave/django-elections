import datetime

from django.core.management.base import LabelCommand

from elections.models import State, PresidentialElectionResult
from elections.import_utils import populate_obj_w_import_data, \
                                   create_checksum, normalize_data, create_date

class Command(LabelCommand):
    args = '[file1 file2 ...]'
    help = 'Imports election events'

    def handle_label(self, label, **options):
        import csv
        events = csv.reader(open(label, 'rb'), delimiter='|')
        for row in events:
            # normalize the data.
            row = normalize_data(row)
            
            # covert the date columns to actual dates
            if row[99]:
                row[99] =create_date(row[99])
            
            
            state_columns = row[0:3]
            # skip 3-12 this are election events that are on the calendar
            state_columns.extend(row[13:34])
            
            # Note this file is not normalized therefore after 2012 election, 
            # they will probably add 6 rows. Which
            # will have to be acounted for. So just in increase the 60 to 66 or whatever. Then add
            # those 6 rows to their own presidential election
            presidential_election_columns = row[34:60]
            state_columns.extend(row[60:])
            
            checksum = create_checksum(state_columns)
            state = None
            try:
                state = State.objects.get(state_id=row[0])
                if state.checksum != checksum.hexdigest():
                    populate_obj_w_import_data(state, state_columns)
                   
                    print 'Updating %s' % row[2]
                    state.save()
                else:
                    print "Skipping %s. No change." % row[2]
            except State.DoesNotExist:
                print 'Adding %s' % row[2]
                state = State()
                populate_obj_w_import_data(state, state_columns)
                state.save()
                
            votes_1976 = row[34:36]
            votes_1980 = row[36:38]
            votes_1984 = row[38:40]
            votes_1988 = row[40:42]
            votes_1992 = row[42:44]
            votes_1996 = row[44:46]
            votes_2000 = row[46:48]
            votes_2004 = row[48:50]
            votes_2008 = row[50:52]
            primary_2004 = row[52:56]
            primary_2008 = row[56:60]
            
            presidential_election_dict = {1976:votes_1976 + [None,None, None, None],
                                          1980:votes_1980 + [None,None, None, None],
                                          1984:votes_1984 + [None,None, None, None],
                                          1988:votes_1988 + [None,None, None, None],
                                          1992:votes_1992 + [None,None, None, None],
                                          1996:votes_1996 + [None,None, None, None],
                                          2000:votes_2000 + [None,None, None, None],
                                          2004:votes_2004 + primary_2004,
                                          2008:votes_2008 + primary_2008}
            for year, data in presidential_election_dict.items():
                # We also want year to be part of the data
                data.insert(0, year)
                checksum = create_checksum(data)
                try:
                    pres_election_result = PresidentialElectionResult.objects.get(
                                                        election_year=year, 
                                                        state=state.state_id)
                    if pres_election_result.checksum != checksum.hexdigest():
                        populate_obj_w_import_data(pres_election_result, data)
                        print 'Updating pres election result (%s-%s)' % (state, year)
                        pres_election_result.save()
                    else:
                        print "Skipping pres election (%s-%s). No change." % (state, year)
                except PresidentialElectionResult.DoesNotExist:
                    print 'Adding Presidential Election %s' % year
                    pres_election_result = PresidentialElectionResult()
                    populate_obj_w_import_data(pres_election_result, data)
                    pres_election_result.state = state
                    pres_election_result.save()
                    