from django.db.models import signals
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.hashers import CryptPasswordHasher, make_password
from django.contrib import auth
import datetime
from datetime import timedelta
from datetime import datetime as dt
import requests
import json
from django.http import HttpResponseRedirect
from .forms import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
today = datetime.date.today()
from.forms import *
from django.contrib import messages

# Create your views here.

def Signal_subscription(request):
	new_signal_membership = SignalUserMembership.objects.filter(user=request.user) 
	new_signal_subscription = SignalSubscription.objects.all
	user = request.user
	print(new_signal_membership)

	context={
		'new_signal_membership':new_signal_membership,
		'user':user,
		'new_signal_subscription':new_signal_subscription
	}
	return render(request, 'membership/student-account-billing-upgrade.html',context)
	

def Signal_end_sub(request):
	return render(request, 'signals/sub.html')
	
@login_required
def Signal_subscribe(request):
	plan = request.GET.get('signal_sub_plan')
	fetch_membership = SignalMembership.objects.filter(membership_type=plan).exists()
	if fetch_membership == False:
		return redirect('signal_subscribe')
	signal_membership = SignalMembership.objects.get(membership_type=plan)
	price = float(signal_membership.price)*100 # We need to multiply the price by 100 because Paystack receives in kobo and not naira.
	price = int(price)

	def init_payment(request):
		url = 'https://api.paystack.co/transaction/initialize'
		headers = {
			'Authorization': 'Bearer '+ settings.PAYSTACK_SECRET_KEY,
			'Content-Type' : 'application/json',
			'Accept': 'application/json',
			}
		datum = {
			"email": request.user.email,
			"amount": price,
			"callback_url":'http://127.0.0.1:8000/signals/payment/'
			}
		print(request.user.email)
		x = requests.post(url, data=json.dumps(datum), headers=headers)
		
		if x.status_code != 200:
			return str(x.status_code)
		
		results = x.json()
		print(results)
	
		return results
	initialized = init_payment(request)
	print(initialized['data']['authorization_url'])
	amount = price/100
	instance = SignalPayHistory.objects.create(amount=amount, payment_for=signal_membership, user=request.user, paystack_charge_id=initialized['data']['reference'], paystack_access_code=initialized['data']['access_code'])
	SignalUserMembership.objects.filter(user=instance.user).update(reference_code=initialized['data']['reference'])
	link = initialized['data']['authorization_url']
	return HttpResponseRedirect(link)
	return render(request, 'dashboard/student/signals.html')  # change to subscription page
	


def Signal_call_back_url(request):
	reference = request.GET.get('reference')
	# We need to fetch the reference from PAYMENT
	check_pay = SignalPayHistory.objects.filter(paystack_charge_id=reference).exists()
	if check_pay == False:
		# This means payment was not made error should be thrown here...
		print("Error")
	else:
		payment = SignalPayHistory.objects.get(paystack_charge_id=reference)
		# We need to fetch this to verify if the payment was successful.
		def verify_payment(request):
			url = 'https://api.paystack.co/transaction/verify/'+reference
			headers = {
				'Authorization': 'Bearer '+settings.PAYSTACK_SECRET_KEY,
				'Content-Type' : 'application/json',
				'Accept': 'application/json',
				}
			datum = {
				"reference": payment.paystack_charge_id
				}
			x = requests.get(url, data=json.dumps(datum), headers=headers)
			if x.status_code != 200:
				return str(x.status_code)
			
			results = x.json()
			return results
	initialized = verify_payment(request)
	if initialized['data']['status'] == 'success':
		SignalPayHistory.objects.filter(paystack_charge_id=initialized['data']['reference']).update(paid=True)
		new_payment = SignalPayHistory.objects.get(paystack_charge_id=initialized['data']['reference'])
		instance = SignalMembership.objects.get(id=new_payment.payment_for.id)
		sub = SignalUserMembership.objects.filter(reference_code=initialized['data']['reference']).update(signal_membership=instance)
		#check subscription status and delete free subscription before subscribing
		subscriber = request.user
		check_membership_status = SignalUserMembership.objects.filter(user = subscriber).first()
		if check_membership_status:
			check_sub_status=SignalSubscription.objects.filter(signal_user_membership = check_membership_status.id).delete()
		
        #subscribe new user
		
		signal_user_membership = SignalUserMembership.objects.get(reference_code=initialized['data']['reference'])
		SignalSubscription.objects.create(signal_user_membership=signal_user_membership, expires_in=dt.now().date() + timedelta(days=signal_user_membership.signal_membership.duration))
		return redirect('signal_subscribed')
	return render(request, 'signal/payment.html')


