import json
import time
from django.http import HttpResponse,JsonResponse,HttpResponseForbidden
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
# from django.template.loader import render_to_string
from .tokens import email_verification_token
from django.contrib.auth import get_backends
from django.utils.html import strip_tags

# from datetime import datetime,date,timedelta

from django.shortcuts import render,redirect,get_object_or_404
from django.middleware.csrf import REASON_NO_CSRF_COOKIE

from zqUsers.models import *
from wallet.models import *
from zqapp.forms import *
from zqUsers.forms import UserForm
from zqapp.models import *
import requests
from django.db.models import Sum
import base64
from django.http import JsonResponse
import random
import string
from datetime import datetime,timedelta
from django.core.mail import EmailMessage,get_connection
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.urls import reverse

import os
import logging

logger = logging.getLogger(__name__)




def custom_csrf_failure_view(request, reason=""):
    # Check the reason for failure and log it if necessary
    if reason == REASON_NO_CSRF_COOKIE:
        # Handle the specific case where there is no CSRF cookie
        pass

    # Redirect to the previous page if available, otherwise to the home page
    messages.warning(request,"Please fill all details carefully ")
    return redirect(request.META.get('HTTP_REFERER', '/'))



    
    

def testitout(request):
    
    current_time = timezone.now()
    curr=datetime.now()
    return HttpResponse(f'<h1>Time is</h1><p>{current_time}</p><p>{curr}</p>')


def index(request):
    
    referralId=request.GET.get('referralid')
    print(referralId)
    
    
    currencies = [
        "Afghan Afghani (AFN)", "Albanian Lek (ALL)", "Algerian Dinar (DZD)", "Angolan Kwanza (AOA)", "Argentine Peso (ARS)",
        "Armenian Dram (AMD)", "Aruban Florin (AWG)", "Australian Dollar (AUD)", "Azerbaijani Manat (AZN)", "Bahamian Dollar (BSD)",
        "Bahraini Dinar (BHD)", "Bangladeshi Taka (BDT)", "Barbadian Dollar (BBD)", "Belarusian Ruble (BYN)", "Belgian Franc (BEF)",
        "Belize Dollar (BZD)", "Bermudian Dollar (BMD)", "Bhutanese Ngultrum (BTN)", "Bolivian Boliviano (BOB)", "Bosnia-Herzegovina Convertible Mark (BAM)",
        "Botswana Pula (BWP)", "Brazilian Real (BRL)", "British Pound (GBP)", "Brunei Dollar (BND)", "Bulgarian Lev (BGN)",
        "Burundian Franc (BIF)", "Cambodian Riel (KHR)", "Canadian Dollar (CAD)", "Cape Verdean Escudo (CVE)", "Cayman Islands Dollar (KYD)",
        "Central African CFA Franc (XAF)", "Chilean Peso (CLP)", "Chinese Yuan (CNY)", "Colombian Peso (COP)", "Comorian Franc (KMF)",
        "Congolese Franc (CDF)", "Costa Rican Colón (CRC)", "Croatian Kuna (HRK)", "Cuban Convertible Peso (CUC)", "Cuban Peso (CUP)",
        "Czech Koruna (CZK)", "Danish Krone (DKK)", "Djiboutian Franc (DJF)", "Dominican Peso (DOP)", "East Caribbean Dollar (XCD)",
        "Egyptian Pound (EGP)", "Eritrean Nakfa (ERN)", "Estonian Kroon (EEK)", "Eswatini Lilangeni (SZL)", "Ethiopian Birr (ETB)",
        "Euro (EUR)", "Falkland Islands Pound (FKP)", "Fijian Dollar (FJD)", "Gambian Dalasi (GMD)", "Georgian Lari (GEL)",
        "Ghanaian Cedi (GHS)", "Gibraltar Pound (GIP)", "Guatemalan Quetzal (GTQ)", "Guinean Franc (GNF)", "Guyanaese Dollar (GYD)",
        "Haitian Gourde (HTG)", "Honduran Lempira (HNL)", "Hong Kong Dollar (HKD)", "Hungarian Forint (HUF)", "Icelandic Króna (ISK)",
        "Indian Rupee (INR)", "Indonesian Rupiah (IDR)", "Iranian Rial (IRR)", "Iraqi Dinar (IQD)", "Israeli New Shekel (ILS)",
        "Jamaican Dollar (JMD)", "Japanese Yen (JPY)", "Jordanian Dinar (JOD)", "Kazakhstani Tenge (KZT)", "Kenyan Shilling (KES)",
        "Kuwaiti Dinar (KWD)", "Kyrgystani Som (KGS)", "Lao Kip (LAK)", "Latvian Lats (LVL)", "Lebanese Pound (LBP)",
        "Lesotho Loti (LSL)", "Liberian Dollar (LRD)", "Libyan Dinar (LYD)", "Lithuanian Litas (LTL)", "Macanese Pataca (MOP)",
        "Macedonian Denar (MKD)", "Malagasy Ariary (MGA)", "Malawian Kwacha (MWK)", "Malaysian Ringgit (MYR)", "Maldivian Rufiyaa (MVR)",
        "Mauritanian Ouguiya (MRU)", "Mauritian Rupee (MUR)", "Mexican Peso (MXN)", "Moldovan Leu (MDL)", "Mongolian Tögrög (MNT)",
        "Moroccan Dirham (MAD)", "Mozambican Metical (MZN)", "Myanmar Kyat (MMK)", "Namibian Dollar (NAD)", "Nepalese Rupee (NPR)",
        "Netherlands Antillean Guilder (ANG)", "New Taiwan Dollar (TWD)", "New Zealand Dollar (NZD)", "Nicaraguan Córdoba (NIO)", "Nigerian Naira (NGN)",
        "North Korean Won (KPW)", "Norwegian Krone (NOK)", "Omani Rial (OMR)", "Pakistani Rupee (PKR)", "Panamanian Balboa (PAB)",
        "Papua New Guinean Kina (PGK)", "Paraguayan Guaraní (PYG)", "Peruvian Sol (PEN)", "Philippine Peso (PHP)", "Polish Złoty (PLN)",
        "Qatari Riyal (QAR)", "Romanian Leu (RON)", "Russian Ruble (RUB)", "Rwandan Franc (RWF)", "Saint Helena Pound (SHP)",
        "Samoan Tala (WST)", "Sao Tome and Principe Dobra (STN)", "Saudi Riyal (SAR)", "Serbian Dinar (RSD)", "Seychellois Rupee (SCR)",
        "Sierra Leonean Leone (SLL)", "Singapore Dollar (SGD)", "Solomon Islands Dollar (SBD)", "Somali Shilling (SOS)", "South African Rand (ZAR)",
        "South Korean Won (KRW)", "South Sudanese Pound (SSP)", "Sri Lankan Rupee (LKR)", "Sudanese Pound (SDG)", "Surinamese Dollar (SRD)",
        "Swazi Lilangeni (SZL)", "Swedish Krona (SEK)", "Swiss Franc (CHF)", "Syrian Pound (SYP)", "Tajikistani Somoni (TJS)",
        "Tanzanian Shilling (TZS)", "Thai Baht (THB)", "Tongan Paʻanga (TOP)", "Trinidad and Tobago Dollar (TTD)", "Tunisian Dinar (TND)",
        "Turkmenistani Manat (TMT)", "Ugandan Shilling (UGX)", "Ukrainian Hryvnia (UAH)", "United Arab Emirates Dirham (AED)", "United States Dollar (USD)",
        "Uruguayan Peso (UYU)", "Uzbekistani Som (UZS)", "Vanuatu Vatu (VUV)", "Venezuelan Bolívar Soberano (VES)", "Vietnamese Đồng (VND)",
        "West African CFA Franc (XOF)", "Yemeni Rial (YER)", "Zambian Kwacha (ZMW)", "Zimbabwean Dollar (ZWL)"
    ]

    countries = [
        "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda",
        "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain",
        "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia",
        "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso",
        "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic",
        "Chad", "Chile", "China", "Colombia", "Comoros", "Congo, Democratic Republic of the",
        "Congo, Republic of the", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic",
        "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador",
        "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland",
        "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala",
        "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India",
        "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan",
        "Kazakhstan", "Kenya", "Kiribati", "Korea, North", "Korea, South", "Kosovo", "Kuwait",
        "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein",
        "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta",
        "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco",
        "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal",
        "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Macedonia", "Norway",
        "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru",
        "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis",
        "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe",
        "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia",
        "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka",
        "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand",
        "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu",
        "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan",
        "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
    ]
    
    indian_states = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal"
]
    context = {'currencies':currencies, 'countries':countries,'states':indian_states}
    
    
    
    return render(request,'surveyappHome/page-register.html', context)


