from django.core.management.base import LabelCommand
from elections.models import Candidate, CandidateMoney
from elections.import_utils import create_date, populate_obj_w_import_data, \
                normalize_data, create_checksum
class Command(LabelCommand):
    args = '[file1 file2 ...]'
    help = 'Imports Candidate money info'

    def handle_label(self, label, **options):
        import csv
        bios = csv.reader(open(label, 'rb'), delimiter='|')
        candidate_id_list = []
        added_count = 0
        skipped_count = 0
        modified_count = 0
        
        for row in bios:
            row[13] = create_date(row[13])

            row = normalize_data(row)
            candidate_id_list.append(row[0])
            try:
                Candidate.objects.get(politician_id=row[0])
            except Candidate.DoesNotExist:
                # A 0 or something that doesn't a match a candiate should
                # be considered None since thats how it will in the DB
                row[0] = None
            checksum = create_checksum(row)
            
            try:
                candidate_money = CandidateMoney.objects.get(candidate=row[0])
                if candidate_money.checksum != checksum.hexdigest():
                    populate_obj_w_import_data(candidate_money, row)
                   
                    modified_count += 1
                    candidate_money.save()
                else:
                    skipped_count += 1
            except CandidateMoney.DoesNotExist:
                added_count += 1
                contribution = CandidateMoney()
                populate_obj_w_import_data(contribution, row)
                contribution.save()
        # For all candiates that were missing in the files mark as inactive
        removed_money = CandidateMoney.objects.exclude(candidate__in=candidate_id_list)
        removed_count = removed_money.count()
        removed_money.delete()
        print "Summary"
        print 'Added %d candidate money results.' % added_count
        print "Modified %d candidate money results." % modified_count
        print 'Skipped %d candidate money results. No changes found' % skipped_count
        if removed_count:
            print "%d candidate money were not found in the import file. "\
                   "Removing these money records" % removed_count