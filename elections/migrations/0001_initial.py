# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Candidate'
        db.create_table('elections_candidate', (
            ('test_flag', self.gf('elections.fields.TestFlagField')(default='l', max_length=1)),
            ('politician_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('ap_candidate_id', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('candidate_number', self.gf('django.db.models.fields.IntegerField')()),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('junior', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('use_junior', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('year_first_elected', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('birth_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('birth_place', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('birth_state', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('birth_province', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('birth_country', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('residence_place', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('residence_state', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('ethnicity', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('hispanic', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('religion', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('biography', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('profile', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('campaigns', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('photo_fk', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='alternate_photo', null=True, to=orm['massmedia.Image'])),
            ('thumbnail_fk', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='alternate_thumbnail', null=True, to=orm['massmedia.Image'])),
            ('photo', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('photo_width', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('photo_height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('thumbnail', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('thumbnail_width', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('thumbnail_height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('is_presidential_candidate', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('elections', ['Candidate'])

        # Adding model 'RaceCounty'
        db.create_table('elections_racecounty', (
            ('test_flag', self.gf('elections.fields.TestFlagField')(default='l', max_length=1)),
            ('race_county_id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('race_number', self.gf('django.db.models.fields.IntegerField')()),
            ('election_date', self.gf('django.db.models.fields.DateField')()),
            ('state_postal', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('county_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('fips_code', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('county_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('office_id', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('race_type_id', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('seat_number', self.gf('django.db.models.fields.IntegerField')()),
            ('office_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('seat_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('race_type_party', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('race_type', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('office_description', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('number_of_winners', self.gf('django.db.models.fields.IntegerField')()),
            ('number_in_runoff', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('precincts_reporting', self.gf('django.db.models.fields.IntegerField')()),
            ('total_precincts', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('elections', ['RaceCounty'])

        # Adding model 'RaceDistrict'
        db.create_table('elections_racedistrict', (
            ('test_flag', self.gf('elections.fields.TestFlagField')(default='l', max_length=1)),
            ('race_district_id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('race_number', self.gf('django.db.models.fields.IntegerField')()),
            ('election_date', self.gf('django.db.models.fields.DateField')()),
            ('state_postal', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('district_type', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('cd_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('district_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('office_id', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('race_type_id', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('seat_number', self.gf('django.db.models.fields.IntegerField')()),
            ('office_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('seat_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('race_type_party', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('race_type', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('office_description', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('number_of_winners', self.gf('django.db.models.fields.IntegerField')()),
            ('number_in_runoff', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('precincts_reporting', self.gf('django.db.models.fields.IntegerField')()),
            ('total_precincts', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('elections', ['RaceDistrict'])

        # Adding model 'CountyResult'
        db.create_table('elections_countyresult', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('test_flag', self.gf('elections.fields.TestFlagField')(default='l', max_length=1)),
            ('race_county', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elections.RaceCounty'])),
            ('ap_candidate', self.gf('django.db.models.fields.related.ForeignKey')(related_name='county_results', to_field='ap_candidate_id', to=orm['elections.Candidate'])),
            ('party', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('incumbent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('vote_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('winner', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('natl_order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('elections', ['CountyResult'])

        # Adding model 'DistrictResult'
        db.create_table('elections_districtresult', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('test_flag', self.gf('elections.fields.TestFlagField')(default='l', max_length=1)),
            ('race_district', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elections.RaceDistrict'])),
            ('ap_candidate', self.gf('django.db.models.fields.related.ForeignKey')(related_name='district_results', to_field='ap_candidate_id', to=orm['elections.Candidate'])),
            ('party', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('incumbent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('vote_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('delegate_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('winner', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('natl_order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('elections', ['DistrictResult'])

        # Adding model 'CandidateOffice'
        db.create_table('elections_candidateoffice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('candidate', self.gf('django.db.models.fields.related.ForeignKey')(related_name='offices', to=orm['elections.Candidate'])),
            ('office_id', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('district_number', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
            ('party_id', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('status_id', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('office', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('state_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('district_name', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('party_name', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('office_description', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('status_description', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('next_election', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('checksum', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('elections', ['CandidateOffice'])

        # Adding model 'CandidateEducation'
        db.create_table('elections_candidateeducation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('candidate', self.gf('django.db.models.fields.related.ForeignKey')(related_name='education', to=orm['elections.Candidate'])),
            ('school_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('school_type', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('major', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('degree', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('school_city', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('school_state', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('school_province', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('school_country', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('checksum', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('elections', ['CandidateEducation'])

        # Adding model 'CandidatePhone'
        db.create_table('elections_candidatephone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('candidate', self.gf('django.db.models.fields.related.ForeignKey')(related_name='phones', to=orm['elections.Candidate'])),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('extension', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('detail', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('checksum', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('elections', ['CandidatePhone'])

        # Adding model 'CandidateURL'
        db.create_table('elections_candidateurl', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('candidate', self.gf('django.db.models.fields.related.ForeignKey')(related_name='urls', to=orm['elections.Candidate'])),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('checksum', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('elections', ['CandidateURL'])

        # Adding model 'CandidateMedia'
        db.create_table('elections_candidatemedia', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('candidate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elections.Candidate'])),
            ('medium_type', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('file_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('file_extension', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('checksum', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('elections', ['CandidateMedia'])

        # Adding model 'CandidateMoney'
        db.create_table('elections_candidatemoney', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('candidate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elections.Candidate'])),
            ('fec_candidate_id', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('fec_office_id', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('fec_postal_id', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('fec_district_id', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('total_receipts', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('candidate_loans', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('other_loans', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('candidate_loan_repayments', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('other_loan_repayments', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('individual_contributions', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('pac_contributions', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('ending_cash', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('date_of_last_report', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('total_disbursements', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('checksum', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('elections', ['CandidateMoney'])

        # Adding model 'CandidateFEC'
        db.create_table('elections_candidatefec', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('committee_link', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('fec_candidate_id', self.gf('django.db.models.fields.CharField')(max_length=9, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=90, null=True, blank=True)),
            ('office', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('office_state', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('district_number', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('party', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('mailing_addr1', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('mailing_addr2', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('mailing_city', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('mailing_state', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('mailing_zipcode', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('individual_itemized_contrib', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('individual_unitemized_contrib', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('individual_contrib', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('party_committee_contrib', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('other_committee_contrib', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('candidate_contrib', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('total_contrib', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('transfer_from_other_commitee', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('candidate_loan', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('other_loan', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('total_loan', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('offsets_to_operating_expenditures', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('offsets_to_fundraising', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('offsets_to_legal_accounting', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('other_receipts', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('total_receipts', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('operating_expenditure', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('exempt_legal_accounting_disbursement', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('fundraising_disbursement', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('transfer_to_other_committee', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('candidate_loan_repayment', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('other_loan_repayment', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('total_loan_repayment', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('individual_refund', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('party_committee_refund', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('other_committee_refund', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('total_contribution_refund', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('other_disbursement', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('total_disbursement', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('cash_on_hand_beginning_of_period', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('cash_on_hand_close_of_period', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('net_contribution', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('net_operating_expenditure', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('debt_owed_by_committee', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('debt_owed_to_committee', self.gf('elections.models.CurrencyField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('coverage_start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('coverage_end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('checksum', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('elections', ['CandidateFEC'])

        # Adding model 'ElectionEvent'
        db.create_table('elections_electionevent', (
            ('event_code', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('state_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('event_date', self.gf('django.db.models.fields.DateField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('checksum', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('elections', ['ElectionEvent'])

        # Adding model 'PACContribution'
        db.create_table('elections_paccontribution', (
            ('fec_record_number', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('fec_pac_id', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('pac_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('recipient_committee', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('candidate', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='pac_contributions', null=True, to=orm['elections.Candidate'])),
            ('office_id', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('district_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('party_id', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('fec_candidate_id', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('office', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('state_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('district_name', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('party_name', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('date_given', self.gf('django.db.models.fields.DateField')()),
            ('amount', self.gf('django.db.models.fields.IntegerField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('checksum', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('elections', ['PACContribution'])

        # Adding model 'State'
        db.create_table('elections_state', (
            ('population', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('white_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('black_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('indian_alaska_native_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('asian_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('hawian_pacific_islander_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('mixed_race_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('other_race_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('hispanic_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('non_hispanic_white_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('non_hispanic_black_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('households_all_speak_other_than_english_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('median_household_income', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('married_couple_both_work_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('income_poverty_1999_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('different_house_in_1995_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('homes_heated_elec_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('homes_heated_gas_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('homes_heated_coal_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('homes_heated_fuel_oil_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('populations_65_and_up_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('employed_civilians_16_and_up_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('college_degree_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('management_professional_worker_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('sales_office_worker_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('production_transport_worker_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('unemployment_current', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('unemployment_date_current', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('unemployment_monthly_change', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('married_couple_family_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('married_couple_family_w_children_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('unmarried_partner_households_m_with_m_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('unmarried_partner_households_f_with_f_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('state_id', self.gf('django.db.models.fields.CharField')(max_length=2, primary_key=True)),
            ('postal', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('us_senate_split', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('us_house_split', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('state_sentate_split', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('state_house_split', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('president', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('governor', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('us_senate_1', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('us_senate_2', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('us_house', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('questions', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('other_races', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('state_summary', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('capitol', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('bird', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('flower', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('motto_english', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('motto_other', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('electoral_votes', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('dem_delegates', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('rep_delegates', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('sos_last_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('sos_first_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('sos_middle_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('sos_suffix', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('sos_address', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('sos_city', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('sos_state', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('sos_zip', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('sos_phone', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('sos_fax', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('sos_email', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('sos_url', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('livemap_state_id', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=5, blank=True)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=5, blank=True)),
            ('livemap_state_zoom', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('checksum', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('elections', ['State'])

        # Adding model 'PresidentialElectionResult'
        db.create_table('elections_presidentialelectionresult', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elections.State'])),
            ('election_year', self.gf('django.db.models.fields.IntegerField')()),
            ('dem_vote', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('rep_vote', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('dem_pres_primary_winner', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('dem_pres_primary_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('rep_pres_primary_winner', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('rep_pres_primary_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('checksum', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('elections', ['PresidentialElectionResult'])

        # Adding unique constraint on 'PresidentialElectionResult', fields ['state', 'election_year']
        db.create_unique('elections_presidentialelectionresult', ['state_id', 'election_year'])

        # Adding model 'District'
        db.create_table('elections_district', (
            ('population', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('white_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('black_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('indian_alaska_native_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('asian_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('hawian_pacific_islander_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('mixed_race_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('other_race_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('hispanic_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('non_hispanic_white_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('non_hispanic_black_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('households_all_speak_other_than_english_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('median_household_income', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('married_couple_both_work_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('income_poverty_1999_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('different_house_in_1995_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('homes_heated_elec_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('homes_heated_gas_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('homes_heated_coal_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('homes_heated_fuel_oil_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('populations_65_and_up_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('employed_civilians_16_and_up_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('college_degree_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('management_professional_worker_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('sales_office_worker_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('production_transport_worker_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('unemployment_current', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('unemployment_date_current', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('unemployment_monthly_change', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('married_couple_family_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('married_couple_family_w_children_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('unmarried_partner_households_m_with_m_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('unmarried_partner_households_f_with_f_percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('district_id', self.gf('django.db.models.fields.CharField')(max_length=10, primary_key=True)),
            ('district_number', self.gf('django.db.models.fields.IntegerField')()),
            ('state_postal', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('state_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('district_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('general_summary', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('checksum', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('elections', ['District'])

        # Adding model 'PastElection'
        db.create_table('elections_pastelection', (
            ('election_id', self.gf('django.db.models.fields.CharField')(max_length=15, primary_key=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('state_postal', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('office', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('election_type', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('district_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('party', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('state_name', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('office_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('election_type_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('district_name', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('party_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('checksum', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('elections', ['PastElection'])

        # Adding model 'PastElectionResult'
        db.create_table('elections_pastelectionresult', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('election_id', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('suffix', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('party', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('vote', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('percent', self.gf('elections.models.PercentField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('winner', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('checksum', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('elections', ['PastElectionResult'])

        # Adding unique constraint on 'PastElectionResult', fields ['election_id', 'last_name', 'first_name', 'suffix', 'party']
        db.create_unique('elections_pastelectionresult', ['election_id', 'last_name', 'first_name', 'suffix', 'party'])

        # Adding model 'LiveMap'
        db.create_table('elections_livemap', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elections.State'])),
            ('race_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('party', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('race_date', self.gf('django.db.models.fields.DateField')()),
            ('delegate_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('json_file_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('state_notice', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('update_results_start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('update_results_end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('template_name', self.gf('django.db.models.fields.CharField')(default='elections/live_maps/liveresults.html', max_length=70)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('elections', ['LiveMap'])

        # Adding model 'DelegateElection'
        db.create_table('elections_delegateelection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('party', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('race_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('total_delegates', self.gf('django.db.models.fields.IntegerField')()),
            ('delegates_needed', self.gf('django.db.models.fields.IntegerField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('elections', ['DelegateElection'])

        # Adding model 'DelegateStateElection'
        db.create_table('elections_delegatestateelection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('delegate_election', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elections.DelegateElection'])),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elections.State'])),
        ))
        db.send_create_signal('elections', ['DelegateStateElection'])

        # Adding model 'CandidateDelegateCount'
        db.create_table('elections_candidatedelegatecount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('delegate_state_election', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elections.DelegateStateElection'])),
            ('candidate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elections.Candidate'])),
            ('delegate_count', self.gf('django.db.models.fields.IntegerField')()),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('elections', ['CandidateDelegateCount'])

        # Adding model 'Poll'
        db.create_table('elections_poll', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elections.State'], null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('office', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('elections', ['Poll'])

        # Adding model 'PollResult'
        db.create_table('elections_pollresult', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elections.Poll'])),
            ('candidate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elections.Candidate'], null=True, blank=True)),
            ('write_in_candidate_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('result', self.gf('elections.models.PercentField')(max_digits=5, decimal_places=2)),
        ))
        db.send_create_signal('elections', ['PollResult'])

        # Adding model 'HotRace'
        db.create_table('elections_hotrace', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elections.State'], null=True, blank=True)),
            ('office', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('editorial_note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('elections', ['HotRace'])

        # Adding model 'HotRaceCandidate'
        db.create_table('elections_hotracecandidate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hot_race', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elections.HotRace'])),
            ('candidate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elections.Candidate'], null=True, blank=True)),
            ('write_in_candidate_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('elections', ['HotRaceCandidate'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'PastElectionResult', fields ['election_id', 'last_name', 'first_name', 'suffix', 'party']
        db.delete_unique('elections_pastelectionresult', ['election_id', 'last_name', 'first_name', 'suffix', 'party'])

        # Removing unique constraint on 'PresidentialElectionResult', fields ['state', 'election_year']
        db.delete_unique('elections_presidentialelectionresult', ['state_id', 'election_year'])

        # Deleting model 'Candidate'
        db.delete_table('elections_candidate')

        # Deleting model 'RaceCounty'
        db.delete_table('elections_racecounty')

        # Deleting model 'RaceDistrict'
        db.delete_table('elections_racedistrict')

        # Deleting model 'CountyResult'
        db.delete_table('elections_countyresult')

        # Deleting model 'DistrictResult'
        db.delete_table('elections_districtresult')

        # Deleting model 'CandidateOffice'
        db.delete_table('elections_candidateoffice')

        # Deleting model 'CandidateEducation'
        db.delete_table('elections_candidateeducation')

        # Deleting model 'CandidatePhone'
        db.delete_table('elections_candidatephone')

        # Deleting model 'CandidateURL'
        db.delete_table('elections_candidateurl')

        # Deleting model 'CandidateMedia'
        db.delete_table('elections_candidatemedia')

        # Deleting model 'CandidateMoney'
        db.delete_table('elections_candidatemoney')

        # Deleting model 'CandidateFEC'
        db.delete_table('elections_candidatefec')

        # Deleting model 'ElectionEvent'
        db.delete_table('elections_electionevent')

        # Deleting model 'PACContribution'
        db.delete_table('elections_paccontribution')

        # Deleting model 'State'
        db.delete_table('elections_state')

        # Deleting model 'PresidentialElectionResult'
        db.delete_table('elections_presidentialelectionresult')

        # Deleting model 'District'
        db.delete_table('elections_district')

        # Deleting model 'PastElection'
        db.delete_table('elections_pastelection')

        # Deleting model 'PastElectionResult'
        db.delete_table('elections_pastelectionresult')

        # Deleting model 'LiveMap'
        db.delete_table('elections_livemap')

        # Deleting model 'DelegateElection'
        db.delete_table('elections_delegateelection')

        # Deleting model 'DelegateStateElection'
        db.delete_table('elections_delegatestateelection')

        # Deleting model 'CandidateDelegateCount'
        db.delete_table('elections_candidatedelegatecount')

        # Deleting model 'Poll'
        db.delete_table('elections_poll')

        # Deleting model 'PollResult'
        db.delete_table('elections_pollresult')

        # Deleting model 'HotRace'
        db.delete_table('elections_hotrace')

        # Deleting model 'HotRaceCandidate'
        db.delete_table('elections_hotracecandidate')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'elections.candidate': {
            'Meta': {'ordering': "('last_name', 'first_name')", 'object_name': 'Candidate'},
            'ap_candidate_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'biography': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'birth_country': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'birth_place': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'birth_province': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'birth_state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'campaigns': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'candidate_number': ('django.db.models.fields.IntegerField', [], {}),
            'ethnicity': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'hispanic': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_presidential_candidate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'junior': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'photo_fk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'alternate_photo'", 'null': 'True', 'to': "orm['massmedia.Image']"}),
            'photo_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'photo_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'politician_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'profile': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'religion': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'residence_place': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'residence_state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'test_flag': ('elections.fields.TestFlagField', [], {'default': "'l'", 'max_length': '1'}),
            'thumbnail': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'thumbnail_fk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'alternate_thumbnail'", 'null': 'True', 'to': "orm['massmedia.Image']"}),
            'thumbnail_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thumbnail_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'use_junior': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'year_first_elected': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'elections.candidatedelegatecount': {
            'Meta': {'ordering': "['delegate_count']", 'object_name': 'CandidateDelegateCount'},
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.Candidate']"}),
            'delegate_count': ('django.db.models.fields.IntegerField', [], {}),
            'delegate_state_election': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.DelegateStateElection']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'elections.candidateeducation': {
            'Meta': {'object_name': 'CandidateEducation'},
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'education'", 'to': "orm['elections.Candidate']"}),
            'checksum': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'degree': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'major': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'school_city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'school_country': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'school_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'school_province': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'school_state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'school_type': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        'elections.candidatefec': {
            'Meta': {'ordering': "['office_state', 'name']", 'object_name': 'CandidateFEC'},
            'candidate_contrib': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'candidate_loan': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'candidate_loan_repayment': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'cash_on_hand_beginning_of_period': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'cash_on_hand_close_of_period': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'checksum': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'committee_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'coverage_end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'coverage_start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'debt_owed_by_committee': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'debt_owed_to_committee': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'district_number': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'exempt_legal_accounting_disbursement': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'fec_candidate_id': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True', 'blank': 'True'}),
            'fundraising_disbursement': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'individual_contrib': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'individual_itemized_contrib': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'individual_refund': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'individual_unitemized_contrib': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'mailing_addr1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'mailing_addr2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'mailing_city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'mailing_state': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'mailing_zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '90', 'null': 'True', 'blank': 'True'}),
            'net_contribution': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'net_operating_expenditure': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'office': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'office_state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'offsets_to_fundraising': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'offsets_to_legal_accounting': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'offsets_to_operating_expenditures': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'operating_expenditure': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'other_committee_contrib': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'other_committee_refund': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'other_disbursement': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'other_loan': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'other_loan_repayment': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'other_receipts': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'party': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'party_committee_contrib': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'party_committee_refund': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'total_contrib': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'total_contribution_refund': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'total_disbursement': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'total_loan': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'total_loan_repayment': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'total_receipts': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'transfer_from_other_commitee': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'transfer_to_other_committee': ('elections.models.CurrencyField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'})
        },
        'elections.candidatemedia': {
            'Meta': {'object_name': 'CandidateMedia'},
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.Candidate']"}),
            'checksum': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'file_extension': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium_type': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        'elections.candidatemoney': {
            'Meta': {'object_name': 'CandidateMoney'},
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.Candidate']"}),
            'candidate_loan_repayments': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'candidate_loans': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'checksum': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'date_of_last_report': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'ending_cash': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fec_candidate_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'fec_district_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'fec_office_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'fec_postal_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'individual_contributions': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'other_loan_repayments': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'other_loans': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pac_contributions': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_disbursements': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_receipts': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'elections.candidateoffice': {
            'Meta': {'ordering': "['state', 'office', 'district_name']", 'object_name': 'CandidateOffice'},
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'offices'", 'to': "orm['elections.Candidate']"}),
            'checksum': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'district_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'district_number': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'next_election': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'office': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'office_description': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'office_id': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'party_id': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'party_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'state_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'status_description': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'status_id': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'})
        },
        'elections.candidatephone': {
            'Meta': {'object_name': 'CandidatePhone'},
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'phones'", 'to': "orm['elections.Candidate']"}),
            'checksum': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'detail': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'extension': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        },
        'elections.candidateurl': {
            'Meta': {'object_name': 'CandidateURL'},
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'urls'", 'to': "orm['elections.Candidate']"}),
            'checksum': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'elections.countyresult': {
            'Meta': {'object_name': 'CountyResult'},
            'ap_candidate': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'county_results'", 'to_field': "'ap_candidate_id'", 'to': "orm['elections.Candidate']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incumbent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'natl_order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'party': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'race_county': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.RaceCounty']"}),
            'test_flag': ('elections.fields.TestFlagField', [], {'default': "'l'", 'max_length': '1'}),
            'vote_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'winner': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'})
        },
        'elections.delegateelection': {
            'Meta': {'ordering': "['-year', 'party']", 'object_name': 'DelegateElection'},
            'delegates_needed': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'party': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'race_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'total_delegates': ('django.db.models.fields.IntegerField', [], {}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'elections.delegatestateelection': {
            'Meta': {'ordering': "['state__name']", 'object_name': 'DelegateStateElection'},
            'delegate_election': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.DelegateElection']"}),
            'event_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.State']"})
        },
        'elections.district': {
            'Meta': {'ordering': "['state_postal', 'district_number']", 'object_name': 'District'},
            'asian_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'black_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'checksum': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'college_degree_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'different_house_in_1995_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'district_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'}),
            'district_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'district_number': ('django.db.models.fields.IntegerField', [], {}),
            'employed_civilians_16_and_up_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'general_summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'hawian_pacific_islander_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'hispanic_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'homes_heated_coal_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'homes_heated_elec_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'homes_heated_fuel_oil_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'homes_heated_gas_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'households_all_speak_other_than_english_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'income_poverty_1999_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'indian_alaska_native_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'management_professional_worker_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'married_couple_both_work_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'married_couple_family_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'married_couple_family_w_children_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'median_household_income': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mixed_race_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'non_hispanic_black_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'non_hispanic_white_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'other_race_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'population': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'populations_65_and_up_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'production_transport_worker_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'sales_office_worker_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'state_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'state_postal': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'unemployment_current': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'unemployment_date_current': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'unemployment_monthly_change': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'unmarried_partner_households_f_with_f_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'unmarried_partner_households_m_with_m_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'white_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'})
        },
        'elections.districtresult': {
            'Meta': {'object_name': 'DistrictResult'},
            'ap_candidate': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'district_results'", 'to_field': "'ap_candidate_id'", 'to': "orm['elections.Candidate']"}),
            'delegate_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incumbent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'natl_order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'party': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'race_district': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.RaceDistrict']"}),
            'test_flag': ('elections.fields.TestFlagField', [], {'default': "'l'", 'max_length': '1'}),
            'vote_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'winner': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'})
        },
        'elections.electionevent': {
            'Meta': {'ordering': "['event_date', 'state_name']", 'object_name': 'ElectionEvent'},
            'checksum': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'event_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'event_date': ('django.db.models.fields.DateField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'state_name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'elections.hotrace': {
            'Meta': {'ordering': "['date']", 'object_name': 'HotRace'},
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'editorial_note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'office': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.State']", 'null': 'True', 'blank': 'True'})
        },
        'elections.hotracecandidate': {
            'Meta': {'object_name': 'HotRaceCandidate'},
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.Candidate']", 'null': 'True', 'blank': 'True'}),
            'hot_race': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.HotRace']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'write_in_candidate_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'elections.livemap': {
            'Meta': {'ordering': "['-race_date', 'race_type', 'party']", 'object_name': 'LiveMap'},
            'delegate_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'json_file_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'party': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'race_date': ('django.db.models.fields.DateField', [], {}),
            'race_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.State']"}),
            'state_notice': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'template_name': ('django.db.models.fields.CharField', [], {'default': "'elections/live_maps/liveresults.html'", 'max_length': '70'}),
            'update_results_end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'update_results_start_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        'elections.paccontribution': {
            'Meta': {'ordering': "['-date_given']", 'object_name': 'PACContribution'},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pac_contributions'", 'null': 'True', 'to': "orm['elections.Candidate']"}),
            'checksum': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'date_given': ('django.db.models.fields.DateField', [], {}),
            'district_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'district_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fec_candidate_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'fec_pac_id': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'fec_record_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'office': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'office_id': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'pac_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'party_id': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'party_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'recipient_committee': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'state_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'elections.pastelection': {
            'Meta': {'ordering': "['state_postal', 'district_number', '-year', 'party']", 'object_name': 'PastElection'},
            'checksum': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'district_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'district_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'election_id': ('django.db.models.fields.CharField', [], {'max_length': '15', 'primary_key': 'True'}),
            'election_type': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'election_type_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'office': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'office_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'party': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'party_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'state_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'state_postal': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'elections.pastelectionresult': {
            'Meta': {'ordering': "['party', 'last_name']", 'unique_together': "(['election_id', 'last_name', 'first_name', 'suffix', 'party'],)", 'object_name': 'PastElectionResult'},
            'checksum': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'election_id': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'party': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'suffix': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'vote': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'winner': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        'elections.poll': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Poll'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'office': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.State']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'elections.pollresult': {
            'Meta': {'ordering': "['-result']", 'object_name': 'PollResult'},
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.Candidate']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.Poll']"}),
            'result': ('elections.models.PercentField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'write_in_candidate_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'elections.presidentialelectionresult': {
            'Meta': {'ordering': "['-election_year']", 'unique_together': "(('state', 'election_year'),)", 'object_name': 'PresidentialElectionResult'},
            'checksum': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'dem_pres_primary_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'dem_pres_primary_winner': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'dem_vote': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'election_year': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rep_pres_primary_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'rep_pres_primary_winner': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rep_vote': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.State']"})
        },
        'elections.racecounty': {
            'Meta': {'object_name': 'RaceCounty'},
            'county_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'county_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'election_date': ('django.db.models.fields.DateField', [], {}),
            'fips_code': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'number_in_runoff': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'number_of_winners': ('django.db.models.fields.IntegerField', [], {}),
            'office_description': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'office_id': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'office_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'precincts_reporting': ('django.db.models.fields.IntegerField', [], {}),
            'race_county_id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'race_number': ('django.db.models.fields.IntegerField', [], {}),
            'race_type': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'race_type_id': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'race_type_party': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'seat_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'seat_number': ('django.db.models.fields.IntegerField', [], {}),
            'state_postal': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'test_flag': ('elections.fields.TestFlagField', [], {'default': "'l'", 'max_length': '1'}),
            'total_precincts': ('django.db.models.fields.IntegerField', [], {})
        },
        'elections.racedistrict': {
            'Meta': {'object_name': 'RaceDistrict'},
            'cd_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'district_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'district_type': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'election_date': ('django.db.models.fields.DateField', [], {}),
            'number_in_runoff': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'number_of_winners': ('django.db.models.fields.IntegerField', [], {}),
            'office_description': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'office_id': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'office_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'precincts_reporting': ('django.db.models.fields.IntegerField', [], {}),
            'race_district_id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'race_number': ('django.db.models.fields.IntegerField', [], {}),
            'race_type': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'race_type_id': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'race_type_party': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'seat_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'seat_number': ('django.db.models.fields.IntegerField', [], {}),
            'state_postal': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'test_flag': ('elections.fields.TestFlagField', [], {'default': "'l'", 'max_length': '1'}),
            'total_precincts': ('django.db.models.fields.IntegerField', [], {})
        },
        'elections.state': {
            'Meta': {'ordering': "['name']", 'object_name': 'State'},
            'asian_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'bird': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'black_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'capitol': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'checksum': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'college_degree_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'dem_delegates': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'different_house_in_1995_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'electoral_votes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'employed_civilians_16_and_up_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'flower': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'governor': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'hawian_pacific_islander_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'hispanic_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'homes_heated_coal_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'homes_heated_elec_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'homes_heated_fuel_oil_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'homes_heated_gas_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'households_all_speak_other_than_english_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'income_poverty_1999_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'indian_alaska_native_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '5', 'blank': 'True'}),
            'livemap_state_id': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'livemap_state_zoom': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '5', 'blank': 'True'}),
            'management_professional_worker_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'married_couple_both_work_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'married_couple_family_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'married_couple_family_w_children_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'median_household_income': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mixed_race_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'motto_english': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'motto_other': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'non_hispanic_black_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'non_hispanic_white_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'other_race_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'other_races': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'population': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'populations_65_and_up_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'postal': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'president': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'production_transport_worker_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'questions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rep_delegates': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sales_office_worker_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'sos_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'sos_city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'sos_email': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'sos_fax': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'sos_first_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'sos_last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'sos_middle_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'sos_phone': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'sos_state': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'sos_suffix': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'sos_url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'sos_zip': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'state_house_split': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'state_id': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'state_sentate_split': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'state_summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'unemployment_current': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'unemployment_date_current': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'unemployment_monthly_change': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'unmarried_partner_households_f_with_f_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'unmarried_partner_households_m_with_m_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'us_house': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'us_house_split': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'us_senate_1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'us_senate_2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'us_senate_split': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'white_percent': ('elections.models.PercentField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'})
        },
        'massmedia.image': {
            'Meta': {'ordering': "('-creation_date',)", 'object_name': 'Image'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'external_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata': ('massmedia.fields.SerializedObjectField', [], {'blank': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'one_off_author': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'original': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'variations'", 'null': 'True', 'to': "orm['massmedia.Image']"}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'reproduction_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'image_site'", 'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'thumb_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thumb_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'widget_template': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['elections']
