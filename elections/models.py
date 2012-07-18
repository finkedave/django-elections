from datetime import datetime
from django.db import models
from django.db.models import get_model
from django.core.files.storage import get_storage_class
from django.utils.translation import ugettext as _
from .settings import TEST_DATA_ONLY, IMAGE_MODEL, IMAGE_STORAGE
from .fields import TestFlagField
import hashlib
from django.db.models import Sum
from settings import HOT_RACE_RELATION_MODELS, HOT_RACE_RELATIONS
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
import operator 
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
            get_model(*IMAGE_MODEL), 
            verbose_name="Alternate Photo",
            blank=True, 
            null=True,
            related_name='alternate_photo')
        thumbnail_fk = models.ForeignKey(
            get_model(*IMAGE_MODEL), 
            verbose_name="Alternate Thumbnail",
            blank=True, 
            null=True,
            related_name='alternate_thumbnail')
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
    is_presidential_candidate = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
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
    
    def pac_contribution_total_amount(self):
        """ Returns the total amount that has been contributed to a candidate from pacs"""
        return self.pac_contributions.aggregate(total_amount=Sum('amount'))['total_amount']
    
    def alt_photo(self):
        if self.photo_fk:
            return self.photo_fk.file
        else:
            return self.photo
    
    def alt_thumbnail(self):
        if self.thumbnail_fk:
            return self.thumbnail_fk.file
        else:
            return self.thumbnail
        
    objects = TestDataManager()
    
    @property
    def candidate_money(self):
        """ Return the first candidate money object """
        if self.candidatemoney_set.all().count():
            return self.candidatemoney_set.all()[0]
        
    @property
    def fec_info(self):
        """ Retieve the CandidateFEC object from the DB if exists,
        we use candidate money object to get the fec_candidate_id first """
        if not hasattr(self, 'fec_info_object'):
            fec_info_object = None
            candidate_money = self.candidate_money
            if candidate_money and candidate_money.fec_candidate_id:
                try:
                    fec_info_object = CandidateFEC.objects.get(
                                fec_candidate_id=candidate_money.fec_candidate_id)
                except CandidateFEC.DoesNotExist:
                    pass
            setattr(self, 'fec_info_object', fec_info_object)
        return getattr(self, 'fec_info_object')
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
    total_receipts = models.IntegerField(blank=True, null=True)
    candidate_loans = models.IntegerField(blank=True, null=True)
    other_loans = models.IntegerField(blank=True, null=True)
    candidate_loan_repayments = models.IntegerField(blank=True, null=True)
    other_loan_repayments = models.IntegerField(blank=True, null=True)
    individual_contributions = models.IntegerField(blank=True, null=True)
    pac_contributions = models.IntegerField(blank=True, null=True)
    ending_cash = models.IntegerField(blank=True, null=True)
    date_of_last_report = models.DateField(blank=True, null=True)
    total_disbursements = models.IntegerField(blank=True, null=True)
    checksum = models.CharField(max_length=32)
    
    """ Ordered mapping between the import file and the model """
    IMPORT_MAPPING =  ['candidate_id',
                       'fec_candidate_id',
                       'fec_office_id',
                       'fec_postal_id',
                       'fec_district_id',
                       'total_receipts',
                       'candidate_loans',
                       'other_loans',
                       'candidate_loan_repayments',
                       'other_loan_repayments',
                       'individual_contributions',
                       'pac_contributions',
                       'ending_cash',
                       'date_of_last_report',
                       'total_disbursements']
                             
    def calculate_checksum(self):
        """
        Calculate the MD5 checksum for the record
        """
        return calculate_checksum(self)
    
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

FEC_OFFICE_CHOICES = (('P', 'President'),
                      ('S', 'Senate'),
                      ('H', 'House'))
