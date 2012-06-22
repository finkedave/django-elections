""" Tags supporting the django-elections app"""
from django import template
from django.db.models import Sum
from django.template import Variable, VariableDoesNotExist
register = template.Library()

from elections.models import PACContribution, Candidate

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
    try:
        tag_name, as_txt, var = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("'get_pac_contribution_list' requires an 'as variable name'.")
    return PresidentialCandiateListNode(var)


class PresidentialCandiateListNode(template.Node):
    """
    Node that creates the presidential candidate list
    """
    def __init__(self, var_name):
        self.var_name = var_name
        
    def render(self, context):
        presidential_candidate_list = Candidate.objects.filter(is_presidential_candidate=True)
        context[self.var_name] = presidential_candidate_list
        
        return ''