def about(request):
    return render(request,'zqapp/about.html')

def token(request):
    return render(request,'zqapp/token.html')

def termsCondition(request):
    return render(request,'zqapp/termsCondition.html')


def roadmap(request):
    return render(request,'zqapp/roadmap.html')

def mining(request):
    return render(request,'zqapp/mining.html')

def success(request):
    return render(request,'zqapp/success.html')    

def register(request):
    


    currencies = [
        "Afghan Afghani (AFN)", "Albanian Lek (ALL)", "Algerian Dinar (DZD)", "Angolan Kwanza (AOA)", "Argentine Peso (ARS)",
        "Armenian Dram (AMD)", "Aruban Florin (AWG)", "Australian Dollar (AUD)", "Azerbaijani Manat (AZN)", "Bahamian Dollar (BSD)",
        "Bahraini Dinar (BHD)", "Bangladeshi Taka (BDT)", "Barbadian Dollar (BBD)", "Belarusian Ruble (BYN)", "Belgian Franc (BEF)",
        "Belize Dollar (BZD)", "Bermudian Dollar (BMD)", "Bhutanese Ngultrum (BTN)", "Bolivian Boliviano (BOB)", "Bosnia-Herzegovina Convertible Mark (BAM)",
        "Botswana Pula (BWP)", "Brazilian Real (BRL)", "British Pound (GBP)", "Brunei Dollar (BND)", "Bulgarian Lev (BGN)",
        "Burundian Franc (BIF)", "Cambodian Riel (KHR)", "Canadian Dollar (CAD)", "Cape Verdean Escudo (CVE)", "Cayman Islands Dollar (KYD)",
        "Central African CFA Franc (XAF)", "Chilean Peso (CLP)", "Chinese Yuan (CNY)", "Colombian Peso (COP)", "Comorian Franc (KMF)",
        "Congolese Franc (CDF)", "Costa Rican Colón (CRC)", "Croatian Kuna (HRK)", "Cuban Convertible Peso (CUC)", "Cuban Peso (CUP)",
        "Czech Koruna (CZK)", "Danish Krone (DKK)", "Djiboutian Franc (DJF)", "Dominican Peso (DOP)", "East Caribbean Dollar (XCD)",
        "Egyptian Pound (EGP)", "Eritrean Nakfa (ERN)", "Estonian Kroon (EEK)", "Eswatini Lilangeni (SZL)", "Ethiopian Birr (ETB)",
        "Euro (EUR)", "Falkland Islands Pound (FKP)", "Fijian Dollar (FJD)", "Gambian Dalasi (GMD)", "Georgian Lari (GEL)",
        "Ghanaian Cedi (GHS)", "Gibraltar Pound (GIP)", "Guatemalan Quetzal (GTQ)", "Guinean Franc (GNF)", "Guyanaese Dollar (GYD)",
        "Haitian Gourde (HTG)", "Honduran Lempira (HNL)", "Hong Kong Dollar (HKD)", "Hungarian Forint (HUF)", "Icelandic Króna (ISK)",
        "Indian Rupee (INR)", "Indonesian Rupiah (IDR)", "Iranian Rial (IRR)", "Iraqi Dinar (IQD)", "Israeli New Shekel (ILS)",
        "Jamaican Dollar (JMD)", "Japanese Yen (JPY)", "Jordanian Dinar (JOD)", "Kazakhstani Tenge (KZT)", "Kenyan Shilling (KES)",
        "Kuwaiti Dinar (KWD)", "Kyrgystani Som (KGS)", "Lao Kip (LAK)", "Latvian Lats (LVL)", "Lebanese Pound (LBP)",
        "Lesotho Loti (LSL)", "Liberian Dollar (LRD)", "Libyan Dinar (LYD)", "Lithuanian Litas (LTL)", "Macanese Pataca (MOP)",
        "Macedonian Denar (MKD)", "Malagasy Ariary (MGA)", "Malawian Kwacha (MWK)", "Malaysian Ringgit (MYR)", "Maldivian Rufiyaa (MVR)",
        "Mauritanian Ouguiya (MRU)", "Mauritian Rupee (MUR)", "Mexican Peso (MXN)", "Moldovan Leu (MDL)", "Mongolian Tögrög (MNT)",
        "Moroccan Dirham (MAD)", "Mozambican Metical (MZN)", "Myanmar Kyat (MMK)", "Namibian Dollar (NAD)", "Nepalese Rupee (NPR)",
        "Netherlands Antillean Guilder (ANG)", "New Taiwan Dollar (TWD)", "New Zealand Dollar (NZD)", "Nicaraguan Córdoba (NIO)", "Nigerian Naira (NGN)",
        "North Korean Won (KPW)", "Norwegian Krone (NOK)", "Omani Rial (OMR)", "Pakistani Rupee (PKR)", "Panamanian Balboa (PAB)",
        "Papua New Guinean Kina (PGK)", "Paraguayan Guaraní (PYG)", "Peruvian Sol (PEN)", "Philippine Peso (PHP)", "Polish Złoty (PLN)",
        "Qatari Riyal (QAR)", "Romanian Leu (RON)", "Russian Ruble (RUB)", "Rwandan Franc (RWF)", "Saint Helena Pound (SHP)",
        "Samoan Tala (WST)", "Sao Tome and Principe Dobra (STN)", "Saudi Riyal (SAR)", "Serbian Dinar (RSD)", "Seychellois Rupee (SCR)",
        "Sierra Leonean Leone (SLL)", "Singapore Dollar (SGD)", "Solomon Islands Dollar (SBD)", "Somali Shilling (SOS)", "South African Rand (ZAR)",
        "South Korean Won (KRW)", "South Sudanese Pound (SSP)", "Sri Lankan Rupee (LKR)", "Sudanese Pound (SDG)", "Surinamese Dollar (SRD)",
        "Swazi Lilangeni (SZL)", "Swedish Krona (SEK)", "Swiss Franc (CHF)", "Syrian Pound (SYP)", "Tajikistani Somoni (TJS)",
        "Tanzanian Shilling (TZS)", "Thai Baht (THB)", "Tongan Paʻanga (TOP)", "Trinidad and Tobago Dollar (TTD)", "Tunisian Dinar (TND)",
        "Turkmenistani Manat (TMT)", "Ugandan Shilling (UGX)", "Ukrainian Hryvnia (UAH)", "United Arab Emirates Dirham (AED)", "United States Dollar (USD)",
        "Uruguayan Peso (UYU)", "Uzbekistani Som (UZS)", "Vanuatu Vatu (VUV)", "Venezuelan Bolívar Soberano (VES)", "Vietnamese Đồng (VND)",
        "West African CFA Franc (XOF)", "Yemeni Rial (YER)", "Zambian Kwacha (ZMW)", "Zimbabwean Dollar (ZWL)"
        ]

    countries = [
        "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda",
        "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain",
        "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia",
        "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso",
        "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic",
        "Chad", "Chile", "China", "Colombia", "Comoros", "Congo, Democratic Republic of the",
        "Congo, Republic of the", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic",
        "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador",
        "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland",
        "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala",
        "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India",
        "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan",
        "Kazakhstan", "Kenya", "Kiribati", "Korea, North", "Korea, South", "Kosovo", "Kuwait",
        "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein",
        "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta",
        "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco",
        "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal",
        "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Macedonia", "Norway",
        "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru",
        "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis",
        "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe",
        "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia",
        "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka",
        "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand",
        "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu",
        "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan",
        "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
        ]
    
    indian_states = [
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
        "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
        "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
        "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
        "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
        "Uttar Pradesh", "Uttarakhand", "West Bengal"
    ]
            # print(data)
    # print("hello came here")
    referral_id = request.GET.get('referralid') 
    try:
        # print("hello came here")
        if request.method == 'POST':
            fErrors = {}
            # enteredUsername=request.POST.get('username')
            # enteredEmail=request.POST.get('email')
            enteredUsername = request.POST.get('username', '').strip()
            enteredEmail = request.POST.get('email', '').strip()
            password1 = request.POST.get('password1', '').strip()
            password2 = request.POST.get('password2', '').strip()
        
                
            if password1!=password2:
                fErrors['password2'] = 'password and confirm password do not match'
 
            if len(fErrors)>0:
                return render(request, 'surveyappHome/page-register.html',context={'fErrors': fErrors,'logTab':'','regTab':True,'refferalid': referral_id,'aSelectedReg':'true','aSelectedLog':'False','currencies':currencies,'states':indian_states, 'countries':countries})

                   
                

            try:
                doesUserAlreadyExistInDB=ZqUser.objects.get(email=enteredEmail)
            except:
                doesUserAlreadyExistInDB=None
            if doesUserAlreadyExistInDB and  not doesUserAlreadyExistInDB.is_active and not doesUserAlreadyExistInDB.is_verfied:
                
                if doesUserAlreadyExistInDB.username.strip()==enteredUsername.strip():
                    doesUserAlreadyExistInDB.password=make_password(password2)
                    if sendMailVerificationEmail(request,doesUserAlreadyExistInDB,enteredEmail):
                        
                        
                    
                    
                    # result={'success': True, 'msg': 'An activation link had been sent to your entered email please click on that link to activate your account','redirect_url':reverse('preConfirmEmail')}
                        return redirect('unconfirmedEmail')
                #    return redirect('unconfirmedEmail')
                else:
                    
                    try:
                        doesUserNameAlreadyExistInDB=ZqUser.objects.get(username=enteredUsername)
                        fErrors['username'] = 'Username already taken'
                        return render(request,'surveyappHome/page-register.html',context={'fErrors': fErrors,'logTab':'','regTab':True,'refferalid': referral_id,'aSelectedReg':'true','aSelectedLog':'False','currencies':currencies, 'countries':countries,'states':indian_states})

                    except:
                        doesUserNameAlreadyExistInDB=None
                  
                            
                    doesUserAlreadyExistInDB.username=enteredUsername
                    doesUserAlreadyExistInDB.password=make_password(password2)
                    doesUserAlreadyExistInDB.save()
                    # if doesUserAlreadyExistInDB.username.strip()==enteredUsername.strip():
                    if sendMailVerificationEmail(request,doesUserAlreadyExistInDB,enteredEmail):
                    
                    
                    # result={'success': True, 'msg': 'An activation link had been sent to your entered email please click on that link to activate your account','redirect_url':reverse('preConfirmEmail')}
                         return redirect('unconfirmedEmail')
  
            
            
            
            
            # print("hello came here")
            # print(request.POST)
            # data = json.loads(request.body)
            form = UserForm(request.POST)
            # print(form)
            # print(form.is_valid())
            if form.is_valid():
                
                # print("came here")
                
                try:
                    user = form.save(commit=False)
                    user.is_active = False
                    user.is_verfied = False
                    user.save()
                except Exception as e:
                    print(e)
            
               
                
                # mail_subject = 'Activate your account.'
                if sendMailVerificationEmail(request,user,form.cleaned_data.get('email')):
                    
                    
                    # result={'success': True, 'msg': 'An activation link had been sent to your entered email please click on that link to activate your account','redirect_url':reverse('preConfirmEmail')}
                    return redirect('preConfirmEmail')
                else:
                    
                    return render(request, 'surveyappHome/page-register.html',context={'form': form,'logTab':False,'regTab':True,'refferalid': referral_id,'aSelectedReg':'true','aSelectedLog':'False','currencies':currencies, 'countries':countries,'states':indian_states})
                return render(request, 'zqapp/register.html',context={'form': form,'isActive':True,'logTab':False,'regTab':True,'aSelectedReg':'true','aSelectedLog':'False'})
                        
                    
          
                
               
              
            
                    # request.session['new_user_pk']=user.pk
                    # redirect_url = '/authenticate/'  # Change this to your desired URL
                    

                    # return redirect('authenticate')
                
                # else:
                    
                #     logger.error(f"{datetime.now()} :Something went wrong while sending OTP")
                #     return JsonResponse({'success': False, 'msg': 'some erorr occured'})
                #     # return redirect('authenticate')
                    
            
            else:
                if referral_id:
                    return render(request,reverse('register'),context={'form': form,'logTab':False,'regTab':True,'refferalid': referral_id,'aSelectedReg':'true','aSelectedLog':'False','states':indian_states})
                return render(request, reverse('register'),context={'form': form,'isActive':True,'logTab':False,'regTab':True,'aSelectedReg':'true','aSelectedLog':'False','states':indian_states})
                
    except Exception as e:
            return render(request, 'surveyappHome/page-register.html',context={'form': form,'logTab':False,'regTab':True,'aSelectedReg':'true','aSelectedLog':'False','currencies':currencies, 'countries':countries,'states':indian_states})

    form = UserForm()
    
    if referral_id:
        return render(request, 'surveyappHome/page-register.html',context={'form': form,'logTab':False,'regTab':True,'refferalid': referral_id,'aSelectedReg':'true','aSelectedLog':'False','currencies':currencies, 'countries':countries,'states':indian_states})
  
  
    print("came here")
    return render(request,'surveyappHome/page-register.html',context={'form': form,'logTab':False,'regTab':True,'aSelectedReg':'true','aSelectedLog':'False','currencies':currencies, 'countries':countries,'states':indian_states})
 
 