FEC_PARTY_CHOICES = (
    ("AIP", "AMERICAN INDEPENDENT PARTY"),
    ("AMP", "AMERICAN PARTY"),
    ("CIT", "CITIZENS' PARTY"),
    ("CON", "CONSTITUTION PARTY"),
    ("CRV", "CONSERVATIVE PARTY"),
    ("CST", "CONSTITUTIONAL"),
    ("DEM", "DEMOCRATIC PARTY"),
    ("DFL", "DEMOCRATIC-FARM-LABOR"),
    ("FED", "FEDERALIST"),
    ("FRE", "FREEDOM PARTY"),
    ("GRE", "GREEN PARTY"),
    ("IAP", "INDEPENDENT AMERICAN PARTY"),
    ("IDP", "INDEPENDENCE PARTY"),
    ("IND", "INDEPENDENT"),
    ("JCN", "JEWISH/CHRISTIAN NATIONAL"),
    ("LBU", "LIBERTY UNION PARTY"),
    ("LIB ", "LIBERTARIAN PARTY"),
    ("NLP", "NATURAL LAW PARTY"),
    ("NNE", "NONE"),
    ("NPA", "NO PARTY AFFILIATION"),
    ("OTH", "OTHER"),
    ("PAF", "PEACE AND FREEDOM"),
    ("REF", "REFORM PARTY"),
    ("REP", "REPUBLICAN PARTY"),
    ("RTL", "RIGHT TO LIFE"),
    ("SOC", "SOCIALIST PARTY U.S.A."),
    ("SUS", "SOCIALIST PARTY"),
    ("SWP", "SOCIALIST WORKERS PARTY"),
    ("TX", "TAXPAYERS"),
    ("UNK", "UNKNOWN"),
    ("W", "WRITE-IN"),)

class CurrencyField(models.DecimalField):
    """ Custom field that represents percentage for statistics """
    def __init__(self, verbose_name=None, name=None, max_digits=14, decimal_places=2, 
                    blank=True, null=True, **kwargs):
        super(CurrencyField, self).__init__(verbose_name=verbose_name, name=name, 
                    max_digits=max_digits, decimal_places=decimal_places, 
                    blank=blank, null=null, **kwargs)
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^elections\.models\.CurrencyField"])

