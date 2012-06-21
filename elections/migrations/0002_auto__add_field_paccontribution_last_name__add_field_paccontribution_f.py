# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'PACContribution.last_name'
        db.add_column('elections_paccontribution', 'last_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True), keep_default=False)

        # Adding field 'PACContribution.first_name'
        db.add_column('elections_paccontribution', 'first_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True), keep_default=False)

        # Adding field 'PACContribution.middle_name'
        db.add_column('elections_paccontribution', 'middle_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True), keep_default=False)

        # Changing field 'PACContribution.fec_record_number'
        db.alter_column('elections_paccontribution', 'fec_record_number', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True))

        # Changing field 'PACContribution.recipient_committee'
        db.alter_column('elections_paccontribution', 'recipient_committee', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'PACContribution.pac_name'
        db.alter_column('elections_paccontribution', 'pac_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))


    def backwards(self, orm):
        
        # Deleting field 'PACContribution.last_name'
        db.delete_column('elections_paccontribution', 'last_name')

        # Deleting field 'PACContribution.first_name'
        db.delete_column('elections_paccontribution', 'first_name')

        # Deleting field 'PACContribution.middle_name'
        db.delete_column('elections_paccontribution', 'middle_name')

        # Changing field 'PACContribution.fec_record_number'
        db.alter_column('elections_paccontribution', 'fec_record_number', self.gf('django.db.models.fields.CharField')(max_length=7, primary_key=True))

        # Changing field 'PACContribution.recipient_committee'
        db.alter_column('elections_paccontribution', 'recipient_committee', self.gf('django.db.models.fields.CharField')(default='', max_length=100))

        # Changing field 'PACContribution.pac_name'
        db.alter_column('elections_paccontribution', 'pac_name', self.gf('django.db.models.fields.CharField')(default='', max_length=100))


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
            'candidate_loan_repayments': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'candidate_loans': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'checksum': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'date_of_last_report': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'ending_cash': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'fec_candidate_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'fec_district_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'fec_office_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'fec_postal_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'individual_contributions': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'other_loan_repayments': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'other_loans': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pac_contributions': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'total_disbursements': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'total_receipts': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
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
            'Meta': {'ordering': "['event_date']", 'object_name': 'ElectionEvent'},
            'checksum': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'event_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'event_date': ('django.db.models.fields.DateField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'state_name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'elections.livemap': {
            'Meta': {'ordering': "['-race_date', 'race_type', 'party']", 'object_name': 'LiveMap'},
            'delegate_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'json_file_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'party': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'race_date': ('django.db.models.fields.DateField', [], {}),
            'race_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
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
        }
    }

    complete_apps = ['elections']