def activate(request, uidb64, token):
    
    # if not request.session.get('plainPass'):
    #     return
    # print("cam ehere")
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = ZqUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, ZqUser.DoesNotExist):
        user = None
    if user is not None and email_verification_token.check_token(user, token):
        
        user.is_active = True
        user.is_verfied = True
        usersIntroducersUsername=ZqUser.objects.get(memberid=user.introducerid.memberid)
        user.introducer_username=usersIntroducersUsername
        user.save()
        plainPass=user.plain_password
        rimberioBonus=RimberioCoinDistribution.objects.filter(task='registration').first().coin_reward
        # RimberioWallet.objects.create(amount=rimberioBonus,remark=f"rimberio bonus for registration is {rimberioBonus}",trans_for="Register",tran_by=user,trans_from=user,trans_to=user,trans_date=datetime.now(),trans_type='CREDIT')
        
        
        
        
        if 'newUserId' in request.session:
            del request.session['newUserId']
        # for backend in get_backends():
        #     print(backend)
        #     # if backend.user_can_authenticate(user):
                
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        
       
        sendSuccessRegMail(request.user,plainPass )
            
            #     break
        # login(request, user)
        # print(request.user.username)
        # assignSocialJobs(request.user)
        messages.success(request, 'Your email has been verified and  you are now logged in')
        return redirect('newmemberDashboard')
    else:
        return redirect('linkexpired')
  
 
 
 