class CandidateFEC(models.Model):
    """ Model reflecting data from the FEC website http://www.fec.gov/data/CandidateSummary.do,
    this is tied into AP data using fec_candidate_id """
    committee_link = models.URLField(blank=True, null=True)
    fec_candidate_id = models.CharField(blank=True, null=True, max_length=9)
    name = models.CharField(blank=True, null=True, max_length=90)
    office = models.CharField(blank=True, null=True, max_length=1)
    office_state = models.CharField(blank=True, null=True, max_length=2)
    district_number = models.CharField(blank=True, null=True, max_length=2)
    party = models.CharField(blank=True, null=True, max_length=3)
    status = models.CharField(blank=True, null=True, max_length=10)
    mailing_addr1 = models.TextField(blank=True, null=True)
    mailing_addr2 = models.TextField(blank=True, null=True)
    mailing_city = models.CharField(blank=True, null=True, max_length=50)
    mailing_state = models.CharField(blank=True, null=True, max_length=50)
    mailing_zipcode = models.CharField(blank=True, null=True, max_length=10)
    individual_itemized_contrib = CurrencyField(help_text="Sum of itemized contributions from individuals.")
    individual_unitemized_contrib = CurrencyField(help_text="Sum of unitemized contributions from individuals.")
    individual_contrib = CurrencyField(help_text="Total contributions from individuals.")
    party_committee_contrib = CurrencyField()
    other_committee_contrib = CurrencyField()
    candidate_contrib = CurrencyField(help_text = "Contributions from the candidate him(her)self")
    total_contrib = CurrencyField()
    transfer_from_other_commitee = CurrencyField(help_text ="Candidates may have more than one committee working for their election (including jointfundraising committees). Transfers from others within the set appear here.")
    candidate_loan = CurrencyField(help_text="Loans received from the candidate.")
    other_loan = CurrencyField(help_text="Often from banks, but must be made in the normal course of business including interest rates and collateral. Loans from individuals are treated as contributions")
    total_loan = CurrencyField()
    offsets_to_operating_expenditures = CurrencyField(help_text = "e.g. refund of deposit for phone bank, etc.") 
    offsets_to_fundraising = CurrencyField(help_text = "Applies only for Presidential candidates receiving public matching funds in the primaries.")
    offsets_to_legal_accounting =  CurrencyField()
    other_receipts =  CurrencyField()
    total_receipts =  CurrencyField()
    operating_expenditure =  CurrencyField()
    exempt_legal_accounting_disbursement =  CurrencyField()
    fundraising_disbursement = CurrencyField()
    transfer_to_other_committee = CurrencyField()
    candidate_loan_repayment = CurrencyField()
    other_loan_repayment = CurrencyField()
    total_loan_repayment = CurrencyField()
    individual_refund = CurrencyField()
    party_committee_refund = CurrencyField()
    other_committee_refund = CurrencyField()
    total_contribution_refund = CurrencyField()
    other_disbursement = CurrencyField()
    total_disbursement = CurrencyField()
    cash_on_hand_beginning_of_period = CurrencyField(help_text = \
            "Cash balance for the campaign at the start of the two-year period.")
    cash_on_hand_close_of_period = CurrencyField()
    net_contribution = CurrencyField()
    net_operating_expenditure = CurrencyField()
    debt_owed_by_committee = CurrencyField()
    debt_owed_to_committee = CurrencyField()
    coverage_start_date = models.DateField(help_text="Beginning date for the " \
                "first report during the two year period", blank=True, null=True)
    coverage_end_date = models.DateField(help_text="Ending date of the most recent report.", 
                                         blank=True, null=True)
    checksum = models.CharField(max_length=32)
    
    """ Ordered mapping between the import file and the model """
    IMPORT_MAPPING =  [
        "committee_link",
        "fec_candidate_id",
        "name",
        "office",
        "office_state",
        "district_number",
        "party",
        "status",
        "mailing_addr1",
        "mailing_addr2",
        "mailing_city",
        "mailing_state",
        "mailing_zipcode",
        "individual_itemized_contrib",
        "individual_unitemized_contrib",
        "individual_contrib",
        "party_committee_contrib",
        "other_committee_contrib",
        "candidate_contrib",
        "total_contrib",
        "transfer_from_other_commitee",
        "candidate_loan",
        "other_loan",
        "total_loan",
        "offsets_to_operating_expenditures",
        "offsets_to_fundraising",
        "offsets_to_legal_accounting",
        "other_receipts",
        "total_receipts",
        "operating_expenditure",
        "exempt_legal_accounting_disbursement",
        "fundraising_disbursement",
        "transfer_to_other_committee",
        "candidate_loan_repayment",
        "other_loan_repayment",
        "total_loan_repayment",
        "individual_refund",
        "party_committee_refund",
        "other_committee_refund",
        "total_contribution_refund",
        "other_disbursement",
        "total_disbursement",
        "cash_on_hand_beginning_of_period",
        "cash_on_hand_close_of_period",
        "net_contribution",
        "net_operating_expenditure",
        "debt_owed_by_committee",
        "debt_owed_to_committee",
        "coverage_start_date",
        "coverage_end_date"
    ]
    class Meta:
        ordering = ['office_state', 'name',]

    def __unicode__(self):
        return"%s - %s" % (self.name, self.fec_candidate_id)
    
    def save(self, *args, **kwargs):
        """
        Add the checksum
        """
        self.checksum = self.calculate_checksum()
        super(CandidateFEC, self).save(*args, **kwargs)
    
    def calculate_checksum(self):
        """
        Calculate the MD5 checksum for the record
        """
        return calculate_checksum(self)
        
EVENT_PRESIDENTIAL_KEYWORD_LIST = ['president', 'caucuses', 'persidential', 
                            'national', 'general election', 'closed primary']
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
    
    @property
    def race_type(self):
        description_lower = self.description.lower()
        
        # Note the Prmary. Ap doesn't know how to validate data very well
        if description_lower.count('primary') or description_lower.count('prmary'):
            return 'primary'
        elif description_lower.count('caucuses'):
            return 'caucus'
        elif description_lower.count('general election'):
            return 'general'
        else:
            return self.description
    

    
    @property
    def level(self):
        description_lower = self.description.lower()
        is_presidential = False
        for keyword in EVENT_PRESIDENTIAL_KEYWORD_LIST:
            if description_lower.count(keyword):
                is_presidential = True
                break
            
        if is_presidential:
            if description_lower.count('state'):
                return 'Presidential/State'
            else:
                return 'Presidential'
        else:
            return 'State'
        
    @property
    def party(self):
        description_lower = self.description.lower()
        if description_lower.count('republican'):
            return 'republican'
        elif description_lower.count('democrat'):
            return 'democrat'
        elif self.level != 'State':
            return 'both'
        else:
            return ''
    
    def live_results(self):
        return LiveMap.objects.filter(state=self.state, race_date=self.event_date, 
                                      race_type=self.race_type)
    
    class Meta:
        ordering = ['event_date', 'state_name']

    def __unicode__(self):
        return u" ".join([self.state, self.event_date.isoformat(), self.description])

