from django.shortcuts import render,redirect
from .forms import ContactForm
from django.core.mail import send_mail
from django.contrib import messages
from onlinecourses.models import Course
from bettingsubscription .models import BettingMembership
from membership .models import Membership
from signalsubscription . models import SignalMembership

# Create your views here.
def index(request):
    contact_form = ContactForm()
    courses = Course.objects.all().order_by('-created_on')[:6]
    learning_sub = Membership.objects.all()
    betting_sub = BettingMembership.objects.all()
    signal_sub = SignalMembership.objects.all()

    context = {
            'contact_form':contact_form,
            'courses':courses,
            'learning_sub':learning_sub,
            'betting_sub':betting_sub,
            'signal_sub':signal_sub,
    }
    return render(request, 'index/index.html',context)


def Contact(request):
    if request.method =="POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contactData = contact_form.cleaned_data
    
            get_first_name =contactData['first_name']
            get_last_name =contactData['last_name']
            get_phone=contactData['phone']
            get_email=contactData['email']
            get_subject =contactData['subject']
            get_message =contactData['message']
            body =  'First name =',get_first_name ,'\n', 'Last Name =', get_last_name,'\n','Phone =',get_phone,'\n', 'Message =',get_message
	
            #send_mail(get_subject , body , get_email, ['ucktech1@gmail.com', get_email])
            contact_form.save()

            messages.success(request, ('message successfuly sent!'))
            return redirect('index')
        else:
            messages.error(request, ('Message not sent Checkform.'))
    else:
        contact_form = ContactForm()
        context = {
            'contact_form':contact_form,
        }
    return render(request, 'index/index.html', context)