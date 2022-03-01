from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib import messages
from .forms import LoginForm, RegistrationForm, UserForm, ProfileForm, ProfilePhotoForm, ChangePasswordForm, ChangeUsernameForm
from onlinecourses.models import Course
from django.contrib.auth.decorators import login_required
#from onlinecourses.models import StudentCourses, Course
from datetime import date
from .models import Notification
from django.core.paginator import Paginator
from signalsubscription.models import *
from bettingsubscription.models import *
from membership.models import *
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from membership.forms import StudentMembershipSubType
from bettingsubscription.forms import BettingMembershipSubType
from signalsubscription.forms import SignalMembershipSubType
# Create your views here.


def SignIn(request):  
    if request.user.is_authenticated and request.user.is_instructor: 
        return redirect('accounts:instructordashboard')

    if request.user.is_authenticated and request.user.is_student: 
        return redirect('accounts:studentdashboard')  

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'], password=cd['password'])
             
            if user is not None and user.is_student:
                 login(request, user)
                 return redirect('accounts:studentdashboard')
            elif user is not None and user.is_instructor: 
                login(request, user)                              
                return redirect('accounts:instructordashboard')
            else:
                messages.error(request,'incorrect username or password')
                return redirect('accounts:login')
        else:
            form = LoginForm()
            context = {
                 'form':form,
             }           
            return render(request, 'accounts/signin.html', context)
    else:
        form = LoginForm()
        return render(request, 'accounts/signin.html', {'form': form})



def SignUp(request): 
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            get_email = cd['email']
            get_username =cd['username']
            get_password1 = cd['password1']
            
            if User.objects.filter(username=get_username).exists():
                messages.error(request, 'Error username already Exists')
                return redirect('accounts:register')

            elif User.objects.filter(email=get_email).exists():
                messages.error(request, 'Error Email already Exists')
                return redirect('accounts:register')
            else:
                #create new user, but don't save yet
                user = form.save(commit=False)
                #assign password to newly created user
                user.set_password(get_password1)
                #Now save new user
                user.save() 
                print('here is  the fucking email', get_email)
                current_site = get_current_site(request)
                mail_subject = 'Activate your waxion account.'
                message = render_to_string('accounts/acct_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
                 })

                email = EmailMessage(
                        mail_subject, message, to=[get_email]
                    )
                email.send()

                context={
                    'email':get_email,
                    'username': get_username,
                }
            return render(request, 'accounts/register_done.html',context)
        else:
            return render(request, 'accounts/signup.html', {'form': form})
    else:
        form = RegistrationForm()
        return render(request, 'accounts/signup.html', {'form': form})
  


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return render(request,'accounts/email_activation_done.html')
    else:
        return HttpResponse('Activation link is invalid!')



@login_required
def StudentDashboard(request):
    user = request.user

    if user is None:
        return HttpResponse("Session expired")

    if  UserMembership.objects.filter(user=request.user).exists():
        print("user exists")
    else:
        get_membership = Membership.objects.get(membership_type='Free')
        membership_instance = UserMembership.objects.create(user=user, membership=get_membership)

    if SignalUserMembership.objects.filter(user=request.user).exists():
        print("user exists")
    else:
        get_signal_membership = SignalMembership.objects.get(membership_type='Free')
        signal_instance = SignalUserMembership.objects.create(user=user, signal_membership =get_signal_membership)
   
    if BettingUserMembership.objects.filter(user=request.user).exists():
        print("user exists")
    else:
        get_betting_membership = BettingMembership.objects.get(membership_type='Free')
        betting_instance =  BettingUserMembership.objects.create(user=user, betting_membership=get_betting_membership)
    #context = load_dashboard_data(user)

    context ={
        'user':user
    }
    return render(request, 'dashboard/student/student-profile.html', context)
   

