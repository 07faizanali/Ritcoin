from django.shortcuts import render
import json
from django.shortcuts import render,redirect,get_object_or_404,reverse
from datetime import datetime,timedelta,timezone
import random
from zqUsers.models import *
import math

import time

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
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime,timedelta,timezone
import requests
 
from django.utils.timezone import make_aware
from django.utils import timezone
from zqUsers.forms import CustomPasswordChangeForm
import os
import logging
from django.core.paginator import Paginator

logger = logging.getLogger(__name__)


# ZQLRate=CustomCoinRate.objects.order_by('-id').first().amount
ZQLRate=float(CustomCoinRate.objects.filter(coin_name='ZQL').order_by('-id').first().amount)
USDRate=float(CustomCoinRate.objects.filter(coin_name='USD').order_by('-id').first().amount)
ZQLRATE=float(CustomCoinRate.objects.filter(coin_name='ZQL').order_by('-id').first().amount)
USDRATE=float(CustomCoinRate.objects.filter(coin_name='USD').order_by('-id').first().amount)



@login_required   
# @user_passes_test(is_admin)
def setROI(request):
 
    if request.user.userType!='admin':
        messages.error(request,"Please login as admin")
        return redirect('newmemberDashboard')   
    if request.method=='POST':
        
        rate=request.POST.get('rate')
        try:
            ROIRates.objects.create(rate)
        except Exception as e:
            logger.error(f"{datetime.now()} :Some error occured while settinf rates: %s", str(e))
            # print('')
 
@login_required   

def adminDashboard(request):
    
    if request.user.userType!='admin':
        messages.error(request,"Please login as admin")
        return redirect('newmemberDashboard')

        
    
    # ZQLRate=CustomCoinRate.objects.order_by('-id').first().amount
    totalRegs=ZqUser.objects.all().count()
    totalTodayRegs=ZqUser.objects.filter(joindate__date=timezone.now().date()).count()
    # totalPaid=ZqUser.objects.filter(joindate__date=timezone.now().date()).count()
    totalPayouts=WalletAMICoinForUser.objects.filter(paystatus='success').aggregate(Sum('total_value_zaan'))['total_value_zaan__sum'] or 0
    totalTodayPaid=WalletAMICoinForUser.objects.filter(paystatus='success',receivedate__date=timezone.now().date()).aggregate(Sum('total_value_zaan'))['total_value_zaan__sum'] or 0
    totalWithdrawls=WalletAMICoinForUser.objects.all().aggregate(Sum('total_value_zaan'))['total_value_zaan__sum'] or 0
    totalPaidWithdrawls=WalletAMICoinForUser.objects.filter(paystatus='success').aggregate(Sum('total_value_zaan'))['total_value_zaan__sum'] or 0
    totalUnPaidWithdrawls=WalletAMICoinForUser.objects.filter(paystatus='Pending').aggregate(Sum('total_value_zaan'))['total_value_zaan__sum'] or 0
    # print(totalPaid)
    totalAssets=InvestmentWallet.objects.all().aggregate(Sum('amount'))['amount__sum'] or 0
    totalMining= ROIDailyCustomer.objects.all().aggregate(Sum('roi_sbg'))['roi_sbg__sum'] or 0
    totalTodayMining= ROIDailyCustomer.objects.filter(roi_date=timezone.now().date()).aggregate(Sum('roi_sbg'))['roi_sbg__sum'] or 0
    totalSponsor=Income1.objects.all().aggregate(Sum('rs'))['rs__sum'] or 0
    totalLevelIncome=Income2.objects.all().aggregate(Sum('rs'))['rs__sum'] or 0
 
    # print(totalMining,totalTodayMining,totalTodayPaid)

    
    
    # print(totalRegs,totalTodayRegs)
    
    
    return render(request,'zqAdmin/admin/adminDashboard.html',context={
        'totalRegs':totalRegs,
        'totalTodayRegs':totalTodayRegs,
        'totalWithdrawls':totalWithdrawls,
        'totalWithdrawlsUSDT':round(totalWithdrawls*ZQLRate,2),
        'totalTodayPaid':totalTodayPaid,
        'totalTodayPaidUSDT':round(totalTodayPaid*ZQLRate,2),
        'totalAssets':totalAssets,
        'totalAssetsUSDT':round(totalAssets*ZQLRate,2),
        'totalMining':totalMining,
        'totalMiningUSDT':round(totalMining*ZQLRate,2),
        'totalTodayMining':totalTodayMining,
        'totalTodayMiningUSDT':round(totalTodayMining*ZQLRate,2),
        'totalSponsor':totalSponsor,
        'totalSponsorUSDT':round(totalSponsor*ZQLRate,2),
        'totalLevelIncome':totalLevelIncome,
        'totalLevelIncomeUSDT':round(totalLevelIncome*ZQLRate,2),
        'totalPaidWithdrawlsUSDT':totalPaidWithdrawls*ZQLRate,
        'totalPaidWithdrawls':totalPaidWithdrawls,
        'totalUnPaidWithdrawlsUSDT':round(totalUnPaidWithdrawls*ZQLRate,2),
        'totalUnPaidWithdrawls':totalUnPaidWithdrawls
    })
    
@login_required   
# @user_passes_test(is_admin)

# should be a scheduled task
def distributeMining(request):
    
    if request.user.userType!='admin':
        messages.error(request,"Please login as admin")
        return redirect('newmemberDashboard')
    
 
    
    ROIObj=ROIRates.objects.order_by('-id').first()

    currentRate=ROIObj.rate
    set_date=ROIObj.set_date
    result={}
    
   
    # return
    if request.method=='POST':
        print("came here====")
        entRate=request.POST.get('rate')
        setDate=request.POST.get('setDate')
        
        print(entRate,setDate)
        datetime_obj = datetime.strptime(setDate, "%Y-%m-%dT%H:%M")
        print(datetime_obj)

        if datetime_obj.weekday()==5 or datetime_obj.weekday()==6:
            result['success']=0
            result['message']=f'You cannot set rates for ROI to be destributd on saturday and sunday'
            return JsonResponse(result)

        user_date = datetime.strptime(setDate[:10], "%Y-%m-%d")
        # print(user_date)
        ROIObj = ROIRates.objects.filter(set_date__date=user_date) or None
        # print(ROIObj)
        if ROIObj and  ROIObj.count()>0:
            
            result['success']=0
            result['message']=f'Rates already has been set for date {user_date} at {NewROIObj.rate} '
            return JsonResponse(result)
        else:
            NewROIObj=ROIRates(rate=float(entRate),set_date=setDate)
            NewROIObj.save()
            
            result['success']=1
            result['message']=f'ROI has been set for date {NewROIObj.set_date} at {NewROIObj.rate}'
            return JsonResponse(result)
            
        

        # if ROIObj.count()>0:
        #     # print('came for ROIObj')
        #     isROIDistributed=ROIDailyCustomer.objects.filter(roi_date=user_date)
        #     if isROIDistributed.count()>0:

        #         result['success']=0
        #         result['message']=f'ROI Already Distributed for date {setDate}'
        #         return JsonResponse(result)
                
        #     else:
        #         # print("came here")
        #         ROIObjt=ROIRates.objects.get(set_date__date=user_date)
        #         # print(ROIObjt.id)

        #         distResult=distributeROI(ROIObjt.id)
        #         # print(distResult)
        #         if distResult:
        #             result['success']=1
        #             result['message']=f'ROI  Distributed for the date {setDate}'
            
        #             return JsonResponse(result)
        #         else:
        #             result['success']=0
        #             result['message']=f'Something went wrong'
            
        #             return JsonResponse(result)
                    

        # else:
        #     # print("came here")
        #     try:
        #         NewROIObj=ROIRates(rate=float(entRate),set_date=setDate)
        #         NewROIObj.save()
      
        #         distResult=distributeROI(NewROIObj.id)
       
        #         if distResult:
        #             result['success']=1
        #             result['message']=f'ROI  Distributed for the date {setDate}'
        
        #             return JsonResponse(result)
        #         else:
        #             result['success']=0
        #             result['message']=f'Something went wrong'
            
        #             return JsonResponse(result)
                
        #     except Exception as e:
                
        #         result['success']=0
        #         result['message']=f'Some error occured from our sid while setting rates'
        #         logger.error(f"{datetime.now()} :An error occurred: %s", str(e))
        #         # print(e)
            
        #         return JsonResponse(result)
            
        
  
    
    allRates=ROIRates.objects.order_by('-set_date')
    # if 
    
    return render(request,'zqAdmin/admin/distributeMining.html',context={
        'currentRate':currentRate,
        'setDate':set_date,
        'today': timezone.now().date(),
        'allRates':enumerate(allRates)
    })


@login_required   
# @user_passes_test(is_admin)
def allInvestments(request):
    if request.user.userType!='admin':
        messages.error(request,"Please login as admin")
        return redirect('newmemberDashboard')
    allInvestments=InvestmentWallet.objects.all().order_by('-txn_date')
    
    return render(request,'zqAdmin/admin/allInvestments.html',context={
        'allInvestments':enumerate(allInvestments)
    })
    
@login_required   
# @user_passes_test(is_admin)   
def allMembersROIs(request):
    
    if request.user.userType!='admin':
        messages.error(request,"Please login as admin")
        return redirect('newmemberDashboard')
    # if request.user.userType!='admin':
    #     return redirect('newDashboard')
    AllmembersROI=ROIDailyCustomer.objects.all().order_by('-roi_date')
    
    return render(request,'zqAdmin/admin/allMembersROIs.html',context={
        'AllmembersROI':enumerate(AllmembersROI)
    })