class PACContribution(models.Model):
    """
    An individual campaign contributions of $2,000 or more made by a
    Political Action Committee.
    """
    fec_record_number = models.CharField(primary_key=True, max_length=20)
    fec_pac_id = models.CharField(max_length=11)
    pac_name = models.CharField(blank=True, null=True, max_length=100)
    recipient_committee = models.CharField(blank=True, null=True, max_length=100)
    candidate = models.ForeignKey(Candidate, related_name="pac_contributions", blank=True, null=True)
    office_id = models.CharField(blank=True, null=True, max_length=1)
    state = models.CharField(blank=True, null=True, max_length=2)
    district_number = models.IntegerField(blank=True, null=True)
    party_id = models.CharField(blank=True, null=True, max_length=16)
    fec_candidate_id = models.CharField(blank=True, null=True, max_length=10)
    last_name = models.CharField(blank=True, null=True, max_length=50)
    first_name = models.CharField(blank=True, null=True, max_length=50)
    middle_name = models.CharField(blank=True, null=True, max_length=50)
    office = models.CharField(blank=True, null=True, max_length=64)
    state_name = models.CharField(blank=True, null=True, max_length=100)
    district_name = models.CharField(blank=True, null=True, max_length=32)
    party_name = models.CharField(blank=True, null=True, max_length=32)
    date_given = models.DateField()
    amount = models.IntegerField()
    slug = models.SlugField()
    checksum = models.CharField(max_length=32)
    
    """ Ordered mapping between the import file and the model """
    IMPORT_MAPPING =  ['fec_record_number',
                       'fec_pac_id',
                       'pac_name',
                       'recipient_committee',
                       'candidate_id',
                       'office_id',
                       'state',
                       'district_number',
                       'party_id',
                       'fec_candidate_id',
                       'last_name',
                       'first_name',
                       'middle_name',
                       'office',
                       'state_name',
                       'district_name',
                       'party_name',
                       'date_given',
                       'amount']
                    
    def calculate_checksum(self):
        """
        Calculate the MD5 checksum for the record
        """
        return calculate_checksum(self)
    
    def save(self, *args, **kwargs):
        """
        Add the checksum
        """
        self.checksum = self.calculate_checksum()
        if not self.slug:
            from django.template.defaultfilters import slugify
            
            self.slug = slugify("%s %s" % (self.pac_name[:38], self.fec_pac_id))
        super(PACContribution, self).save(*args, **kwargs)
        
    def name(self):
        """ Combines the name of the result field. First name last 
        name and then suffix """
        name_list = []
        if self.first_name:
            name_list.append(self.first_name)
        if self.middle_name:
            name_list.append(self.middle_name)
        if self.last_name:
            name_list.append(self.last_name)
        return " ".join(name_list) 
        
        
    class Meta:
        ordering = ['-date_given',]

    def __unicode__(self):
        return u"%s gave $%s to %s on %s ".join(self.pac_name, self.amount, 
            self.recipient_committee, self.event_date.isoformat())
    
    
class PercentField(models.DecimalField):
    """ Custom field that represents percentage for statistics """
    def __init__(self, verbose_name=None, name=None, max_digits=5, decimal_places=2, **kwargs):
        super(PercentField, self).__init__(verbose_name=None, name=None, 
                                             max_digits=max_digits, decimal_places=decimal_places, **kwargs)
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^elections\.models\.PercentField"])


