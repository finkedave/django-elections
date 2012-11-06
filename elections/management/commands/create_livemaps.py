import datetime
import os
import re

from dateutil.parser import parse as dateparse
from django.core.management.base import BaseCommand
from elections.settings import MAP_RESULTS_DEST
from elections.models import LiveMap, State

class Command(BaseCommand):
    def handle(self, *a,**kw):
        
        if len(a)!=2:
            print 'Wrong format. you must Specify date label, days_for_updates'
        label = a[0]
        days_for_updates = int(a[1])
        race_date = dateparse(label)
        livemaps_already_exist_count = 0
        livemaps_created = 0
        
        file_directory = os.path.join(MAP_RESULTS_DEST, str(race_date.year))

        files_in_directory = os.listdir(file_directory)
        
        pattern_without_seat = re.compile("(.+?)-(.+?)-(.+?).json" )
        pattern_with_seat = re.compile("(.+?)-(.+?)-(.+?)-(.+?).json")
        error = False
        for file_name in files_in_directory:
            if file_name.find(label)!=0:
                continue
            
            file_name_sub_str = file_name.replace('%s-' % label, '')
            
            dash_count = file_name_sub_str.count('-')
            if dash_count == 2:
                matches = pattern_without_seat.match(file_name_sub_str)
            elif dash_count >2:
                matches = pattern_with_seat.match(file_name_sub_str)
            else:
                # malformed file
                continue
            
            if not matches:
                continue
            
            match_group_tuple = matches.groups()
            state_postal = match_group_tuple[0][:2]
            race_type = match_group_tuple[1]
            office = match_group_tuple[2]
            if len(match_group_tuple)>3:
                seat_name = match_group_tuple[3]
            else:
                seat_name = None
            
            try:
                LiveMap.objects.get(state__postal=state_postal, race_type=race_type, office=office, 
                                 race_date=race_date, seat_name=seat_name)
                livemaps_already_exist_count += 1
            except LiveMap.DoesNotExist:
                live_map = LiveMap()
                try:
                    state = State.objects.get(postal=state_postal)
                except State.DoesNotExist:
                    print '**********Error: State with postal %s does not exist. Please '\
                         'create state first then try again' % state_postal
                    error = True
                    break
                live_map.state = state
                live_map.race_type = race_type
                live_map.office = office
                live_map.seat_name = seat_name
                live_map.json_file_name = file_name
                live_map.race_date = race_date
                live_map.update_results_start_date = datetime.datetime(
                            race_date.year, race_date.month, race_date.day, 0,0,0)
                live_map.update_results_end_date =  datetime.datetime(
                                race_date.year, race_date.month, race_date.day+days_for_updates, 23,59, 59)
                live_map.active = False
                live_map.save()
                livemaps_created += 1

        print "Summary"
        if error:
            "Error happened see above to fix and then try again."
        print 'Created %d live maps.' % livemaps_created
        print 'Skipped %d live maps. Already existed' % livemaps_already_exist_count