def Signal_subscribed(request):
	return render(request, 'signals/subscribed.html')
	

@login_required
def all_signal(request):
	signals = CryptoSignal.objects.all().order_by('-created_on')[:6]
	page_number = request.GET.get('page')
	product_paginator = Paginator(signals , 3)
	page = product_paginator.get_page(page_number)
	
	context  = {
		'count':product_paginator.count,
        'page':page,
    }
	return render(request, "dashboard/instructor/all_signals.html", context)


@login_required
def previewSignal(request,pk):
	user = request.user
	signal= CryptoSignal.objects.get(pk=pk)
	context ={
        'user':user,
        'signal':signal, 
    }
	return render(request, 'dashboard/instructor/instructor-preview-signal.html', context)


@login_required	
def CreateSignals(request):
	if request.method == "POST":
		SignalForm = CryptoSignalForm(request.POST)
		if SignalForm.is_valid():
			form =SignalForm.save(commit=False)
			form.instructor_id = request.user.id
			form.save()
			context={
				'message':"new signal added successfully"
			}
			return render(request,'dashboard/instructor/all_signals.html',context)
		else:
			context={
				'message':"error while adding signals: signal was not added"
			}
			return render(request, 'dashboard/instructor/add_signals.html',context)
	else:
		SignalForm = CryptoSignalForm()
		context = {
			'SignalForm':SignalForm,
		}
		return render(request,'dashboard/instructor/add_signals.html',context)



@login_required
def EditSignal(request, pk):
	if request.method =="POST":
		signal = CryptoSignal.objects.get(pk=pk)
		signalForm = CryptoSignalForm(request.post, instance=signal)
		if signalForm.is_valid():
			signalForm.save()
			context ={
				'message':"signal Successfully edited"
			}
			return render(request,'dashboard/instructor/edit_signal.html',context)
		else:
			context ={
				'message':'signal was not saved'
			}
			return render(request, 'dashboard/instructor/edit_signal.html',context)
	else:
		signal= CryptoSignal.objects.get(pk=pk)
		signalForm =CryptoSignalForm(instance=signal)
		context ={
			'signalForm':signalForm,
		}
	return render(request,'dashboard/instructor/edit_signal.html', context)



@login_required
def DeleteSignal(request,pk):
	CryptoSignal.objects.filter(pk=pk).delete()
	signals = CryptoSignal.objects.filter(instructor_id=request.user.id)
	context ={
			'signals':signals
		}
	return render (request, 'dashboard/instructor/all_signals.html',context)


@login_required
def studentAllSignal(request):
	signals = CryptoSignal.objects.all().order_by('created_on')[:6]
	page_number = request.GET.get('page')
	signal_paginator = Paginator(signals, 6)
	page = signal_paginator.get_page(page_number)
	user = request.user
	signal_user_membership = SignalUserMembership.objects.filter(user=user) 
	signal_user_subscription = SignalSubscription.objects.all()
	
	context  = {
		'count':signal_paginator.count,
        'page':page,
		'user':user,
		'signal_user_membership':signal_user_membership,
		'signal_user_subscription':signal_user_subscription,
    }
	return render(request, "dashboard/student/student_all_signal.html", context)


@login_required
def studentViewSignal(request,pk):
	user = request.user
	signal = CryptoSignal.objects.get(pk=pk)
	signal_user_membership = SignalUserMembership.objects.filter(user=request.user) 
	signal_user_subscription = SignalSubscription.objects.all

	context={
        'user':user,
		'signal':signal,
		'signal_user_membership':signal_user_membership,
		'signal_user_subscription':signal_user_subscription,
	}
	return render(request,'dashboard/student/student-view-signal.html',context)


def Instructor_create_signal_sub(request):
	if request.method == 'POST':
		signal_sub_type_form = SignalMembershipSubType(request.POST)
		if signal_sub_type_form.is_valid() and request.user.is_authenticated and request.user.is_instructor:
			signal_sub_type_form.save()
			messages.success(request,'Success: Signal Subscription typpe created successfully')
			return redirect('accounts:instructordashboard')
		else:
			messages.error(request,'Error Signal Subscription was not created')
			signal_sub_type_form = SignalMembershipSubType(request.POST)
			context ={
				'signal_sub_type_form':signal_sub_type_form,
			}
			return render(request,'dashboard/instructor/create-student-subscription.html', context)
	else:
		signal_sub_type_form =SignalMembershipSubType()
		context ={
				'signal_sub_type_form':signal_sub_type_form,
			}
	return render(request, 'dashboard/instructor/create-signal-subscription.html',context)