class Demographics(models.Model):
    """ Abstract class that both State and District extend from """
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
    
    """ This mapping represents the order which these are found in the import file. We
    are just lucky that the order is the same in both state and district. Otherwise this 
    list would just need to be copied and modified to State and District """
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
    """ State Model class that represents a state profile """
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

    # These fields are for use for live maps and are non populated by
    # from import
    livemap_state_id = models.CharField(max_length=3, blank=True, null=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=5, 
                                   blank=True, null=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=5, 
                                    blank=True, null=True)
    livemap_state_zoom = models.IntegerField(blank=True, null=True)
    
    # These fields are due to certain states just being territores/filler states
    # for foregin keys
    
    # Linkable means does it have its own landing page
    linkable = models.BooleanField(default=True)
    
    # Disabled means its a state that should never be shown anywhere, its here
    # just because it was in a data file
    disabled = models.BooleanField(default=False)
    
    slug = models.SlugField()
    checksum = models.CharField(max_length=32)

    """ Ordered mapping between the import file and the model """
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
    
    # The demographics came after the other attributes
    IMPORT_MAPPING.extend(Demographics.IMPORT_MAPPING)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        """ Meta method that sets ordering and unique together """
        ordering = ['name',]
        
    def save(self, *args, **kwargs):
        """
        Add the checksum and slug
        """
        self.checksum = self.calculate_checksum()
        if not self.slug:
            self.slug = self.state_id
        super(State, self).save(*args, **kwargs)

    
    def calculate_checksum(self):
        """
        Calculate the MD5 checksum for the record
        """
        return calculate_checksum(self)
    
    def election_events(self):
        """ "get the election events for the state """
        return ElectionEvent.objects.filter(state=self.state_id)
    
    def districts(self):
        """ Get the list of districts for the state """
        return District.objects.filter(state_postal=self.postal)
    
    def past_elections(self):
        """ Get past elections for the state. Note the districts number = 0 
        that means its a state election and not a district election. Otherwise
        this would pull all elections including district elections """
        return PastElection.objects.filter(state_postal=self.postal,
                                    district_number=0)
    
    def past_non_presidential_elections(self):
        """ get non presidental past elections """
        return PastElection.objects.filter(state_postal=self.postal,
                                    district_number=0).exclude(office='P')
        
    def past_presidential_elections(self):
        """ get presidental past elections """
        return PastElection.objects.filter(state_postal=self.postal, office='P', 
                                           election_type='G', district_number=0,
                                           )
    
    def sos_name(self):
        """ helper method that combines the SOS name """
        name_list = []
        if self.sos_first_name:
            name_list.append(self.sos_first_name)
        if self.sos_middle_name:
            name_list.append(self.sos_middle_name)
        if self.sos_last_name:
            name_list.append(self.sos_last_name)
        if self.sos_suffix:
            name_list.append(self.sos_suffix)
        return " ".join(name_list) 
    
    def historical_year_live_map_list(self, excluded_live_map_id=None):
        """ Create historical list of races by year """
        
        historical_map_qs = self.livemap_set.all()
        if excluded_live_map_id:
            historical_map_qs = historical_map_qs.exclude(id=excluded_live_map_id)
        
        historical_year_live_map_dict = {}
        historical_year_live_map_list = []
        for historical_map in historical_map_qs:
            if historical_map.race_date.year not in historical_year_live_map_dict:
                historical_year_live_map_dict[historical_map.race_date.year] = []
            historical_year_live_map_dict[historical_map.race_date.year].append(historical_map)
        
        
        if historical_year_live_map_dict:
            historical_year_live_map_list = sorted(([year, live_map_list] \
                            for year, live_map_list in historical_year_live_map_dict.iteritems()),
                                                   key = operator.itemgetter(0), reverse=True)
        return historical_year_live_map_list
    
class PresidentialElectionResult(models.Model):
    """ Model that holds info regarding presidential elections. Note this
    info is duplicated in profilestates and oldvoteresults. So really no 
    reason to use this table which is populated from the profilestates.txt
    this is here just to capture the data even though its better not to use this
    table. Its missing to much data """
    state = models.ForeignKey(State)
    election_year = models.IntegerField()
    dem_vote = PercentField(blank=True, null=True)
    rep_vote = PercentField(blank=True, null=True)
    dem_pres_primary_winner = models.CharField(max_length=100, blank=True, null=True)
    dem_pres_primary_percent = PercentField(blank=True, null=True)
    rep_pres_primary_winner = models.CharField(max_length=100, blank=True, null=True)
    rep_pres_primary_percent = PercentField(blank=True, null=True)
    checksum = models.CharField(max_length=32)
    
    """ Ordered mapping """
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
        """ Meta method that sets ordering and unique together """
        ordering = ['-election_year',]
        unique_together = ('state', 'election_year' )
    
    def calculate_checksum(self):
        """
        Calculate the MD5 checksum for the record
        """
        return calculate_checksum(self)
    