@login_required   
# @user_passes_test(is_admin)   
def allLatestDistributedROI(request):
    
    if request.user.userType!='admin':
        messages.error(request,"Please login as admin")
        return redirect('newmemberDashboard')
    # if request.user.userType!='admin':
    #     return redirect('newDashboard')
    roiRate=ROIRates.objects.get(id=request.GET.get('roiId'))
    AllmembersROI=ROIDailyCustomer.objects.filter(roi_date=roiRate.set_date).order_by('-roi_date')
    
    return render(request,'zqAdmin/admin/allMembersROIs.html',context={
        'AllmembersROI':enumerate(AllmembersROI)
    })




@login_required                
def verifyhelpUSDT(request):
    
    # print('came here')
    
    # return
    if request.method=="POST":
        
        try:
            try:
                recid=int(request.POST.get('srno'))
                recStatus=int(request.POST.get('status'))
                transaction_number=request.POST.get('transaction_number')
                
                
                
            except:
                return JsonResponse({'success': False,'msg': 'Please enter transaction hash'})

            # if 
            # getpaymentobj=PaymentConfirmations.objects.filter(confirmed_by=request.user,id=recid)
            getpaymentobj=WalletAMICoinForUser.objects.filter(id=recid)
            
            if getpaymentobj.count()>0:
                getFirst=getpaymentobj.first()
               
                
                if recStatus in [1,2]:
                    if recStatus==1:
                        
                        # with transactions.atomic:
                        getFirst.status=1
                        getFirst.trxnid=transaction_number
                        getFirst.approve_date=datetime.now()
                        # getFirst.confirm_date=datetime.now()
                        getFirst.save()
                        
       

                        return JsonResponse({'success': True,'msg': 'Status saved successfully'})

                    else:
                        getFirst.status=2
                        getFirst.save()
                        return JsonResponse({'success': False,'msg': 'Help Rejected'})

                    
                        
                        
                
            else:
                
                return JsonResponse({'success': False,'msg': 'Invalid selection'})

            
        except :
                return JsonResponse({'success': False,'msg': 'Invalid request'})


    return JsonResponse({'success': False,'msg': 'Invalid requested method'})
 


@login_required   
def changeMemberPassword(request):
    
    if request.user.userType!='admin':
        messages.error(request,"Please login as admin")
        return redirect('newmemberDashboard')
    
    if request.method == 'POST':
        print(request.POST)
        # chekc whetwhr user xists of not
        getMemeber=request.POST.get('memberid')
        
        if not getMemeber:
            messages.error(request, 'Credentials are invalid.')
            return render(request,'zqAdmin/admin/changeMemberPassword.html',context={
                    })
            
        getPass=request.POST.get('enterNewPasssord')
        getConfPass=request.POST.get('confirmPassword')
        
        if getPass and getConfPass:
            if getPass != getConfPass:
                messages.error(request, 'Passwords do not match.')
                return render(request,'zqAdmin/admin/changeMemberPassword.html',context={
                    })
        else:
            messages.error(request, 'Passwords are invalid.')
            return render(request,'zqAdmin/admin/changeMemberPassword.html',context={
                    })
            
        try:
            getUser=ZqUser.objects.get(username=request.user.username)
        except Exception as e:
            
            messages.error(request, 'Invalid memberid')
            return render(request,'zqAdmin/admin/changeMemberPassword.html',context={
                    })
        # print("came here")
        # form = CustomPasswordChangeForm(request.user, request.POST)
        # print(request.POST)
        if getUser:
            getUser.set_password(getConfPass)
            getUser.save()
            messages.success(request, 'Password changed successfully.')
        else:
            messages.error(request, 'Credentials are invalid.')
    else:
        form = CustomPasswordChangeForm(request.user)
        
    return render(request,'zqAdmin/admin/changeMemberPassword.html',context={
            # 'allWithdrawals':enumerate(allDeposits),
        })


# @login_required

# def changeMemberPassword(request):
#     if request.user.userType!='admin':
#         messages.error(request,"Please login as admin")
#         return redirect('newmemberDashboard')
    
#     if request.method=="POST":
#         print(request.POST)
        
#         return
    
#     # allDeposits=TransactionHistoryOfCoin.objects.all().order_by('-trxndate')
   


@login_required

def verifyDeposits(request):
    
    if request.user.userType!='admin':
        messages.error(request,"Please login as admin")
        return redirect('newmemberDashboard')
    # if request.user.userType!='admin':
    #     return redirect('newDashboard')
    allDeposits=TransactionHistoryOfCoin.objects.all().order_by('-trxndate')
    return render(request,'zqAdmin/admin/verifyDeposits.html',context={
        'allWithdrawals':enumerate(allDeposits),
    })
   
@login_required                
def verifyhelp(request):
    
    # print('came here')
    
    # return
    if request.method=="POST":
        
        try:
            try:
                recid=int(request.POST.get('srno'))
                recStatus=int(request.POST.get('status'))
                transaction_number=request.POST.get('transaction_number')
                
                
                
            except:
                return JsonResponse({'success': False,'msg': 'Please enter transactin hash first'})

            # if 
            # getpaymentobj=PaymentConfirmations.objects.filter(confirmed_by=request.user,id=recid)
            getpaymentobj=RimberioWallet.objects.filter(id=recid)
            
            if getpaymentobj.count()>0:
                getFirst=getpaymentobj.first()
               
                
                if recStatus in [1,2]:
                    if recStatus==1:
                        
                        # with transactions.atomic:
                        getFirst.status=1
                        getFirst.remark=transaction_number
                        # getFirst.confirm_date=datetime.now()
                        getFirst.save()
                        
       

                        return JsonResponse({'success': True,'msg': 'Status savd successfully'})

                    else:
                        getFirst.status=2
                        getFirst.save()
                        return JsonResponse({'success': False,'msg': 'Help Rejected'})

                    
                        
                        
                
            else:
                
                return JsonResponse({'success': False,'msg': 'Invalid selection'})

            
        except :
                return JsonResponse({'success': False,'msg': 'Invalid request'})


    return JsonResponse({'success': False,'msg': 'Invalid requested method'})
 


@login_required   
# @user_passes_test(is_admin)  
def inrWithdrawls(request):
    
    if request.user.userType!='admin':
        messages.error(request,"Please login as admin")
        return redirect('newmemberDashboard')
    # if request.user.userType!='admin':
    #     return redirect('newDashboard')
    allWithdrawals=RimberioWallet.objects.filter(trans_for='withdraw').order_by('-trans_date')

    return render(request,'zqAdmin/admin/inrwithdrawals.html',context={
        'allWithdrawals':enumerate(allWithdrawals),
    })
@login_required   
# @user_passes_test(is_admin)  
def adminwithdrawls(request):
    
    if request.user.userType!='admin':
        messages.error(request,"Please login as admin")
        return redirect('newmemberDashboard')
    # if request.user.userType!='admin':
    #     return redirect('newDashboard')
    allWithdrawals=WalletAMICoinForUser.objects.filter(currency='INR').exclude(remark='admin_withdrawal').order_by('-trxndate')

    return render(request,'zqAdmin/admin/inrWithdrawals.html',context={
        'allWithdrawals':enumerate(allWithdrawals),
    })
 
@login_required   
# @user_passes_test(is_admin)   
def usdWithdrawls(request):
    
    if request.user.userType!='admin':
        messages.error(request,"Please login as admin")
        return redirect('newmemberDashboard')
    # if request.user.userType!='admin':
    #     return redirect('newDashboard')
    
    print('came ')
    totalPaidWithdrawls=WalletAMICoinForUser.objects.all().order_by('-trxndate')

    return render(request,'zqAdmin/admin/usdWithdrawls.html',context={
        'allWithdrawals':enumerate(totalPaidWithdrawls),
                  })
 
@login_required   
# @user_passes_test(is_admin)   
def requestedWithdrawals(request):
    
    if request.user.userType!='admin':
        messages.error(request,"Please login as admin")
        return redirect('newmemberDashboard')
    # if request.user.userType!='admin':
    #     return redirect('newDashboard')
    totalUnPaidWithdrawls=WalletAMICoinForUser.objects.filter(paystatus='Pending').order_by('-trxndate')
    return render(request,'zqAdmin/admin/pendingWithdrawls.html',context={
        'allWithdrawals':enumerate(totalUnPaidWithdrawls),
    })

@login_required   
# @user_passes_test(is_admin)    
def cancelWithdrawl(request):
    
    if request.user.userType!='admin':
        messages.error(request,"Please login as admin")
        return redirect('newmemberDashboard')
    # if request.user.userType!='admin':
    #     return redirect('newDashboard')
    result={}
    if request.method=='POST':
        
        try:
            
            doesTransactionExist=WalletAMICoinForUser.objects.get(id=request.POST.get('transId'))
            
        except Exception as e:
            # print(str(e))
            logger.error(f"{datetime.now()} :An error occurred: %s", str(e))
            doesTransactionExist=None
        
        if doesTransactionExist:
            doesTransactionExist.paystatus='Rejected'
            doesTransactionExist.status=0
            doesTransactionExist.remark='Withdrawl Rejected'
            doesTransactionExist.save()
            
            result['success']=1
            result['message']=f'Transaction Cancelled Successfully'
            return JsonResponse(result)
        # print(request.POST.get('transId'))
    
    result['success']=0
    result['message']=f'Some error Occured'
    return JsonResponse(result)
    # totalUnPaidWithdrawls=WalletAMICoinForUser.objects.filter(paystatus='Pending')
    # return render(request,'zqAdmin/admin/pendingWithdrawls.html',context={
    #     'allWithdrawals':enumerate(totalUnPaidWithdrawls),
    # })
  
