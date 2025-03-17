from celery import Celery
# from celery import task
from celery import shared_task

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
from dateutil import parser
from django.utils import timezone


from datetime import datetime,timedelta,timezone
import requests
 
from django.utils.timezone import make_aware
from django.utils import timezone

# import os
# import logging

import os
import logging

logger = logging.getLogger(__name__)

celery = Celery('tasks')

# celery = Celery('tasks', broker='redis://localhost:6379/0')
# @login_required   
# @user_passes_test(is_admin) 



# @celery.task
# def ppppk():
#     print(1)
#     return 1

# @celery.task

# def distributeROI(ROIid):
              
#                 rt=ROIRates.objects.get(id=ROIid)
#                 # print(rt)
#                 isROIDistributed=ROIDailyCustomer.objects.filter(roi_date=rt.set_date)
                
#                 if isROIDistributed.count()>0:
#                     return

#                 allObjs=InvestmentWallet.objects.all() 
#                 # return
#                 try:
#                     #   for rt in allrates:
#                     for obj in allObjs:
#                         # if obj.txn_by_id='FB11857'
#                         dt = parser.parse(str(obj.txn_date))
        
#                         dtDate = dt.date() + timedelta(days=2)

#                         rat = parser.parse(str(rt.set_date))
#                         rtDate = rat.date()
                    
                    
#                         if dtDate<=rtDate:
                          
#                             # print(obj.id)
#                             roiEnts=ROIDailyCustomer.objects.filter(userid=obj.txn_by.memberid,investment_id=obj.id).count()
#                             # print(roiEnts)
#                             datROI=float(obj.amount)*(float(rt.rate)/float(100))
#                             roi_dates=datetime.now()-timedelta(days=1)
#                             newobjs=ROIDailyCustomer(userid=obj.txn_by,remark=f'roi at prcent {rt.rate}',total_sbg=obj.amount,roi_sbg=datROI,roi_date=roi_dates,status=1,daily_amount=datROI,roi_days=roiEnts+1,investment_id=obj)
#                             newobjs.save()
                            

                            
#                 except Exception as e:
#                     # print(str(e))
#                     # logger.error(f"{datetime.now()} :An error occurred: %s", str(e))
#                     print(e)
#                     # print(e)
                    
#                     return False    

#                 return True


# @celery.task
# def distributeReturn():
    
#     # print(datetime.now().date())
#     current_date = datetime.now().date()

#     # Calculate one day before
#     one_day_before = current_date - timedelta(days=1)
#     rt=ROIRates.objects.filter(set_date__date=one_day_before)
#     if rt.count()>0:
#         rt=rt.first()
#         isROIDistributed=ROIDailyCustomer.objects.filter(roi_date=rt.set_date)
                    
#         if isROIDistributed.count()>0:
#             return
#     else:
        
#         if datetime.now().weekday()==5 or datetime.now().weekday()==6:
#             # result['success']=0
#             # result['message']=f'You cannot distribute ROI for saturday and sunday'
#             return
#         rtPrev=ROIRates.objects.order_by('-id').first()
#         todaysdate = datetime.now()
#         yesterdaysdate = todaysdate - timedelta(days=1)
#         rt=ROIRates(set_date=yesterdaysdate,rate=rtPrev.rate)
#         rt.save()
        
    
#     distributeROI(rt.id)
#     # allObjs=InvestmentWallet.objects.all() 
    

# @shared_task
# def distribute_roi():
#     # Check if today is Saturday (5) or Sunday (6)
#     # today = datetime.today().weekday()
#     # if today in [5, 6]:
#     #     return "Today is a weekend. No ROI distributed."

#     # # Your logic for distributing $1 ROI
#     # # Assuming you have a ROI model to log the distribution
#     # roi_distribution = ROI(amount=1.0, distributed_at=make_aware(datetime.now()))
#     # roi_distribution.save()

#     # return "Distributed $1 ROI"
    
#     print("Hello")
    


# def activateMining():
    
#     chckDate=datetime.now().date()- timedelta(days=2)
#     allUsers=InvestmentWallet.objects.filter(joindate__date=chckDate)
    
#     for user in allUsers:
        
#         user.is_mining_activated=True
        
#         # if 
#         if sendEMail(user,user.email,subject='Activation Request for Mining Machine',template='newMemPanel/emailtemps/machineActivationRequest.html',context={'activatedmachineName':activatedMachineName},whatFor='activationRequest'):
            
#             ...

        
# def sendEMail(userObj,email,subject='',template='',context={}):
    

#     if userObj.first_name:
#         context['name']=userObj.first_name
#     else:
#         context['username']=userObj.username
        
            
#     html_content = render_to_string(template, context)
#     # print(html_content)
    

#     with get_connection(  
                        
#         host=settings.EMAIL_HOST, 
#         port=settings.EMAIL_PORT,  
#         username=settings.EMAIL_HOST_USER, 
#         password=settings.EMAIL_HOST_PASSWORD, 
#         use_tls=settings.EMAIL_USE_TLS  
#         ) as connection:  
#             subject = str(subject) 
#             email_from = "noreply@shifra.in" 
#             recipient_list = [email] 
#             # message ="This is testing email" 
#             body=html_content 
#             sendEmail=EmailMessage(subject, body, email_from, recipient_list, connection=connection).send()
            
