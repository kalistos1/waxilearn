from django import forms
from .models import SignalMembership,  CryptoSignal

class SignalMembershipSubType(forms.ModelForm):
    class Meta:
        model=SignalMembership
        fields=('slug','membership_type','duration','duration_period','price')

    def __init__(self, *args, **kwargs):
        super(SignalMembershipSubType, self).__init__(*args, **kwargs)
        self.fields['slug'].widget.attrs.update({'class' : 'form-control', 'id':'slug'})
        self.fields['membership_type'].widget.attrs.update({'class' : 'form-control', 'id':'membership_type'})
        self.fields['duration'].widget.attrs.update({'class' : 'form-control', 'id':'duration'})
        self.fields['duration_period'].widget.attrs.update({'class' : 'form-control', 'id':'duration_period'})
        self.fields['price'].widget.attrs.update({'class' : 'form-control', 'id':'price'})




class CryptoSignalForm(forms.ModelForm):
    class Meta:
        model = CryptoSignal
        fields ={
            'instructor','title','slug','photo','description','body',
        }
    
    def __init__(self ,*args, **kwargs):
        super(CryptoSignalForm, self).__init__(*args, **kwargs)
        self.fields['instructor'].widget.attrs.update({'class' : 'form-control'})     
        self.fields['title'].widget.attrs.update({'class' : 'form-control'})     
        self.fields['slug'].widget.attrs.update({'class' : 'form-control'})   
        self.fields['photo'].widget.attrs.update({'class' : 'form-control'})    
        self.fields['description'].widget.attrs.update({'class' : 'form-control'})
        self.fields['body'].widget.attrs.update({'class' : 'form-control'})   
        
