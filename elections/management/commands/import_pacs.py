import time
import datetime
import hashlib

from django.core.management.base import LabelCommand, CommandError
from elections.models import Candidate, PACContribution
from elections.import_utils import create_date, populate_obj_w_import_data, \
                normalize_data, create_checksum
class Command(LabelCommand):
    args = '[file1 file2 ...]'
    help = 'Imports PAC contributions'

    def handle_label(self, label, **options):
        import csv
        bios = csv.reader(open(label, 'rb'), delimiter='|')
        fec_record_number_id_list = []
        added_count = 0
        skipped_count = 0
        modified_count = 0
        
        for row in bios:
            row[17] = create_date(row[17])

            try:
                row[18] = int(row[18])
            except ValueError:
                row[18] = 0
            row = normalize_data(row)
            
            fec_record_number_id_list.append(row[0])
            try:
                Candidate.objects.get(politician_id=row[4])
            except Candidate.DoesNotExist:
                # A 0 or something that doesn't a match a candiate should
                # be considered None since thats how it will in the DB
                row[4] = None
            checksum = create_checksum(row)
            
            try:
                contribution = PACContribution.objects.get(fec_record_number=row[0])
                if contribution.checksum != checksum.hexdigest():
                    populate_obj_w_import_data(contribution, row)
                   
                    modified_count += 1
                    contribution.save()
                else:
                    skipped_count += 1
            except PACContribution.DoesNotExist:
                added_count += 1
                contribution = PACContribution()
                populate_obj_w_import_data(contribution, row)
                contribution.save()
        # For all candiates that were missing in the files mark as inactive
        removed_pacs = PACContribution.objects.exclude(fec_record_number__in=fec_record_number_id_list)
        removed_count = removed_pacs.count()
        removed_pacs.delete()
        print "Summary"
        print 'Added %d past election results.' % added_count
        print "Modified %d past election results." % modified_count
        print 'Skipped %d past election results. No changes found' % skipped_count
        if removed_count:
            print "%d PAC(s) were not found in the import file. Removing these PACS" % removed_count