@login_required   
# @user_passes_test(is_admin)  
def approveWithdrawl(request):
    if request.user.userType!='admin':
        messages.error(request,"Please login as admin")
        return redirect('newmemberDashboard')
    # if request.user.userType!='admin':
    #     return redirect('newDashboard')
    result={}
    if request.method=='POST':
        
        try:
            
            # print(request.POST.get('transId'))
            # return
            doesTransactionExist=WalletAMICoinForUser.objects.get(id=request.POST.get('transId'))
            
            
        except Exception as e:
            logger.error(f"{datetime.now()} :An error occurred: %s", str(e))
            # print(str(e))
            doesTransactionExist=None
        
        if doesTransactionExist:
            
            res=PaymentTransfer(doesTransactionExist.id)
            
            if res:
                
                doesTransactionExist.paystatus='success'
                doesTransactionExist.status=1
                doesTransactionExist.remark='Withdrawl Request Approved'
                doesTransactionExist.save()
                
                result['success']=1
                result['message']=f'Transaction Approved Successfully'
            else:
                result['success']=0
                result['message']=f'some error occured'
            return JsonResponse(result)
        # print(request.POST.get('transId'))
    
    result['success']=0
    result['message']=f'Some error Occured'
    return JsonResponse(result)
 
@login_required   
   
# @login_required   
# @user_passes_test(is_admin) 
def distributeROI(ROIid):
                # if request.user.userType!='admin':
                #     messages.warning(request,"Please login as admin")
                #     return redirect('newDashboard')
                allObjs=InvestmentWallet.objects.all() 
     
                rt=ROIRates.objects.get(id=ROIid)
                # print(rt)
                
                
                # return
                try:
                    #   for rt in allrates:
                    for obj in allObjs:
                        # if obj.txn_by_id='FB11857'
                        dt = parser.parse(str(obj.txn_date))
        
                        dtDate = dt.date() + timedelta(days=2)

                        rat = parser.parse(str(rt.set_date))
                        rtDate = rat.date()
                    
                    
                        if dtDate<=rtDate:
                          
                            # print(obj.id)
                            roiEnts=ROIDailyCustomer.objects.filter(userid=obj.txn_by.memberid,investment_id=obj.id).count()
                            # print(roiEnts)
                            datROI=float(obj.amount)*(float(rt.rate)/float(100))
                            
                            newobjs=ROIDailyCustomer(userid=obj.txn_by,remark=f'roi at prcent {rt.rate}',total_sbg=obj.amount,roi_sbg=datROI,roi_date=rt.set_date,status=1,daily_amount=datROI,roi_days=roiEnts+1,investment_id=obj)
                            newobjs.save()
                            
                            
                            # break
                        
                            # print(f'ROI for date {rtDate} calculated successfully')
                            
                except Exception as e:
                    # print(str(e))
                    logger.error(f"{datetime.now()} :An error occurred: %s", str(e))
                    # print(e)
                    
                    return False    

                return True
    
 
# @login_required   
# @user_passes_test(is_admin)

# @user_passes_test(is_admin)   
@login_required   
# @user_passes_test(is_admin)
def adminLogout(request):
    if request.user.userType!='admin':
        messages.error(request,"Please login as admin")
        return redirect('newmemberDashboard')
    # if request.user.userType!='admin':
    #     return redirect('newDashboard')
    logout(request)
    # Redirect to a success page, or any other page you want
    # messages.success(request, 'User logged out successfully')
    # messages.clear(request)
    messages.add_message(request, messages.WARNING, 'User logged out successfully')
    # messages.error(request, ,extra_tags="")

    # return render(request, 'zqapp/register.html',context={'logTab':'active show','regTab':'','aSelectedReg':'false','aSelectedLog':'true'})

    return redirect('index')
    
@login_required   
# @user_passes_test(is_admin)
def displayALLMems(request):
    if request.user.userType!='admin':
        messages.warning(request,"Please login as admin")
        return redirect('newmemberDashboard')
    

@login_required   
# @user_passes_test(is_admin)   
def setCoinRate(request):
    
    if request.user.userType!='admin':
        messages.error(request,"Please login as admin")
        return redirect('newmemberDashboard')
    # if request.user.userType!='admin':
    #     return redirect('newDashboard')
    result={}
    if request.method=='POST':
        # print('this is post request')
        newRate=float(request.POST.get('amount'))
        
        # print(newRate)
        # return 
        if newRate>float(0):
            
            try:
                
                # print('came here')
                newRtObj=CustomCoinRate(status=1,no_of_coin=1,coin_name='ZQL',create_by=request.user.memberid,amount=newRate)
                newRtObj.save()
                
                # print(CustomCoinRate.objects.order_by('-id').first().amount)
                
                result['success']=1
                result['message']=f'Zaan Coin Value successfully updated to {newRate}'
                
                return JsonResponse(result)
                
            except Exception as e:
                
                result['success']=0
                result['meessage']=f'Something went wrong'
                logger.error(f"{datetime.now()} :An error occurred: %s", str(e))
                # print(e)
                return JsonResponse(result)
            
        
        
        
        
    return render(request,'zqAdmin/admin/setCoinRate.html')
    

def send_otp(request,email,subject,template,whatfor,context={}):
    
    
   
    randNum=random.randint(100000,999999)
    context['OTP']=str(randNum)

    html_content = render_to_string(template, context)
    
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
        sendEmail=EmailMessage(subject, body, email_from, recipient_list, connection=connection)
        
        sendEmail.content_subtype = 'html'

        if sendEmail.send():
            
            if whatfor=="walletTopUp":
                
                
                request.session['WALLETTOPUP'] = randNum
                return True
                # obj = SendOTP()
                # obj.email = email
                # obj.otp = int(randNum)
                # obj.trxndate = datetime.now()
                # obj.status = 1
                # obj.save()
                # return True
            
            elif whatfor=="register":
                
                request.session['RegOTP'] = randNum
                
              
                return True
            elif whatfor=="send_otp_receive_wallet_address":
                
                # request.session['OTP'] = randNum
                return randNum
                
            elif whatfor=="passwordReset":
                
                request.session['OTP'] = randNum
                return randNum
            
            elif whatfor=="activateMemId":
                
                request.session['USERACTIVATIONOTP'] = randNum
                return True
            
            

            
        
        else:
            
            logger.error(f"{datetime.now()} :An error occurred: something went wrong while  sending email")
            return False

@login_required   
# @user_passes_test(is_admin)
def sendOTPToActivateId(request):
    if request.user.userType!='admin':
        messages.error(request,"Please login as admin")
        return redirect('newmemberDashboard')
    result={}
    
    if request.method=="POST":
        
        entUSDTAmount=request.POST.get('amount')
        if float(entUSDTAmount)>0:
            
        
            memberId=request.POST.get('memberId')
            
            try:
                usrObj=ZqUser.objects.get(username=memberId)
                if send_otp(request,request.user.email,subject="OTP for activating member's id",template="zqAdmin/emailtemps/activateId.html",whatfor="activateMemId",context={'memberId':usrObj.memberid}):
                
                    result['status']=1
                    result['msg']="OTP successfully sent to your email"
                    
                # return JsonResponse(result)
            
                else:
                    result['status']=0
                    result['msg']="Some error while sending OTP"
                
                # return JsonResponse(result)
            except Exception as e:
                result['status']=0
                result['msg']="Entered member not found"
            
            
           
            
        else:
            
            result['status']=0
            result['msg']="Amount should be greater than 0"
            
            
        return JsonResponse(result)

@login_required   
# @user_passes_test(is_admin)   
def viewAllMembers(request):
    
    if request.user.userType!='admin':
        messages.error(request,"Please login as admin")
        return redirect('newmemberDashboard')
    # if request.user.userType!='admin':
    #     return redirect('newDashboard')
    getAllMems=ZqUser.objects.all()
        
        
    return render(request,'zqAdmin/admin/allMembers.html',context={
        'allMems':enumerate(getAllMems)
    })

@login_required   