class District(Demographics):
    """ District model for containing facts and staticts on state districts """
    district_id = models.CharField(max_length=10, primary_key=True)
    district_number = models.IntegerField()
    state_postal = models.CharField(max_length=2)
    state_name = models.CharField(max_length=25)
    district_name = models.CharField(max_length=25)
    # For ordering demographics go next
    general_summary = models.TextField(blank=True, null=True)
    slug = models.SlugField()
    checksum = models.CharField(max_length=32)
    
    # The ordered mapping that maps the import file to the model.
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
        Add the checksum and slug
        """
        self.checksum = self.calculate_checksum()
        if not self.slug:
            self.slug = self.district_id
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
    @property
    def state(self):
        """ Didn't want foreign key relationship due to imports. Instead
        just a property to link it to state """
        try:
            return State.objects.get(state_id=self.state_postal)
        except State.DoesNotExist:
            return None
        
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
    """ Past election model """
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
        Add the checksum and slug
        """
        self.checksum = self.calculate_checksum()
        if not self.slug:
            from django.template.defaultfilters import slugify
            
            self.slug = slugify(self.election_id)
        super(PastElection, self).save(*args, **kwargs)
        
    class Meta:
        """ Meta """
        ordering = ['state_postal', 'district_number', '-year', 'party']
    
    def results(self):
        """ Returns the list of results for this election """
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
    
    """ Ordered mapping that maps the import file to the model """
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
        """ party that is imported from the DB is ugly text. All caps. 
        Here we just want to uppercase the first letter of each word and
        lower the rest of the characters """
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
        """ Combines the name of the result field. First name last 
        name and then suffix """
        name_list = []
        if self.first_name:
            name_list.append(self.first_name)
        if self.last_name:
            name_list.append(self.last_name)
        if self.suffix:
            name_list.append(self.suffix)
        return " ".join(name_list) 


RACE_TYPE_CHOICES = (('general', 'General Election'),
                    ('primary', 'Presidential Primary'),
                    ('caucus', 'Caucus'))

PARTY_CHOICES = (('republican', 'Republican'),
                 ('democrat', 'Democrat'))

class PublishedManager(models.Manager):
    """ Manager for querying only published artwork entries """
    def get_query_set(self):
        queryset = super(PublishedManager, self).get_query_set()
        return queryset.filter(
            update_results_start_date__lte=datetime.now())
                   
class LiveMap(models.Model):
    """ Model representing a live map """
    state = models.ForeignKey(State)
    race_type = models.CharField(max_length=20, choices=RACE_TYPE_CHOICES)
    party =  models.CharField(max_length=20, choices=PARTY_CHOICES, blank=True, null=True)
    race_date = models.DateField()
    delegate_count = models.IntegerField(blank=True, null=True)
    json_file_name = models.CharField(max_length=100, blank=True, null=True)
    state_notice = models.TextField(blank=True, null=True)
    
    update_results_start_date = models.DateTimeField(
        help_text=_("The date/time that AP will start receiving results for the state."))
    update_results_end_date = models.DateTimeField(
        help_text=_("The date/time that AP will stop receiving results for the state."))
    
    template_name = models.CharField(_('template name'), max_length=70, 
                                     default='elections/live_maps/liveresults.html',
        help_text=_("Example: 'elections/live_maps/2012_rep_primary_live_results.html'"))
    slug = models.SlugField()
    uncontested = models.BooleanField(default=False)
    objects = models.Manager()
    published = PublishedManager()
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ['-race_date', 'race_type', 'party']
    
    def save(self, *args, **kwargs):
        """
        Make sure the slug is created when imported
        """
        if not self.slug:
            from django.template.defaultfilters import slugify
            
            self.slug = slugify("%s %s %s" % (self.race_date, 
                                self.party, self.state.postal))
        super(LiveMap, self).save(*args, **kwargs)
        
    def race_complete(self):
        """ Race complete means that results are finished being updated """
        return datetime.now() > self.update_results_end_date
    
    def is_published(self):
        """ "published means that results have started coming in. Most of the
        time we don't want maps being showed that have no results"""
        return datetime.now() >= self.update_results_start_date
    
    @models.permalink
    def get_absolute_url(self):
        """
        Get the absolute url for the candidate
        """
        return ('elections.views.live_map', (), {'state':self.state.postal, 'slug': self.slug })

    
    @property
    def title(self):
        """ The title of the live. This is used to specify for historical maps """
        if self.party:
            return "%s %s %s" %(self.race_date.year, self.get_party_display(), 
                                self.get_race_type_display())
        else:
            return "%s %s" %(self.race_date.year, self.get_race_type_display())