def assignSocialJobs(user):
    
        allDummyUsersForTesting=ZqUser.objects.filter(id=user.id)
        # allDummyUsersForTesting=ZqUser.objects.filter(is_dummy=True,username='vagak1')
        for user in allDummyUsersForTesting:
            
            
            allPackages=InvestmentWallet.objects.filter(txn_by=user)
            allSocialJobs=SocialJobs.objects.all()
            # if allPackages.count()>0:
            #     isPaidUser=True
            # else:
            isPaidUser=False
            
            if isPaidUser:
                
                for package in allPackages:
                    for socialjob in  allSocialJobs:
                        assignedJobsForThisPackage=AssignedSocialJob.objects.filter(assigned_to=user,package_id=package,social_job_id=socialjob).count()
                        if assignedJobsForThisPackage>0:
                            continue
                        else:
                            allPreviousPackagesCount=AssignedSocialJob.objects.filter(assigned_to=user,package_id=package)
                            
                            if allPreviousPackagesCount.count()>0:
                                
                                lastObj=allPreviousPackagesCount.order_by('-id').first()
                                newEntryForThisPackage=AssignedSocialJob(assigned_to=user,package_id=package,social_job_id=socialjob,valid_from=lastObj.valid_upto,valid_upto=lastObj.valid_upto+timedelta(days=5)+ timedelta(days=2))
                                newEntryForThisPackage.save()
                            else:
                                newEntryForThisPackage=AssignedSocialJob(assigned_to=user,package_id=package,social_job_id=socialjob,valid_from=package.txn_date,valid_upto=package.txn_date+timedelta(days=5)+ timedelta(days=2))
                                newEntryForThisPackage.save()
            
            else:
                   
                for socialjob in  allSocialJobs:
                    
                    assignedJobsForThisPackage=AssignedSocialJob.objects.filter(assigned_to=user,social_job_id=socialjob).count()
                    if assignedJobsForThisPackage>0:
                        continue
                    else:
                        allPreviousPackagesCount=AssignedSocialJob.objects.filter(assigned_to=user)
                        if allPreviousPackagesCount.count()>0:
                            lastObj=allPreviousPackagesCount.order_by('-id').first()
                            newEntryForThisPackage=AssignedSocialJob(assigned_to=user,social_job_id=socialjob,valid_from=lastObj.valid_upto,valid_upto=lastObj.valid_upto+timedelta(days=5)+ timedelta(days=2))
                            newEntryForThisPackage.save()
                        else:
                            newEntryForThisPackage=AssignedSocialJob(assigned_to=user,social_job_id=socialjob,valid_from=user.date_joined,valid_upto=user.date_joined+timedelta(days=5)+ timedelta(days=2))
                            newEntryForThisPackage.save()                 
 
 
 
 
 
 
def sendMailVerificationEmail(request,user,email):
    # randNum=random.randint(100000,999999)
    
    
    
    print(request.META['HTTP_HOST'])
    html_content = render_to_string('zqapp/emailtemps/verifyEmailToRegister.html',{
                    'user': user,
                    'domain': request.META['HTTP_HOST'],
                    # 'domain': 'www.rimberio.world',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': email_verification_token.make_token(user),
                })
    
    # print(https://{{ domain }}{% url 'activate' uidb64=uid token=token)
    
    # print('came here')
    
    with get_connection(  
                        
        host=settings.EMAIL_HOST, 
        port=settings.EMAIL_PORT,  
        username=settings.EMAIL_HOST_USER, 
        password=settings.EMAIL_HOST_PASSWORD, 
        use_tls=settings.EMAIL_USE_TLS  
    ) as connection:  
        subject = "Activate your account"  
        email_from = "noreply@ritcoin.exchange" 
        recipient_list = [email]  
        # message ="This is testing email" 
        body=html_content 
        sendEmail=EmailMessage(subject, body, email_from, recipient_list, connection=connection)
        # body=html_content 
        # sendEmail=EmailMessage(subject, body, email_from, recipient_list, connection=connection)
        sendEmail.content_subtype = 'html'
        # print(sendEmail)
        if sendEmail.send():
            # print('mail sent successfully')
            request.session['newUserId'] = user.id
            current_time = timezone.now()
            request.session['otp_timestamp'] = current_time.timestamp()
            return True
        
        else:
            # print('')
            logger.error(f"{datetime.now()} :something went wrong while  sending email")
            return False

 
 
def otpVerify(request):
        
    if request.method == 'POST':
        
        print("came here")
        print(json.loads(data))
        
        return
        
        form = OTPVerificationForm(request.POST or None,request=request)
        # print("========came here to verify OTP====",form.is_valid())
        if form.is_valid():
            del request.session['RegOTP']
            
            introId=ZqUser.objects.get(memberid=request.session.get('RegUserIntroID'))
            
            if introId:
                print(introId)
                user = ZqUser.objects.create(username=request.session.get('RegUserUsername'),email=request.session.get('regEmail'),introducerid=introId,password=make_password(request.session.get('RegUserPassword')), country=request.session.get('country'), local_currency=request.session.get('local_currency')) 

                user.is_verfied = True  # Set the field to True
                
                try:
                    user.save()
                except Exception as e:
                    # print(e)
                    logger.error(f"{datetime.now()} :An error occurred: %s", str(e))
            

            # del request.session['new_user_pk']
            del request.session['regEmail']
            # request.session['regUserEmail']=email
            del request.session['RegUserUsername']
            del request.session['RegUserIntroID']
            del request.session['RegUserPassword']
            del request.session['country']
            del request.session['local_currency']

            messages.success(request,  'Thanks for being part of Rimberio Please Login to continue!')
# ===============================changes made here=====================================
            return redirect('index')
            # return None
            
        else:
            
            return render(request,'zqapp/user-otp-auth.html',context={
                
                'form':form
            })
                
    form = OTPVerificationForm(request.POST)
    return render(request, 'zqapp/user-otp-auth.html',context={
        'form':'form'
    })



 
def resetPassword(request):
    
    if request.method=="POST":
         
        ent_email_or_username=request.POST.get('email_or_username')
        # print(ent_email)

        try:
            if '@' in ent_email_or_username and '.' in ent_email_or_username:
                user = ZqUser.objects.filter(email=ent_email_or_username)
                if user.count()>1:
                    error_message = 'Multiple accounts exist with this email. Please reset  password through username.'

                    return render(request,'zqapp/reset-password.html',context={
                        'error_message':error_message
                    })
                else:
                    user=ZqUser.objects.get(email=ent_email_or_username)
                
            else:
                user = ZqUser.objects.get(username=ent_email_or_username)
                
        except ZqUser.DoesNotExist:
            user = None
            
        if user:
            

          
            sentOTP=send_otp(request=request,email=user.email,subject='otp to reset password',template='resetPassEmailTemplate.html',whatfor='passwordReset')
 
            if sentOTP:
                    
                # newOTP=USEROTP.objects.create(email=ent_email,type='resetPass',otp_code=sentOTP)
                # newOTP.save()
                request.session['MEMID']=user.memberid
                # request.session['OTP']
                
                messages.success(request, "OTP sent successfully please verify it to change password")     
                return render(request,'zqapp/password-reset-otp-auth.html',context={
                    'email': user.email
                })
        else:
            messages.add_message(request,messages.WARNING, "member with this email doesn't exist")
            # messages.error(request, "member with this email doesn't exist")
            # redirect('passwordReset')
            error_message = 'member with this email or username does not exist please enter correct username or email'

            return render(request,'zqapp/reset-password.html',context={
                'error_message':error_message
            })
        
        
    
    return render(request,'zqapp/reset-password.html')
    
    