@login_required
def InstructorDashboard(request): 
    user = request.user
    list_of_user = User.objects.all()
    courses = Course.objects.all()
    active_learning_subscription = Subscription.objects.all()
    active_bet_forecast_subscription = BettingSubscription.objects.all()
    active_crypto_signal_subscription =  SignalSubscription.objects.all()
    student_membership_types = Membership.objects.all()
    betting_membership_types = BettingMembership.objects.all()
    signals_membership_types = SignalMembership.objects.all()
    crypto_signals = CryptoSignal.objects.all()
    bet_forecasts = BetForcast.objects.all()

    context = {
         'list_of_user':list_of_user,
         'count_total_user':list_of_user.count,
         'courses':courses,
          'total_courses': courses.count,
         'crypto_signal':crypto_signals,
         'total_crypto_signal':crypto_signals.count,
         'bet_forecast':bet_forecasts,
         'total_bet_forecast':bet_forecasts.count,
         'active_learning_subscription':active_learning_subscription,
         'active_bet_forecast_subscription':active_bet_forecast_subscription,
         'active_crypto_signal_subscription':active_crypto_signal_subscription,
         'student_membership_types':student_membership_types,
         'betting_membership_types': betting_membership_types,
         'signals_membership_types':signals_membership_types,
    }
    return render(request, 'dashboard/instructor/dashboard.html',context)



@login_required
def delete_user(request,pk):
    User.objects.filter(pk=pk).delete()
    list_of_user = User.objects.all()

    context={
         'list_of_user':list_of_user,
    }
    return render(request, 'dashboard/instructor/dashboard.html',context)



@login_required
def delete_bet_subscriber(request,id):
    subscriber = BettingUserMembership.objects.get(id=id)
    user = subscriber.user
    delete_subscriber = BettingUserMembership.objects.filter(id=id).delete()
    
    if delete_subscriber:
        get_betting_membership = BettingMembership.objects.get(membership_type='Free')
        betting_instance =  BettingUserMembership.objects.create(user=user, betting_membership=get_betting_membership)
        messages.success(request, 'Subscriber was deleted successfully, Now On Free Subscription')
        return redirect('accounts:instructordashboard')
    else:
        messages.error(request,'Error: Something went wrong unable to delete Subscriber')
        return redirect('accounts:instructordashboard')


@login_required
def delete_signal_subscriber(request,id):
    subscriber = SignalUserMembership.objects.get(id=id)
    user = subscriber.user
    delete_subscriber = SignalUserMembership.objects.filter(id=id).delete()
    
    if delete_subscriber:
        get_signal_membership = SignalMembership.objects.get(membership_type='Free')
        signal_instance = SignalUserMembership.objects.create(user=user, signal_membership =get_signal_membership)
        messages.success(request, 'Subscriber was deleted successfully, Now On Free Subscription')
        return redirect('accounts:instructordashboard')
    else:
        messages.error(request,'Error: Something went wrong unable to delete Subscriber')
        return redirect('accounts:instructordashboard')


@login_required
def delete_learning_subscriber(request,id):
    subscriber = UserMembership.objects.get(id=id)
    user = subscriber.user
    delete_subscriber = UserMembership.objects.filter(id=id).delete()

    if delete_subscriber:
        get_membership = Membership.objects.get(membership_type='Free')
        membership_instance = UserMembership.objects.create(user=user, membership=get_membership)
        messages.success(request, 'Subscriber was deleted successfully, Now On Free Subscription')
        return redirect('accounts:instructordashboard')
    else:
        messages.error(request,'Error: Something went wrong unable to delete Subscriber')
        return redirect('accounts:instructordashboard')
       

@login_required 
def InstructorProfile(request):
    user = request.user
    today = date.today()
    courses = Course.objects.filter(instructor_id=user.id)
    page_number = request.GET.get('page')
    course_paginator = Paginator(courses , 4)
    page = course_paginator.get_page(page_number)
   
    context = {
        'today':today,
        'user':user,
        'courses':courses,
        'count':course_paginator.count,
        'page':page,
    }
    return render(request, 'dashboard/instructor/instructor-profile.html',context)


def signout(request):
    logout(request)
    form = LoginForm
    return redirect('index')



def InstructorProfileEdit(request, ):
    return render(request, 'dashboard/instructor/instructor-account-edit.html')



def studentprofilepost(request):
    return render(request, 'dashboard/student/student-profile-posts.html')