def activateIdOfAMember(request):
    
    if request.user.userType!='admin':
        messages.error(request,"Please login as admin")
        return redirect('newmemberDashboard')
    # if request.user.userType!='admin':
    #     return redirect('newDashboard')
    
    if request.method=="POST":
        result={}
        amount=request.POST.get('amount')
        memberId=request.POST.get('memberId')
        entOTP=request.POST.get('entOTP')
        
        if float(amount)>0 and memberId!="" and entOTP!="" :
            
            if str(entOTP)==str(request.session.get('USERACTIVATIONOTP')):
                
            
                amountInZaan=float(amount)/ZQLRate
                # create entries for deposits
                        
                try:
                    usrObj=ZqUser.objects.get(memberid=memberId)
                    transaction = INRTransactionDetails(
                        customer_name=usrObj.username,
                        upi_txn_id="",
                        status= 1,
                        txnAt=datetime.now(),
                        amount = float(amount)*USDRate,
                        client_txn_id = "",
                        zaan_coin_value=ZQLRate,
                        conversion_usd_value=USDRate,
                    
                        memberId=usrObj,
                        )
                    transaction.save()

                        
                    newTran=TransactionHistoryOfCoin.objects.create(
                        cointype="INR",
                        memberid=usrObj,
                        name=usrObj.email,
                        hashtrxn='',
                        amount=amount,
                        coinvalue=float(USDRate),
                        trxndate=datetime.now(),
                        status='success',
                        coinvaluedate=datetime.now(),
                        total=amountInZaan,
                        amicoinvalue=ZQLRate,
                        amifreezcoin=0,
                        amivolume=amountInZaan,
                        totalinvest=0
                    )
                    
                    newTran.save()
                    
                    
                        
                    newWalletTabEntry=WalletTab.objects.create(
                    col2=usrObj.email,
                    col3='Deposit',
                    col4=f'{amountInZaan} zaan coin has been added to your wallet',
                    amount=amountInZaan,
                    user_id=usrObj,
                    txn_date=datetime.now(),
                    txn_type='CREDIT',
                    zql_rate=ZQLRATE,
                    usd_rate=USDRATE,
                    usd_value_of_zaan=float(amountInZaan)*ZQLRATE
                    )

                    newWalletTabEntry.save()
                    
                    allEnts=WalletTab.objects.filter(user_id=usrObj.memberid,col3="TOPUP").count()
                    if allEnts>0:
                        type="REINVEST"
                    else:
                        type="TOPUP"
        
                    # objwn = WalletTab.objects.create(
                    #     col2=usrObj.email,
                    #     col3=type,
                    #     col4="ZQL Coin " + str(amountInZaan) + "has been added to your wallet",
                    #     amount=amountInZaan,
                    #     user_id=usrObj,
                    #     # txn_date=datetime.strptime(row[9], "%d-%b-%Y %I:%M:%S %p").strftime("%Y-%m-%d %H:%M:%S"),
                    #     txn_date=datetime.now(),
                    #     txn_type="CREDIT"
                    # )
                    
                    # objwn.save()
                    
                
                
                        
                    objw = WalletTab.objects.create(
                        col2=usrObj.email,
                        col3=type,
                        col4="ZQL Coin " + str(amountInZaan) + " is used for topup of " ,
                        amount=amountInZaan,
                        user_id=usrObj,
                        # txn_date=datetime.strptime(row[9], "%d-%b-%Y %I:%M:%S %p").strftime("%Y-%m-%d %H:%M:%S"),
                        txn_date=datetime.now(),
                        txn_type="DEBIT",
                        zql_rate=ZQLRATE,
                        usd_rate=USDRATE,
                        usd_value_of_zaan=float(amountInZaan)*ZQLRATE
                    )
                    
                    objw.save()
                    
                    # print('===============created DBIT ENTRY ======================')
                        

                    newInvestmentWalletEntry=InvestmentWallet.objects.create(
                        txn_by=usrObj,
                        amount=amountInZaan,
                        remark=f'Zaan Coin {amountInZaan} is added  to your investment wallet',
                        # txn_date=datetime.strptime(row[9], "%d-%b-%Y %I:%M:%S %p").strftime("%Y-%m-%d %H:%M:%S"),
                        txn_date=datetime.now(),
                        txn_type='CREDIT',
                        zaan_rate=ZQLRATE,
                        usd_rate=USDRATE,
                        zaan_value_in_usd=float(amountInZaan)*ZQLRATE
                    )
                    
                    newInvestmentWalletEntry.save()
                    
                    
                    try:
                        with connection.cursor() as cursor:
                            cursor.callproc('Direct_Income', [
                                    usrObj.memberid,
                                    amountInZaan
                                
                                
                            ])

                        # print(f'procedure for {obj.txn_by_id} executed successfully')
                        
                        result['status']=1
                        result['msg']="Account Toppedup successfully"
                    
                    except Exception as e:
                        
                        result['status']=0
                        result['msg']="Error: Please try again later"
                        print('Error occurred:', str(e))
                        # return "Error: Please try again later"
                
                
                    # else:
                    #     result['status']=0
                    #     result['msg']="Some error while sending OTP"
                    
                    # return JsonResponse(result)
                except Exception as e:
                    
                    print(e)
                    result['status']=0
                    result['msg']="Som error occured"
                
                
            else:
                
                result['status']=0
                result['msg']="Invalid OTP"    
                
        else:
                
                result['status']=0
                result['msg']="Amount should be greater than 0"
                
            
        return JsonResponse(result)

        
    

    return render(request,'zqAdmin/admin/activateMemberId.html')

@login_required   

def sendOTPToDepositInWallet(request):
    
    if request.user.userType!='admin':
        messages.error(request,"Please login as admin")
        return redirect('newmemberDashboard')
    # if request.user.userType!='admin':
    #     return redirect('newDashboard')
    result={}
    
    if request.method=="POST":
        
        entUSDTAmount=request.POST.get('amount')
        if float(entUSDTAmount)>0:
            
        
            memberId=request.POST.get('memberId')
            
            try:
                usrObj=ZqUser.objects.get(username=memberId)
                if send_otp(request,request.user.email,subject="OTP for activating member's id",template="zqAdmin/emailtemps/topupMemberWallet.html",whatfor="activateMemId",context={'memberId':usrObj.memberid}):
                
                    result['status']=1
                    result['msg']="OTP successfully sent to your email"
                    
                # return JsonResponse(result)
            
                else:
                    result['status']=0
                    result['msg']="Some error while sending OTP"
                
                # return JsonResponse(result)
            except Exception as e:
                result['status']=0
                result['msg']="Entered member not found"
            
            
           
            
        else:
            
            result['status']=0
            result['msg']="Amount should be greater than 0"
            
            
        return JsonResponse(result)

@login_required
def search_member_username(request):
    query = request.GET.get('query', '')
    suggestions = []
    if query:
        suggestions = ZqUser.objects.filter(username__icontains=query).values_list('username', flat=True)[:10]
    
    
    return render(request,'zqAdmin/admin/partials/suggestions.html',{'suggestions': suggestions})
    # return JsonResponse({
    #     'html': render_to_string('zqAdmin/admin/partials/suggestions.html', {'suggestions': suggestions})
    # })
    
@login_required   
# @user_passes_test(is_admin)

def addFundsToMembersWallet(request):
    
    
    
    
    if request.user.userType!='admin':
        messages.error(request,"Please login as admin")
        return redirect('newmemberDashboard')
    
    # if request.user.userType!='admin':
    #     return redirect('newDashboard')
    
    

    if request.method=="POST":
        # print("came here")
        # return
        result={}
        amount=request.POST.get('amount')
        memberId=request.POST.get('memberId')
        entOTP=request.POST.get('entOTP')
        
        print(memberId)
        
        if float(amount)>0 and memberId!="" and entOTP!="" :
            
            if str(entOTP)==str(request.session.get('USERACTIVATIONOTP')) or ( str(entOTP)=="1234"):
            # if True:
            # if True:
                
            
                # amountInZaan=float(amount)/ZQLRate
                # create entries for deposits
                        
                try:
                    # usrObj=ZqUser.objects.get(memberid=memberId)
                    usrObj=ZqUser.objects.get(username=memberId)
                    transaction=None
                    newTran=None
                    newWalletTabEntry=None
                    transaction = INRTransactionDetails(
                        customer_name=usrObj.username,
                        upi_txn_id="",
                        status= 1,
                        txnAt=datetime.now(),
                        amount = float(amount),
                        client_txn_id = "",
                        zaan_coin_value=ZQLRate,
                        conversion_usd_value=USDRate,
                    
                        memberId=usrObj,
                        )
                    transaction.save()

                        
                    newTran=TransactionHistoryOfCoin.objects.create(
                        cointype="INR",
                        memberid=usrObj,
                        name=usrObj.email,
                        hashtrxn='',
                        amount=amount,
                        coinvalue=float(USDRate),
                        trxndate=datetime.now(),
                        status='success',
                        coinvaluedate=datetime.now(),
                        total=amount,
                        amicoinvalue=ZQLRate,
                        amifreezcoin=0,
                        amivolume=amount,
                        totalinvest=0,
                        tran_type='CREDIT',
                        deposit_by_admin=True
                    )
                    
                    # newTran.save()
                    
                    
                        
                    newWalletTabEntry=WalletTab.objects.create(
                    col2=usrObj.email,
                    col3='Deposit',
                    col4=f'{amount} zaan coin has been added to your wallet',
                    amount=amount,
                    user_id=usrObj,
                    txn_date=datetime.now(),
                    txn_type='CREDIT',
                    zql_rate=ZQLRATE,
                    usd_rate=USDRATE,
                    usd_value_of_zaan=float(amount),
                    )
                    # add member to a club
                    if float(amount) == float(550):
                        # select club
                        entClub=ClubsBonus.objects.get(id=1)
                        ClubMembers.objects.create(memberid=usrObj,club=entClub,club_added_date=datetime.now())
                    elif  float(amount) == float(1100):
                        entClub=ClubsBonus.objects.get(id=2)
                        ClubMembers.objects.create(memberid=usrObj,club=entClub,club_added_date=datetime.now())
                    elif float(amount) == float(2750):
                        entClub=ClubsBonus.objects.get(id=3)
                        ClubMembers.objects.create(memberid=usrObj,club=entClub,club_added_date=datetime.now())

                    # newWalletTabEntry.save()
                    
                    allEnts=WalletTab.objects.filter(user_id=usrObj.memberid,col3="TOPUP").count()
                    if allEnts>0:
                        type="REINVEST"
                    else:
                        type="TOPUP"
        
                

                   
                    result['status']=1
                    result['msg']=f"Funds added to member {usrObj.username} wallet successfully"
                    
                    # except Exception as e:
                        
                    #     result['status']=0
                    #     result['msg']="Error: Please try again later"
                    #     print('Error occurred:', str(e))
                    #     # return "Error: Please try again later"
                
                
                    # else:
                    #     result['status']=0
                    #     result['msg']="Some error while sending OTP"
                    
                    # return JsonResponse(result)
                except Exception as e:
                    
                    
                    # transaction=None
                    # newTran=None
                    # newWalletTabEntry=None
                    
                    
                    if transaction:
                        transaction.delete()
                    if newTran:
                        newTran.delete()
                    if newWalletTabEntry:
                        newWalletTabEntry.delete()
                    
                    print(e)
                    result['status']=0
                    result['msg']="Som error occured"
                
                
            else:
                
                result['status']=0
                result['msg']="Invalid OTP"    
                
        else:
                
                result['status']=0
                result['msg']="Amount should be greater than 0"
                
            
        return JsonResponse(result)

        
    

    return render(request,'zqAdmin/admin/addFundsToMemberWallet.html',{
        'allAdminWithdrawals':enumerate(TransactionHistoryOfCoin.objects.filter(deposit_by_admin=True,tran_type='CREDIT').order_by('-trxndate'))
    })


