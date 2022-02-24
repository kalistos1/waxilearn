from django import forms
from .models import ContactMessage



class ContactForm(forms.ModelForm):

    class Meta:
        model = ContactMessage
        fields = {'first_name','last_name','email','phone','subject','message'}

    def __init__(self, *args , **kwargs):
        super(ContactForm,self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class' : 'form-control text-center','id':'form_name','placeholder':'Enter your first name *','required':'required','data-error':'First name is required', })
        self.fields['last_name'].widget.attrs.update({'class' : 'form-control text-center','id':'form_lastname','placeholder':'Enter your last name *','required':'required','data-error':'last name is required', })
        self.fields['email'].widget.attrs.update({'class' : 'form-control text-center','id':'form_email','placeholder':'Enter your email *','required':'required','data-error':'valid email is required', })
        self.fields['phone'].widget.attrs.update({'class' : 'form-control text-center','id':'form_phone','placeholder':'Enter your phone *','required':'required','data-error':'valid phone number is required', })
        self.fields['subject'].widget.attrs.update({'class' : 'form-control text-center','id':'form_subject','placeholder':'subject of the message *','required':'required','data-error':'Subject is required', })
        self.fields['message'].widget.attrs.update({'class' : 'form-control text-center','id':'form_message','placeholder':'Your message *','required':'required','data-error':'Please leave your Message', })



