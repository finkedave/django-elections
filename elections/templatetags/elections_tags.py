""" Tags supporting the django-elections app"""
from django import template
from django.core.cache import cache
from django.db.models import Sum
from django.template import Variable, VariableDoesNotExist, TemplateSyntaxError
from elections.models import PACContribution, Candidate, Poll, HotRace, \
                             CandidateFEC, CandidateMoney, HotRaceRelation
from elections import to_bool

from django.db.models import get_model

register = template.Library()

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
            pac_qs = PACContribution.objects.filter(
                        party_id=resolve(self.party, context))
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
            raise template.TemplateSyntaxError(
                "%s tag shoud be in the form: %s" % (bits[0], proper_form))
    except ValueError:
        raise template.TemplateSyntaxError(
            "%s tag shoud be in the form: %s" % (bits[0], proper_form))
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
        presidential_candidate_qs = Candidate.objects.filter(
                                        is_presidential_candidate=True)
        if self.is_active:
            is_active_resolved = resolve(self.is_active, context)
            if is_active_resolved:
                presidential_candidate_qs = presidential_candidate_qs.filter(
                                    is_active=to_bool(resolve(self.is_active, context)))
        if self.party:
            party_resolved = resolve(self.party, context)
            if party_resolved:
                presidential_candidate_qs = presidential_candidate_qs.filter(
                                offices__party_id=resolve(self.party, context))
        presidential_candidate_qs = presidential_candidate_qs.order_by(
                                            '-is_active', 'offices__party_id')
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
        raise template.TemplateSyntaxError(
                    "%s tag shoud be in the form: %s" % (bits[0], proper_form))
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
    proper_form = "{% get_hot_races [office] [state_id] [featured] as var %}"

    try:
        bits = token.split_contents()
        
        counter = 0
        
        tag_name = None
        office = None
        state_id = None
        featured = None
        var = None
        variables = [tag_name, office, state_id, featured]
        # Set the variables if sent in
        for bit in bits:
            if bit == 'as':
                var = bits[counter+1]
                break
            else:
                variables[counter] = bit.replace("'", '').replace('"', '')
            counter += 1
            
    except IndexError:
        raise template.TemplateSyntaxError(
                "%s tag shoud be in the form: %s" % (tag_name, proper_form))
    
    if not var:
        raise template.TemplateSyntaxError(
                "%s tag shoud be in the form: %s" % (bits[0], proper_form))
    return HotRacesNode(variables[1], variables[2], variables[3], var)

class HotRacesNode(template.Node):
    """
    Node that uses the arguments sent in to return the list
    """
    def __init__(self, office, state_id, featured, var):
        self.var_name = var
        if state_id:
            self.state_id = Variable(state_id)
        else:
            self.state_id = None
        if office:
            self.office = Variable(office)
        else:
            self.office = None
            
        if featured:
            self.featured = Variable(featured)
        else:
            self.featured = None

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
            
            
        if self.featured:
            
            hot_race_qs = hot_race_qs.filter(
                            featured=to_bool(resolve(self.featured, context)))
        context[self.var_name] = hot_race_qs
        
        return ''
@register.tag('get_latest_objects_by_content_type')
def do_get_latest_objects_by_content_type(parser, token):
    """
    Get the latest objects by special
    
    {% get_latest_objects_by_content_type special app_label model_name [relation_type,-relation_type2,etc] [date_field] [number] as [var_name] %}
    """
    proper_form = "{% get_latest_objects_by_content_type special app_label model_name [relation_type,-relation_type2,etc] [date_field] [number] as [var_name] %}"
    bits = token.split_contents()
    
    if bits[-2] != 'as':
        raise TemplateSyntaxError("%s tag shoud be in the form: %s" % (bits[0], proper_form))
    if len(bits) < 6:
        raise TemplateSyntaxError("%s tag shoud be in the form: %s" % (bits[0], proper_form))
    if len(bits) > 9:
        raise TemplateSyntaxError("%s tag shoud be in the form: %s" % (bits[0], proper_form))
    special = bits[1]
    app_label = bits[2]
    model_name = bits[3]
    var_name = bits[-1]
    
    
    if bits[4] != 'as':
        relation_type_string = bits[4]
    else:
        relation_type_string = None
    
    if len(bits) > 6 and bits[5] != 'as':
        date_field = bits[5]
    else:
        date_field = None

    if len(bits) > 7 and bits[6] != 'as':
        num = bits[6]
    else:
        num = None 
    return LatestObjectsNode(var_name, special,  app_label, model_name, relation_type_string,
                     date_field, num)