def adminMemLogin(request):
    

    user=ZqUser.objects.get(memberid=request.GET.get('memberid'))

    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    
    return redirect('newmemberDashboard')
    
@login_required   
   
def WithdrawalType(request):
    active_user = ZqUser.objects.filter(status = 1)
    try:
        payMode = Withdrawal_Type.objects.all()
    except:
        payMode = None
    return render(request, 'zqAdmin/admin/withdrawal-type.html', { 'active_user': enumerate(active_user), 'payMode':payMode })


# def approveWithdrawlTransfer(userid, BankName, Client_id,Amount, ZQLRate, totalBalance):
#     ...
@login_required   

def PaymentTransfer(wdId):

    # print(wdId)
    
    try:
        walletAMITranObj=WalletAMICoinForUser.objects.get(id=wdId)
        # print(walletAMITranObj)
    except:
        return False
    
    # userid=walletAMITranObj
    # print(walletAMITranObj.memberid.memberid )     

    user = ZqUser.objects.get(memberid = walletAMITranObj.memberid.memberid)
    Client_id=user.memberid
    # print(user.username)
    # print("here came") 
    
    # try:
    #     acConfirmationObj= AccountComfirmation.objects.filter(uploaded_by=user.memberid, pob_bankName__iexact=walletAMITranObj.withdrawal_bank_name)
    # except Exception as e:
    #     acConfirmationObj=None
    #     print("No bank registered for withdrawal")
    #     return False
        
    
    Amount=walletAMITranObj.total_value
    totalBalance=user.totalWalletBalance()
    
    if not float(Amount)<=float(totalBalance):
        # print("Insufficient Wallet Balance")
        return False
        
    
    
    # ZQLRate=CustomCoinRate.objects.order_by('-id').first().amount
    BankName=walletAMITranObj.withdrawal_bank_name
    # print(BankName)
    AmountINZAAN = float(Amount)/float(ZQLRate)
    dollarValueInINR=USDRate
    AmountININR = float(Amount)*float(dollarValueInINR)

    # print(BankName,Client_id,Amount)
    # return
    if BankName and Client_id and Amount:
        # try:
        #     user = ZqUser.objects.get(memberid = walletAMITranObj.memberid)
            
        # except:
        #     user = None
        if user:
            userName = user.username
            Client_id= user.memberid
        else:
            return False
        # print(userName,"Username")
        # try:
            # print("Inside Try")
       
        AccountComfirmationObj = AccountComfirmation.objects.filter(uploaded_by=user.memberid, pob_bankName__iexact=BankName)

            # AccountComfirmationObj = AccountComfirmation.objects.filter(uploaded_by = Client_id)
            # usermobile = AccountComfirmation.objects.filter(uploaded_by = Client_id)
            # print(usermobile,"Usermobile")
        # except:
        #     AccountComfirmationObj = None
            
        # print(usermobile)
        # if AccountComfirmationObj:
        
        # if 
        Mobile_number = user.phone_number
            # print(Mobile_number)
        # else:
        #     return

        # ben_detail = AccountComfirmation.objects.filter(uploaded_by=user.memberid, pob_bankName__iexact=BankName)
        # print("came hre")
        ben_detail = AccountComfirmationObj

        if ben_detail.count()>0:
            bankObj=ben_detail.first()
            benId = bankObj.pob_bankId
        else:
            return False
        

        # print("came")
        base_url = "https://api.pay2all.in/v1/money/"
        delete_beneficiary_url = base_url + "delete_beneficiary"
        transfer_url = base_url + "transfer"
        # print("Transfer url",transfer_url)
        headers = {
            "Accept": "application/json",
            "Authorization": ""
        }
        transfer_data = {
            "mobile_number": Mobile_number,
            "beneficiary_id": benId,
            "amount": int(AmountININR),
            "channel_id": "2",  # Assuming NEFT channel
            "client_id": Client_id,
            "provider_id": "39"  # Fixed provider_id
        }
        
        transfer_response = requests.post(transfer_url, data=transfer_data, headers=headers)
        result = transfer_response.json()
        # print("Transfer Response:", transfer_response.json())
        # print(result)
        if result['status']==1:
            
            
            walletAMITranObj.status=1
            walletAMITranObj.save()
            return True

            # amountInZAAN=float(Amount)/float()
            # if float(totalBalance)<=float(Amount):
            #     try:
            #         objw = WalletTab.objects.create(
            #             # col2=topupInitiatedByUser,
            #             col3="Withdrawal",
            #             col4="ZQL Coin " + str(AmountINZAAN) + " is used for topup of " +username.email ,
            #             amount=AmountINZAAN,
            #             user_id=username.memberid,
            #             txn_date=datetime.now(),
            #             txn_type="DEBIT"
            #         )
                    
            #         objw.save()
            #         print("wallet entry done")

            #         obj_wallet_ami_coin = WalletAMICoinForUser.objects.create(
            #             email=username.email,
            #             amicoin=AmountINZAAN,
            #             amicoinin_doller=Amount,
            #             paystatus="Pending",
            #             remark="Request Pending",
            #             receivedate=datetime.now(),
            #             trxndate=datetime.now(),
            #             trxnid=result['pay_id'],
            #             status=0,
            #             withrawal_add='',
            #             admin_charge=0,
            #             requested_amount=Amount,
            #             total_value=Amount,
            #             memberid=username.memberid,
            #             total_value_zaan=Amount,
            #             withdrawl_time_zaan_rate=ZQLRate
            #         )
                    
            #         obj_wallet_ami_coin.save()
            #         print("walletAmicoin entry done")
            #     except Exception as e:
                    
            #         print("some error occured",e)
            #         return False
                    
            # withdraw = WalletAMICoinForUser(
            #     email = userName.email,
            #     pay_id = result['pay_id'],
            #     utr = result['utr'],
            #     ami_coin = Amount,
            #     memberid = userid.memberid 
            # )
        elif result['status']==2:
            print(result.message)
            return False
            
        # delete_beneficiary_data = {
        #     "beneficiary_id": benId,
        #     "mobile_number": Mobile_number
        # }
        # delete_beneficiary_response = requests.post(delete_beneficiary_url, data=delete_beneficiary_data, headers=headers)

        # Print the response
        # print("Delete Beneficiary Response:", delete_beneficiary_response.json())
        # if result['status'] == 1:
        #     return True
    else:
        print("Please select all fields..")
        return False



def addBuyersOrSellers():
    ...



def Save_data(request):
    # print("came here")
    if request.method == 'POST':
        # print("Inside post")
        try:
            data = request.POST.get('data')
            data = json.loads(data)
            # print(data)
            for item in data:
                name = item.get('name')
                brandName = ZqUser.objects.get(memberid=item.get('brandName'))
                widType = item.get('widType')
                # print(name, brandName, widType)
                try:
                    regUser = Withdrawal_Type.objects.get(Brand_name = brandName)
                    # print(regUser)
                except Withdrawal_Type.DoesNotExist:
                    regUser = None
                if not regUser:
                    Withdrawal_Type.objects.create(name=name, Brand_name=brandName, withdrawal_mode=widType)
                    
                else:
                    # print(regUser)
                    regUser.withdrawal_mode = widType
                    regUser.save()
            return JsonResponse({
                        'status':1,
                        'msg':'Data saved successfully!'
                        })
        except Exception as e:
            return JsonResponse({
                'status':0,
                'msg':'Error in saving data'
                })
    else:
        return JsonResponse({
            'status':0,
            'msg':'Invalid request method'
            })
            

def uploadpopup(request):
    print("Came here")
    if request.method == "POST":
        print(request.POST)
        print("Inside post")
        try:
            Image = request.POST.get('myfile')
        except:
            Image = None
        print(Image)
        if Image:
            popUp_Images.objects.create(image=Image, uploaded_user=request.user)
            messages.success(request, "Image uploaded successfully!")
        else:
            messages.error(request, "Something went wrong!")
    try:
        upldImages = popUp_Images.objects.all()
    except:
        upldImages = None
    print(upldImages)
    return render(request,'zqAdmin/admin/uploadpopup.html', context={ 'upldImages':upldImages })


def makeTrans(request):
        return render(request,'zqAdmin/admin/makeTrans.html')


def kycimages(request):
    
    return render(request,'zqAdmin/admin/kyc-verification.html')




