from django import forms
from elections.models import PollResult, HotRaceCandidate

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