def resetOtpVerify(request):
    
    if request.method == 'POST':
        Otp =request.POST.get('otp')
 
        if str(Otp)==str(request.session.get('OTP')):

           
            del request.session['OTP']
            
            messages.success(request, "OTP verified successfully")
            return render(request,'zqapp/new-password.html')
        
        else:
            
            messages.warning(request, "Invalid OTP")
            return render(request,'zqapp/password-reset-otp-auth.html',context={
                'message':'Invalid OTP',
                
            })
        

    return render(request, 'zqapp/password-reset-otp-auth.html')


def newPassword(request):
    
    if request.method == 'POST':
        
 
        password =request.POST.get('password')
        confPassword =request.POST.get('confPassword')     
   
        if password==confPassword:


            try:
                user=ZqUser.objects.get(memberid=request.session.get('MEMID'))
                user.set_password(password)
                user.save()
            except Exception as e:
                logger.error(f"{datetime.now()} :An error occurred: %s", str(e))
                # print(e)
            
            messages.success(request, "Password changed successfully please login to continue")
            return redirect('login')
        

        
        else:
            
             messages.warning(request, "Invalid Password")
             return render(request,'zqapp/new-password.html',context={
                    'message':'Password does not match'
                })
        
            
            

    return render(request, 'zqapp/new-password.html')
    

def send_mail(request,email,template):

    randNum=random.randint(100000,999999)
    html_content = render_to_string('zqapp/emailtemps/'+template, {'OTP': randNum})
    
    # print('came here')
    
    with get_connection(  
                        
        host=settings.EMAIL_HOST, 
        port=settings.EMAIL_PORT,  
        username=settings.EMAIL_HOST_USER, 
        password=settings.EMAIL_HOST_PASSWORD, 
        use_tls=settings.EMAIL_USE_TLS  
    ) as connection:  
        subject = "This is testing email"  
        email_from = "noreply@ritcoin.exchange" 
        recipient_list = [email]  
        # message ="This is testing email" 
        body=html_content 
        sendEmail=EmailMessage(subject, body, email_from, recipient_list, connection=connection).send()
       
        # print(sendEmail)
        if sendEmail:
            # print('mail sent successfully')
            request.session['OTP'] = randNum
            return True
        
        else:
            # print('')
            logger.error(f"{datetime.now()} :something went wrong while  sending email")
            return False


def send_otp(request,email,subject,template,whatfor):
    
   
    randNum=random.randint(100000,999999)

    html_content = render_to_string('zqapp/emailtemps/'+template, {'OTP': randNum})
    
    # print('came here')
    
    with get_connection(  
                        
        host=settings.EMAIL_HOST, 
        port=settings.EMAIL_PORT,  
        username=settings.EMAIL_HOST_USER, 
        password=settings.EMAIL_HOST_PASSWORD, 
        use_tls=settings.EMAIL_USE_TLS  
    ) as connection:  
        subject = subject  
        email_from = "noreply@ritcoin.exchange" 
        recipient_list = [email]  
        # message ="This is testing email" 
        body=html_content 
        sendEmail=EmailMessage(subject, body, email_from, recipient_list, connection=connection).send()
       

        if sendEmail:
            
            if whatfor=="topup":
                
                obj = SendOTP()
                obj.email = email
                obj.otp = int(randNum)
                obj.trxndate = datetime.now()
                obj.status = 1
                obj.save()
                return True
            
            elif whatfor=="register":
                
                request.session['RegOTP'] = randNum
                print(randNum)
                
              
                return True
            elif whatfor=="send_otp_receive_wallet_address":
                
                # request.session['OTP'] = randNum
                return randNum
                
            elif whatfor=="passwordReset":
                
                request.session['OTP'] = randNum
                return randNum
                
            
            
            # print('mail sent successfully')
            
            
        
        else:
            
            logger.error(f"{datetime.now()} :An error occurred: something went wrong while  sending email")
            return False


def encrypt_otp(otp_value):
    # Replace 'your_secret_key' with a strong secret key
    secret_key = b'\x92#\xe4\xf7\x9a\x87\xc1\x1e\x9b\xbf\x87\xbb5w\x81'
    encrypted_value = base64.b64encode(otp_value.encode())
    return encrypted_value


def decrypt_otp(encrypted_value):
    secret_key = b'\x92#\xe4\xf7\x9a\x87\xc1\x1e\x9b\xbf\x87\xbb5w\x81'
    decrypted_value = base64.b64decode(encrypted_value)
    return decrypted_value.decode()


def set_otp_cookie(request, otp_value):
    encrypted_otp = encrypt_otp(otp_value)
    
    # print("OTP cookie set successfully")
    response = HttpResponse()
    response.set_cookie('OTP', encrypted_otp, max_age=None)  # Set max_age=None to make the cookie a session cookie
    return response


def get_otp_cookie(request):
    encrypted_otp = request.COOKIES.get('OTP')
    if encrypted_otp:
        decrypted_otp = decrypt_otp(encrypted_otp)
        return HttpResponse(f"Decrypted OTP value from cookie: {decrypted_otp}")
    else:
        return HttpResponse("OTP cookie not found")


def resendOTPResetPass(request):

    result={}
    user=ZqUser.objects.get(memberid=request.session.get('MEMID'))
    
    try:
        
        sentOTP=send_otp(request=request,email=user.email,subject='otp to reset password',template='resetPassEmailTemplate.html',whatfor='passwordReset')

        if sentOTP:   
            result['status']=1
            result['message']='OTP resent to your email successfully'
            return JsonResponse(result)
        else:
            
            result['status']=0
            result['message']='Some error occured while sending email'
            return JsonResponse(result)
            
    except Exception as e:
        
        # print(e)
        logger.error(f"{datetime.now()} :An error occurred: %s", str(e))
        result['status']=0
        result['message']='Some error occured'
        return JsonResponse(result)
        
    
def resendOTPReg(request):
    result={}
    Regemail=request.session.get('regEmail')

    try:
        
        sentOTP=send_otp(request=request,email=Regemail,subject='otp to reset password',template='resetPassEmailTemplate.html',whatfor='register')

        if sentOTP:   
            result['status']=1
            result['message']='OTP resent to your email successfully'
            return JsonResponse(result)
        else:
            
            result['status']=0
            result['message']='Some error occured while sending email'
            return JsonResponse(result)
            
    except Exception as e:
        
        # print(e)
        logger.error(f"{datetime.now()} :An error occurred: %s", str(e))
        result['status']=0
        result['message']='Some error occured'
        return JsonResponse(result)
        
                                
def returnMemberName(request):    
    result={}
    if request.method=='POST':
        
        entMemId=request.POST.get('memberid').strip()
        fieldType=request.POST.get('fieldType')
        # print(entMemId)
        
        if fieldType == 'introducerid':
    
        
            try:
                
                if  entMemId.strip().lower().startswith('rbo') or entMemId.strip().lower().startswith('zql'):
                    entMemId=ZqUser.objects.get(memberid=entMemId)
                else:
                    entMemId=ZqUser.objects.get(username=entMemId)
                    
                if entMemId.first_name:
                    
                    result['memberName']=entMemId.first_name
                    
                else:
                    result['memberName']=entMemId.username
                    
                result['status']=1
                return JsonResponse(result)
                
            except:
                
                result['status']=0
                result['msg']="User with entered memberid doesn't exist"
                return JsonResponse(result)
                
                # entMemId=None
                

        if fieldType == 'username':
            
            userName=request.POST.get('username')
            
            
            try:
                
                # if entMemId.strip().lower().startswith('fb') or entMemId.strip().lower().startswith('zq'):
                entMemId=ZqUser.objects.get(username=userName)
              
                
                
            except Exception as e:
                
                entMemId=None
              
            
            if entMemId:
                result['status']=1
                result['msg']='Username already taken'
                return JsonResponse(result)
            else:
                result['status']=0
                result['msg']=''
                return JsonResponse(result)
        
