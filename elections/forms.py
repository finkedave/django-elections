from django import forms
from elections.models import PollResult, HotRaceCandidate, HotRace, LiveMap, DelegateElection

class PollResultForm(forms.ModelForm):
    """ Form for making sure that a candidate object or 
    candidate name is populated"""
    class Meta:
        model = PollResult
    
    def clean(self):
        if not self.cleaned_data['candidate'] and \
                not self.cleaned_data['write_in_candidate_name']:
            raise forms.ValidationError("Candidate or 'write in candidate name' is required.")
        return self.cleaned_data


class HotRaceForm(forms.ModelForm):
    """ Form for making sure that when a office that is not president is selected that state is
    selected """
    class Meta:
        model = HotRace
    
    def clean(self):
        if self.cleaned_data['office'] != 'P' and \
                not self.cleaned_data['state']:
            raise forms.ValidationError("State is required when office type is House, Senate or Governor.")
        return self.cleaned_data
        
class HotRaceCandidateForm(forms.ModelForm):
    """ Form for making sure that a candidate object or 
    candidate name is populated"""
    class Meta:
        model = HotRaceCandidate
    
    def clean(self):
        if not self.cleaned_data['candidate'] and \
                not self.cleaned_data['write_in_candidate_name']:
            raise forms.ValidationError("Candidate or 'write in candidate name' is required.")
        return self.cleaned_data

class LiveMapForm(forms.ModelForm):
    """ Form for making sure that a candidate object or 
    candidate name is populated"""
    class Meta:
        model = LiveMap
    
    def clean(self):
        slug = self.cleaned_data['slug']
        year = self.cleaned_data['race_date'].year
        state = self.cleaned_data['state']
        error = False
        try:
            live_map = LiveMap.objects.get(race_date__year=year,
                                      slug=slug, state__state_id=state.state_id)
            if live_map.id != self.instance.id:
                error = True
        except LiveMap.DoesNotExist:
                pass
        if error:
            raise forms.ValidationError(u"Please enter a different slug. Slug must be unique per state, race date year.")
        return self.cleaned_data
    