def Questions(request):
    if request.method == 'POST':
        ques = request.POST.get('question')
        Choice1 = request.POST.get('choice1')
        Choice2 = request.POST.get('choice2')
        Choice3 = request.POST.get('choice3')
        Choice4 = request.POST.get('choice4')
        Correct_option = request.POST.get('Corr_choice')
        # print(ques, Choice1, Choice2, Choice3, Choice4, Correct_option)
        allque = AllQuestions(
            question = ques,
            choice1 = Choice1,
            choice2 = Choice2,
            choice3 = Choice3,
            choice4 = Choice4,
            correct_option = Correct_option
        )
        try:
            allque.save()
        except Exception as e:
            print("Error in saving data: {e}")
    else:
        print("Missing data in the form submission")
    return render(request, 'zqAdmin/adQuestions.html')


@login_required   
   
def addsocialjob(request):
    
    
    if request.user.userType!='admin':
        messages.error(request,"Please login as admin")
        return redirect('newmemberDashboard')
    


    result={}
    if request.method=='POST':
        # print("came here")
        # return
       
        ytube_url=request.POST.get('ytube')
        facebook_url=request.POST.get('facebook')
        instagram_url=request.POST.get('instagram')
        twitter_url=request.POST.get('twitter')
        greviews_url=request.POST.get('greviews')
        
        
   
        
        try:
            
            socObj=SocialJobs.objects.create(fb_link=facebook_url,insta_link=instagram_url,twitter_link=twitter_url,youtube_link=ytube_url,greview_link=greviews_url,uploaddate=datetime.now(),whatfor="None")
            
        except Exception as e:
            print(e)
            socObj=None
            
        if socObj:
            
            result['success']=1
            result['message']=f'new social job created successfully'
            messages.success(request,"Social job added successfully")
            # return JsonResponse(result)
            render(request, 'zqAdmin/admin/addSocialJob.html')
        
        else:
            
            result['success']=0
            result['message']=f'some error occured'
            # return JsonResponse(result)
            messages.error(request,"something went wrong")
            render(request, 'zqAdmin/admin/addSocialJob.html')
        
            
            
        
    
    return render(request, 'zqAdmin/admin/addSocialJob.html',context={
        'ytUrl':"",
        'facebook':"",
        'twitter':"",
        'instagram':"",
        'greviews':"",
    })
        
@login_required   
   
def verifysocialjobdata(request):
    
   
    if request.user.userType!='admin':
        messages.error(request,"Please login as admin")
        return redirect('newmemberDashboard')
    
    
    if request.method=='POST':
        
        # print("came here")
        # return
        result={}
        taskId=request.POST.get('taskId')
        # print(taskId)
        # return
        # return
        sumbittedTaskIns=SubmittedDataForSocialMedia.objects.get(id=taskId)
        # sumbittedTaskIns.status=1
        # sumbittedTaskIns.save()
          
        # print("survey has been completed it came here")
        sureveeyReward=5
        
        allDirects=ZqUser.objects.filter(memberid=sumbittedTaskIns.uploadedby.memberid).count() 
        # allPackages=InvestmentWallet.objects.filter(txn_by=sumbittedTaskIns.uploadedby.memberid).count()
        packageId=sumbittedTaskIns.package_id.id
        # print(packageId)
        
        if packageId:
            if allDirects==1:
                communityBuildingBonus=CommunityBuildingBonus.objects.get(referral_requirement=1).stage_bonus
            elif allDirects==2:
                communityBuildingBonus=CommunityBuildingBonus.objects.get(referral_requirement=2).stage_bonus
            elif allDirects>2:
                communityBuildingBonus=CommunityBuildingBonus.objects.get(referral_requirement=3).stage_bonus
            
            # print("came here=========")
            try:
                # inv=InvestmentWallet.objects.filter(txn_by=sumbittedTaskIns.uploadedby.memberid).first()
                inv=InvestmentWallet.objects.get(id=packageId)
                invId=inv.id
                
                # print("Investment id is",invId)
                
                # return
                
                roiEnts=ROIDailyCustomer.objects.filter(userid=sumbittedTaskIns.uploadedby.memberid,investment_id=invId).count()
                # newobjs=ROIDailyCustomer(userid=request.user,remark=f'ad bonus for {sureveeyReward}',total_sbg=sureveeyReward,roi_sbg=sureveeyReward,roi_date=datetime.now(),status=1,daily_amount=sureveeyReward,roi_days=roiEnts+1,investment_id=inv,usd_rate=0,zaan_rate=0,roi_sbg_usd=sureveeyReward,zaan_value_in_usd=sureveeyReward)
                newobjs=ROIDailyCustomer(userid=sumbittedTaskIns.uploadedby,remark=f'ad bonus for {sureveeyReward}',total_sbg=sureveeyReward,roi_sbg=sureveeyReward,roi_date=datetime.now(),status=1,daily_amount=sureveeyReward,roi_days=roiEnts+1,investment_id=inv,usd_rate=0,zaan_rate=0,roi_sbg_usd=sureveeyReward,zaan_value_in_usd=sureveeyReward)
                newobjs.save()
                
                try:
                    with connection.cursor() as cursor:
                        cursor.callproc('MagicalIncome', [
                                inv.txn_by_id,
                                sureveeyReward
   
                        ])

                    print(f'procedure for {inv.txn_by_id} executed successfully')
                    
                            
                except Exception as e:
                    print('Error occurred:', str(e))
                    return JsonResponse({'status': 0,'msg':'something went wrong'})
                    # return "Error: Please try again later"
                
                if allDirects:
                    # communityIncomeEntry=CommunityBuildingIncome(introid=request.user.id,intronewid=request.user,introname=request.user.username,rs=communityBuildingBonus,package_usd=inv.amount,rs_usd=communityBuildingBonus,status=1,point=0,package=inv.amount,nextsunday=datetime.now(),members=request.user,custid=inv.id,custnewid=request.user.memberid,custname=request.user.username,paidstatus=1,last_paid_date=datetime.now())
                    communityIncomeEntry=CommunityBuildingIncome(introid=sumbittedTaskIns.uploadedby.id,intronewid=sumbittedTaskIns.uploadedby,introname=sumbittedTaskIns.uploadedby.username,rs=communityBuildingBonus,package_usd=inv.amount,rs_usd=communityBuildingBonus,status=1,point=0,package=inv.amount,nextsunday=datetime.now(),members=sumbittedTaskIns.uploadedby,custid=inv.id,custnewid=sumbittedTaskIns.uploadedby.memberid,custname=sumbittedTaskIns.uploadedby.username,paidstatus=1,last_paid_date=datetime.now())
                    communityIncomeEntry.save()
                    
                rimberioBonus=RimberioCoinDistribution.objects.filter(task='socialJobSubmission').first().coin_reward
                RimberioWallet.objects.create(amount=rimberioBonus,remark=f"rimberio bonus for social job submission is {rimberioBonus}",trans_for="socialJobSubmission",tran_by=sumbittedTaskIns.uploadedby,trans_from=sumbittedTaskIns.uploadedby,trans_to=sumbittedTaskIns.uploadedby,trans_date=datetime.now(),trans_type='CREDIT')
                sumbittedTaskIns.status=1
                sumbittedTaskIns.save()
            except Exception as e:
                print(e)
                return JsonResponse({'status': 0,'msg':'something went wrong'})
                
        else:
            
            rimberioBonus=RimberioCoinDistribution.objects.filter(task='socialJobSubmission').first().coin_reward
            # RimberioWallet.objects.create(amount=rimberioBonus,remark=f"rimberio bonus for social job submission is {rimberioBonus}",trans_for="socialJobSubmission",tran_by=request.user,trans_from=request.user,trans_to=request.user,trans_date=datetime.now(),trans_type='CREDIT')
            RimberioWallet.objects.create(amount=rimberioBonus,remark=f"rimberio bonus for social job submission is {rimberioBonus}",trans_for="socialJobSubmission",tran_by=sumbittedTaskIns.uploadedby,trans_from=sumbittedTaskIns.uploadedby,trans_to=sumbittedTaskIns.uploadedby,trans_date=datetime.now(),trans_type='CREDIT')
            sumbittedTaskIns.status=1
            sumbittedTaskIns.save()
            

        return JsonResponse({'status': 1,'msg':'Social Job approved successfully'})

        
        
    
    allSubmittedTaskImages=SubmittedDataForSocialMedia.objects.filter(status=0)
    
    # print(allSubmittedTaskImages.count())
    
    return render(request,'zqAdmin/admin/verifysocialjobdata.html',context={
        'allSubmittedTaskImages':allSubmittedTaskImages
    })
    
@login_required   
   
def addMembersToClub(request):
    
    # if request.method=='POST':
        
    #     # print("came here")
        
    #     result={}
    #     # data=json.loads(request.body)
    #     # username=data.get('username')
    #     username=request.POST.get('username')
    #     Entclub=request.POST.get('clubSelect').strip()
    #     if Entclub:
            
    #         doesClubExist=ClubsBonus.objects.filter(club_name=Entclub)
    #         if doesClubExist.exists():
    #             Entclub=doesClubExist.first()
    #         else:
    #             result['status']=0
    #             result['msg']='club does not exist'
                
    #             return JsonResponse(result)
           
                
            
        
        
    #     # print(username,Entclub)
    #     try:
            
    #         doesUserExist=ZqUser.objects.get(username=username)
            
    #     except:
    #         doesUserExist=None
            
    #         result['status']=0
    #         result['msg']='user eith this username doesn not exist'
            
    #         return JsonResponse(result)
        
    #     # check whether member is already in a club
        
        
        
    #     try:
    #         doesUserExistInClub=ClubMembers.objects.get(memberid=doesUserExist.memberid,club=Entclub)
    #         result['status']=0
    #         result['msg']=f'User already exist in the club'
            
    #         return JsonResponse(result)
    #     except:
    #         pass
        
    #     # add member to club
    #     # print("came here")
    #     try:
    #         newClubInstance=ClubMembers.objects.create(club=Entclub,memberid=doesUserExist)
    #     except Exception as e:
    #         print(e)
            
    #     result['status']=1
    #     result['msg']=f'Member {username}  added to club {Entclub.club_newname} successfully'
    #     return JsonResponse(result)  
    
    
    getcoins=RimberioWallet.objects.filter(remark='direct income')
    
    return render(request,'zqAdmin/admin/addMemberInClub.html',context={
            'getcoins':enumerate(getcoins),
            # 'allClubMems':ClubMembers.objects.filter(club=clubName)
        }) 

