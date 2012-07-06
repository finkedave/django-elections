""" Tags supporting the django-elections app"""
from django import template
from django.db.models import Sum
from django.template import Variable, VariableDoesNotExist
register = template.Library()

from elections.models import PACContribution, Candidate, Poll, HotRace
from elections import to_bool

def resolve(var, context):
    try:
        return var.resolve(context)
    except VariableDoesNotExist:
        try:
            return var.var
        except AttributeError:
            return var

@register.tag('get_pac_contribution_list')
def do_get_pac_contribution_list(parser, token):
    """
    Get set amount of pacs that have contributed the most money. Where 
    count is the number you want returned
    """
    try:
        tag_name, count, as_txt, var = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("'get_pac_contribution_list' requires a count, a variable name.")
    return PacContributionListNode(count, var)


class PacContributionListNode(template.Node):
    """
    Contribution Node that creates the pac list
    """
    def __init__(self, count, var_name):
        self.count = Variable(count)
        self.var_name = var_name
        
    def render(self, context):
        count = resolve(self.count, context)
        top_pac_list = PACContribution.objects.values(
                            'fec_pac_id', 'pac_name', 'slug').annotate(
                            total_amount=Sum('amount')).order_by('-total_amount')
        # If the count is greater count only use the first to count
        if len(top_pac_list) > count:
            top_pac_list = top_pac_list[:count]
        context[self.var_name] = top_pac_list
        
        return ''
    
@register.tag('get_pac_contribution_candidate_list')
def do_get_pac_contribution_candidate_list(parser, token):
    """
    Get the top candidates who have received the most money from pacs
    """
    proper_form = "{% get_pac_contribution_candidate_list count [party_id] as var %}"

    try:
        bits = token.split_contents()
        count = bits[1]
        if len(bits) == 5:
            party = bits[2]
            var = bits[4]
        elif len(bits) == 4:
            var = bits[3]
            party = None
        else:
            raise template.TemplateSyntaxError("%s tag shoud be in the form: %s" % (bits[0], proper_form))

    except ValueError:
        raise template.TemplateSyntaxError("%s tag shoud be in the form: %s" % (bits[0], proper_form))
    return PacContributionCandidateListNode(count, party, var)


class PacContributionCandidateListNode(template.Node):
    """ Node that creates the list and sets it in context"""
    def __init__(self, count, party, var_name):
        self.count = Variable(count)
        if party:
            self.party = Variable(party)
        else:
            self.party = None
        self.var_name = var_name
        
    def render(self, context):
        count = resolve(self.count, context)
        if self.party:
            pac_qs = PACContribution.objects.filter(party_id=resolve(self.party, context))
        else:
            pac_qs = PACContribution.objects 
            
        top_pac_contribution_cadidate_list = pac_qs.exclude(
                                candidate=None).values('candidate').annotate(
                                total_amount=Sum('amount')).order_by('-total_amount')
        
        # if the returned number is greater them max cut the rest off
        if len(top_pac_contribution_cadidate_list) > count:
            top_pac_contribution_cadidate_list = top_pac_contribution_cadidate_list[:count]
        
        # We actually need the candidate object here instead of just the id. So get the 
        # object and set the total contribution into the object
        candidate_list = []
        for pac_contribution_cadidate in top_pac_contribution_cadidate_list:
            candidate = Candidate.objects.get(pk=pac_contribution_cadidate['candidate'])
            candidate.total_contribution = pac_contribution_cadidate['total_amount']
            candidate_list.append(candidate)
        context[self.var_name] = candidate_list
        
        return ''
    

@register.tag('get_presidential_candidate_list')
def do_get_presidential_candidate_list(parser, token):
    """
    Gets all the candidates that are have is_presidential_candidate set to True
    """
    proper_form = "{% get_presidential_candidate_list [party_id] [is_active] as var %}"
    try:
        bits = token.split_contents()

        if len(bits) > 3:
            party = bits[1]
            if len(bits) == 5:
                is_active = bits[2]
                var = bits[4]
            else:
                is_active = None
                var = bits[3]
        elif len(bits)==3:
            var = bits[2]
            party = None
            is_active = None
        else:
            raise template.TemplateSyntaxError("%s tag shoud be in the form: %s" % (bits[0], proper_form))
    except ValueError:
        raise template.TemplateSyntaxError("%s tag shoud be in the form: %s" % (bits[0], proper_form))
    return PresidentialCandiateListNode(is_active, party, var)


