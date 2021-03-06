from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from datetime import datetime
import numpy as np
from operator import itemgetter
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
import io
import matplotlib.pyplot as plt
import pandas as pd
import base64,urllib
import math
from covid import Covid
import json
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
user = get_user_model()
from .data import *
from django.views.decorators.csrf import csrf_exempt




class ChartData(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = []
    permission_classes = []



    def get(self, request, format=None):


        data = {
            "sales": 100,
            "customers": 10,
            "total_cases":total_cases(),
            "total_deaths": total_deaths(),
            "continents_names" : continents_names ,
            "continents_cases": continents_total_cases,
            "continents_active_cases": continents_active_cases,
            "world_dates_day_by_day" : world_dates_day_by_day ,
            "world_cases_day_by_day" : world_cases_day_by_day,
            "world_deaths_day_by_day" : world_deaths_day_by_day,
            "all_countries" : all_countries



        }

        return Response(data)

def data(request):

    dix=data[:10]
    plt.plot(range(10))
    fig = plt.gcf()
    # convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    return render(request,'welcome/data.html',{'column':column,'data':data,'index':index,'range':dix,'data':uri})
externe=[]
def welcome(request):
    return render(request,'welcome/index.html')
def country(request,country):

    country_data_day_by_day=[]
    country_cases_day_by_day=[]
    country_dates_day_by_day=[]
    country_deaths_day_by_day=[]
    for cnt in data1 :
        if cnt[0]==country or cnt[2]==country :
            country_data_day_by_day.append(cnt),country_cases_day_by_day.append(cnt[5]),
            country_dates_day_by_day.append(cnt[3]), country_deaths_day_by_day.append(cnt[8])






    country_data = covid.get_status_by_country_name(country)
    country_data.pop("total_tests_per_million", None)
    for k, v in country_data.items():
        if k != "country":
            country_data[k] = format(v, ",")
    total_cases=country_data['confirmed']
    total_deaths = country_data['deaths']
    total_recovered = country_data['recovered']
    active_cases = country_data['active']
    return render(request, 'welcome/country.html',{'country':country,'country_data':country_data,
                                                   'country_cases_day_by_day' :country_cases_day_by_day,
                                                   'country_deaths_day_by_day' :country_deaths_day_by_day,
                                                   'country_dates_day_by_day' :country_dates_day_by_day,

                                                 'total_cases':total_cases,'active_cases':active_cases,'total_recovered' : total_recovered ,'total_deaths':total_deaths  })
class HomeView(View):
    def get(self,request,*args,**kwargs):



        return render(request,'welcome/charts.html',{"customers":10,"total_cases":total_cases(),
                                                     "total_deaths":total_deaths(),"active_cases":active_cases(),
                                                     "total_recovered":total_recovered(),"europe":europe,
                                                     "asia":asia,"oceania":oceania,"africa":africa,
                                                     "north_america":north_america,"south_america":south_america,
                                                     "covid":covid1,"world":world,"europe_all":europe_all,
                                                     "asia_all":asia_all,"oceania_all":oceania_all,"africa_all":africa_all,
                                                     "north_america_all":north_america_all,"south_america_all":south_america_all})

def get_data(request,*args,**kwargs):
    data={
        "sales":100,
        "customers":10,
    }
    return JsonResponse(data)

@csrf_exempt
def contactus(request):
    if (request.POST):
        login_data = request.POST.dict()
        firstname = login_data.get("firstname")
        laststname = login_data.get("lastname")
        name = firstname + " " + laststname
        areacode =login_data.get("areacode")
        telnum =login_data.get("telnum")
        tel = areacode +" " + telnum
        approve = request.POST.get('approve', "false")
        subject = "Registration to receive daily updates about COVID-19"
        #feedback = login_data.get("feedback")
        emailid = login_data.get("emailid")
        select = request.POST['dropdown']
        contenu="Hi DataViz community, \n My name is : " + name + " . \n My telephone number is : " + tel +" .\n "
        if approve != "false" :
            #contenu+= "Yes , I have no problem if you contact me but via " + select +" , please ! \n"
            if select=="Telephone" :
                contenu= "Hi " + name +",\n Thank you for registration . You will receive daily updates about COVID-19 by message on your Phone "+ tel + " .\n cdt,\n DataViz Community."
            else :
                contenu= "Hi " + name +",\n \n Thank you for registration . You will receive daily updates about COVID-19 by Mail .\n \n cdt,\n DataViz Community."

       # else :
       # contenu += "No , please don\'t disturb me .\n"
        #contenu+="Feedback : "

        send_mail(subject, contenu, 'salem.dhouimir@ensi-uma.tn',[emailid])

        return render(request, 'welcome/contactus.html')
    else:
        return render(request, 'welcome/contactus.html')

def news(request):
    return render(request, 'welcome/news.html')
def qa(request):
    return render(request, 'welcome/qa.html')






#read csv data


"""
def total_cases():
    return format((int(countries_cases()['World'])),",")
def total_deaths():
    return format((int(countries_deaths()['World'])),",")



def countries_cases():
    dictcases={}
    for i in range(len(data1)) :
        if not math.isnan(float(data1[i][4])):
            dictcases[data1[i][2]]=int(data1[i][4])
    return dictcases
def countries_deaths():
    dictcases = {}
    for i in range(len(data1)):
        if not math.isnan(float(data1[i][6])):
            dictcases[data1[i][2]] = int(data1[i][6])
    return dictcases
"""