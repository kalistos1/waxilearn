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
from .models import *
from django.core.paginator import Paginator
from .forms import *
from django.contrib.auth.decorators import login_required
today = datetime.date.today()
from django.contrib import messages

# Create your views here.

def Betting_end_sub(request):
	return render(request, 'betting/sub.html')
	
	
@login_required
def Betting_subscribe(request):
	plan = request.GET.get('betting_sub_plan')
	fetch_membership = BettingMembership.objects.filter(membership_type=plan).exists()
	if fetch_membership == False:
		return redirect('betting_subscribe')
	betting_membership = BettingMembership.objects.get(membership_type=plan)
	price = float(betting_membership.price)*100 # We need to multiply the price by 100 because Paystack receives in kobo and not naira.
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
			"callback_url":'http://127.0.0.1:8000/betting/payment/'
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
	instance = BettingPayHistory.objects.create(amount=amount, payment_for=betting_membership, user=request.user, paystack_charge_id=initialized['data']['reference'], paystack_access_code=initialized['data']['access_code'])
	BettingUserMembership.objects.filter(user=instance.user).update(reference_code=initialized['data']['reference'])
	link = initialized['data']['authorization_url']
	return HttpResponseRedirect(link)
	return render(request, 'dashboard/student/bet_codes.html')
	


def Betting_call_back_url(request):
	reference = request.GET.get('reference')
	# We need to fetch the reference from PAYMENT
	check_pay = BettingPayHistory.objects.filter(paystack_charge_id=reference).exists()
	if check_pay == False:
		# This means payment was not made error should be thrown here...
		print("Error")
	else:
		payment = BettingPayHistory.objects.get(paystack_charge_id=reference)
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
		BettingPayHistory.objects.filter(paystack_charge_id=initialized['data']['reference']).update(paid=True)
		new_payment = BettingPayHistory.objects.get(paystack_charge_id=initialized['data']['reference'])
		instance = BettingMembership.objects.get(id=new_payment.payment_for.id)
		sub = BettingUserMembership.objects.filter(reference_code=initialized['data']['reference']).update(betting_membership=instance)
		betting_user_membership = BettingUserMembership.objects.get(reference_code=initialized['data']['reference'])
		
		#check subscription status and delete free subscription before subscribing
		subscriber = request.user
		check_membership_status = BettingUserMembership.objects.filter(user = subscriber).first()
		if check_membership_status:
			check_sub_status=BettingSubscription.objects.filter(betting_user_membership = check_membership_status.id).delete()
		
        #subscribe new user
		BettingSubscription.objects.create(betting_user_membership=betting_user_membership, expires_in=dt.now().date() + timedelta(days=betting_user_membership.betting_membership.duration))
		return redirect('betting_subscribed')
	return render(request, 'betting/payment.html')


def Betting_subscribed(request):
	return render(request, 'betting/subscribed.html')
	

@login_required	
def AllForecast(request):
	forecasts = BetForcast.objects.all().order_by('-created_on')[:6]
	page_number = request.GET.get('page')
	product_paginator = Paginator(forecasts , 3)
	page = product_paginator.get_page(page_number)
	
	context  = {
		'count':product_paginator.count,
        'page':page,
    }
	return render(request, "dashboard/instructor/all_forecast.html", context)


@login_required
def PreviewForecast(request,pk):
	user = request.user
	signal= BetForcast.objects.get(pk=pk)
	context ={
        'user':user,
        'signal':signal, 
    }
	return render(request, 'dashboard/instructor/instructor-preview-signal.html', context)


@login_required	
def CreateForecast(request):
	if request.method == "POST":
		ForecastForm = BetForecastForm(request.POST)
		if ForecastForm.is_valid():
			form =ForecastForm.save(commit=False)
			form.instructor_id = request.user.id
			form.save()
			context={
				'message':"new bet forecast added successfully"
			}
			return render(request,'dashboard/instructor/all_forecast.html',context)
		else:
			context={
				'message':"error while adding bet forecast: forecast was not added"
			}
			return render(request, 'dashboard/instructor/add_forecast.html',context)
	else:
		ForecastForm = BetForecastForm()
		context = {
			'ForecastForm':ForecastForm,
		}
		return render(request,'dashboard/instructor/add_forecast.html',context)


@login_required
def EditForecast(request, pk):
	if request.method =="POST":
		forecast = BetForcast.objects.get(pk=pk)
		ForecastForm = BetForecastForm(request.post, instance=forecast)
		if ForecastForm.is_valid():
			ForecastForm.save()
			context ={
				'message':"Forecast Successfully edited"
			}
			return render(request,'dashboard/instructor/edit_forecast.html',context)
		else:
			context ={
				'message':'Forecast was not saved'
			}
			return render(request, 'dashboard/instructor/edit_forecast.html',context)
	else:
		forecast= BetForcast.objects.get(pk=pk)
		ForecastForm = BetForecastForm(instance=forecast)
		context ={
			'ForecastForm':ForecastForm,
		}
	return render(request,'dashboard/instructor/edit_forecast.html', context)



@login_required
def DeleteForecast(request,pk):
	BetForcast.objects.filter(pk=pk).delete()
	forecast = BetForcast.objects.filter(instructor_id=request.user.id)
	context ={
			'forecast':forecast
		}
	return render (request, 'dashboard/instructor/all_forecast.html',context)


@login_required	
def subscriberAllForecast(request):
	forecast = BetForcast.objects.all().order_by('created_on')[:6]
	page_number = request.GET.get('page')
	forecast_paginator = Paginator(forecast, 6)
	page = forecast_paginator.get_page(page_number)
	user = request.user
	betting_user_membership = BettingUserMembership.objects.filter(user=user) 
	betting_user_subscription = BettingSubscription.objects.all()
	
	context  = {
		'count':forecast_paginator.count,
        'page':page,
		'user':user,
		'betting_user_membership':betting_user_membership,
		'betting_user_subscription':betting_user_subscription,
    }
	return render(request, "dashboard/student/student_all_forecast.html", context)


@login_required
def subscriberViewForecast(request,pk):
	user = request.user
	forecast = BetForcast.objects.get(pk=pk)
	betting_user_membership = BettingUserMembership.objects.filter(user=request.user) 
	betting_user_subscription = BettingSubscription.objects.all

	context={
        'user':user,
		'forecast':forecast,
		'betting_user_membership':betting_user_membership,
		'betting_user_subscription':betting_user_subscription,
	}
	return render(request,'dashboard/student/student-view-forecast.html',context)


def Instructor_create_sports_sub(request):
	if request.method == 'POST':
		sport_sub_type_form = BettingMembershipSubType(request.POST)
		if sport_sub_type_form.is_valid() and request.user.is_authenticated and request.user.is_instructor:
			sport_sub_type_form.save()
			messages.success(request,'Success: Learning Subscription typpe created successfully')
			return redirect('accounts:instructordashboard')
		else:
			messages.error(request,'Error Learning Subscription was not created')
			sport_sub_type_form = BettingMembershipSubType(request.POST)
			context ={
				'sport_sub_type_form':sport_sub_type_form,
			}
			return render(request,'dashboard/instructor/create-student-subscription.html', context)
	else:
		sport_sub_type_form = BettingMembershipSubType()
		context ={
				'sport_sub_type_form':sport_sub_type_form,
			}
	return render(request, 'dashboard/instructor/create-sports-subscription.html',context)