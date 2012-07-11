from django.conf.urls.defaults import *
# try:
#     from django.views.generic import ListView, DetailView
# except ImportError:
#     from cbv import ListView, DetailView
from django.views.generic.simple import direct_to_template
from .models import (Candidate, RaceCounty, RaceDistrict, CountyResult, 
                    DistrictResult, CandidateOffice, CandidateEducation, 
                    CandidateOffice, CandidatePhone, CandidateURL,
                    PACContribution)

# urlpatterns = patterns('',
#     # url(r'^$', 'views.index', name='index'),
#     url(r'^candidates/$', ListView.as_view(model=Candidate), name='candidate_list'),
#     url(r'^candidates/(?P<pk>\d+)/$', 
#         DetailView.as_view(model=Candidate), 
#         name='candidate_detail'),
#     # url(r'^state/$'),
#     # url(r'^state/districts/$'),
#     # url(r'^state/pacs/$'),
#     
# )

urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^candidates/$', 'object_list', {
        'queryset': Candidate.objects.all(),
    }, name='candidate_list'),
    url(r'^candidates/(?P<slug>[a-zA-Z0-9_-]+)/$', 'object_detail', {
        'queryset': Candidate.objects.all(),
    }, name='candidate_detail'),
    url(r'^presidential-candidate/$', 'object_list', {
        'queryset': Candidate.objects.filter(is_presidential_candidate=True),
    }, name='presidential_candidate_list'),
    url(r'^presidential-candidate//(?P<slug>[a-zA-Z0-9_-]+)/$', 'object_detail', {
        'queryset': Candidate.objects.filter(is_presidential_candidate=True),
    }, name='presidential_candidate_detail'),
)

urlpatterns += patterns('',
    url(r'^(?P<state>[a-zA-Z]+)/profile/$', 'elections.views.state_profile', name="state_profile"),
    url(r'^(?P<state>[a-zA-Z0-9_-]+)/districts/(?P<district>[a-zA-Z0-9_-]+)/profile/$', 'elections.views.district_profile', name='district_profile'),
    url(r'^(?P<state>[A-Z][A-Z])/districts/$', 'elections.views.district_list', name="district_list"),
    
    url(r'^(?P<state>[A-Z][A-Z])/live-map/(?P<slug>[a-zA-Z0-9_-]+)/$', 'elections.views.live_map'),
    url(r'^(?P<state>[A-Z][A-Z])/live-map/$', 'elections.views.live_map'),
       
    url(r'^(?P<state>[A-Z][A-Z])/$', 'elections.views.state_detail', name="state_election_details"),
    url(r'^(?P<state>\w\w)/$', 'elections.views.lc_state_redirect', name="lc_state_redirect"),
    url(r'^pacs/(?P<slug>[a-zA-Z0-9_-]+)/$', 'elections.views.pac_detail', name='pac_detail'),
    url(r'^delegate-tracker/(?P<category>[a-zA-Z0-9_-]+)/(?P<slug>[a-zA-Z0-9_-]+)/$', 'elections.views.delegate_tracker'),
    url(r'^delegate-tracker/(?P<category>[a-zA-Z0-9_-]+)/$', 'elections.views.delegate_tracker'),
    url(r'^calendar/$', 'elections.views.calendar'),
    url(r'^polls/$', direct_to_template, {'template': 'elections/polls.html'}),
    url(r'^hot-races/$', direct_to_template, {'template': 'elections/hot_races.html'}),
    
    
    
    
        
)