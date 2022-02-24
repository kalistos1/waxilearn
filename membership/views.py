from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.hashers import make_password
from django.contrib import auth
import datetime
from datetime import timedelta
from datetime import datetime as dt
import requests
import json
from django.http import HttpResponseRedirect
from signalsubscription.models import *
from bettingsubscription.models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
today = datetime.date.today()

# Create your views here.

def subscription(request):
	
	user_membership = UserMembership.objects.filter(user=request.user) 
	user_subscription = Subscription.objects.all
	get_medium_membership = Membership.objects.get(membership_type='Medium')
	user = request.user
	
	new_signal_membership = SignalUserMembership.objects.filter(user=request.user) 
	new_signal_subscription = SignalSubscription.objects.all
	get_gold_membership = SignalMembership.objects.get(membership_type='Gold')

	new_betting_membership = BettingUserMembership.objects.filter(user=request.user) 
	new_betting_subscription = BettingSubscription.objects.all
	get_silver_membership = BettingMembership.objects.get(membership_type='Silver')

	context={
		'user_membership':user_membership,
		'user':user,
		'user_subscription':user_subscription,
		'new_signal_membership':new_signal_membership,
		'new_signal_subscription':new_signal_subscription,
		'get_medium_membership':get_medium_membership,
		'get_gold_membership':get_gold_membership,
		'new_betting_membership':new_betting_membership,
		'new_betting_subscription':new_betting_subscription,
		'get_silver_membership':get_silver_membership,
	}
	return render(request, 'membership/student-account-billing-upgrade.html',context)
	

def end_sub(request):
	return render(request, 'sub.html')
	
	
@login_required
def subscribe(request):
	plan = request.GET.get('sub_plan')
	fetch_membership = Membership.objects.filter(membership_type=plan).exists()
	if fetch_membership == False:
		return redirect('subscribe')
	membership = Membership.objects.get(membership_type=plan)
	price = float(membership.price)*100 # We need to multiply the price by 100 because Paystack receives in kobo and not naira.
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
			"callback_url":'http://127.0.0.1:8000/payment/'
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
	instance = PayHistory.objects.create(amount=amount, payment_for=membership, user=request.user, paystack_charge_id=initialized['data']['reference'], paystack_access_code=initialized['data']['access_code'])
	UserMembership.objects.filter(user=instance.user).update(reference_code=initialized['data']['reference'])
	link = initialized['data']['authorization_url']
	return HttpResponseRedirect(link)
	return render(request, 'dashboard/student/student-browse-courses.html')
	


def call_back_url(request):
	reference = request.GET.get('reference')
	# We need to fetch the reference from PAYMENT
	check_pay = PayHistory.objects.filter(paystack_charge_id=reference).exists()
	if check_pay == False:
		# This means payment was not made error should be thrown here...
		print("Error")
	else:
		payment = PayHistory.objects.get(paystack_charge_id=reference)
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
		PayHistory.objects.filter(paystack_charge_id=initialized['data']['reference']).update(paid=True)
		new_payment = PayHistory.objects.get(paystack_charge_id=initialized['data']['reference'])
		instance = Membership.objects.get(id=new_payment.payment_for.id)
		sub = UserMembership.objects.filter(reference_code=initialized['data']['reference']).update(membership=instance)
		user_membership = UserMembership.objects.get(reference_code=initialized['data']['reference'])

		#check subscription status and delete free subscription before subscribing
		subscriber = request.user
		check_membership_status = UserMembership.objects.filter(user = subscriber).first()
		if check_membership_status:
			check_sub_status=Subscription.objects.filter(user_membership = check_membership_status.id).delete()
		
        #subscribe new user 
		Subscription.objects.create(user_membership=user_membership, expires_in=dt.now().date() + timedelta(days=user_membership.membership.duration))
		return redirect('subscribed')
	return render(request, 'membership/payment.html')


def subscribed(request):
	return render(request, 'membership/subscribed.html')


def Instructor_create_student_sub(request):
	if request.method == 'POST':
		student_sub_type_form = StudentMembershipSubType(request.POST)
		if student_sub_type_form.is_valid() and request.user.is_authenticated and request.user.is_instructor:
			student_sub_type_form.save()
			messages.success(request,'Success: Learning Subscription typpe created successfully')
			return redirect('accounts:instructordashboard')
		else:
			messages.error(request,'Error Learning Subscription was not created')
			student_sub_type_form = StudentMembershipSubType(request.POST)
			context ={
				'student_sub_type_form':student_sub_type_form,
			}
			return render(request,'dashboard/instructor/create-student-subscription.html', context)
	else:
		student_sub_type_form = StudentMembershipSubType()
		context ={
				'student_sub_type_form':student_sub_type_form,
			}
	return render(request,'dashboard/instructor/create-student-subscription.html',context)