# import json
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from .forms import LoginForm  # Make sure to import your LoginForm
# from django.shortcuts import redirect  # Import redirect if you plan to use it
# from django.contrib.auth import authenticate, login

def userLogin(request):
    # try:
    # print("came here")
    
    currencies = [
    "Afghan Afghani (AFN)", "Albanian Lek (ALL)", "Algerian Dinar (DZD)", "Angolan Kwanza (AOA)", "Argentine Peso (ARS)",
    "Armenian Dram (AMD)", "Aruban Florin (AWG)", "Australian Dollar (AUD)", "Azerbaijani Manat (AZN)", "Bahamian Dollar (BSD)",
    "Bahraini Dinar (BHD)", "Bangladeshi Taka (BDT)", "Barbadian Dollar (BBD)", "Belarusian Ruble (BYN)", "Belgian Franc (BEF)",
    "Belize Dollar (BZD)", "Bermudian Dollar (BMD)", "Bhutanese Ngultrum (BTN)", "Bolivian Boliviano (BOB)", "Bosnia-Herzegovina Convertible Mark (BAM)",
    "Botswana Pula (BWP)", "Brazilian Real (BRL)", "British Pound (GBP)", "Brunei Dollar (BND)", "Bulgarian Lev (BGN)",
    "Burundian Franc (BIF)", "Cambodian Riel (KHR)", "Canadian Dollar (CAD)", "Cape Verdean Escudo (CVE)", "Cayman Islands Dollar (KYD)",
    "Central African CFA Franc (XAF)", "Chilean Peso (CLP)", "Chinese Yuan (CNY)", "Colombian Peso (COP)", "Comorian Franc (KMF)",
    "Congolese Franc (CDF)", "Costa Rican Colón (CRC)", "Croatian Kuna (HRK)", "Cuban Convertible Peso (CUC)", "Cuban Peso (CUP)",
    "Czech Koruna (CZK)", "Danish Krone (DKK)", "Djiboutian Franc (DJF)", "Dominican Peso (DOP)", "East Caribbean Dollar (XCD)",
    "Egyptian Pound (EGP)", "Eritrean Nakfa (ERN)", "Estonian Kroon (EEK)", "Eswatini Lilangeni (SZL)", "Ethiopian Birr (ETB)",
    "Euro (EUR)", "Falkland Islands Pound (FKP)", "Fijian Dollar (FJD)", "Gambian Dalasi (GMD)", "Georgian Lari (GEL)",
    "Ghanaian Cedi (GHS)", "Gibraltar Pound (GIP)", "Guatemalan Quetzal (GTQ)", "Guinean Franc (GNF)", "Guyanaese Dollar (GYD)",
    "Haitian Gourde (HTG)", "Honduran Lempira (HNL)", "Hong Kong Dollar (HKD)", "Hungarian Forint (HUF)", "Icelandic Króna (ISK)",
    "Indian Rupee (INR)", "Indonesian Rupiah (IDR)", "Iranian Rial (IRR)", "Iraqi Dinar (IQD)", "Israeli New Shekel (ILS)",
    "Jamaican Dollar (JMD)", "Japanese Yen (JPY)", "Jordanian Dinar (JOD)", "Kazakhstani Tenge (KZT)", "Kenyan Shilling (KES)",
    "Kuwaiti Dinar (KWD)", "Kyrgystani Som (KGS)", "Lao Kip (LAK)", "Latvian Lats (LVL)", "Lebanese Pound (LBP)",
    "Lesotho Loti (LSL)", "Liberian Dollar (LRD)", "Libyan Dinar (LYD)", "Lithuanian Litas (LTL)", "Macanese Pataca (MOP)",
    "Macedonian Denar (MKD)", "Malagasy Ariary (MGA)", "Malawian Kwacha (MWK)", "Malaysian Ringgit (MYR)", "Maldivian Rufiyaa (MVR)",
    "Mauritanian Ouguiya (MRU)", "Mauritian Rupee (MUR)", "Mexican Peso (MXN)", "Moldovan Leu (MDL)", "Mongolian Tögrög (MNT)",
    "Moroccan Dirham (MAD)", "Mozambican Metical (MZN)", "Myanmar Kyat (MMK)", "Namibian Dollar (NAD)", "Nepalese Rupee (NPR)",
    "Netherlands Antillean Guilder (ANG)", "New Taiwan Dollar (TWD)", "New Zealand Dollar (NZD)", "Nicaraguan Córdoba (NIO)", "Nigerian Naira (NGN)",
    "North Korean Won (KPW)", "Norwegian Krone (NOK)", "Omani Rial (OMR)", "Pakistani Rupee (PKR)", "Panamanian Balboa (PAB)",
    "Papua New Guinean Kina (PGK)", "Paraguayan Guaraní (PYG)", "Peruvian Sol (PEN)", "Philippine Peso (PHP)", "Polish Złoty (PLN)",
    "Qatari Riyal (QAR)", "Romanian Leu (RON)", "Russian Ruble (RUB)", "Rwandan Franc (RWF)", "Saint Helena Pound (SHP)",
    "Samoan Tala (WST)", "Sao Tome and Principe Dobra (STN)", "Saudi Riyal (SAR)", "Serbian Dinar (RSD)", "Seychellois Rupee (SCR)",
    "Sierra Leonean Leone (SLL)", "Singapore Dollar (SGD)", "Solomon Islands Dollar (SBD)", "Somali Shilling (SOS)", "South African Rand (ZAR)",
    "South Korean Won (KRW)", "South Sudanese Pound (SSP)", "Sri Lankan Rupee (LKR)", "Sudanese Pound (SDG)", "Surinamese Dollar (SRD)",
    "Swazi Lilangeni (SZL)", "Swedish Krona (SEK)", "Swiss Franc (CHF)", "Syrian Pound (SYP)", "Tajikistani Somoni (TJS)",
    "Tanzanian Shilling (TZS)", "Thai Baht (THB)", "Tongan Paʻanga (TOP)", "Trinidad and Tobago Dollar (TTD)", "Tunisian Dinar (TND)",
    "Turkmenistani Manat (TMT)", "Ugandan Shilling (UGX)", "Ukrainian Hryvnia (UAH)", "United Arab Emirates Dirham (AED)", "United States Dollar (USD)",
    "Uruguayan Peso (UYU)", "Uzbekistani Som (UZS)", "Vanuatu Vatu (VUV)", "Venezuelan Bolívar Soberano (VES)", "Vietnamese Đồng (VND)",
    "West African CFA Franc (XOF)", "Yemeni Rial (YER)", "Zambian Kwacha (ZMW)", "Zimbabwean Dollar (ZWL)"
]

    countries = [
        "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda",
        "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain",
        "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia",
        "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso",
        "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic",
        "Chad", "Chile", "China", "Colombia", "Comoros", "Congo, Democratic Republic of the",
        "Congo, Republic of the", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic",
        "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador",
        "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland",
        "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala",
        "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India",
        "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan",
        "Kazakhstan", "Kenya", "Kiribati", "Korea, North", "Korea, South", "Kosovo", "Kuwait",
        "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein",
        "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta",
        "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco",
        "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal",
        "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Macedonia", "Norway",
        "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru",
        "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis",
        "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe",
        "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia",
        "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka",
        "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand",
        "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu",
        "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan",
        "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
    ]
    

   
    
    if request.method == 'POST':
        
        # data = json.loads(request.body)
        
        form = LoginForm(request.POST)
        # print(form)
        # print(form.is_valid())
        # print("came here")
        if form.is_valid():
            email_or_username = form.cleaned_data['email_or_username']
            password = form.cleaned_data['password']
            
            
        
            if  '@' in email_or_username and '.' in  email_or_username :
                userInfo=ZqUser.objects.get(email=email_or_username)
            else:
                userInfo=ZqUser.objects.get(username=email_or_username)
             
            if  userInfo.is_blocked:
                return redirect('login')

        
            if userInfo.is_verfied :
                
                
                
                if userInfo.userType=='member' :
                    if 'email' in form.cleaned_data:
                        # userInfo=ZqUser.objects.filter(email=email_or_username)
                        user = authenticate(request, email=email_or_username, password=password)
                    else:
                        # userInfo=ZqUser.objects.filter(username=email_or_username)
                        user = authenticate(request, username=email_or_username, password=password)
                    
                    # print(user)
                
                    if user is not None:
                        login(request, user)
                
                        messages.success(request, "You have been logged in successfully.")
                        # next_url = request.GET.get('next')
                        next_url = request.POST.get('next') 
                        
                        
                        # print(next_url)
                        if next_url:
                            return redirect(next_url)
                            # redirect_url = next_url  # Change this to your desired URL
                            # return JsonResponse({'success': True, 'redirect_url': redirect_url})
                        else:
                        # If there's no next parameter, redirect to a default URL
                        
                        # ==========================================changs ==============================
                            # redirect_url = '/member/'  # Change this to your desired URL
                            # return JsonResponse({'success': True, 'redirect_url': redirect_url})
                            return redirect('newmemberDashboard') 
                            # return

                    # return redirect('success')
                    else:
                        # Return an error message
                        messages.error(request, "Invalid username or password.")
                        # messages.add_message(request, messages.WARNING, 'User logged out successfully')
                        
                        # error_message = "Invalid username or password."
                        # return JsonResponse({'success': False, 'msg': 'Invalid credentials'}, status=400)

                        return render(request,'surveyappHome/page-login.html',context={
                            'login_error': 'Invalid username or password',
                            'currencies':currencies, 'countries':countries,
                            'logTab':True
                            })
                        
                elif userInfo.userType=='admin':
                    
                    if 'email' in form.cleaned_data:
                    # userInfo=ZqUser.objects.filter(email=email_or_username)
                        user = authenticate(request, email=email_or_username, password=password)
                    else:
                    # userInfo=ZqUser.objects.filter(username=email_or_username)
                        user = authenticate(request, username=email_or_username, password=password)
                
            
                    if user is not None:
                        login(request, user)
                
                        messages.success(request, "You have been logged in successfully.")
                        # next_url = request.GET.get('next')
                        next_url = request.POST.get('next') 
                        # print(next_url)
                        if next_url:
                            # return redirect(next_url)
                            return redirect(next_url)
                        else:
                        # If there's no next parameter, redirect to a default URL
                            # redirect_url = '/member/'  # Change this to your desired URL
                            return redirect('zqAdminDashboard') 
                            # return redirect('newmemberDashboard')  # R
                            
                            # return

                    # return redirect('success')
                    else:
                        # Return an error message
                        messages.error(request, "Invalid username or password.")
                        # messages.add_message(request, messages.WARNING, 'User logged out successfully')
                        
                        # error_message = "Invalid username or password."
                    #    ============================== # chnages heer======================================================
                    #     return render(request,'zqUsers/register.html',context={
                    #     'login_error': 'Invalid username or password'
                    # })
                        # return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=400)
                    #     return render(request,'zqapp/register.html',context={
                    #     'login_error': 'Invalid username or password'
                    # })
                        return render(request, 'surveyappHome/page-login.html',context={'form': form,'logTab':True,'regTab':'','aSelectedReg':'false','aSelectedLog':'true','currencies':currencies, 'countries':countries})

                    
                    
                
                        
            else:

                # messages.error(request, "Please verify your email to continue")
                if send_otp(request,userInfo.email,'otp for user registration','registerEmailOtp.html','register'):
                
                    # print("PK is ",userInfo.pk)
                    request.session['new_user_pk']=userInfo.pk
                    # messages.add_message(request,messages.ERROR, "Your email hasn't been verified yet please verify otp sent to your  email to continue")
                    messages.warning(request, "Your email hasn't been verified yet please verify otp sent to your  email to continue")
                    # return redirect('authenticate')
                    return redirect('register')
                else:
                    # print('Something went wrong while sending OTP')
                    logger.error(f"{datetime.now()} :Something went wrong while sending OTP ")
                    messages.add_message(request,messages.ERROR, "Your email hasn't been verified yet please verify otp sent to your  email to continue")
                    # return redirect('authenticate')
                    return redirect('register')
                    # return redirect('email-verify')
                
        else:

            return render(request, 'surveyappHome/page-login.html',context={'form': form,'logTab':True,'regTab':'','aSelectedReg':'false','aSelectedLog':'true','currencies':currencies, 'countries':countries})

    # except django.middleware.csrf.CsrfViewMiddleware as e:
    #     # Handle CSRF verification failure
    #     # error_message = "CSRF verification failed. Please refresh the page and try again."
    #     # return HttpResponseForbidden(error_message)
    #     return render(request, 'zqapp/register.html',context={'logTab':'active show','regTab':'','aSelectedReg':'false','aSelectedLog':'true'})

    

    return render(request, 'surveyappHome/page-login.html',context={'logTab':True,'regTab':'','aSelectedReg':'false','aSelectedLog':'true','currencies':currencies, 'countries':countries})