class PresidentialCandiateListNode(template.Node):
    """
    Node that creates the presidential candidate list
    """
    def __init__(self, is_active, party, var_name):
        self.var_name = var_name
        if is_active:
            self.is_active = Variable(is_active)
        else:
            self.is_active = None
        if party:
            self.party = Variable(party)
        else:
            self.party = None

    def render(self, context):
        presidential_candidate_qs = Candidate.objects.filter(is_presidential_candidate=True)
        if self.is_active:
            is_active_resolved = resolve(self.is_active, context)
            if is_active_resolved:
                presidential_candidate_qs = presidential_candidate_qs.filter(is_active=to_bool(
                                                                resolve(self.is_active, context)))
        if self.party:
            party_resolved = resolve(self.party, context)
            if party_resolved:
                presidential_candidate_qs = presidential_candidate_qs.filter(offices__party_id=resolve(
                                        self.party, context))
        presidential_candidate_qs = presidential_candidate_qs.order_by('-is_active', 'offices__party_id')
        context[self.var_name] = presidential_candidate_qs.distinct('politician_id')
        
        return ''

@register.tag('get_latest_polls')
def do_get_latest_polls(parser, token):
    """
    Get the latest polls, latest polls are counted by date. So if someone says i want 
    the lateest 10 polls. That means get all the polls for the latest 10
    dates. Thre might be more then 10 polls returned because more then one poll
    can be done in a day for different races.
    """
    proper_form = "{% get_latest_polls count [office] [state_id] as var %}"

    try:
        bits = token.split_contents()
        count = bits[1]
        
        if len(bits) >= 5:
            office = bits[2]
            office = office.replace("'", '').replace('"', '')
            if len(bits) > 5:
                state_id = bits[3]
                state_id = state_id.replace("'", '').replace('"', '')
                var = bits[5]
            else:
                var = bits[4]
                state_id = None
        else:
            office = None
            var = bits[3]
            state_id = None

    except ValueError:
        raise template.TemplateSyntaxError("%s tag shoud be in the form: %s" % (bits[0], proper_form))
    return LatestPollsNode(count, office, state_id, var)

class LatestPollsNode(template.Node):
    """
    Node that uses the arguments sent in to return the list
    """
    def __init__(self, count, office, state_id, var):
        self.count = Variable(count)
        self.var_name = var
        if state_id:
            self.state_id = Variable(state_id)
        else:
            self.state_id = None
        if office:
            self.office = Variable(office)
        else:
            self.office = None
    
    def render(self, context):
        count = resolve(self.count, context)
        
        polls_qs = Poll.objects.order_by('-date')
        
        if self.state_id:
            state_id = resolve(self.state_id, context)
            # All states mean genearl poll, ie no state definted
            if state_id.lower()=='all':
                polls_qs = polls_qs.filter(state=None)
            else:
                polls_qs = polls_qs.filter(state__state_id=state_id)
        if self.office:
            polls_qs = polls_qs.filter(office=resolve(self.office, context))
            
        dates = polls_qs.values_list('date', flat=True)    
        if dates.count() > count:
            dates = dates[:count]
        
        latest_polls = polls_qs.filter(date__in=dates)

        context[self.var_name] = latest_polls
        
        return ''

@register.tag('get_hot_races')
def do_get_hot_races(parser, token):
    """
    Get Hot Races. Office and state can be defined for filtering.
    The valies for office are P, G, H and S
    """
    proper_form = "{% get_hot_races [office] [state_id] as var %}"

    try:
        bits = token.split_contents()
        if len(bits) >= 4:
            office = bits[1]
            office = office.replace("'", '').replace('"', '')
            if len(bits) > 4:
                state_id = bits[2]
                state_id = state_id.replace("'", '').replace('"', '')
                var = bits[4]
            else:
                var = bits[3]
                state_id = None
        else:
            office = None
            var = bits[2]
            state_id = None

    except ValueError:
        raise template.TemplateSyntaxError("%s tag shoud be in the form: %s" % (bits[0], proper_form))
    return HotRacesNode(office, state_id, var)

class HotRacesNode(template.Node):
    """
    Node that uses the arguments sent in to return the list
    """
    def __init__(self, office, state_id, var):
        self.var_name = var
        if state_id:
            self.state_id = Variable(state_id)
        else:
            self.state_id = None
        if office:
            self.office = Variable(office)
        else:
            self.office = None
    
    def render(self, context):
        """ Set the queryset list into context as variable name"""
        hot_race_qs = HotRace.objects.order_by('date')
        
        if self.state_id:
            state_id = resolve(self.state_id, context)
            # All states mean genearl poll, ie no state definted
            if state_id.lower()=='all':
                hot_race_qs = hot_race_qs.filter(state=None)
            else:
                hot_race_qs = hot_race_qs.filter(state__state_id=state_id)
        if self.office:
            hot_race_qs = hot_race_qs.filter(office=resolve(self.office, context))

        context[self.var_name] = hot_race_qs
        
        return ''