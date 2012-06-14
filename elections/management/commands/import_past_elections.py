from django.core.management.base import LabelCommand
from elections.models import PastElection

from elections.import_utils import populate_obj_w_import_data, \
                    create_checksum, normalize_data

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
            # normalize the data
            row = normalize_data(row)
            checksum = create_checksum(row)
            try:
                past_election = PastElection.objects.get(election_id=row[0])
                if past_election.checksum != checksum.hexdigest():
                    populate_obj_w_import_data(past_election, row)
                    past_election.save()
                    modified_count += 1
                else:
                    skipped_count += 1
            except PastElection.DoesNotExist:
                past_election = PastElection()
                populate_obj_w_import_data(past_election, row)
                past_election.save()
                added_count += 1
        print "Summary"
        print 'Added %d past elections.' % added_count
        print "Modified %d past elections." % modified_count
        print 'Skipped %d past elections. No changes found' % skipped_count