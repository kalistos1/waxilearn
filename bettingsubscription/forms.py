from django import forms
from django.forms import fields
from .models import BetForcast,BettingMembership



class BetForecastForm(forms.ModelForm):
    class Meta:
        model = BetForcast
        fields ={
            'title','slug','description','home_team','away_team','total_odd','start_time','play_status','forcast_win_status',
        }
    
    def __init__(self ,*args, **kwargs):
        super(BetForecastForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class' : 'form-control'}) 
        self.fields['slug'].widget.attrs.update({'class' : 'form-control'})     
        self.fields['description'].widget.attrs.update({'class' : 'form-control'})     
        self.fields['home_team'].widget.attrs.update({'class' : 'form-control'})   
        self.fields['away_team'].widget.attrs.update({'class' : 'form-control'})     
        self.fields['total_odd'].widget.attrs.update({'class' : 'form-control'})
        self.fields['start_time'].widget.attrs.update({'class' : 'form-control'})   
        self.fields['play_status'].widget.attrs.update({'class' : 'form-control'})     
        self.fields['forcast_win_status'].widget.attrs.update({'class' : 'form-control'})


class BettingMembershipSubType(forms.ModelForm):
    class Meta:
        model=BettingMembership
        fields=('slug','membership_type','duration','duration_period','price')

    def __init__(self, *args, **kwargs):
        super(BettingMembershipSubType, self).__init__(*args, **kwargs)
        self.fields['slug'].widget.attrs.update({'class' : 'form-control', 'id':'slug'})
        self.fields['membership_type'].widget.attrs.update({'class' : 'form-control', 'id':'membership_type'})
        self.fields['duration'].widget.attrs.update({'class' : 'form-control', 'id':'duration'})
        self.fields['duration_period'].widget.attrs.update({'class' : 'form-control', 'id':'duration_period'})
        self.fields['price'].widget.attrs.update({'class' : 'form-control', 'id':'price'})
    