@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            if user is not None and user.is_student and user.is_authenticated:
                messages.success(request, ('Your profile was successfully updated!'))
                return redirect('accounts:student_edit_profile')

            elif user is not None and user.is_instructor and user.is_authenticated: 
                messages.success(request, ('Your profile was successfully updated!'))               
                return redirect('accounts:instructor_edit_profile')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    if user.is_instructor and user.is_authenticated:
            return render(request, 'dashboard/instructor/instructor-account-edit.html', {
                'user_form': user_form,
                'profile_form': profile_form
            })
    elif user.is_student and user.is_authenticated:
            return render(request, 'dashboard/student/student-account-edit.html', {
                'user_form': user_form,
                'profile_form': profile_form
            })
    else:
        form = LoginForm()
        return render(request, 'accounts/signin.html', {'form': form})



@login_required
def change_login_details(request):
    username_form = ChangeUsernameForm()
    password_form = ChangePasswordForm()        
    context = {
        'username_form':username_form,
        'password_form':password_form,
    }
    return render(request, 'dashboard/student/student-account-edit-login-details.html', context)



@login_required
def change_username(request, pk):  
    user = request.user         
    if request.method == 'POST':        
        username_form = ChangeUsernameForm(request.POST)
        
        if username_form.is_valid():            
            user = User.objects.get(pk=pk)  

            if user.username == request.POST.get("old_username"):
                user.username = request.POST.get("new_username")
                user.save()
                if user is not None and user.is_student and user.is_authenticated:
                    messages.success(request, ('Your Username was successfully updated!'))
              
                    username_form = ChangeUsernameForm()
                    password_form = ChangePasswordForm()
                    context = {
                        
                        'username_form':username_form,
                        'password_form':password_form,
                    }
                    return render(request, 'dashboard/student/student-account-edit-login-details.html', context)

                elif user is not None and user.is_instructor and user.is_authenticated:
                    messages.success(request, ('Your Username was successfully updated!'))
              
                    username_form = ChangeUsernameForm()
                    password_form = ChangePasswordForm()
                    context = {
                        
                        'username_form':username_form,
                        'password_form':password_form,
                    }
                    return render(request, 'dashboard/instructor/instructor-account-edit-login-details.html', context)
            
            else:
                if user is not None and user.is_student and user.is_authenticated:
                    username_form = ChangeUsernameForm()
                    password_form = ChangePasswordForm()
                    context = {
                        
                        'error': 'Error: Unable to update Username',
                        'username_form':username_form,
                        'password_form':password_form,
                    }                
                    return render(request, 'dashboard/student/student-account-edit-login-details.html', context)

                elif  user is not None and user.is_instructor and user.is_authenticated:
                    username_form = ChangeUsernameForm()
                    password_form = ChangePasswordForm()
                    context = {
                        
                        'error': 'Error: Unable to update Username',
                        'username_form':username_form,
                        'password_form':password_form,
                    }                
                    return render(request, 'dashboard/instructor/instructor-account-edit-login-details.html', context)
            
        else:
            if user is not None and user.is_student and user.is_authenticated:
                    username_form = ChangeUsernameForm()
                    password_form = ChangePasswordForm()
                    context = {
                        
                        'error': 'Error: Unable to update Username',
                        'username_form':username_form,
                        'password_form':password_form,
                    }                
                    return render(request, 'dashboard/student/student-account-edit-login-details.html', context)

            elif  user is not None and user.is_instructor and user.is_authenticated:
                    username_form = ChangeUsernameForm()
                    password_form = ChangePasswordForm()
                    context = {
                        
                        'error': 'Error: Unable to update Username',
                        'username_form':username_form,
                        'password_form':password_form,
                    }                
                    return render(request, 'dashboard/instructor/instructor-account-edit-login-details.html', context)     
    else:
        if user is not None and user.is_student and user.is_authenticated:
            username_form = ChangeUsernameForm()
            password_form = ChangePasswordForm()
            context = {
                        'username_form':username_form,
                        'password_form':password_form,
                    }                
            return render(request, 'dashboard/student/student-account-edit-login-details.html', context)

        elif  user is not None and user.is_instructor and user.is_authenticated:
            username_form = ChangeUsernameForm()
            password_form = ChangePasswordForm()
            context = {
                        'username_form':username_form,
                        'password_form':password_form,
                    }                
            return render(request, 'dashboard/instructor/instructor-account-edit-login-details.html', context)
       



