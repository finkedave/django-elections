from django.db import models
from django.db.models import get_model
from django.core.files.storage import get_storage_class

from .settings import TEST_DATA_ONLY, IMAGE_MODEL, IMAGE_STORAGE
from .fields import TestFlagField

STORAGE_MODEL = get_storage_class(IMAGE_STORAGE)

class TestDataManager(models.Manager):
    """
    Redefines get_query_set() to use test data based on settings switch.
    Provides "live" and "test" to specifically get those records.
    """
    
    def get_query_set(self):
        """
        if TEST_DATA_ONLY, only provide test data
        """
        qset = super(TestDataManager, self).get_query_set()
        if TEST_DATA_ONLY:
            return qset.filter(test_flag='t')
        else:
            return qset
    
    def test(self):
        """
        Return only test data
        """
        return super(TestDataManager, self).get_query_set().filter(test_flag='t')
    
    def live(self):
        """
        Return only live data
        """
        return super(TestDataManager, self).get_query_set().filter(test_flag='l')

class Candidate(models.Model):
    """
    An election candidate
    """
    test_flag = TestFlagField()
    politician_id = models.IntegerField(primary_key=True)
    slug = models.SlugField()
    ap_candidate_id = models.IntegerField(unique=True)
    candidate_number = models.IntegerField()
    first_name = models.CharField(blank=True, null=True, max_length=64)
    middle_name = models.CharField(blank=True, null=True, max_length=64)
    last_name = models.CharField(blank=True, null=True, max_length=64)
    junior = models.CharField(blank=True, null=True, max_length=16)
    use_junior = models.BooleanField(default=False)
    year_first_elected = models.IntegerField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    birth_place = models.CharField(blank=True, null=True, max_length=100)
    birth_state = models.CharField(blank=True, null=True, max_length=2)
    birth_province = models.CharField(blank=True, null=True, max_length=100)
    birth_country = models.CharField(blank=True, null=True, max_length=100)
    residence_place = models.CharField(blank=True, null=True, max_length=100)
    residence_state = models.CharField(blank=True, null=True, max_length=2)
    gender = models.CharField(
        blank=True, null=True, 
        max_length=1, 
        choices=(('M', 'Male'), ('F', 'Female')))
    ethnicity = models.CharField(blank=True, null=True, max_length=100)
    hispanic = models.CharField(blank=True, null=True, max_length=100)
    religion = models.CharField(blank=True, null=True, max_length=100)
    biography = models.TextField(blank=True, null=True)
    profile = models.TextField(blank=True, null=True)
    campaigns = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    if IMAGE_MODEL:
        photo_fk = models.ForeignKey(
            get_model(IMAGE_MODEL), 
            blank=True, 
            null=True)
        thumbnail_tk = models.ForeignKey(
            get_model(IMAGE_MODEL), 
            blank=True, 
            null=True)
    photo = models.FileField(
        upload_to='elections', 
        storage=STORAGE_MODEL(),
        blank=True,
        null=True)
    photo_width = models.IntegerField(blank=True, null=True)
    photo_height = models.IntegerField(blank=True, null=True)
    thumbnail = models.FileField(
        upload_to='elections/thumbs/', 
        storage=STORAGE_MODEL(),
        blank=True,
        null=True)
    thumbnail_width = models.IntegerField(blank=True, null=True)
    thumbnail_height = models.IntegerField(blank=True, null=True)

    @property
    def full_name(self):
        names =[]
        if self.first_name:
            names.append(self.first_name)
        if self.middle_name:
            names.append(self.middle_name)
        if self.last_name:
            names.append(self.last_name)
        name = u" ".join(names)
        if self.junior:
            name = u"%s, %s" % (name, self.junior)
        return name
    
    @models.permalink
    def get_absolute_url(self):
        """
        Get the absolute url for the candidate
        """
        return ('candidate_detail', (), {'slug': self.slug })
    
    def save(self, *args, **kwargs):
        """
        Make sure the slug is created when imported
        """
        if not self.slug:
            from django.template.defaultfilters import slugify
            
            self.slug = slugify("%s %s" % (self.full_name.replace(",", ""), self.politician_id))
        super(Candidate, self).save(*args, **kwargs)
    
    objects = TestDataManager()
    
    class Meta:
        ordering = ('last_name', 'first_name')
    
    def __unicode__(self):
        return self.full_name