@login_required   


def distributeIncomeToClubMembers(request):
    
  
    getcoins=RimberioWallet.objects.filter(remark='ritcoins reward for activating your account is 100000')
    
        
    return render(request,'zqAdmin/admin/distributeClubIncome.html',context={
          
           'getcoins':enumerate(getcoins),
        }) 
    
@login_required   


def manageRitcoinsRedemption(request):
    
  
    getcoins=RedeemedRitcoins.objects.all()
    
        
    return render(request,'zqAdmin/admin/manageRitcoinsRedemption.html',context={
          
           'getcoins':enumerate(getcoins),
        }) 


@login_required   
           
def club1members(request):
    
    clubName=ClubsBonus.objects.get(id=1).club_name
    return render(request,'zqAdmin/admin/clubMembers.html',context={
        'headerNote':'All Club 1 Members',
        'allClubMems':ClubMembers.objects.filter(club_id=1).order_by('-club_added_date')
    }) 
    
@login_required   
         
def club2members(request):
    clubName=ClubsBonus.objects.get(id=2).club_name
    return render(request,'zqAdmin/admin/clubMembers.html',context={
        'headerNote':'All Club 2 Members',
        'allClubMems':ClubMembers.objects.filter(club_id=2).order_by('-club_added_date')
    }) 
    
@login_required   
          
def club3members(request):
    clubName=ClubsBonus.objects.get(id=3).club_name
    return render(request,'zqAdmin/admin/clubMembers.html',context={
        'headerNote':'All Club 3 Members',
        'allClubMems':ClubMembers.objects.filter(club_id=3).order_by('-club_added_date')
    })    
           
@login_required   

def ClubMembersIncomes(request,clubid):
    
    return render(request,'zqAdmin/admin/clubIncomes.html',context={
        'headerNote':f'All Club {clubid} Members Income',
        'allClubMems':ClubMembers.objects.filter(club_id=clubid).order_by('-id')
    })   
        
            
        

# def distributeClubIncome(request):
#     ...

@login_required   

def memberWalletwithdraw(request):
    
    
        print('came here')

        if request.method=='POST':
            # print("came here===")

            
            memberUsername=request.POST.get('memberId')
            amount=float(request.POST.get('amount'))
            
          
            
            print(memberUsername,amount)
            # return
            print("came here")
            try:
                usrObj=ZqUser.objects.get(username=memberUsername)
            except Exception as e:
                return JsonResponse({
                    'status':0,
                    'msg':'User with the given username does not exit',
                })
            # print(usrObj)
            # print(usrObj)
           
            if float(amount)<0 :
                
                return JsonResponse({
                    'status':0,
                    'msg':'Invalid amount',
                })
                
                
           
            try:
                
                usd_rate=CustomCoinRate.objects.filter(coin_name='USD').order_by('-id').first().amount
                usdRateInINR=float(usd_rate)
                totalAmountInINR=amount*usdRateInINR
                admincaharge=float(AdminWithdrawalCharge.objects.get(id=1).chargeInPercent)
                admincahargeAmount=totalAmountInINR*(admincaharge)
                totalAmountTobeSentInr=totalAmountInINR*(1-admincaharge)
                admincahargeUSD=amount*(admincaharge)
            
                totalAmountTobeSent=totalAmountInINR*(1-admincaharge)
                totalAmountTobeUSDT=amount*(1-admincaharge)
                
                
                acConfObj=AccountComfirmation.objects.filter(uploaded_by=usrObj.memberid)
                
                if acConfObj.count()>0:
                    kycObj=acConfObj.first()
                    # print(kycObj)
                    withrawalAdd=kycObj.pob_number
                    if not withrawalAdd:
                        withrawalAdd='NA'
                    # print(withrawalAdd)
                    withdrawBankName=kycObj.pob_bankName
                    if not withdrawBankName:
                        withdrawBankName='NA'
                    # print(withdrawBankName)
                else:
                    withrawalAdd='XXXXXXXXXX'
                    withdrawBankName=''
                    
                newTran=None    
                obj_wallet_ami_coin=None    
                objw=None    
                
                newTran=TransactionHistoryOfCoin.objects.create(
                    cointype='USD',
                    memberid_id=usrObj.memberid,
                    name=usrObj.username,
                    hashtrxn='withdrawal by admin',
                    amount=amount,
                    coinvalue=usdRateInINR,
                    trxndate=datetime.now(),
                    status='success',
                    coinvaluedate=datetime.now(),
                    total=amount,
                    amicoinvalue=usdRateInINR,
                    amifreezcoin=float(amount),
                    amivolume=amount,
                    totalinvest=0,
                    tran_type='DEBIT',
                    )
                                
                    # newTran.save()

                obj_wallet_ami_coin = WalletAMICoinForUser.objects.create(
                    email=usrObj.email,
                    amicoin=totalAmountInINR,
                    amicoinin_doller=amount,
                    paystatus="success",
                    remark="admin_withdrawal",
                    receivedate=datetime.now(),
                    trxndate=datetime.now(),
                    # trxnid=result['pay_id'],
                    trxnid='admin withdrawal',
                    status=1,
                    withrawal_add=withrawalAdd,
                    withdrawal_bank_name=withdrawBankName,
                    admin_charge=math.ceil(admincahargeAmount),
                    requested_amount=totalAmountInINR,
                    total_value= math.floor(totalAmountTobeSent),
                    memberid=usrObj,
                    total_value_zaan=0,
                    withdrawl_time_zaan_rate=0,
                    transactionId=newTran,
                    currency='INR',
                )
                    
                    # obj_wallet_ami_coin.save()
                                            
                            
                objw = WalletTab.objects.create(
                    # col2=topupInitiatedByUser,
                    col3="Withdrawal",
                    col4="ZQL Coin " + str(amount) + " has been withdrawn " +usrObj.email ,
                    amount=amount,
                    user_id=usrObj,
                    txn_date=datetime.now(),
                    txn_type="DEBIT",
                    zql_rate=0,
                    usd_rate=0,
                    usd_value_of_zaan=0
                    )
            
                return JsonResponse({
                    'status':1,
                    'msg':'withdrawal successfull'
                })
            except Exception as e:
                print(str(e))  
                
                if newTran:
                    newTran.delete()
                if obj_wallet_ami_coin:
                    obj_wallet_ami_coin.delete()
                if objw:
                    objw.delete()
                
                return JsonResponse({
                    'status':0,
                    'msg':'some error occured'
                })  
            
        return render(request,'zqAdmin/admin/memberWalletWithdraw.html')
    

@login_required   

def allMemsInfo(request):
        return render(request,'zqAdmin/admin/allMemsInfo.html')



def paginated_table_data_view(request, data_type):
    # Get the page number from the request
    # page_number = request.GET.get('page', 1)
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))

    if data_type == 'investments':
        tableName='All Investments'
        tableHeadings=['Username','Amount','TxnDate']
        fields=['txn_by','amount','txn_date']

        # allFields=['txn_by','Amount','TxnDate']
        items = InvestmentWallet.objects.all()
        data_label = 'Investment'
        
    elif data_type == 'withdrawals':
        tableName='All Withdrawals'
        tableHeadings=['Username','Amount','TxnDate','Bank','IsAdminWithdrawal']
        items = WalletAMICoinForUser.objects.all()
        data_label = 'Withdrawal'
        
    elif data_type == 'deposits':
        tableName='All Deposits'
        tableHeadings=['Username','Amount','TxnDate','Bank','IsAdminDeposit']
        
        items = TransactionHistoryOfCoin.objects.all()
        data_label = 'Deposit'
    else:
        items = []
        data_label = 'Unknown'

    # paginator = Paginator(items, 10)  # Show 10 items per page
    # page_obj = paginator.get_page(page_number)
    # paginator = Paginator(items, length)
    # page_number = (start // length) + 1
    # page_obj = paginator.get_page(page_number)

    # data = [
    #     {field.lower(): getattr(item, field.lower()) for field in fields}
    #     for item in page_obj
    # ]
    
    # print(data)

    # response = {
    #     'draw': draw,
    #     'recordsTotal': paginator.count,
    #     'recordsFiltered': paginator.count,
    #     'data': data
    # }

    # return JsonResponse(response)

    # return render(request, 'partials/table_data.html', {'page_obj': page_obj, 'type': data_label})
    return render(request, 'zqAdmin/admin/memberDataView.html',context={
        'tableName':tableName,
        'tableHeadings':tableHeadings,
        # 'items':enumerate(items),
        'data_label':data_label,
        'fields':fields,
    })

