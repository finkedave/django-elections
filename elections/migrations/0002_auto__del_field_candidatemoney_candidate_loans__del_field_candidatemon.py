# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'CandidateMoney.candidate_loans'
        db.delete_column('elections_candidatemoney', 'candidate_loans')

        # Deleting field 'CandidateMoney.ending_cash'
        db.delete_column('elections_candidatemoney', 'ending_cash')

        # Deleting field 'CandidateMoney.total_receipts'
        db.delete_column('elections_candidatemoney', 'total_receipts')

        # Deleting field 'CandidateMoney.individual_contributions'
        db.delete_column('elections_candidatemoney', 'individual_contributions')

        # Deleting field 'CandidateMoney.other_loan_repayments'
        db.delete_column('elections_candidatemoney', 'other_loan_repayments')

        # Deleting field 'CandidateMoney.total_disbursements'
        db.delete_column('elections_candidatemoney', 'total_disbursements')

        # Deleting field 'CandidateMoney.candidate_loan_repayments'
        db.delete_column('elections_candidatemoney', 'candidate_loan_repayments')

        # Deleting field 'CandidateMoney.pac_contributions'
        db.delete_column('elections_candidatemoney', 'pac_contributions')

        # Deleting field 'CandidateMoney.date_of_last_report'
        db.delete_column('elections_candidatemoney', 'date_of_last_report')

        # Deleting field 'CandidateMoney.other_loans'
        db.delete_column('elections_candidatemoney', 'other_loans')


    def backwards(self, orm):
        
        # Adding field 'CandidateMoney.candidate_loans'
        db.add_column('elections_candidatemoney', 'candidate_loans', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True), keep_default=False)

        # Adding field 'CandidateMoney.ending_cash'
        db.add_column('elections_candidatemoney', 'ending_cash', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True), keep_default=False)

        # Adding field 'CandidateMoney.total_receipts'
        db.add_column('elections_candidatemoney', 'total_receipts', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True), keep_default=False)

        # Adding field 'CandidateMoney.individual_contributions'
        db.add_column('elections_candidatemoney', 'individual_contributions', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True), keep_default=False)

        # Adding field 'CandidateMoney.other_loan_repayments'
        db.add_column('elections_candidatemoney', 'other_loan_repayments', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True), keep_default=False)

        # Adding field 'CandidateMoney.total_disbursements'
        db.add_column('elections_candidatemoney', 'total_disbursements', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True), keep_default=False)

        # Adding field 'CandidateMoney.candidate_loan_repayments'
        db.add_column('elections_candidatemoney', 'candidate_loan_repayments', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True), keep_default=False)

        # Adding field 'CandidateMoney.pac_contributions'
        db.add_column('elections_candidatemoney', 'pac_contributions', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True), keep_default=False)

        # Adding field 'CandidateMoney.date_of_last_report'
        db.add_column('elections_candidatemoney', 'date_of_last_report', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True), keep_default=False)

        # Adding field 'CandidateMoney.other_loans'
        db.add_column('elections_candidatemoney', 'other_loans', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True), keep_default=False)


    models = {
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
            'junior': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
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
            'thumbnail_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thumbnail_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'use_junior': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'year_first_elected': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
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
            'checksum': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'fec_candidate_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'fec_district_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'fec_office_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'fec_postal_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'Meta': {'ordering': "['event_date']", 'object_name': 'ElectionEvent'},
            'checksum': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'event_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'event_date': ('django.db.models.fields.DateField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'state_name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
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
            'fec_record_number': ('django.db.models.fields.CharField', [], {'max_length': '7', 'primary_key': 'True'}),
            'office': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'office_id': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'pac_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'party_id': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'party_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'recipient_committee': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'state_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
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
        }
    }

    complete_apps = ['elections']