DELEGATE_ELECTION_PARTY_CHOICES = (('Dem', 'Democrat'),
                                   ('GOP', 'Republican'),)
class DelegateElection(models.Model):
    year = models.IntegerField()
    party = models.CharField(max_length=10, choices=DELEGATE_ELECTION_PARTY_CHOICES)
    race_type = models.CharField(max_length=20, choices=RACE_TYPE_CHOICES)
    total_delegates = models.IntegerField()
    delegates_needed = models.IntegerField()
    slug = models.SlugField()
    
    def __unicode__(self):
        return "%s %s - %s" % (self.year, self.get_party_display(), self.get_race_type_display())
    
    class Meta:
        ordering = ['-year', 'party']
    
    def save(self, *args, **kwargs):
        """
        Make sure the slug is created when imported
        """
        if not self.slug:
            from django.template.defaultfilters import slugify
            if self.party:
                self.slug = slugify("%s %s %s" % (self.year, 
                                self.party, self.race_type))
            else:
                self.slug = slugify("%s %s" % (self.year, 
                                self.race_type))
        super(DelegateElection, self).save(*args, **kwargs)
    
    @models.permalink
    def get_absolute_url(self):
        """
        Get the absolute url for the candidate
        """
        if not self.party:
            category = self.race_type
        else:
            category = self.party
        return ('elections.views.delegate_tracker', (), {'category':category, 'slug': self.slug })
    
    def get_state_elections(self):
        return self.delegatestateelection_set.filter(state__disabled=False)
    
    def title(self):
        return self.__unicode__()
    
class DelegateStateElection(models.Model):
    event_date = models.DateField(blank=True, null=True)
    delegate_election = models.ForeignKey(DelegateElection, editable=False)
    state = models.ForeignKey(State, editable=False)
    
    class Meta:
        ordering = ['state__name']
    
    def __unicode__(self):
        return "%s - %s" %(self.state, self.event_date)
    
    def get_candidate_results(self):
        return self.candidatedelegatecount_set.filter(delegate_count__gt=0).exclude(
                                                        candidate__last_name='Uncommitted').select_related('candidate')
    
    def candidate_count(self):
        return self.get_candidate_results().count()
    
class CandidateDelegateCount(models.Model):
    delegate_state_election = models.ForeignKey(DelegateStateElection)
    candidate = models.ForeignKey(Candidate)
    delegate_count = models.IntegerField()
    last_modified = models.DateTimeField(auto_now=True)
    winner = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s - %s" %(self.delegate_state_election, self.candidate)
    
    class Meta:
        ordering = ['delegate_count']
    
class Poll(models.Model):
    """ Model representing a Poll  """
    date = models.DateField()
    state = models.ForeignKey(State, blank=True, null=True)
    source = models.CharField(max_length=50)
    office = models.CharField(max_length=1, choices=ELECTION_OFFICE_CHOICES)
    url = models.URLField(blank=True, null=True)
    
    class Meta:
        ordering = ['-date']
    
    def __unicode__(self):
        return "%s - %s (%s)" %(self.date, self.candidate_vs_string(), self.source)
    
    def spread(self):
        """ helper method that returns the spread of applicable. This will
        only return a value. If there are 2 results """
        poll_results = self.results()
        if poll_results.count() == 2:
            ahead_result = poll_results[0]
            behind_result = poll_results[1]
            if ahead_result.result==behind_result.result:
                return 'Tie'
            else:
                return '%s + %d' %(ahead_result.candidate_name, 
                                   int(ahead_result.result-behind_result.result))
    def results(self):
        """ Helper method for returning the poll results """
        return self.pollresult_set.order_by('-result')
    
    def candidate_vs_string(self):
        candidate_name_list = []
        for result in self.results():
            candidate_name_list.append(result.candidate_name)
        return " vs. ".join(candidate_name_list)
    
