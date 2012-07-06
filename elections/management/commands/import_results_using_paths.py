""" Command for getting the top of the ticket results specifing the 
paths to the files """
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = """date path_to_delegate_data(ie /Delegate_Tracking/US/flat/archive) 
        path_to_inits (ie /inits/US/archive)"""
    help = 'Imports Top Of the Ticket results'

    def handle(self, *a,**kw):
        from elections.electionmap import write_results
        if len(a) < 3:
            raise CommandError('Command arguments directory is required')
        election_date = a[0]
        path_to_data= a[1] 
        path_to_inits= a[2]
        write_results(election_date, path_to_data, path_to_inits)
