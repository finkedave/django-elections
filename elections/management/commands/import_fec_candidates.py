""" Module that imports FEC data into the database"""
import csv
import urllib

from django.core.management.base import BaseCommand
from elections.models import CandidateFEC
from elections.import_utils import create_date, populate_obj_w_import_data, \
                normalize_data, create_checksum
                
FEC_URL = "http://www.fec.gov/data/CandidateSummary.do?format=csv"
class Command(BaseCommand):
    args = '[file1 file2 ...]'
    help = 'Imports FEC candidates'

    def handle(self, *a,**kw):
        webpage = urllib.urlopen(FEC_URL)
        
        reader = csv.reader(webpage)
        fec_candidate_id_list = []
        added_count = 0
        skipped_count = 0
        modified_count = 0
        headerline = reader.next()
        for row in reader:
            # normalize all the data, the true means normalize the currency values too
            row = normalize_data(row, True)
            if row[48]:
                row[48] = create_date(row[48])
            if row[49]:
                row[49] = create_date(row[49])
            fec_candidate_id_list.append(row[1])

            checksum = create_checksum(row)
            try:
                candidate = CandidateFEC.objects.get(fec_candidate_id=row[1])
                if candidate.checksum != checksum.hexdigest():
                    populate_obj_w_import_data(candidate, row)
                    modified_count += 1
                    candidate.save()
                else:
                    skipped_count += 1
            except CandidateFEC.DoesNotExist:
                added_count += 1
                candidate = CandidateFEC()
                populate_obj_w_import_data(candidate, row)
                candidate.save()
        # For all candiates that were missing in the files mark as inactive
        removed_candidates = CandidateFEC.objects.exclude(fec_candidate_id__in=fec_candidate_id_list)
        removed_count = removed_candidates.count()
        removed_candidates.delete()
        print "Summary"
        print 'Added %d FEC Candidates.' % added_count
        print "Modified %d FEC Candidates." % modified_count
        print 'Skipped %d FEC Candidates. No changes found' % skipped_count
        if removed_count:
            print "%d FEC Candidates were not found in the import file. Removing these FEC Candidates" % removed_count