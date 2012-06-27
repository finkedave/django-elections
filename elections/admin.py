from django.contrib import admin
from .models import (Candidate, RaceCounty, RaceDistrict, CountyResult, 
                    DistrictResult, CandidateOffice, CandidateEducation, 
                    CandidateOffice, CandidatePhone, CandidateURL, State, LiveMap,
                    ElectionEvent)
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
    list_display = ('state', 'race_date', 'race_type', 'party', 
                    'update_results_start_date')
    list_filter = ('state', 'race_date', 'party')
    date_hierarchy = 'race_date'
    prepopulated_fields = {"slug": ('race_date', 'party', 'state')}
    
class StateAdmin(admin.ModelAdmin):
    """ State Admin, We only want to show the required fields and fields
    for live maps. We don't want one to change fields that are imported """
    fields = ('state_id', 'postal', 'name', 'livemap_state_id', 'latitude', 
              'longitude', 'livemap_state_zoom')
    
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