def upload_profile_photo(request ):
    user=request.user
    if request.method == 'POST':        
        profile_photo_form = ProfilePhotoForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_photo_form.is_valid():            
            profile_photo_form.save()
            messages.success(request, ('Your profile Photo was successfully updated!'))
            
            return redirect('accounts:studentdashboard')
        else:
            messages.error(request, ('Error: unable to update photo'))
            
    else:   
        
        profile_photo_form = ProfilePhotoForm(instance=request.user.profile)
        context={
            'form': profile_photo_form,
            'user':user,
            }
        return render(request, 'dashboard/student/student-account-edit-profile-image.html',context)



  
@login_required
def change_password(request, pk):  
    user = request.user         
    if request.method == 'POST':        
        password_form = ChangePasswordForm(request.POST)
        
        if password_form.is_valid():            
            user = User.objects.get(pk=pk)  

            if user.password == request.POST.get("old_password"):
                user.password = request.POST.get("new_password")
                user.save()
                if user is not None and user.is_student and user.is_authenticated:
                    messages.success(request, ('Your profile was successfully updated!'))
              
                    username_form = ChangeUsernameForm()
                    password_form = ChangePasswordForm()
                    context = {
                        
                        'username_form':username_form,
                        'password_form':password_form,
                    }
                    return render(request, 'dashboard/student/student-account-edit-login-details.html', context)

                elif user is not None and user.is_instructor and user.is_authenticated:
                    messages.success(request, ('Your profile was successfully updated!'))
              
                    username_form = ChangeUsernameForm()
                    password_form = ChangePasswordForm()
                    context = {
                        
                        'username_form':username_form,
                        'password_form':password_form,
                    }
                    return render(request, 'dashboard/instructor/instructor-account-edit-login-details.html', context)
            
            else:
                if user is not None and user.is_student and user.is_authenticated:
                    username_form = ChangeUsernameForm()
                    password_form = ChangePasswordForm()
                    context = {
                        
                        'error': 'Error: unable to update password',
                        'username_form':username_form,
                        'password_form':password_form,
                    }                
                    return render(request, 'dashboard/student/student-account-edit-login-details.html', context)

                elif  user is not None and user.is_instructor and user.is_authenticated:
                    username_form = ChangeUsernameForm()
                    password_form = ChangePasswordForm()
                    context = {
                        
                        'error': 'Error: unable to update password',
                        'username_form':username_form,
                        'password_form':password_form,
                    }                
                    return render(request, 'dashboard/instructor/instructor-account-edit-login-details.html', context)
                  
    else:        
        if user is not None and user.is_student and user.is_authenticated:
            username_form = ChangeUsernameForm()
            password_form = ChangePasswordForm()
            context = {
                        'username_form':username_form,
                        'password_form':password_form,
                    }                
            return render(request, 'dashboard/student/student-account-edit-login-details.html', context)

        elif  user is not None and user.is_instructor and user.is_authenticated:
            username_form = ChangeUsernameForm()
            password_form = ChangePasswordForm()
            context = {
                        'username_form':username_form,
                        'password_form':password_form,
                    }                
            return render(request, 'dashboard/instructor/instructor-account-edit-login-details.html', context)


def delete_student_sub_type(request,pk):
    delete_sub = Membership.objects.filter(pk=pk).delete()
    if delete_sub:
       messages.success(request,'Success: subscription type was deleted sucessfully')
       return redirect('accounts:instructordashboard')
    else:
        messages.error(request, 'Error: unable to delete the selected subscription type')
    return redirect('accounts:instructordashboard')


def delete_betting_sub_type(request,pk):
    delete_sub = BettingMembership.objects.filter(pk=pk).delete()
    if delete_sub:
       messages.success(request,'Success: subscription type was deleted sucessfully')
       return redirect('accounts:instructordashboard')
    else:
        messages.error(request, 'Error: unable to delete the selected subscription type')
    return redirect('accounts:instructordashboard')


def delete_signal_sub_type(request,pk):
    delete_sub = SignalMembership.objects.filter(pk=pk).delete()
    if delete_sub:
       messages.success(request,'Success: subscription type was deleted sucessfully')
       return redirect('accounts:instructordashboard')
    else:
        messages.error(request, 'Error: unable to delete the selected subscription type')
    return redirect('accounts:instructordashboard')



