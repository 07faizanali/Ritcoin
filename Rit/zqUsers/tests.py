from django.test import TestCase
# from celery import Celery
# from celery import task
from django.db import connection,transaction
# from datetime import datetime
# from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404,reverse
from datetime import datetime,timedelta,timezone
import random
from zqUsers.models import *
from wallet.models import *
# Create your views here.
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.hashers import make_password
from django.db.models import Sum,F,Q, ExpressionWrapper, DecimalField,Value, OuterRef, Subquery
from django.db import connection
from django.core.mail import EmailMessage,get_connection
from django.conf import settings
from django.template.loader import render_to_string

# from django.shortcuts import redirect
# from django.contrib.auth import login
# from .models import ZqUser
# import pytz
# from django.utils import timezone
# from dateutil import parser
# from django.utils import timezone


from datetime import datetime,timedelta,timezone
import requests
 
from django.utils.timezone import make_aware
from django.utils import timezone
# Create your tests here.
# from datetime import datetime

# print(datetime.now().date())



    
# rt=ROIRates.objects.filter(set_date__date=datetime.now().date())

# print(datetime.now().weekday())
    


