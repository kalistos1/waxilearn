from django import forms
from .models import Membership

class StudentMembershipSubType(forms.ModelForm):
    class Meta:
        model=Membership
        fields=('slug','membership_type','duration','duration_period','price')

    def __init__(self, *args, **kwargs):
        super(StudentMembershipSubType, self).__init__(*args, **kwargs)
        self.fields['slug'].widget.attrs.update({'class' : 'form-control', 'id':'slug'})
        self.fields['membership_type'].widget.attrs.update({'class' : 'form-control', 'id':'membership_type'})
        self.fields['duration'].widget.attrs.update({'class' : 'form-control', 'id':'duration'})
        self.fields['duration_period'].widget.attrs.update({'class' : 'form-control', 'id':'duration_period'})
        self.fields['price'].widget.attrs.update({'class' : 'form-control', 'id':'price'})
    