class PollResult(models.Model):
    """ Poll Result Object """
    poll = models.ForeignKey(Poll)
    candidate = models.ForeignKey(Candidate, blank=True, null=True)
    write_in_candidate_name = models.CharField(max_length=100, blank=True, null=True)
    result = PercentField()
    
    class Meta:
        ordering = ['-result']
    
    def __unicode__(self):
        return "%s" %(self.candidate_name)
    
    @property
    def candidate_name(self):
        """ Return the candidates name for ease of use within templates. Note if
        the object has a candidate then this returns the last name. Else it returns
        the write in name """
        if self.candidate:
            return self.candidate.last_name
        else:
            return self.write_in_candidate_name
        
class HotRace(models.Model):
    """ Model representing a Hot Race  """
    
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, blank=True, null=True)
    office = models.CharField(max_length=1, choices=ELECTION_OFFICE_CHOICES)
    editorial_note = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True, help_text='Date of the Election')
    featured = models.BooleanField(default=False)
    class Meta:
        ordering = ['date']
    
    def __unicode__(self):
        return "%s %s - %s (%s)" %(self.name, self.candidate_vs_string(), 
                                  self.get_office_display(), self.date)
    
    def candidate_vs_string(self):
        """ create candidate vs string """
        candidate_name_list = []
        for candidate in self.candidates():
            candidate_name_list.append(candidate.candidate_name)
        return " vs. ".join(candidate_name_list)
    
    def candidates(self):
        """ Return candidate queryset """
        return self.hotracecandidate_set.all()

    if HOT_RACE_RELATION_MODELS:
        def get_related_content_type(self, content_type, relation_type=None):
            """
            Get all related items of the specified content type
            """
            objects =  self.hotracerelation_set.filter(
                content_type__model=content_type)
            if relation_type:
                objects = objects.filter(relation_type=relation_type)
            return objects
        
        def get_relation_type(self, relation_type):
            """
            Get all relations of the specified relation type
            """
            return self.hotracerelation_set.filter(relation_type=relation_type)
        
        
        
        
        
        
if HOT_RACE_RELATION_MODELS:      
    HOT_RACE_RELATION_LIMITS = reduce(lambda x, y: x|y, HOT_RACE_RELATIONS)
    class HotRaceRelationManager(models.Manager):
        """Basic manager with a few convenience methods"""
        def get_content_type(self, content_type):
            """
            Get all the related items with a specific content_type
            """
            qs = self.get_query_set()
            return qs.filter(content_type__name=content_type)
        
        def get_relation_type(self, relation_type):
            """
            Get all the related items with a specific relation_type
            """
            qs = self.get_query_set()
            return qs.filter(relation_type=relation_type)
    
    
    class HotRaceRelation(models.Model):
        """Related special items """
        hot_race = models.ForeignKey(HotRace)
        content_type = models.ForeignKey(
            ContentType, 
            limit_choices_to=HOT_RACE_RELATION_LIMITS)
        object_id = models.PositiveIntegerField()
        content_object = generic.GenericForeignKey('content_type', 'object_id')
        relation_type = models.CharField(_("Relation Type"), 
            max_length="200", 
            blank=True, 
            null=True,
            help_text=_(
                "A generic name that can be used to access the relation directly."))
        order = models.PositiveIntegerField(null=True, blank=True)
        objects = HotRaceRelationManager()
        
        def __unicode__(self):
            return unicode(self.content_object)
        
        class Meta:
            ordering = ('order',)
            
class HotRaceCandidate(models.Model):
    """ Hot Race Candidate Object """
    hot_race = models.ForeignKey(HotRace)
    candidate = models.ForeignKey(Candidate, blank=True, null=True)
    write_in_candidate_name = models.CharField(max_length=100, blank=True, null=True)
    
    def __unicode__(self):
        return "%s" %(self.candidate_name)
    
    @property
    def candidate_name(self):
        """ Return the candidates name for ease of use within templates. Note if
        the object has a candidate then this returns the last name. Else it returns
        the write in name """
        if self.candidate:
            return self.candidate.last_name
        else:
            return self.write_in_candidate_name

def calculate_checksum(obj, mapping=None):
    """ Universal checksum for models that uses the IMPORT_MAPPING attribute
    to make sure that it matches the checksum that will be calculated for an
    imported file row """
    if not mapping:
        mapping = obj.IMPORT_MAPPING
    checksum = hashlib.md5()
    for item in mapping:
        value = getattr(obj, item)
        if value:
            checksum.update(str(value))
        else:
            checksum.update('')
    return checksum.hexdigest()