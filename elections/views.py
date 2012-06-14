from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.template import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _
from django.shortcuts import get_object_or_404

from .models import (Candidate, RaceCounty, RaceDistrict, CountyResult, 
                    DistrictResult, CandidateOffice, CandidateEducation, 
                    CandidateOffice, CandidatePhone, CandidateURL, 
                    ElectionEvent, PACContribution, State, District)

def state_detail(request, state):
    """
    Get a list of stuff for the state
    """
    offices = CandidateOffice.objects.filter(state=state, status_id__in=["I", "Q"])
    office_groups = {}
    for ofc in offices:
        if ofc.office in office_groups:
            office_groups[ofc.office].append(ofc)
        else:
            office_groups[ofc.office] = [ofc]
    events = ElectionEvent.objects.filter(state=state)
    if offices:
        return render_to_response(
            "elections/state_detail.html", 
            {
                "offices": office_groups,
                "all_offices": offices,
                "state": offices[0].state_name,
                "events": events,
            },
            context_instance=RequestContext(request))
    else:
        raise Http404

def lc_state_redirect(request, state):
    """
    Redirect a mixed- or lower- case state into an upper case state
    """
    return HttpResponseRedirect(reverse('state_election_details', kwargs={'state': state.upper()}))

def pac_detail(request, slug):
    contributions = PACContribution.objects.filter(slug=slug)
    if contributions:
        return render_to_response(
            "elections/pac_detail.html", 
            {
                "pac_name": contributions[0].pac_name,
                "fec_pac_id": contributions[0].fec_pac_id,
                "contributions": contributions,
            },
            context_instance=RequestContext(request))
    else:
        raise Http404
    
def state_profile(request, state):
    """
    Get the state profile 
    """
    state = get_object_or_404(State,
        slug__iexact = state)

    return render_to_response(
        "elections/state_profile.html", 
        {
            'state':state
        },
        context_instance=RequestContext(request))

def district_profile(request, state, district):
    """
    Get the district profile
    """
    district = get_object_or_404(District, 
        slug__iexact = district)

    return render_to_response(
        "elections/district_profile.html", 
        {
            'district':district,
            'state':state
        },
        context_instance=RequestContext(request))

def district_list(request, state):
    """
    Get a list of districts for the state
    """
    state = get_object_or_404(State,
        slug__iexact = state)

    return render_to_response(
        "elections/district_list.html", 
        {
            'state':state,
            'district_list':state.districts()
        },
        context_instance=RequestContext(request))
