from django.contrib import admin
from .models import (Candidate, RaceCounty, RaceDistrict, CountyResult, 
                    DistrictResult, CandidateEducation, 
                    CandidateOffice, CandidatePhone, CandidateURL, State, LiveMap,
                    ElectionEvent, Poll, PollResult, HotRace, HotRaceCandidate,
                    CandidateDelegateCount, DelegateStateElection)
from elections.forms import PollResultForm, HotRaceCandidateForm, HotRaceForm, \
                LiveMapForm
from genericcollection import GenericCollectionTabularInline
from settings import HOT_RACE_RELATION_MODELS
from .settings import IMAGE_MODEL

if IMAGE_MODEL:
    IMAGE_FIELDS = ('photo', 'photo_fk', 'thumbnail', 'thumbnail_fk')
else:
    IMAGE_FIELDS = ('photo', 'thumbnail')

class EducationInline(admin.TabularInline):
    model = CandidateEducation
    fields = ('degree', 'major', 'school_name', 'school_type')
    extra = 0


class OfficeInline(admin.TabularInline):
    model = CandidateOffice
    fields = ('office',)
    extra = 0

class PhoneInline(admin.TabularInline):
    model = CandidatePhone
    fields = ('phone_number',)
    extra = 0

class URLInline(admin.TabularInline):
    model = CandidateURL
    fields = ('url',)
    extra = 0

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'timestamp',)
    list_filter = ('gender', 'religion', 'ethnicity',)
    search_fields = ('last_name', 'first_name')
    prepopulated_fields = {"slug": ('first_name', 'middle_name', 'last_name', 'junior', 'politician_id')}
    if IMAGE_MODEL:
        raw_id_fields = ('photo_fk', 'thumbnail_fk')
    fieldsets = (
        (None, {
            'fields': (('first_name', 'middle_name', 'last_name', 'junior'), 
                       ('residence_place', 'residence_state'),'is_presidential_candidate', 'is_active'),
        }),
        ('Demographics', {
            'fields': ('gender', ('ethnicity', 'hispanic'), 'religion',)
        }),
        ('Birth Info', {
            'fields': ('birth_date', ('birth_place', 'birth_state', 'birth_country'), 'birth_province',)
        }),
        ('Other Info', {
            'fields': ('year_first_elected', 'biography', 'profile', 'campaigns', 'slug', 'politician_id',)
        }),
        ('Images', {
            'fields': IMAGE_FIELDS
        }),
    )
    
    inlines = [
        EducationInline, OfficeInline, PhoneInline, URLInline,
    ]

class ElectionEventAdmin(admin.ModelAdmin):
    list_display = ('state', 'event_date', 'description')
    list_filter = ('state',)
    date_hierarchy = 'event_date'
    search_fields = ('state', 'description')

class LiveMapAdmin(admin.ModelAdmin):
    """ Live Map Admin """
    list_display = ('state', 'race_date', 'race_type', 'office', 'seat_name',
                    'update_results_start_date', 'active')
    list_editable = ('active',)
    list_filter = ('state', 'race_date', 'race_type', 'office')
    date_hierarchy = 'race_date'
    prepopulated_fields = {"slug": ('race_type', 'office', 'seat_name')}
    form = LiveMapForm
    
class StateAdmin(admin.ModelAdmin):
    """ State Admin, We only want to show the required fields and fields
    for live maps. We don't want one to change fields that are imported """
    fields = ('state_id', 'postal', 'name', 'disabled', 'linkable', 'livemap_state_id', 'latitude', 
              'longitude', 'livemap_state_zoom')

class PollResultInline(admin.TabularInline):
    """ Inline for Poll result """
    model = PollResult
    raw_id_fields = ['candidate']
    form = PollResultForm
    extra = 2
    
class PollAdmin(admin.ModelAdmin):
    """ Admin for the Poll model  """
    list_display = ('date', 'state', 'office', 'source')
    inlines = [
        PollResultInline
    ]

if IMAGE_MODEL:
    RAW_ID_FIELDS = ['candidate', 'write_in_photo_fk']
else:
    RAW_ID_FIELDS = ['candidate']
    
class HotRaceCandidateInline(admin.TabularInline):
    """ Inline for Hot race candidates """
    model = HotRaceCandidate
    raw_id_fields = RAW_ID_FIELDS
    form = HotRaceCandidateForm
    extra = 2

if HOT_RACE_RELATION_MODELS:
    from elections.models import HotRaceRelation
    
    class InlineHotRaceRelation(GenericCollectionTabularInline):
        """ Inline Special Relation class for showing relations """
        model = HotRaceRelation
        template = 'admin/edit_inlines/gen_coll_tabular.html'
            
class HotRaceAdmin(admin.ModelAdmin):
    """ Hot Race admin. Only show inline relations if in settings
    HOT_RACE_RELATION_MODELS is set """
    list_display = ('name', 'office', 'state', 'date')
    form = HotRaceForm
    if HOT_RACE_RELATION_MODELS:
        inlines = [HotRaceCandidateInline, InlineHotRaceRelation]
    else:
        inlines = [HotRaceCandidateInline]

class CandidateDelegateCountInline(admin.TabularInline):
    model = CandidateDelegateCount
    raw_id_fields = ['candidate']
    extra = 0
    
class DelegateStateElectionAdmin(admin.ModelAdmin):
    list_display = ('delegate_election', 'state', 'event_date',)
    search_fields = ['state__name', 'state__state_id']
    inlines = [CandidateDelegateCountInline]
    
admin.site.register(RaceCounty)
admin.site.register(RaceDistrict)
admin.site.register(CountyResult)
admin.site.register(DistrictResult)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(ElectionEvent, ElectionEventAdmin)
admin.site.register(CandidateOffice)
admin.site.register(CandidateEducation)
admin.site.register(CandidatePhone)
admin.site.register(State, StateAdmin)
admin.site.register(LiveMap, LiveMapAdmin)
admin.site.register(Poll, PollAdmin)
admin.site.register(HotRace, HotRaceAdmin)
admin.site.register(DelegateStateElection, DelegateStateElectionAdmin)