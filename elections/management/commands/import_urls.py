import time
import datetime
import hashlib

from django.core.management.base import LabelCommand, CommandError
from elections.models import Candidate, CandidateURL

class Command(LabelCommand):
    args = '[file1 file2 ...]'
    help = 'Imports candidate urls'

    def handle_label(self, label, **options):
        import csv
        bios = csv.reader(open(label, 'rb'), delimiter='|')
        url_pk_list = []
        for row in bios:
            row[0] = int(row[0]) #politician id
            checksum = hashlib.md5()
            
            for item in row[:-1]:
                if item:
                    checksum.update(str(item))
                else:
                    checksum.update('')
            try:
                candidate, created = Candidate.objects.get_or_create(politician_id=row[0])
                if created:
                    print "Had to create the candidate"
                url = candidate.urls.get(url=row[1], description=row[2])
                url_pk_list.append(url.pk)
                if url.checksum != checksum.hexdigest():
                    url.url = row[1]
                    url.description = row[2]
                    print 'Updating %s' % (" ".join([row[2], row[1],]))
                    url.save()
                else:
                    print "Skipping %s. No change." % (" ".join([row[2], row[1],]))
            
            except CandidateURL.DoesNotExist:
                print 'Adding %s' % (" ".join([row[2], row[1],]))
                url = candidate.urls.create()
                url.url = row[1]
                url.description = row[2]
                url.save()
                url_pk_list.append(url.pk)
        removed_urls = CandidateURL.objects.exclude(pk__in=url_pk_list)
        print "%d urls were not found in the import file. Deleting records" % removed_urls.count()
        removed_urls.delete()