#             if sendEmail:
#                 return True
#             else:
#                 return False

#             # if sendEmail:
                
#             #     if whatFor=='LicenseNum':

#             #         # request.session['RandomLicNumber'] = RandomLicenseNumber
#             #         request.session['licenseNum'] = {
#             #             # 'value':RandomLicenseNumber,
#             #             'timestamp': timezone.now().timestamp(),
#             #             'machineName': context['machineName']
#             #         }
#             #         # print()
                
#             #     return True
            
#             # else:
#             #     # print('')
#             #     logger.error(f"{datetime.now()} :something went wrong while  sending email")
#             #     return False

     
# def distributeDirectIncome():
#     ...

    
# @celery.task

    # should be a scheduled task
    # def distributeMining(request):
        

    #     ROIObj=ROIRates.objects.order_by('-id').first()

    #     currentRate=ROIObj.rate
    #     set_date=ROIObj.set_date
    #     result={}
        
        # if request.method=='POST':
        #     entRate=request.POST.get('rate')
        #     setDate=request.POST.get('setDate')
        #     datetime_obj = datetime.strptime(setDate, "%Y-%m-%dT%H:%M")

        #     if datetime_obj.weekday()==5 or datetime_obj.weekday()==6:
        #         result['success']=0
        #         result['message']=f'You cannot distribute ROI for saturday and sunday'
        #         return JsonResponse(result)
            
            # return
            
            # user_date = datetime.strptime(setDate[:10], "%Y-%m-%d")
            # ROIObj = ROIRates.objects.filter(set_date__date=user_date)
            

        #     if ROIObj.count()>0:
        #         # print('came for ROIObj')
        #         isROIDistributed=ROIDailyCustomer.objects.filter(roi_date=user_date)
        #         if isROIDistributed.count()>0:

        #             result['success']=0
        #             result['message']=f'ROI Already Distributed for date {setDate}'
        #             return JsonResponse(result)
                    
        #         else:
        #             # print("came here")
        #             ROIObjt=ROIRates.objects.get(set_date__date=user_date)
        #             # print(ROIObjt.id)

        #             distResult=distributeROI(ROIObjt.id)
        #             # print(distResult)
        #             if distResult:
        #                 result['success']=1
        #                 result['message']=f'ROI  Distributed for the date {setDate}'
                
        #                 return JsonResponse(result)
        #             else:
        #                 result['success']=0
        #                 result['message']=f'Something went wrong'
                
        #                 return JsonResponse(result)
                        

        #     else:
        #         # print("came here")
        #         try:
        #             NewROIObj=ROIRates(rate=float(entRate),set_date=setDate)
        #             NewROIObj.save()
        
        #             distResult=distributeROI(NewROIObj.id)
        
        #             if distResult:
        #                 result['success']=1
        #                 result['message']=f'ROI  Distributed for the date {setDate}'
            
        #                 return JsonResponse(result)
        #             else:
        #                 result['success']=0
        #                 result['message']=f'Something went wrong'
                
        #                 return JsonResponse(result)
                    
        #         except Exception as e:
                    
        #             result['success']=0
        #             result['message']=f'Some error occured from our sid while setting rates'
        #             logger.error(f"{datetime.now()} :An error occurred: %s", str(e))
        #             # print(e)
                
        #             return JsonResponse(result)
                
            
    
    
    # allRates=ROIRates.objects.order_by('-set_date')
        
        # return render(request,'zqAdmin/admin/distributeMining.html',context={
        #     'currentRate':currentRate,
        # #     'setDate':set_date,
        # #     'allRates':enumerate(allRates)
        # })



# @celery.task
# def calculateROI():
    
#         with transaction.atomic():


#             with connection.cursor() as cursor:
                
                
                
#                 try:
                
#                     res=cursor.callproc('roi_daily_customers', [datetime.now()])
                
#                     if res:
                        
#                         print('Procedure executed successsfully')
                    
                    
#                 except Exception as e:
                    
#                     print(e)
                    
#                     print('some error occured')
                    



@shared_task
def send_payment(jobId):
    # allAssignedJobsToUsers = AssignedSocialJob.objects.all()
    assignedJob = AssignedSocialJob.objects.get(id=jobId)
    # Implement your payment logic here
    
    # for asj in allAssignedJobsToUsers:
    
    try:
        prepaidSocialMediaBonus.objects.create(assigned_task_id=assignedJob,memberid=assignedJob.assigned_to,bonus=1,given_date=datetime.now())
    except Exception as e:
        print("spme error occured",str(e))    
    
    # print(f"Sending $1 to {user.email}")
    

@shared_task
def schedule_payments():
    today = timezone.now()
    if today.weekday() < 5:  # Only run on weekdays
        socialjobs = AssignedSocialJob.objects.filter(status=0)
        for sj in socialjobs:
            # Calculate the next payment time
            next_payment_time = sj.valid_from + datetime.timedelta(days=1)
            if today >= next_payment_time:
                send_payment.delay(sj.id)