def resendActivationEmail(request):
    
    
    current_time = timezone.now()
    otp_timestamp = request.session.get('otp_timestamp')
    
    if otp_timestamp:
        otp_time = timezone.make_aware(datetime.fromtimestamp(otp_timestamp))
        if current_time < otp_time + timedelta(minutes=1):
            return JsonResponse({'success': True,'msg':'You can request for new activation link after 60 seconds'})
            # messages.error(request, "You can request a new OTP after 5 minutes.")
        
            # return redirect('send_otp') 

    # print("came here")
    usrId=request.session.get('newUserId')
    if usrId:
        
        User=ZqUser.objects.get(id=usrId)

    else:
        User=None
    
    
    if User:
        
        if sendMailVerificationEmail(request,User,User.email):
            
            return JsonResponse({'success': True,'msg':'An activation link has been resent to your email succesfully'})
        
        else:
            return JsonResponse({'success': False,'msg':'Something went wrong'})
            
            
    else:
        
        return JsonResponse({'success': False,'msg':'Something went wrong'})
        

def sendRestPassLink(request,user,email):
    # randNum=random.randint(100000,999999)
    
    
    
    # print(request.META['HTTP_HOST'])
    html_content = render_to_string('zqapp/emailtemps/resetPassEmail.html',{
                    'user': user,
                    'domain': request.META['HTTP_HOST'],
                    # 'domain': 'www.rimberio.world',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': email_verification_token.make_token(user),
                })
    
    # print(https://{{ domain }}{% url 'activate' uidb64=uid token=token)
    
    # print('came here')
    
    with get_connection(  
                        
        host=settings.EMAIL_HOST, 
        port=settings.EMAIL_PORT,  
        username=settings.EMAIL_HOST_USER, 
        password=settings.EMAIL_HOST_PASSWORD, 
        use_tls=settings.EMAIL_USE_TLS  
    ) as connection:  
        subject = "Reset password request"  
        email_from = "noreply@ritcoin.exchange" 
        recipient_list = [email]  
        # message ="This is testing email" 
        body=html_content 
        sendEmail=EmailMessage(subject, body, email_from, recipient_list, connection=connection).send()
       
        # print(sendEmail)
        if sendEmail:
            # print('mail sent successfully')
            request.session['newUserId'] = user.id
            current_time = timezone.now()
            request.session['otp_timestamp'] = current_time.timestamp()
            return True
        
        else:
            # print('')
            logger.error(f"{datetime.now()} :something went wrong while  sending email")
            return False