class LatestObjectsNode(template.Node):
    def __init__(self, var_name, special, app_label, model_name, relation_type_string,
                date_field, num):
        """Get latest objects of app_label.model_name"""
        self.special = Variable(special)
        self.model_name = Variable(model_name)
        self.app_label = Variable(app_label)
        if date_field:
            self.date_field = Variable(date_field)
        else:
            self.date_field = None
        if num:
            self.num =  Variable(num)
        else:
            self.num = None
        if relation_type_string:
            self.relation_type_string = Variable(relation_type_string)
        else:
            self.relation_type_string = None
        self.var_name = var_name
    
    def get_cache_key(self, special,  app_label, model_name, relation_type_string, 
                     date_field, num):
        """Get the cache key"""
        key = 'latest_objects.special_%s' % '.'.join([str(special.id),  app_label,
                             model_name, str(relation_type_string),
                str(date_field), str(num)])
        return key
    
    def render(self, context):
        """Render this sucker"""
        special = resolve(self.special, context)
        app_label = resolve(self.app_label, context)
        model_name = resolve(self.model_name, context)
        if self.relation_type_string:
            relation_type_string = resolve(self.relation_type_string, context)
        else:
            relation_type_string = None
            
        if self.date_field:
            date_field = resolve(self.date_field, context)
        else:
            date_field = None
        if self.num:
            num = resolve(self.num, context)
        else:
            num = None
            
        relation_type_include_list = []
        relation_type_exclude_list = []
        if relation_type_string:
            relation_type_list = relation_type_string.split(',')
            for relation_type in relation_type_list:
                if relation_type[0] == '-':
                    relation_type_exclude_list.append(relation_type[1:])
                elif relation_type:
                    relation_type_include_list.append(relation_type)

        cache_key = self.get_cache_key(special, app_label,  model_name, relation_type_string, date_field, num)
        result = cache.get(cache_key)
        if not result:
            result = get_latest_objects_by_content_type(special, app_label, model_name, relation_type_include_list,
                                                        relation_type_exclude_list, date_field, num)
        
            cache.set(cache_key, result, 300)
        context[self.var_name] = result
        
        return ''
    
def get_latest_objects_by_content_type(hot_race, app_label, model_name, 
                                       relation_type_include_list,
                                       relation_type_exclude_list, date_field, num):
    """ Helper method that constructs latest objects. First we get the objects by content
    type. Include relattion types, exclude ones that are asked to be excluded. Then get
    the ids and use them in a query directly against the related Model object. This
    way they can be sorted, one cavet is the ability for a relation to have an order
    associated to it. So. First we sort by order, then any relations that don't have 
    order will be ordered by field sent in. So things with order will always come first"""
    if not isinstance(hot_race, HotRace):
        hot_race = HotRace.objects.get(slug=str(hot_race))
    related_objects_qs = hot_race.get_related_content_type(model_name)
   
    
    if relation_type_include_list:
        related_objects_qs = related_objects_qs.filter(relation_type__in=relation_type_include_list)
    if relation_type_exclude_list:
        related_objects_qs = related_objects_qs.exclude(relation_type__in=relation_type_exclude_list)
    
    ordered_related_objects = related_objects_qs.exclude(order=None)  
    non_ordered_related_objects = related_objects_qs.filter(order=None)  
                                               
    non_ordered_related_objects_id_list = non_ordered_related_objects.values_list('object_id', flat=True)
    ordered_related_objects_id_list = ordered_related_objects.values_list('object_id', flat=True)
    
    m = get_model(app_label, model_name)
    
    relation_table = HotRaceRelation._meta.db_table
    object_table = m._meta.db_table
    relation_pk = HotRaceRelation._meta.pk.column
    
    order_by_list=['%s.order' % relation_table]
    
    non_ordered_related_objects =  m.objects.filter(pk__in=non_ordered_related_objects_id_list)
    if date_field:
        non_ordered_related_objects = non_ordered_related_objects.order_by('-%s' % date_field)
        order_by_list.append('-%s' % date_field)
    # now filter the the ordered related objects 
    
    ordered_related_objects = m.objects.filter(pk__in=ordered_related_objects_id_list).extra(
                                tables=[relation_table],
                                where=['%s.object_id=%s.%s' % (relation_table, object_table, relation_pk)],
                                order_by=order_by_list
                            )
    
    related_objects = list(ordered_related_objects)
    related_objects.extend(list(non_ordered_related_objects))
    
    if num:
        related_objects = related_objects[:num]
    
        if num == 1:
            result_count = related_objects.count()
            if result_count==1:
                return related_objects[0]
            else:
                return []
        
    return related_objects
    