class RaceCounty(models.Model):
    """
    Description of an election race by county
    """
    test_flag = TestFlagField()
    race_county_id = models.BigIntegerField(primary_key=True)
    race_number = models.IntegerField()
    election_date = models.DateField()
    state_postal = models.CharField(max_length=2)
    county_number = models.IntegerField(blank=True, null=True)
    fips_code = models.IntegerField(blank=True, null=True)
    county_name = models.CharField(max_length=64)
    office_id = models.CharField(max_length=1)
    race_type_id = models.CharField(max_length=1)
    seat_number = models.IntegerField()
    office_name = models.CharField(blank=True, null=True, max_length=64)
    seat_name = models.CharField(blank=True, null=True, max_length=64)
    race_type_party = models.CharField(blank=True, null=True, max_length=16)
    race_type = models.CharField(blank=True, null=True, max_length=32)
    office_description = models.CharField(blank=True, null=True, max_length=64)
    number_of_winners = models.IntegerField()
    number_in_runoff = models.IntegerField(blank=True, null=True)
    precincts_reporting = models.IntegerField()
    total_precincts = models.IntegerField()

    objects = TestDataManager()
    
    class Meta:
        verbose_name_plural = "Race counties"

    def __unicode__(self):
        return u"RaceCounty"


class RaceDistrict(models.Model):
    """
    Description of an election race by district
    """
    test_flag = TestFlagField()
    race_district_id = models.BigIntegerField(primary_key=True)
    race_number = models.IntegerField()
    election_date = models.DateField()
    state_postal = models.CharField(max_length=2)
    district_type = models.CharField(blank=True, null=True, max_length=16)
    cd_number = models.IntegerField(blank=True, null=True)
    district_name = models.CharField(blank=True, null=True, max_length=64)
    office_id = models.CharField(max_length=1)
    race_type_id = models.CharField(max_length=1)
    seat_number = models.IntegerField()
    office_name = models.CharField(blank=True, null=True, max_length=64)
    seat_name = models.CharField(blank=True, null=True, max_length=64)
    race_type_party = models.CharField(blank=True, null=True, max_length=16)
    race_type = models.CharField(blank=True, null=True, max_length=32)
    office_description = models.CharField(blank=True, null=True, max_length=64)
    number_of_winners = models.IntegerField()
    number_in_runoff = models.IntegerField(blank=True, null=True)
    precincts_reporting = models.IntegerField()
    total_precincts = models.IntegerField()

    objects = TestDataManager()
    

    class Meta:
        pass

    def __unicode__(self):
        return u"RaceDistrict"


class CountyResult(models.Model):
    """
    Results of a county election
    """
    test_flag = TestFlagField()
    race_county = models.ForeignKey(RaceCounty)
    ap_candidate = models.ForeignKey(
        Candidate, 
        to_field='ap_candidate_id',
        related_name="county_results")
    party = models.CharField(blank=True, null=True, max_length=16)
    incumbent = models.BooleanField(default=False)
    vote_count = models.IntegerField(default=0)
    winner = models.CharField(blank=True, null=True, max_length=1)
    natl_order = models.IntegerField(blank=True, null=True)
    
    objects = TestDataManager()
    
    class Meta:
        pass
    
    def __unicode__(self):
        return u"CountyResult"

class DistrictResult(models.Model):
    """
    Results of a district election
    """
    test_flag = TestFlagField()
    race_district = models.ForeignKey(RaceDistrict)
    ap_candidate = models.ForeignKey(
        Candidate, 
        to_field='ap_candidate_id',
        related_name="district_results")
    party = models.CharField(blank=True, null=True, max_length=16)
    incumbent = models.BooleanField(default=False)
    vote_count = models.IntegerField(default=0)
    delegate_count = models.IntegerField(default=0)
    winner = models.CharField(blank=True, null=True, max_length=1)
    natl_order = models.IntegerField(blank=True, null=True)
    
    objects = TestDataManager()
    
    class Meta:
        pass

    def __unicode__(self):
        return u"DistrictResult"