def generate_random_string(length=10):
    # Define the possible characters in the string
    characters = string.ascii_letters + string.digits  # This includes lowercase, uppercase letters, and digits
    # Generate a random string using random.choices
    random_string = ''.join(random.choices(characters, k=length))
    return random_string

# # Example usage
# random_string = generate_random_string(10)
# print(random_string)
 
def resetPassConf(request, uidb64, token):
    # print("cam ehere")
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = ZqUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, ZqUser.DoesNotExist):
        user = None
    if user is not None and email_verification_token.check_token(user, token):
        
        # retun redirect
        
        if 'newUserId' in request.session:
            del request.session['newUserId']
            
        uniqueIdentifier=generate_random_string()
        
        request.session[uniqueIdentifier]=user.id
            
        messages.success(request, 'Your email has been verified please change your password')
    
        return render(request,'surveyappHome/confResetPass.html',context={
            'uniqueIdentifier':uniqueIdentifier
        })
        # for backend in get_backends():
        #     print(backend)
        #     # if backend.user_can_authenticate(user):
                
        # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            #     break
        # login(request, user)
        # print(request.user.username)
        # messages.success(request, 'Your email has been verified and  you are now logged in')
        # return redirect('newmemberDashboard')
    else:
        messages.error(request, 'Invalid credentials please try again')
        return redirect('changePassword')
  
 
 


def changePassword(request):
    
    
   
    if request.method=='POST':
        
       
        
        type = request.POST.get('type').strip()
        
        
        
        if type == "resetPass" :
            
            data = request.POST.get('email').strip()
            
            if data:
            
                try:
                    
                    member=ZqUser.objects.get(email=data)
                except Exception as e:
                    member=None
                    
                if member:
                    # print("++++++came here")
                    if sendRestPassLink(request,member,member.email):
                            return JsonResponse({
                            'status':1,
                            'msg':'A reset passwowrd link has been sent to your email please click on it to reset your password'
                            })

                    else:
                            return JsonResponse({
                            'status':0,
                            'msg':'something went wrong plase try again '
                            })
                        
                
                else:
                    return JsonResponse({
                        'status':0,
                        'msg':'Please enter valid email'
                    })
            else:
                # else:
                    return JsonResponse({
                        'status':0,
                        'msg':'Email field is required'
                    })        
        
        elif type == "changePass":
            password = request.POST.get('password').strip()
            conf_password = request.POST.get('conf_password').strip()
            uIdentifier = request.POST.get('uIdentifier').strip()
            print(uIdentifier)
            if uIdentifier in request.session:
                
                userId= request.session.get(uIdentifier)
                try:
                   mem=ZqUser.objects.get(id=userId)
                   del request.session[uIdentifier]
                except:
                    mem=None
                    
                if mem:
                    mem.password=make_password(password)
                    mem.save()
                    
                    messages.success(request,'Your password has been reset successfully please login with your new credentials')
                    return redirect('login')
                
                else:
                    messages.error(request,'unauthenticated operation  was performed please try again')
                    return redirect('changePassword')
                    
            else:
                
                messages.error(request,'unauthenticated operation  was performed please try again')
                return redirect('changePassword')
                       
            
    
    
    return render(request,"surveyappHome/forgot-password.html")
    
def resetPass(request):
    
    
    return render(request,"surveyappHome/resetPass.html")
    
def mainConfirm(request):
    
    
    return render(request,"surveyappHome/mainConfirm.html")
    
  



def confirmEmail(request):
    
    return render(request,"surveyappHome/preConfirmEmailPage.html")
    
   
   
   
def hasUsernameAlreadyTaken(request):
    
    if request.method=='POST':
        ... 
   





def sendSuccessRegMail(user,plainPass):
    # user = ZqUser.objects.get(pk=user_id)
    # token = email_verification_token(user)
    # uid = urlsafe_base64_encode(force_bytes(user.pk))
    # asid = urlsafe_base64_encode(force_bytes(assignedSocialJobId))

    # token = long_email_verification_token.make_token(user)
    html_content = render_to_string('zqapp/emailtemps/regisuccess.html',{
                'username': user.username,
                'password': plainPass,
                # 'domain': request.META['HTTP_HOST'],
                # 'domain': 'www.rimberio.world',
                # 'uid': uid,
                # 'asid': asid,
                # 'token': email_verification_token.make_token(user),
            })


    with get_connection(  
                        
        host=settings.EMAIL_HOST, 
        port=settings.EMAIL_PORT,  
        username=settings.EMAIL_HOST_USER, 
        password=settings.EMAIL_HOST_PASSWORD, 
        use_tls=settings.EMAIL_USE_TLS  
    ) as connection:  
        subject = "Ritcoin Onboarding"  
        email_from = "noreply@ritcoin.exchange" 
        recipient_list = [user.email]  
        # message ="This is testing email" 
        body=html_content 
        sendEmail=EmailMessage(subject, body, email_from, recipient_list, connection=connection)
        sendEmail.content_subtype = 'html'
       
        # print(sendEmail)
        if sendEmail.send():
            # print('mail sent successfully')
            # request.session['newUserId'] = user.id
            # current_time = timezone.now()
            # request.session['otp_timestamp'] = current_time.timestamp()
            return True
        
        else:
            # print('')
            logger.error(f"{datetime.now()} :something went wrong while  sending email")
            return False

def sendMailTest():
    # user = ZqUser.objects.get(pk=user_id)
    # token = email_verification_token(user)
    # uid = urlsafe_base64_encode(force_bytes(user.pk))
    # asid = urlsafe_base64_encode(force_bytes(assignedSocialJobId))

    # token = long_email_verification_token.make_token(user)
    html_content = render_to_string('zqUsers/emailtemps/testuseremail.html',{
                'username':'Abhishek',
                'password': 'Abhishek',
                # 'domain': request.META['HTTP_HOST'],
                # 'domain': 'www.rimberio.world',
                # 'uid': uid,
                # 'asid': asid,
                # 'token': email_verification_token.make_token(user),
            })


    with get_connection(  
                        
        host=settings.EMAIL_HOST, 
        port=settings.EMAIL_PORT,  
        username=settings.EMAIL_HOST_USER, 
        password=settings.EMAIL_HOST_PASSWORD, 
        use_tls=settings.EMAIL_USE_TLS  
    ) as connection:  
        subject = "Ritcoin Onboarding"  
        email_from = "noreply@ritcoin.exchange" 
        recipient_list = ['amrevrp@gmail.com']  
        # message ="This is testing email" 
        body=html_content 
        sendEmail=EmailMessage(subject, body, email_from, recipient_list, connection=connection)
        sendEmail.content_subtype = 'html'
       
        # print(sendEmail)
        if sendEmail.send():
            # print('mail sent successfully')
            # request.session['newUserId'] = user.id
            # current_time = timezone.now()
            # request.session['otp_timestamp'] = current_time.timestamp()
            return True
        
        else:
            # print('')
            logger.error(f"{datetime.now()} :something went wrong while  sending email")
            return False



def sendtestmail(request):
    if sendMailTest():
        return JsonResponse({
            'success':'Mail sent successfully'
        })
        
    else:
         return JsonResponse({
            'error':'Something went wrong'
        })