class RelatedNode(template.Node):
    """ Related Node for getting related objects for hot races, / anything"""
    def __init__(self, the_object, var_name, content_type=None, relation_type=None):
        self.content_type = content_type
        self.relation_type = relation_type
        self.object = template.Variable(the_object)
        self.var_name = var_name
        
    def render(self, context):
        try:
            the_obj = self.object.resolve(context)
            if self.content_type:
                context[self.var_name] = the_obj.get_related_content_type(self.content_type)
            elif self.relation_type:
                context[self.var_name] = the_obj.get_relation_type(self.relation_type)
            else:
                context[self.var_name] = []
            return ''
        except template.VariableDoesNotExist:
            return ''
            
@register.tag('get_related_content_type')
def do_get_related_content_type(parser, token):
    """
    Gets relations to a story based on the content type
    
    {% get_related_content_type item content_type as var_name %}
    
    {% get_related_content_type object Image as photo %}
    """
    try:
        tag_name, obj, content_type, as_txt, var = token.split_contents()
        content_type = content_type.replace("'", '').replace('"', '')
    except ValueError:
        raise template.TemplateSyntaxError("'get_related_content_type' requires an object, content_type and a variable name.")
    return RelatedNode(obj, var, content_type=content_type)

@register.tag('get_relation_type')
def do_get_relation_type(parser, token):
    """
    Gets the relations to a story based on the relation type
    
    {% get_relation_type item relation_type as var_name %}
    
    {% get_relation_type object leadphoto as leadphoto %}
    """
    try:
        tag_name, obj, relation_type, as_txt, var = token.split_contents()
        relation_type = relation_type.replace("'", '').replace('"', '')
    except ValueError:
        raise template.TemplateSyntaxError("'get_relation_type' requires an object, relation_type and a variable name.")
    return RelatedNode(obj, var, relation_type=relation_type)
    
@register.tag('get_fec_money_candidate_list')
def do_get_fec_money_candidate_list(parser, token):
    """
    Get the top candidates who have the most money in any field that is sent in, via the
    field comaprison
    """
    proper_form = "{% get_fec_money_candidate_list field_comparison count [party_id] as var %}"

    try:
        bits = token.split_contents()
        field_comparison = bits[1]
        count = bits[2]
        if len(bits) == 6:
            party = bits[3]
            var = bits[5]
        elif len(bits) == 5:
            var = bits[4]
            party = None
        else:
            raise template.TemplateSyntaxError("%s tag shoud be in the form: %s" % (bits[0], proper_form))
    except:
        raise template.TemplateSyntaxError("%s tag shoud be in the form: %s" % (bits[0], proper_form))
    return FECMoneyCandidateListNode(field_comparison, count, party, var)


class FECMoneyCandidateListNode(template.Node):
    """ Node that creates the list and sets it in context"""
    def __init__(self, field_comparison, count, party,  var_name):
        self.count = Variable(count)
        self.field_comparison = Variable(field_comparison)
        self.var_name = var_name
        
        if party:
            self.party = template.Variable(party)
        else:
            self.party = None
            
    def render(self, context):
        """ To get a list of candidates since there are no foriegn keys between
        tables to get to the fec table. We use extra to join all the tables and
        add an order by field """
        count = resolve(self.count, context)
        field_comparison = resolve(self.field_comparison, context)

        fec_table = CandidateFEC._meta.db_table
        money_table = CandidateMoney._meta.db_table
        candidate_table = Candidate._meta.db_table
        
        candidate_qs = Candidate.objects
        if self.party:
            party_resolved = resolve(self.party, context)
            if party_resolved:
                party_where = "%s.party='%s'" % (fec_table, party_resolved.upper())
            else:
                party_where = '1=1'
        candidate_list = candidate_qs.extra(
                    tables=[fec_table, money_table],
                    where=['%s.fec_candidate_id=%s.fec_candidate_id' % (fec_table, money_table), 
                           '%s.candidate_id=%s.politician_id' %(money_table, candidate_table),
                           '%s.%s is not null' %(fec_table, field_comparison),
                           party_where
                           ],
                    order_by=['-%s.%s' % (fec_table, field_comparison)],
                    )
        # if the returned number is greater them max cut the rest off
        if len(candidate_list) > count:
            candidate_list = candidate_list[:count]
        
        context[self.var_name] = candidate_list
        
        return ''