class CandidateOffice(models.Model):
    """
    Record for each office and politician holding or seeking that office.
    """
    candidate = models.ForeignKey(Candidate, related_name="offices")
    office_id = models.CharField(blank=True, null=True, max_length=1)
    state = models.CharField(blank=True, null=True, max_length=2)
    district_number = models.CharField(blank=True, null=True, max_length=4)
    party_id = models.CharField(blank=True, null=True, max_length=16)
    status_id = models.CharField(blank=True, null=True, max_length=1)
    office = models.CharField(blank=True, null=True, max_length=64)
    state_name = models.CharField(blank=True, null=True, max_length=100)
    district_name = models.CharField(blank=True, null=True, max_length=32)
    party_name = models.CharField(blank=True, null=True, max_length=32)
    office_description = models.CharField(blank=True, null=True, max_length=64)
    status_description = models.CharField(blank=True, null=True, max_length=64)
    next_election = models.IntegerField(blank=True, null=True)
    checksum = models.CharField(max_length=32)
    
    def calculate_checksum(self):
        """
        Calculate the MD5 checksum for the record
        """
        import hashlib
        checksum = hashlib.md5()
        checksum.update(str(self.candidate.pk))
        checksum.update(self.office_id or '')
        checksum.update(self.state or '')
        checksum.update(self.district_number or '')
        checksum.update(self.party_id or '')
        checksum.update(self.status_id or '')
        checksum.update(self.office or '')
        checksum.update(self.state_name or '')
        checksum.update(self.district_name or '')
        checksum.update(self.party_name or '')
        checksum.update(self.office_description or '')
        checksum.update(self.status_description or '')
        checksum.update(str(self.next_election) or '')
        return checksum.hexdigest()
    
    def save(self, *args, **kwargs):
        """
        Add the checksum
        """
        self.checksum = self.calculate_checksum()
        super(CandidateOffice, self).save(*args, **kwargs)

    class Meta:
        ordering = ['state', 'office', 'district_name']

    def __unicode__(self):
        name = [
            self.state or '', 
            self.office or '', 
            self.district_name or '',]
        return u" ".join(name)

