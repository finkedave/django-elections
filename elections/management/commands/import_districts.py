import datetime

from django.core.management.base import LabelCommand
from elections.import_utils import populate_obj_w_import_data, create_checksum, \
                                   normalize_data
from elections.models import District

class Command(LabelCommand):
    args = '[file1 file2 ...]'
    help = 'Imports election events'

    def handle_label(self, label, **options):
        import csv
        events = csv.reader(open(label, 'rb'), delimiter='|')
        for row in events:
            row = normalize_data(row)
            
            # turn the columns that re dates into dates
            if row[32]:
                row[32] = datetime.datetime.strptime(row[32], "%Y-%m").date()
            checksum = create_checksum(row)
            try:
                district = District.objects.get(district_id=row[0])
                if district.checksum != checksum.hexdigest():
                    populate_obj_w_import_data(district, row)
                   
                    print 'Updating district %s' % district.district_id
                    district.save()
                else:
                    print "Skipping district %s. No change." % district.district_id
            except District.DoesNotExist:
                district = District()
                populate_obj_w_import_data(district, row)
                district.save()
                print 'Adding district %s' % district.district_id