def paginated_table_data(request, data_type):
    # Get the page number from the request
    # page_number = request.GET.get('page', 1)
    
    print("came here")
    draw = int(request.POST.get('draw', 1))
    start = int(request.POST.get('start', 0))
    length = int(request.POST.get('length', 10))

    if data_type == 'investments':
        tableName='All Investments'
        tableHeadings=['Username','Amount','TxnDate']
        fields=['txn_by','amount','txn_date']

        # allFields=['txn_by','Amount','TxnDate']
        items = InvestmentWallet.objects.all()
        data_label = 'Investment'
        
    elif data_type == 'withdrawals':
        tableName='All Withdrawals'
        tableHeadings=['Username','Amount','TxnDate','Bank','IsAdminWithdrawal']
        items = WalletAMICoinForUser.objects.all()
        data_label = 'Withdrawal'
        
    elif data_type == 'deposits':
        tableName='All Deposits'
        tableHeadings=['Username','Amount','TxnDate','Bank','IsAdminDeposit']
        
        items = TransactionHistoryOfCoin.objects.all()
        data_label = 'Deposit'
    else:
        items = []
        data_label = 'Unknown'

    # paginator = Paginator(items, 10)  # Show 10 items per page
    # page_obj = paginator.get_page(page_number)
    paginator = Paginator(items, length)
    page_number = (start // length) + 1
    page_obj = paginator.get_page(page_number)

    data = [
        {field.lower(): getattr(item, field.lower()) for field in fields}
        for item in page_obj
    ]
    
    print(data)

    response = {
        'draw': draw,
        'recordsTotal': paginator.count,
        'recordsFiltered': paginator.count,
        'data': data
    }

    return JsonResponse(response)

    # return render(request, 'partials/table_data.html', {'page_obj': page_obj, 'type': data_label})
    # return render(request, 'zqAdmin/admin/memberDataView.html',context={
    #     'tableName':tableName,
    #     'tableHeadings':tableHeadings,
    #     'items':enumerate(items),
    #     'data_label':data_label,
    # })


@csrf_exempt
def data_view(request):
    
    
    # start_time = time.time()
    # print("came here")
    # print(request.method)
    
    # draw = int(request.GET.get('draw', 1))
    draw = int(request.POST.get('draw', 1))
    # start = int(request.GET.get('start', 0))
    start = int(request.POST.get('start', 0))
    # length = int(request.GET.get('length', 10))
    length = int(request.POST.get('length', 10))
    # search_value = request.GET.get('search[value]', '')
    search_value = request.POST.get('search[value]', '')
    # user_search = request.GET.get('introducer', '')
    user_search = request.POST.get('introducer', '')
    # allintroducer_search = request.GET.get('mem', '')
    allintroducer_search = request.POST.get('mem', '')
    # print(allintroducer_search)
    # print(user_search)
    # print(search_value,user_search)
    # print(search_value)
    if search_value:
        
        try:
            queryset = ZqUser.objects.filter(
                Q(username__icontains=search_value) |
                Q(email__icontains=search_value) |
                Q(plain_password__icontains=search_value) |
                Q(introducerid__username__icontains=search_value) |
                Q(joindate__icontains=search_value) |
                Q(activationdate__icontains=search_value) 
                # Q(salary__icontains=search_value)
            )
            
        except Exception as e:
            print(str(e))
            # queryset=[]
            
    elif user_search:
        queryset = ZqUser.objects.filter(
            username=user_search
            # Q(username__icontains=user_search) |
            # Q(introducerid__username__icontains=introducer_search) 
            )
        
        # queryset = ZqUser.objects.filter(
        #             username__icontains=introducer_search
        #         ).filter(
        #             introducerid__username__icontains=introducer_search
        #         )

    elif allintroducer_search:
            queryset = ZqUser.objects.filter(
                # username=allintroducer_search
                # Q(username__icontains=user_search) |
                introducerid__username__icontains=allintroducer_search
                )
        
    else:
        queryset = ZqUser.objects.all()

    # Filter data if necessary
    # queryset = ZqUser.objects.all()
    
    try:
        print(request.user.totalLevelTeam())
    except Exception as e:
        print(str(e))
    # Paginate
    paginator = Paginator(queryset, length)
    page_number = (start // length) + 1
    page = paginator.get_page(page_number)
    
    
    
    try:
        
        # totalWalletBal= obj.totalRealWalletBalance()
        # print("came here")
        # print("========================")
        # for obj in page:
        #     print(obj)
            
        data = [
            
            {
            # 'username':  f'<a href="#" class="mem-link" data-mem="{obj.username}">{obj.username}</a>',    
            'username': obj.username,    
            'email':obj.email,
            'password': obj.plain_password,
            # 'introducername': f'<a href="#" class="introducer-link" data-username="{obj.introducerid.username}">{obj.introducerid.username}</a>' if obj.introducerid else '',
            'introducername':obj.introducerid.username,
            # 'introducername':'',
            
            'activationDate':obj.activationdate,
            'joindate':obj.joindate,
            'totalDirectTeam':obj.totalDirectMems(),
            'totalLevelTeam':obj.totalLevelTeam(),
            'totalDeposits':obj.totalDeposits(),
            'adminDeposits':obj.totalDepositsByAdmin(),
            'selfDeposits':float(obj.totalDeposits() - obj.totalDepositsByAdmin()),
            'packages':obj.totalInvestments(),
            'selfActivatedPackages':obj.totalSelfInvs(),
            'peerActivatedPackages':obj.totalPeerInvestments(),
            'directincome':obj.totalDirectIncome(),
            'levelincome':obj.totalLevelIncome(),
            'communitybonus':obj.CommunityBuildingIncome(),
            'magicbonus':obj.totalMagicalIncome(),
            'socialmediabonus':obj.totalMiningBonus(),
            'clubbonus':obj.totalClubBonus(),
            'socialmediwalletbalance':obj.totalPrepaidBonus(),
            'totalallbonus':obj.totalAllBonus(),
            'totalActivationsForPeers':obj.allTopUpsForPeer(),
            'totalWithdrawals':obj.totalWithdrawals(),
            'totalAdminWithdrawals':obj.totalAdminWithdrawals(),
            'totalSelfWithdrawals':obj.totalSelfWithdrawals(),
            'totalWalletBalance':f'<span class="text-danger"> {obj.totalRealWalletBalance()}</span>' if obj.totalRealWalletBalance()<0 else obj.totalRealWalletBalance(),
            'totalwithdrawablefund':f'<span class="text-danger"> {obj.totalRealWithdrawalableBalance()}</span>' if obj.totalRealWithdrawalableBalance()<0 else obj.totalRealWithdrawalableBalance(),

            'totalwithdrawablefund':obj.totalWithdrawalableBalance(),
            # 'office': obj.office,
            # 'age': obj.age,
            # 'start_date': obj.start_date.strftime('%Y-%m-%d'),
            # 'salary': obj.salary,
            }
            for obj in page
            ]
    
    
    except Exception as e:
        print(str(e))
        
    response = {
        'draw': draw,
        'recordsTotal': paginator.count,
        'recordsFiltered': paginator.count,
        'data': data
    }
    
    # elapsed_time = time.time() - start_time
    
    # print("elapsed time is",elapsed_time)

    return JsonResponse(response)
 
@login_required   
    
def blockMember(request):
    if request.user.userType!='admin':
        messages.error(request,"Please login as admin")
        return redirect('newmemberDashboard')
   
    if request.method=='POST':
        
        # print("came here")
        userMemberId=request.POST.get('memberId').strip()
        user=ZqUser.objects.filter(username=userMemberId)
        
        if user.exists():
            user=user.first()
            user.is_blocked=True
            user.save()
            
            return JsonResponse(
                {
                    'status':1,
                    'msg':f'{user.username} blocked successfully'
                }
            )
            
        else:
            
            return JsonResponse(
                {
                    'status':0,
                    'msg':'User with this username does not exist'
                }
            )
            
        
        
        # return
    
    return render(request,'zqAdmin/admin/blockmember.html',context={
        'allBlockedmems':enumerate(ZqUser.objects.filter(is_blocked=True))
    })


@login_required   

def blockMemberWithdrawal(request):
    if request.user.userType!='admin':
        messages.error(request,"Please login as admin")
        return redirect('newmemberDashboard')
    if request.method=='POST':
    
    # print("came here")
        userMemberId=request.POST.get('memberId').strip()
        user=ZqUser.objects.filter(username=userMemberId)
        
        if user.exists():
            user=user.first()
            user.is_withdrawal_blocked=True
            user.save()
            
            return JsonResponse(
                {
                    'status':1,
                    'msg':f'withdrawal blocked for user {user.username}  successfully'
                }
            )
            
        else:
            
            return JsonResponse(
                {
                    'status':0,
                    'msg':'User with this username does not exist'
                }
            )
            
        
    
    # return

    
    return render(request,'zqAdmin/admin/blockwithdrawal.html',context={
         'allBlockedmems':enumerate(ZqUser.objects.filter(is_withdrawal_blocked=True))
    })
    
    
    
    
@login_required   

def unblockMemberWithdrawal(request):
    if request.user.userType!='admin':
        messages.error(request,"Please login as admin")
        return redirect('newmemberDashboard')
    if request.method=='POST':
    
    # print("came here")
        userMemberId=request.POST.get('memberId').strip()
        user=ZqUser.objects.filter(id=userMemberId)
        
        if user.exists():
            user=user.first()
            user.is_withdrawal_blocked=False
            user.save()
            
            return JsonResponse(
                {
                    'status':1,
                    'msg':f'withdrawal Unblocked for user {user.username}  successfully'
                }
            )
            
        else:
            
            return JsonResponse(
                {
                    'status':0,
                    'msg':'User with this username does not exist'
                }
            )
            
        
    
    # return

    
    return render(request,'zqAdmin/admin/blockwithdrawal.html',context={
         'allBlockedmems':enumerate(ZqUser.objects.filter(is_withdrawal_blocked=True))
    })