class CandidateEducation(models.Model):
    """
    Record for each post-high-school educational institution attended 
    by each politician.
    """
    candidate = models.ForeignKey(Candidate, related_name="education")
    school_name = models.CharField(blank=True, null=True, max_length=64)
    school_type = models.CharField(blank=True, null=True, max_length=64)
    major = models.CharField(blank=True, null=True, max_length=64)
    degree = models.CharField(blank=True, null=True, max_length=64)
    school_city = models.CharField(blank=True, null=True, max_length=100)
    school_state = models.CharField(blank=True, null=True, max_length=2)
    school_province = models.CharField(blank=True, null=True, max_length=100)
    school_country = models.CharField(blank=True, null=True, max_length=64)
    checksum = models.CharField(max_length=32)
    
    def calculate_checksum(self):
        """
        Calculate the MD5 checksum for the record
        """
        import hashlib
        checksum = hashlib.md5()
        checksum.update(str(self.candidate.pk))
        checksum.update(self.school_name or '')
        checksum.update(self.school_type or '')
        checksum.update(self.major or '')
        checksum.update(self.degree or '')
        checksum.update(self.school_city or '')
        checksum.update(self.school_state or '')
        checksum.update(self.school_province or '')
        checksum.update(self.school_country or '')
        return checksum.hexdigest()
        
        
    class Meta:
        verbose_name_plural = 'education'
    
    def save(self, *args, **kwargs):
        """
        Add the checksum
        """
        self.checksum = self.calculate_checksum()
        super(CandidateEducation, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return u"%s's %s in %s from %s" % (self.candidate, self.degree, 
            self.major, self.school_name)


class CandidatePhone(models.Model):
    """
    Record for each voice telephone number available for each politician.
    """
    candidate = models.ForeignKey(Candidate, related_name="phones")
    phone_number = models.CharField(blank=True, null=True, max_length=15)
    extension = models.CharField(blank=True, null=True, max_length=10)
    location = models.CharField(blank=True, null=True, max_length=64)
    detail = models.CharField(blank=True, null=True, max_length=64)
    checksum = models.CharField(max_length=32)
    
    def calculate_checksum(self):
        """
        Calculate the MD5 checksum for the record
        """
        import hashlib
        checksum = hashlib.md5()
        checksum.update(str(self.candidate.pk))
        checksum.update(self.phone_number or '')
        checksum.update(self.extension or '')
        checksum.update(self.location or '')
        checksum.update(self.detail or '')
        return checksum.hexdigest()
    
    def save(self, *args, **kwargs):
        """
        Add the checksum
        """
        self.checksum = self.calculate_checksum()
        super(CandidatePhone, self).save(*args, **kwargs)

    class Meta:
        pass

    def __unicode__(self):
        return u"%s %s: %s" % (self.candidate, self.detail, self.phone_number)

class CandidateURL(models.Model):
    """
    Record for each voice telephone number available for each politician.
    """
    candidate = models.ForeignKey(Candidate, related_name="urls")
    url = models.CharField(blank=True, null=True, max_length=255)
    description = models.CharField(blank=True, null=True, max_length=255)
    checksum = models.CharField(max_length=32)
    
    def calculate_checksum(self):
        """
        Calculate the MD5 checksum for the record
        """
        import hashlib
        checksum = hashlib.md5()
        checksum.update(str(self.candidate.pk))
        checksum.update(self.url or '')
        checksum.update(self.description or '')
        return checksum.hexdigest()
    
    def save(self, *args, **kwargs):
        """
        Add the checksum
        """
        self.checksum = self.calculate_checksum()
        super(CandidateURL, self).save(*args, **kwargs)

    class Meta:
        pass

    def __unicode__(self):
        return u"%s %s %s" % (self.candidate, self.description, self.url)

class CandidateMedia(models.Model):
    """
    Record for each voice telephone number available for each politician.
    """
    candidate = models.ForeignKey(Candidate)
    medium_type = models.CharField(blank=True, null=True, max_length=64)
    file_name = models.CharField(blank=True, null=True, max_length=255)
    file_extension = models.CharField(blank=True, null=True, max_length=10)
    checksum = models.CharField(max_length=32)
    
    def calculate_checksum(self):
        """
        Calculate the MD5 checksum for the record
        """
        import hashlib
        checksum = hashlib.md5()
        checksum.update(str(self.candidate.pk))
        checksum.update(self.medium_type or '')
        checksum.update(self.file_name or '')
        checksum.update(self.file_extension or '')
        return checksum.hexdigest()
    
    def save(self, *args, **kwargs):
        """
        Add the checksum
        """
        self.checksum = self.calculate_checksum()
        super(CandidateMedia, self).save(*args, **kwargs)

    class Meta:
        pass

    def __unicode__(self):
        return u"%s %s" % (self.candidate, self.file_name)


class CandidateMoney(models.Model):
    """
    Record for each office and politician holding or seeking that office.
    """
    candidate = models.ForeignKey(Candidate)
    fec_candidate_id = models.CharField(blank=True, null=True, max_length=64)
    fec_office_id = models.CharField(blank=True, null=True, max_length=64)
    fec_postal_id = models.CharField(blank=True, null=True, max_length=64)
    fec_district_id = models.CharField(blank=True, null=True, max_length=64)
    total_receipts = models.CharField(blank=True, null=True, max_length=100)
    candidate_loans = models.CharField(blank=True, null=True, max_length=100)
    other_loans = models.CharField(blank=True, null=True, max_length=100)
    candidate_loan_repayments = models.CharField(blank=True, null=True, max_length=64)
    other_loan_repayments = models.CharField(blank=True, null=True, max_length=100)
    individual_contributions = models.CharField(blank=True, null=True, max_length=100)
    pac_contributions = models.CharField(blank=True, null=True, max_length=100)
    ending_cash = models.CharField(blank=True, null=True, max_length=100)
    date_of_last_report = models.CharField(blank=True, null=True, max_length=100)
    total_disbursements = models.CharField(blank=True, null=True, max_length=100)
    checksum = models.CharField(max_length=32)
    
    def calculate_checksum(self):
        """
        Calculate the MD5 checksum for the record
        """
        import hashlib
        checksum = hashlib.md5()
        checksum.update(str(self.candidate.pk))
        checksum.update(self.fec_candidate_id or '')
        checksum.update(self.fec_office_id or '')
        checksum.update(self.fec_postal_id or '')
        checksum.update(self.fec_district_id or '')
        checksum.update(self.total_receipts or '')
        checksum.update(self.candidate_loans or '')
        checksum.update(self.other_loans or '')
        checksum.update(self.candidate_loan_repayments or '')
        checksum.update(self.other_loan_repayments or '')
        checksum.update(self.individual_contributions or '')
        checksum.update(self.pac_contributions or '')
        checksum.update(self.ending_cash or '')
        checksum.update(self.date_of_last_report or '')
        checksum.update(self.total_disbursements or '')
        return checksum.hexdigest()
    
    def save(self, *args, **kwargs):
        """
        Add the checksum
        """
        self.checksum = self.calculate_checksum()
        super(CandidateMoney, self).save(*args, **kwargs)
    

    class Meta:
        pass

    def __unicode__(self):
        return u"CandidateMoney"

class ElectionEvent(models.Model):
    """An event that is going to happen in an election"""
    event_code = models.CharField(primary_key=True, max_length=20)
    state = models.CharField(max_length=2)
    state_name = models.CharField(max_length=32)
    event_date = models.DateField()
    description = models.CharField(blank=True, max_length=255)
    checksum = models.CharField(max_length=32)
    
    def calculate_checksum(self):
        """
        Calculate the MD5 checksum for the record
        """
        import hashlib
        checksum = hashlib.md5()
        checksum.update(self.event_code)
        checksum.update(self.state or '')
        checksum.update(self.state_name or '')
        checksum.update(self.event_date.isoformat() or '')
        checksum.update(self.description or '')
        return checksum.hexdigest()
    
    def save(self, *args, **kwargs):
        """
        Add the checksum
        """
        self.checksum = self.calculate_checksum()
        super(ElectionEvent, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ['event_date',]

    def __unicode__(self):
        return u" ".join([self.state, self.event_date.isoformat(), self.description])

class PACContribution(models.Model):
    """
    An individual campaign contributions of $2,000 or more made by a
    Political Action Committee.
    """
    fec_record_number = models.CharField(primary_key=True, max_length=7)
    fec_pac_id = models.CharField(max_length=11)
    pac_name = models.CharField(blank=True, max_length=100)
    recipient_committee = models.CharField(blank=True, max_length=100)
    candidate = models.ForeignKey(Candidate, related_name="pac_contributions", blank=True, null=True)
    office_id = models.CharField(blank=True, null=True, max_length=1)
    state = models.CharField(blank=True, null=True, max_length=2)
    district_number = models.IntegerField(blank=True, null=True)
    party_id = models.CharField(blank=True, null=True, max_length=16)
    fec_candidate_id = models.CharField(blank=True, null=True, max_length=10)
    # LastName
    # FirstName
    # MiddleName
    office = models.CharField(blank=True, null=True, max_length=64)
    state_name = models.CharField(blank=True, null=True, max_length=100)
    district_name = models.CharField(blank=True, null=True, max_length=32)
    party_name = models.CharField(blank=True, null=True, max_length=32)
    date_given = models.DateField()
    amount = models.IntegerField()
    slug = models.SlugField()
    checksum = models.CharField(max_length=32)
    
    def calculate_checksum(self):
        """
        Calculate the MD5 checksum for the record
        """
        import hashlib
        checksum = hashlib.md5()
        checksum.update(self.fec_record_number)
        checksum.update(self.fec_pac_id)
        checksum.update(self.pac_name or '')
        checksum.update(self.recipient_committee or '')
        if self.candidate:
            checksum.update(str(self.candidate.pk))
        else:
            checksum.update('')
        checksum.update(self.office_id or '')
        checksum.update(self.state or '')
        checksum.update(str(self.district_number) or '')
        checksum.update(self.party_id or '')
        checksum.update(self.fec_candidate_id or '')
        checksum.update(self.office or '')
        checksum.update(self.state_name or '')
        checksum.update(self.district_name or '')
        checksum.update(self.party_name or '')
        if self.date_given:
            checksum.update(self.date_given.isoformat())
        else:
            checksum.update('')
        checksum.update(str(self.amount) or '')
        return checksum.hexdigest()
    
    def save(self, *args, **kwargs):
        """
        Add the checksum
        """
        self.checksum = self.calculate_checksum()
        if not self.slug:
            from django.template.defaultfilters import slugify
            
            self.slug = slugify("%s %s" % (self.pac_name[:38], self.fec_pac_id))
        super(PACContribution, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-date_given',]

    def __unicode__(self):
        return u"%s gave $%s to %s on %s ".join(self.pac_name, self.amount, 
            self.recipient_committee, self.event_date.isoformat())
    
    
class PercentField(models.DecimalField):
    def __init__(self, verbose_name=None, name=None, max_digits=5, decimal_places=2, **kwargs):
        super(PercentField, self).__init__(verbose_name=None, name=None, 
                                             max_digits=5, decimal_places=2, **kwargs)
    
class Demographics(models.Model):
    population = models.IntegerField(blank=True, null=True)
    white_percent = PercentField(blank=True, null=True)
    black_percent = PercentField(blank=True, null=True)
    indian_alaska_native_percent = PercentField(blank=True, null=True)
    asian_percent = PercentField(blank=True, null=True)
    hawian_pacific_islander_percent = PercentField(blank=True, null=True)
    mixed_race_percent = PercentField(blank=True, null=True)
    other_race_percent = PercentField(blank=True, null=True)
    hispanic_percent = PercentField(blank=True, null=True)
    non_hispanic_white_percent = PercentField(blank=True, null=True)
    non_hispanic_black_percent = PercentField(blank=True, null=True)
    households_all_speak_other_than_english_percent = PercentField(blank=True, null=True)
    median_household_income = models.IntegerField(blank=True, null=True)
    married_couple_both_work_percent = PercentField(blank=True, null=True)
    income_poverty_1999_percent = PercentField(blank=True, null=True)
    different_house_in_1995_percent = PercentField(blank=True, null=True)
    homes_heated_elec_percent = PercentField(blank=True, null=True)
    homes_heated_gas_percent = PercentField(blank=True, null=True)
    homes_heated_coal_percent = PercentField(blank=True, null=True)
    homes_heated_fuel_oil_percent = PercentField(blank=True, null=True)
    populations_65_and_up_percent = PercentField(blank=True, null=True)
    employed_civilians_16_and_up_percent = PercentField(blank=True, null=True)
    college_degree_percent = PercentField(blank=True, null=True)
    management_professional_worker_percent = PercentField(blank=True, null=True)
    sales_office_worker_percent = PercentField(blank=True, null=True)
    production_transport_worker_percent = PercentField(blank=True, null=True)
    unemployment_current = PercentField(blank=True, null=True)
    unemployment_date_current = models.DateField(blank=True, null=True)
    unemployment_monthly_change = PercentField(blank=True, null=True)
    married_couple_family_percent = PercentField(blank=True, null=True)
    married_couple_family_w_children_percent = PercentField(blank=True, null=True)
    unmarried_partner_households_m_with_m_percent = PercentField(blank=True, null=True)
    unmarried_partner_households_f_with_f_percent = PercentField(blank=True, null=True) 
    
    IMPORT_MAPPING = [
        'population',
        'white_percent',
        'black_percent',
        'indian_alaska_native_percent',
        'asian_percent',
        'hawian_pacific_islander_percent',
        'mixed_race_percent',
        'other_race_percent',
        'hispanic_percent',
        'non_hispanic_white_percent',
        'non_hispanic_black_percent',
        'households_all_speak_other_than_english_percent',
        'median_household_income',
        'married_couple_both_work_percent',
        'income_poverty_1999_percent',
        'different_house_in_1995_percent',
        'homes_heated_elec_percent',
        'homes_heated_gas_percent',
        'homes_heated_coal_percent',
        'homes_heated_fuel_oil_percent',
        'populations_65_and_up_percent' ,
        'employed_civilians_16_and_up_percent',
        'college_degree_percent',
        'management_professional_worker_percent',
        'sales_office_worker_percent',
        'production_transport_worker_percent',
        'unemployment_current',
        'unemployment_date_current',
        'unemployment_monthly_change',
        'married_couple_family_percent',
        'married_couple_family_w_children_percent',
        'unmarried_partner_households_m_with_m_percent',
        'unmarried_partner_households_f_with_f_percent']

    class Meta:
        abstract = True
        
class State(Demographics):
    state_id = models.CharField(max_length=2, primary_key=True)
    postal = models.CharField(max_length=2)
    name = models.CharField(max_length=25)
    us_senate_split = models.CharField(max_length=100, blank=True, null=True)
    us_house_split = models.CharField(max_length=100, blank=True, null=True)
    state_sentate_split = models.CharField(max_length=100, blank=True, null=True)
    state_house_split = models.CharField(max_length=100, blank=True, null=True)
    president = models.CharField(max_length=100, blank=True, null=True)
    governor = models.CharField(max_length=100, blank=True, null=True)
    us_senate_1 = models.CharField(max_length=100, blank=True, null=True)
    us_senate_2 = models.CharField(max_length=100, blank=True, null=True)
    us_house = models.CharField(max_length=100, blank=True, null=True)
    questions = models.TextField(blank=True, null=True)
    other_races = models.TextField(blank=True, null=True)
    state_summary = models.TextField(blank=True, null=True)
    capitol = models.CharField(max_length=100, blank=True, null=True)
    nickname = models.CharField(max_length=100, blank=True, null=True)
    bird = models.CharField(max_length=100, blank=True, null=True)
    flower = models.CharField(max_length=100, blank=True, null=True)
    motto_english = models.CharField(max_length=255, blank=True, null=True)
    motto_other = models.CharField(max_length=255, blank=True, null=True)
    electoral_votes = models.IntegerField(blank=True, null=True)
    dem_delegates = models.IntegerField(blank=True, null=True)
    rep_delegates = models.IntegerField(blank=True, null=True) 
    
    sos_last_name = models.CharField(max_length=50, blank=True, null=True)
    sos_first_name = models.CharField(max_length=50, blank=True, null=True)
    sos_middle_name = models.CharField(max_length=50, blank=True, null=True)
    sos_suffix = models.CharField(max_length=25, blank=True, null=True)
    sos_address = models.CharField(max_length=255, blank=True, null=True)
    sos_city = models.CharField(max_length=50, blank=True, null=True)
    sos_state = models.CharField(max_length=25, blank=True, null=True)
    sos_zip = models.CharField(max_length=25, blank=True, null=True)
    sos_phone = models.CharField(blank=True, null=True, max_length=30)
    sos_fax = models.CharField(blank=True, null=True, max_length=30)
    sos_email = models.CharField(blank=True, null=True, max_length=50) 
    sos_url = models.CharField(blank=True, null=True, max_length=100) 

    slug = models.SlugField()
    checksum = models.CharField(max_length=32)

    IMPORT_MAPPING =  [
        'state_id',
        'postal',
        'name',
        'us_senate_split',
        'us_house_split',
        'state_sentate_split',
        'state_house_split',
        'president',
        'governor',
        'us_senate_1',
        'us_senate_2',
        'us_house',
        'questions',
        'other_races',
        'state_summary',
        'capitol',
        'nickname',
        'bird',
        'flower',
        'motto_english',
        'motto_other',
        'electoral_votes',
        'dem_delegates',
        'rep_delegates',
        'sos_last_name',
        'sos_first_name',
        'sos_middle_name',
        'sos_suffix',
        'sos_address',
        'sos_city',
        'sos_state',
        'sos_zip',
        'sos_phone',
        'sos_fax',
        'sos_email',
        'sos_url']
    IMPORT_MAPPING.extend(Demographics.IMPORT_MAPPING)
    
    def __unicode__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        """
        Add the checksum
        """
        self.checksum = self.calculate_checksum()
        if not self.slug:
            from django.template.defaultfilters import slugify
            
            self.slug = slugify(self.state_id)
        super(State, self).save(*args, **kwargs)

    
    def calculate_checksum(self):
        """
        Calculate the MD5 checksum for the record
        """
        return calculate_checksum(self)
    
    def election_events(self):
        return ElectionEvent.objects.filter(state=self.state_id)
    
    def districts(self):
        return District.objects.filter(state_postal=self.postal)
    
    def past_elections(self):
        return PastElection.objects.filter(state_postal=self.postal,
                                    district_number=0)
    
    def past_non_presidential_elections(self):
        return PastElection.objects.filter(state_postal=self.postal,
                                    district_number=0).exclude(office='P')
        
    def past_presidential_elections(self):
        return PastElection.objects.filter(state_postal=self.postal, office='P', 
                                           election_type='G', district_number=0,
                                           )
        
class PresidentialElectionResult(models.Model):
    state = models.ForeignKey(State)
    election_year = models.IntegerField()
    dem_vote = PercentField(blank=True, null=True)
    rep_vote = PercentField(blank=True, null=True)
    dem_pres_primary_winner = models.CharField(max_length=100, blank=True, null=True)
    dem_pres_primary_percent = PercentField(blank=True, null=True)
    rep_pres_primary_winner = models.CharField(max_length=100, blank=True, null=True)
    rep_pres_primary_percent = PercentField(blank=True, null=True)
    checksum = models.CharField(max_length=32)
    
    IMPORT_MAPPING = [
    'election_year',
    'dem_vote',
    'rep_vote',
    'dem_pres_primary_winner',
    'dem_pres_primary_percent',
    'rep_pres_primary_winner',
    'rep_pres_primary_percent',                                 
    ]
    
    def save(self, *args, **kwargs):
        """
        Add the checksum
        """
        self.checksum = self.calculate_checksum()
        super(PresidentialElectionResult, self).save(*args, **kwargs)
        
    class Meta:
        ordering = ['-election_year',]
        unique_together = ('state', 'election_year' )
    
    def calculate_checksum(self):
        """
        Calculate the MD5 checksum for the record
        """
        return calculate_checksum(self)
    
class District(Demographics):
    district_id = models.CharField(max_length=10, primary_key=True)
    district_number = models.IntegerField()
    state_postal = models.CharField(max_length=2)
    state_name = models.CharField(max_length=25)
    district_name = models.CharField(max_length=25)
    # For ordering demographics go next
    general_summary = models.TextField(blank=True, null=True)
    slug = models.SlugField()
    checksum = models.CharField(max_length=32)
    
    IMPORT_MAPPING = [
    'district_id',
    'state_postal',
    'district_number',
    'state_name',
    'district_name']

    IMPORT_MAPPING.extend(Demographics.IMPORT_MAPPING)
    IMPORT_MAPPING.append('general_summary')

    def save(self, *args, **kwargs):
        """
        Add the checksum
        """
        self.checksum = self.calculate_checksum()
        if not self.slug:
            from django.template.defaultfilters import slugify
            
            self.slug = slugify(self.district_id)
        super(District, self).save(*args, **kwargs)
        
    class Meta:
        ordering = ['state_postal', 'district_number']
    
    def calculate_checksum(self):
        """
        Calculate the MD5 checksum for the record
        """
        return calculate_checksum(self)
    
    def past_elections(self):
        return PastElection.objects.filter(state_postal=self.state_postal, 
                                district_number=self.district_number)
        
ELECTION_TYPE_CHOICES = (('G', 'General Election'),
                        ('GR', 'General Election Runoff'),
                        ('SG', 'Special General Election'),
                        ('P', 'Primary'),
                        ('SP', 'Special Primary'),
                        ('SR', 'Special Primary Runoff'),
                        ('PR', 'Primary Runoff'),
                        ('SB', 'All Party Special Blanket Primary'),
                        ('NR', 'Nonpartisan Runoff Election'),
                        ('NS', 'Nonpartisan Special Election'),
                        ('C', 'Caucus'),
                        ('LA', 'La. Style Nonpartisan Election'),
                        ('LR', 'La. Style Nonpartisan Special Runoff'),
                        ('LS', 'La. Style Nonpartisan Special Election'),)

ELECTION_PARTY_CHOICES = (('D', 'Democratic Primaries'),
                        ('R', 'Republican Primaries'),
                        ('O', 'Mult-Party Elections'))

ELECTION_OFFICE_CHOICES = (('P', 'President'),
                        ('G', 'Governor'),
                        ('S', 'Senate'),
                        ('H', 'House'))

class PastElection(models.Model):
    election_id =   models.CharField(max_length=15, primary_key=True)
    year = models.IntegerField()
    state_postal = models.CharField(max_length=2)
    office = models.CharField(max_length=1, choices=ELECTION_OFFICE_CHOICES, blank=True, null=True)
    election_type = models.CharField(max_length=2, choices=ELECTION_TYPE_CHOICES, blank=True, null=True)               
    district_number = models.IntegerField(blank=True, null=True)
    party = models.CharField(max_length=1, choices=ELECTION_PARTY_CHOICES, blank=True, null=True)
    state_name = models.CharField(max_length=25, blank=True, null=True)
    office_name = models.CharField(max_length=100, blank=True, null=True)
    election_type_name = models.CharField(max_length=100, blank=True, null=True)
    district_name = models.CharField(max_length=25, blank=True, null=True)
    party_name = models.CharField(max_length=100, blank=True, null=True)
    checksum = models.CharField(max_length=32)
    slug = models.SlugField()
    
    IMPORT_MAPPING =  [
    'election_id',
    'year',
    'state_postal',
    'office',
    'election_type',
    'district_number',
    'party',
    'state_name',
    'office_name',
    'election_type_name',
    'district_name',
    'party_name',
    ]
    
    def save(self, *args, **kwargs):
        """
        Add the checksum
        """
        self.checksum = self.calculate_checksum()
        if not self.slug:
            from django.template.defaultfilters import slugify
            
            self.slug = slugify(self.election_id)
        super(PastElection, self).save(*args, **kwargs)
        
    class Meta:
        ordering = ['state_postal', 'district_number', '-year', 'party']
    
    def results(self):
        return PastElectionResult.objects.filter(election_id=self.election_id, percent__gte=2)
    
    def calculate_checksum(self):
        """
        Calculate the MD5 checksum for the record
        """
        return calculate_checksum(self)
    
class PastElectionResult(models.Model):
    election_id =   models.CharField(max_length=15)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    suffix = models.CharField(max_length=25, blank=True, null=True)
    party = models.CharField(max_length=25, blank=True, null=True)
    vote = models.IntegerField(blank=True, null=True)
    percent = PercentField(blank=True, null=True)
    winner = models.NullBooleanField(blank=True, null=True)
    checksum = models.CharField(max_length=32)
    
    IMPORT_MAPPING = [
        'election_id',
        'last_name',
        'first_name',
        'suffix',
        'party',
        'vote',
        'percent',
        'winner']
    
    def save(self, *args, **kwargs):
        """
        Add the checksum
        """
        self.checksum = self.calculate_checksum()
        super(PastElectionResult, self).save(*args, **kwargs)
        
    class Meta:
        ordering = ['party', 'last_name']
        unique_together = ['election_id', 'last_name', 'first_name', 'suffix', 'party']
    
    def calculate_checksum(self):
        """
        Calculate the MD5 checksum for the record
        """
        return calculate_checksum(self)
    
    def party_displayable(self):
        displayable_party_word_list = []
        if self.party:
            lowercase_party = self.party.lower()
            party_word_list = lowercase_party.split(" ")
            displayable_party_word_list = []
            for party_word in party_word_list:
                if len(party_word) > 1:
                    displayable_party_word_list.append(
                                party_word[0].capitalize() + party_word[1:])
                else:
                    displayable_party_word_list.append(
                                lowercase_party.capitalize())
            return " ".join(displayable_party_word_list)
            
    def name(self):
        name_list = []
        if self.first_name:
            name_list.append(self.first_name)
        if self.last_name:
            name_list.append(self.last_name)
        if self.suffix:
            name_list.append(self.suffix)
        return " ".join(name_list) 
    
def calculate_checksum(obj, mapping=None):
    import hashlib
    checksum = hashlib.md5()
    
    if not mapping:
        mapping = obj.IMPORT_MAPPING
    for item in mapping:
        value = getattr(obj, item)
        if value:
            checksum.update(str(value))
        else:
            checksum.update('')
    return checksum.hexdigest()