from django.core.management.base import LabelCommand
from elections.models import PastElectionResult

from elections.import_utils import populate_obj_w_import_data, create_checksum, normalize_data

class Command(LabelCommand):
    args = '[file1 file2 ...]'
    help = 'Imports election events'

    def handle_label(self, label, **options):
        import csv
        events = csv.reader(open(label, 'rb'), delimiter='|')
        added_count = 0
        skipped_count = 0
        modified_count = 0
        for row in events:
            checksum = create_checksum(row)
            row = normalize_data(row)
            try:
                past_election_result = PastElectionResult.objects.get(
                                                          election_id=row[0],
                                                          last_name=row[1],
                                                          first_name=row[2],
                                                          suffix=row[3],
                                                          party=row[4])
                if past_election_result.checksum != checksum.hexdigest():
                    populate_obj_w_import_data(past_election_result, row)
                    past_election_result.save()
                    modified_count += 1
                else:
                    skipped_count += 1
            except PastElectionResult.DoesNotExist:
                past_election_result = PastElectionResult()
                populate_obj_w_import_data(past_election_result, row)
                past_election_result.save()
                added_count += 1
        print "Summary"
        print 'Added %d past election results.' % added_count
        print "Modified %d past election results." % modified_count
        print 'Skipped %d past election results. No changes found' % skipped_count
        