def edit_student_sub_type(request,pk):
    user = request.user
    if request.method =="POST":
        edit_sub_type = Membership.objects.get(pk=pk)
        edit_sub_form = StudentMembershipSubType(request.POST, instance= edit_sub_type)
        if edit_sub_form.is_valid() and user.is_instructor and user.is_authenticated:
            edit_sub_form.save()
            messages.success(request,'success:subscription type successfully updated')
            return redirect('accounts:instructordashboard')
        else:
            edit_sub_type = Membership.objects.get(pk=pk)
            edit_sub_form = StudentMembershipSubType(instance= edit_sub_type)
            messages.error(request,'Error: Something went wrong unable to update subscription type')
            context ={
                'edit_sub_form':edit_sub_form,
            }
            return render(request,'dashboard/instructor/edit-student-subscription.html',context)
    else:
        edit_sub_type = Membership.objects.get(pk=pk)
        edit_sub_form = StudentMembershipSubType(instance= edit_sub_type)
        messages.error(request,'Error: Something went wrong unable to update subscription type')
        context ={
                'edit_sub_form':edit_sub_form,
            }
        return render(request,'dashboard/instructor/edit-student-subscription.html',context)


       
def edit_betting_sub_type(request,pk):
    user = request.user
    if request.method =="POST":
        edit_sub_type = BettingMembership.objects.get(pk=pk)
        edit_sub_form = BettingMembershipSubType(request.POST, instance= edit_sub_type)
        if edit_sub_form.is_valid() and user.is_instructor and user.is_authenticated:
            edit_sub_form.save()
            messages.success(request,'success:subscription type successfully updated')
            return redirect('accounts:instructordashboard')
        else:
            edit_sub_type = BettingMembership.objects.get(pk=pk)
            edit_sub_form = BettingMembershipSubType(instance= edit_sub_type)
            messages.error(request,'Error: Something went wrong unable to update subscription type')
            context ={
                'edit_sub_form':edit_sub_form,
            }
            return render(request,'dashboard/instructor/edit-betting-subscription.html',context)
    else:
        edit_sub_type = BettingMembership.objects.get(pk=pk)
        edit_sub_form = BettingMembershipSubType(instance= edit_sub_type)
        messages.error(request,'Error: Something went wrong unable to update subscription type')
        context ={
                'edit_sub_form':edit_sub_form,
            }
        return render(request,'dashboard/instructor/edit-betting-subscription.html',context)



def edit_signal_sub_type(request,pk):
    user = request.user
    if request.method =="POST":
        edit_sub_type = SignalMembership.objects.get(pk=pk)
        edit_sub_form = SignalMembershipSubType(request.POST, instance= edit_sub_type)
        if edit_sub_form.is_valid() and user.is_instructor and user.is_authenticated:
            edit_sub_form.save()
            messages.success(request,'success:subscription type successfully updated')
            return redirect('accounts:instructordashboard')
        else:
            edit_sub_type = SignalMembership.objects.get(pk=pk)
            edit_sub_form = SignalMembershipSubType(instance= edit_sub_type)
            messages.error(request,'Error: Something went wrong unable to update subscription type')
            context ={
                'edit_sub_form':edit_sub_form,
            }
            return render(request,'dashboard/instructor/edit-signal-subscription.html',context)
    else:
        edit_sub_type = SignalMembership.objects.get(pk=pk)
        edit_sub_form = SignalMembershipSubType(instance= edit_sub_type)
        messages.error(request,'Error: Something went wrong unable to update subscription type')
        context ={
                'edit_sub_form':edit_sub_form,
            }
        return render(request,'dashboard/instructor/edit-signal-subscription.html',context)




       
"""
def load_dashboard_data(user):
    total_courses = StudentCourses.objects.filter(user__pk=user.id).count()   
    try:
        recent_notification = Notification.objects.get(active=True)
    except Notification.DoesNotExist:
        recent_notification = None
                    
    context = {
        'total_courses':total_courses, 
        'recent_notification':recent_notification,
        'user':user,
    }

    return context
    """