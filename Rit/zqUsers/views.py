from decimal import Decimal
import time
# import pytz
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
# from django.template.loader import render_to_string
from .tokens import email_verification_token
from django.utils.http import base36_to_int
# from .utils import base36_to_int
from django.utils.encoding import force_str

from .models import *
import requests
from django.http import JsonResponse
import random
from datetime import datetime,date,timedelta
# from django.utils import timezone
from django.utils.timezone import make_aware,is_naive
import math
from faker import Faker
# from web3 import Web3
from web3.exceptions import TimeExhausted
# from datetime import datetime
# from decimal import Decimal
from django.core.mail import EmailMessage,get_connection
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from .forms import *
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from django.db import connection,transaction
from django.contrib.auth import update_session_auth_hash
from wallet.models import *
import json
from collections import Counter
from django.db.models import Sum,F,Q, ExpressionWrapper, DecimalField,Value, OuterRef, Subquery,DateTimeField
from django.db.models.functions import Coalesce
from django.utils import timezone
import uuid
from django.views.decorators.csrf import csrf_exempt
from web3 import Web3
# from web3.middleware import geth_poa_middleware

# from .utils import pyCoinPayments    
import os
import logging
from dateutil import parser
from channels.layers import get_channel_layer
from web3.middleware import ExtraDataToPOAMiddleware

from asgiref.sync import async_to_sync
import asyncio
logger = logging.getLogger(__name__)


@login_required                
def newmemberDashboard(request):

    print(request.user.groupIncome())
    # print(request.user.doesMemberHaveAssocialtedIds())
    # lt = get_introducer_hierarchy(request.user.memberid)
    lt = get_introducer_hierarchy(request.user.username)
    unique_users = list({user for user, _ in lt})
    
    totalInvs=0
    for user in unique_users:
        if user.memberid!=request.user.memberid:
            totalInvs+=float(InvestmentWallet.objects.filter(txn_by=user.memberid).aggregate(Sum('amount'))['amount__sum'] or 0)
    # print(totalInvs)   

    

    return render(request,"zqUsers/member/memDashboard.html",context={
        'totalInvs':totalInvs,
        'allClubsMemsCount':{
            'club1mems':ClubMembers.objects.filter(club=1).count(),
            'club2mems':ClubMembers.objects.filter(club=2).count(),
            'club3mems':ClubMembers.objects.filter(club=3).count(),
        }
    })
    
@login_required                
def groupDashboard(request):

    # print(request.user.groupIncome())
    # print(request.user.doesMemberHaveAssocialtedIds())
    # lt = get_introducer_hierarchy(request.user.memberid)
    lt = get_introducer_hierarchy(request.user.username)
    unique_users = list({user for user, _ in lt})
    
    totalInvs=0
    for user in unique_users:
        if user.memberid!=request.user.memberid:
            totalInvs+=float(InvestmentWallet.objects.filter(txn_by=user.memberid).aggregate(Sum('amount'))['amount__sum'] or 0)
    # print(totalInvs)   

    

    return render(request,"zqUsers/member/groupDashboard.html",context={
        'totalInvs':totalInvs
    })


@login_required                
def viewClubs(request):


    # print(totalInvs)  
    memClub=ClubMembers.objects.filter(memberid=request.user.memberid)
    # memClub=ClubMembers.objects.all().order_by('club')
    
    if memClub.count()>0:
        memClub=memClub.first().club
        allClubMems=ClubMembers.objects.filter(club=memClub)
        
    else:
        allClubMems=[]
        
    return render(request,"zqUsers/member/allclubmems.html",context={
            'allClubMems':allClubMems
        })
                

@login_required                
def Activation(request):
    
    doesuserhavesubmittedform=SubmittedDataForSocialMedia.objects.filter(uploadedby=request.user)
    if doesuserhavesubmittedform.count()>0:
        if not doesuserhavesubmittedform.first().status:
            messages.warning(request, 'please complete your kyc first')
            return redirect('socialmedia')
    allInvs=TransactionHistoryOfCoin.objects.filter(memberid_id=request.user.memberid,tran_type='CREDIT')
    
    return render(request,"zqUsers/member/activateid.html",context={
        'allInvs':enumerate(allInvs),
        'allPs':AllPackageDetails.objects.all()
    })


@login_required                
def activate_id_TOPUPByUser(request, amount):
    

        
        if int(amount) >= 0 and request.user.status == 0:
        # if int(amount) >= 0 :
           
            try:
                    
                    print('Came here=======================')
                    with connection.cursor() as cursor:
                        # cursor.execute("EXEC activate_id @memberid=%s, @package=%s, @comment='Self id activation', @activation_by='User', @activation_time_no_of_btc=0, @activation_time_no_of_trx=0, @activation_time_no_of_eth=0, @btc_rate=0, @trx_rate=0, @eth_rate=0;", [memberid, num])
                        res=cursor.execute("CALL activate_id(%s, %s, 'Self id activation', 'User', 0, 0, 0, 0, 0, 0,%s,%s,%s);", (request.user.memberid, amount,0,0,amount))
                        # print(res)
                        str_result = "Success"
                        
                        return res
                        # print('Came here=======================')
                        
            except Exception as e:
                # print(e)
                logger.error(f"{datetime.now()}:An error occurred: %s", str(e))
                return 0
                # return e
                
        else:
        #    print("=========================rinvestment")
           
        #    print("status is ",_userinformation.status )
            
           if request.user.status == 1:
               
                # print("===================came for reinvestment")
                try:
                    with connection.cursor() as cursor:
                        
                        # CREATE DEFINER=`zaanqueriladmin`@`%` PROCEDURE `reinvestproc`(IN `_memberid` VARCHAR(255), IN `_package` FLOAT, IN `comment` VARCHAR(255), IN `activation_by` VARCHAR(255), IN `activation_time_no_of_btc` FLOAT, IN `activation_time_no_of_trx` FLOAT, IN `activation_time_no_of_eth` FLOAT, IN `btc_rate` FLOAT, IN `eth_rate` FLOAT, IN `trx_rate` FLOAT)
                        # res=cursor.execute("CALL activate_id(%s, %s, 'Self id activation', 'User', 0, 0, 0, 0, 0, 0);", (request.user.memberid, num))

                        res=cursor.execute("CALL reinvestproc (%s, %s, 'Self id activation', 'User', 0, 0, 0,0, 0, 0,%s,%s,%s);", [request.user.memberid, amount,0,0,amount])
                        # print("retune====================================")
                        # print(res)
                        return res
                except Exception as e:
                    # print(e)
                    logger.error(f"{datetime.now()}: An error occurred: %s", str(e))
                    #  return e
                    return 0


@login_required                
def activateMemberId(request):
    
 
    if request.method=='POST':
 
        result={}
        TOTALWALLETBALANCE=request.user.totalWalletBalance()
        data = json.loads(request.body)
        package = float(data.get('Package'))
       
        
        if package and float(package)>0 and package<=TOTALWALLETBALANCE:
            # print("came here")
            res=activate_id_TOPUPByUser(request=request,amount=package)
            
            
            if res:

               
                try:
                    
                    objw = WalletTab.objects.create(
                        # col2=topupInitiatedByUser,
                        col3="TOPUP",
                        col4="ZQL Coin " + str(package) + " is used for topup of " +request.user.email ,
                        amount=package,
                        user_id=request.user,
                        txn_date=datetime.now(),
                        txn_type="DEBIT",
                        zql_rate=0,
                        usd_rate=0,
                        usd_value_of_zaan=package
                    )
                    
                    objw.save()
                    # print("wallet entry done")

                    newInvestmentWalletEntry=InvestmentWallet.objects.create(
                        txn_by=request.user,
                        amount=package,
                        remark=f'Zaan Coin {package} is added  to your investment wallet',
                        txn_date=datetime.now(),
                        txn_type='CREDIT',
                        zaan_rate=0,
                        usd_rate=0,
                        zaan_value_in_usd=package,
                        activated_by=request.user,
                    )
                    
                    newInvestmentWalletEntry.save()
                    
           
                    # rimberioBonus=RimberioCoinDistribution.objects.filter(task='activateId').first().coin_reward

                    # RimberioWallet.objects.create(amount=rimberioBonus,remark=f"rimberio bonus for package activation  is {rimberioBonus}",trans_for="packageactivation",tran_by=request.user,trans_from=request.user,trans_to=request.user,trans_date=datetime.now(),trans_type='CREDIT',package_id=newInvestmentWalletEntry)

                    # # print("came here")
                    # # print("came here=========================================>")
                    # usersMemId=request.user.memberid
                    # invwalletId=str(newInvestmentWalletEntry.id)
                    # try:
                    #     with connection.cursor() as cursor:
                    #         cursor.callproc('rimberio_coin_distribution_activateid', [
                    #                 str(usersMemId),
                    #                 1,
                    #                 'IdActivationDownlineDistribution',
                    #                 invwalletId
                                    
                                    
                                
                    #         ])
                            
                    #     print("entry done")


                            
                    # except Exception as e:
                    #     print('Error occurred:', str(e))
                    #     # return "Error: Please try again later"
                    
            
                    
                except Exception as e:
                    
                    print(e)
                    logger.error(f"{datetime.now()}: An error occurred: %s", str(e))
                    if objw:
                        
                        objw.delete()
                        
                    if newInvestmentWalletEntry:
                        newInvestmentWalletEntry.delete()
                    
                    
                    
                    
                    result['status'] = 0
                    result['msg'] = "some error occured from our end"
                    result['alertMsg'] = "some error occured from our end"
                    
                    return JsonResponse(result)
                
                
                
                
               
                return JsonResponse({'success': True,'msg': 'Your Id has been activated successfully'})

            
                
            
            
            
            else:
                # result['status'] = 0
                # result['message'] = "You Package activation has been failed"
                
                return JsonResponse({'success': True,'msg': 'some error occured please try again later'})

        else:
            return JsonResponse({'success': False,'msg': 'Invalid amount'})


@login_required                
def NewActivation(request):
    
    # print('came here')
    if request.method == 'POST':
        
        
        if request.user.status:
                        
            return JsonResponse({'success': True, 'msg': 'You have already activated your account'})
        
        
        
        packageValue=request.POST.get('package') #55
        
        if not packageValue:
            msg = "Please select a valid package"
            return JsonResponse({'success': False, 'msg': msg})
        
        try:
            
            getPackageValue=float(packageValue)
        except Exception as e:
            
            msg = "Invalid selected package"
            return JsonResponse({'success': False, 'msg': msg})
        
        
        doesChoosenPackageIsValid=AllPackageDetails.objects.filter(package_price=getPackageValue)
        
        if not doesChoosenPackageIsValid.count()>0:
            msg = "Invalid selected package"
            return JsonResponse({'success': False, 'msg': msg})
        
    
        
        try:
            if activateIdNew(user=request.user,package=doesChoosenPackageIsValid.first().package_price):
                # msg = "Invalid selected package"
                return JsonResponse({'success': True, 'msg': 'Your account has been activated successfully'})
                # return 
            else:
                # print("came here")
                msg = "Some error occured please try again later"
                return JsonResponse({'success': True, 'msg': msg})
            
        except Exception as e:
            print(str(e))
            return JsonResponse({'success': False, 'msg': 'Something went wrong..............'})

                
        


    allInvs=TransactionHistoryOfCoin.objects.filter(memberid_id=request.user.memberid,tran_type='CREDIT')
    allps=AllPackageDetails.objects.all()
    print(allps)
    return render(request,"zqUsers/member/activateIdNew.html",context={
        'allInvs':enumerate(allInvs),
        'allPs':AllPackageDetails.objects.all()
    })


# @login_required                
def activate_id_TOPUPByUserNew(user, package,activated_by_user):
    
    
        try:
            
            newInvestmentWalletEntry=InvestmentWallet.objects.create(amount=package,txn_by=user,activated_by= activated_by_user  )
            
            # distribut rit coins
            
            getcoin=CoinReward.objects.get(what_for='activation').coin_reward
            
            newrimberiocoinentry=RimberioWallet.objects.create(amount=getcoin,remark=f"ritcoins reward for activating your account is {getcoin}",trans_for="activation",tran_by=user,trans_from=user,trans_to=user,trans_date=datetime.now(),trans_type='CREDIT',package_id=newInvestmentWalletEntry)

        except Exception as e:
            print(str(e))
            return False

        
        if int(package) >= 0 and user.status == 0:
       
           
            try:
                 
                with connection.cursor() as cursor:
                    
                    res=cursor.execute("CALL activate_id_new(%s, %s,%s,%s);", [user.memberid, package,newInvestmentWalletEntry.id,newrimberiocoinentry.amount])
                    # str_result = "Success"
                    
                    if res:
                        # ditribute direct direct income upon meeting a condition
                        directMember=newInvestmentWalletEntry.txn_by.introducerid
                        gteAllActiveRefers=ZqUser.objects.filter(status=1,introducerid=directMember).count()
                        
                        if gteAllActiveRefers>0:
                            
                            getamounttobedistributed=DirectReferalRewards.objects.filter(ref_requirement=gteAllActiveRefers)
                            
                            if getamounttobedistributed.count()>0:
                                
                                if newInvestmentWalletEntry.amount > 0:
                                    
                                
                                    try:
                                        createANewEntry=Income1.objects.create(
                                            introid=newInvestmentWalletEntry.txn_by.introducerid.id,
                                            intronewid=newInvestmentWalletEntry.txn_by.introducerid,
                                            introname=newInvestmentWalletEntry.txn_by.introducerid.username,
                                            rs=getamounttobedistributed.first().ref_reward,
                                            package_usd=newInvestmentWalletEntry.amount,
                                            rs_usd=getamounttobedistributed.first().ref_reward,
                                            package=newInvestmentWalletEntry.amount,
                                            members=newInvestmentWalletEntry.txn_by,
                                            packageId=newInvestmentWalletEntry,
                                            custid=newInvestmentWalletEntry.txn_by.id,
                                            custnewid=newInvestmentWalletEntry.txn_by.id,
                                            custname=newInvestmentWalletEntry.txn_by.username,
                                        )
                                        
                                    except Exception as e:
                                        print(str(e))
                                
                        
                        
                        return newInvestmentWalletEntry
                    else: 
                        return False
                   
                    
            except Exception as e:
            
                logger.error(f"{datetime.now()}:An error occurred: %s", str(e))
                newInvestmentWalletEntry.delete()
                return 0
               
                
        # else:
      
            
        #    if user.status == 1:
               
        #         print('came here again..')
        #         print("came to execute")
        #         try:
        #             with connection.cursor() as cursor:
                        
        #                 res=cursor.execute("CALL reinvestproc_new (%s, %s,%s);",(user.memberid, package,newInvestmentWalletEntry.id))
                       
        #                 if res:
        #                     return newInvestmentWalletEntry
        #                 else: 
        #                     return False
        #         except Exception as e:
                   
        #             logger.error(f"{datetime.now()}: An error occurred: %s", str(e))
        #             newInvestmentWalletEntry.delete()
        #             return 0


# activateIdNew
# @login_required                
def activateIdNew(user,package,activated_by_user='self'):
    
    # print('came here  inside activateidnew')
    # return

    result={}
    TOTALWALLETBALANCE=user.totalWalletBalance()
    
    # if user.status == 1:
    #     return False

    # print(TOTALWALLETBALANCE)
    # return
    if package and float(package)>0 and package<=TOTALWALLETBALANCE:
       

        res=activate_id_TOPUPByUserNew(user,package,user if activated_by_user == 'self' else activated_by_user )
       
        

        if res:

            # print("cam here")
            try:
                
                objw = WalletTab.objects.create(
                    # col2=topupInitiatedByUser,
                    col3="TOPUP",
                    col4="4 " + str(package) + " is used for topup of " +user.email ,
                    amount=package,
                    user_id=user,
                    txn_date=datetime.now(),
                    txn_type="DEBIT",
                    zql_rate=0,
                    usd_rate=0,
                    usd_value_of_zaan=package
                )
                
                
                # get total active users
                
                
                
                # objw.save()
               
                
                # assignSocialJobs(user,res)
                # # print("investnet entery done")
                
                # # add member to a club if topup amount is valid
                
                # rimberioBonus=RimberioCoinDistribution.objects.filter(task='activateId').first().coin_reward
                # getmultiplier=AllPackageDetails.objects.filter(package_price=package).first().multiplier

                # RimberioWallet.objects.create(amount=rimberioBonus*getmultiplier,remark=f"rimberio bonus for package activation  is {rimberioBonus*getmultiplier}",trans_for="packageactivation",tran_by=user,trans_from=user,trans_to=user,trans_date=datetime.now(),trans_type='CREDIT',package_id=res)

                # # print("came here")
                # # print("came here=========================================>")
                # usersMemId=user.memberid
                # invwalletId=str(res.id)
                # try:
                #     with connection.cursor() as cursor:
                #         cursor.callproc('rimberio_coin_distribution_activateid', [
                #                 str(usersMemId),
                #                 1*getmultiplier,
                #                 'IdActivationDownlineDistribution',
                #                 invwalletId
                                
                                
                            
                #         ])
                        
                #     # print("entry done")


                        
                # except Exception as e:
                #     print('Error occurred:', str(e))
                    # return "Error: Please try again later"
                
        

               
                
            except Exception as e:
                
                print(e)
                logger.error(f"{datetime.now()}: An error occurred: %s", str(e))
               
                
                
                
                
                result['status'] = 0
                result['msg'] = "some error occured from our end"
                result['alertMsg'] = "some error occured from our end"
                
               
                return False
            
            
            

            return True


        
        
        else:
          
            
            # return JsonResponse({'success': True,'msg': 'some error occured please try again later'})
            return False

    else:
        return False


@login_required                
def peerActivationNew(request):
    
    # print("came here")
 
    if request.method == 'POST':
 
        result={}
        TOTALWALLETBALANCE=request.user.totalWalletBalance()
        # print(TOTALWALLETBALANCE)
        data = json.loads(request.body)
        # print(data)
        package = float(data.get('Package'))
        memberId = data.get('Username').strip()
        type = data.get('type').strip()
        
        # check whether usr exist
        
        if not  ZqUser.objects.filter(username=memberId).exists():
            result['status']=0
            result['msg']='User with this username does not exist'
            return JsonResponse(result)
        
        # check whether slcted package is valid
        if not  AllPackageDetails.objects.filter(package_price=package).exists():
            result['status']=0
            result['msg']='Please select a valid package'
            return JsonResponse(result)
        

        if type == 'sendOTP':
            try:
                if send_otp(request,email=request.user.email,subject="OTP to verify peer account activation",template="zqUsers/emailtemps/peerIdActivation.html",whatfor="ACTIVATEPEERID"):
                    
                    result['status']=1
                    result['msg']='OTP sent successfully'
                    return JsonResponse(result)
                
                else:
                    result['status']=0
                    result['msg']='something went wrong while sending otp'
                    return JsonResponse(result)
            except Exception as e:
                print(e)
                result['status']=0
                result['msg']='something went wrong while sending otp'
                return JsonResponse(result)
                    
        
        # check whether otp is in session
        
        if 'ACTIVATEPEERID' in request.session:
            
            userEnteredOTP=data.get('otp').strip()

            sessionOTP=str(request.session.get('ACTIVATEPEERID'))
            if (userEnteredOTP!=sessionOTP):
                
                result['status']=0
                result['msg']='Incorrect otp'
                return JsonResponse(
                    result
                )
        else:
            
            result['status']=0
            result['msg']='unauthenticated otp'
            return JsonResponse(
                result
            )
                
  
        try:
            toBeActivatedMember=ZqUser.objects.get(username=memberId)
        except:
            toBeActivatedMember=None
        
        if not toBeActivatedMember:
            result['status'] = 0
            result['msg'] = "No member found associated with this username"
            
            return JsonResponse(result)

        
        if package and float(package)>0 and package<=TOTALWALLETBALANCE:
            
            # first amount  worth package to be debited from payee wallet
            
            try:
            
                
                debitFromPayeeWallet=TransactionHistoryOfCoin.objects.create(
                            cointype='USD',
                            memberid=request.user,
                            name=request.user.username,
                            hashtrxn='PEER TOPUP',
                            amount=package,
                            coinvalue=90,
                            trxndate=datetime.now(),
                            status='success',
                            coinvaluedate=datetime.now(),
                            total=package,
                            amicoinvalue=90,
                            amifreezcoin=float(90),
                            amivolume=90,
                            totalinvest=package,
                            tran_type='DEBIT',
                        )
                
                creditToReceiverWallet=TransactionHistoryOfCoin.objects.create(
                            cointype='USD',
                            memberid=toBeActivatedMember,
                            name=toBeActivatedMember.username,
                            hashtrxn='PEER TOPUP',
                            amount=package,
                            coinvalue=90,
                            trxndate=datetime.now(),
                            status='success',
                            coinvaluedate=datetime.now(),
                            total=package,
                            amicoinvalue=90,
                            amifreezcoin=float(90),
                            amivolume=90,
                            totalinvest=package,
                            tran_type='CREDIT',
                        )
                            

                
            except Exception as e:
                print(e)
                    
            
            
            # print("came here to check if fund====")
            
            if package<=float(toBeActivatedMember.totalWalletBalance()):
                # res=activate_id_TOPUPByUserNew(user=request.user,package=package,activated_by_user= toBeActivatedMember)
                res=activate_id_TOPUPByUserNew(user=toBeActivatedMember,package=package,activated_by_user=request.user )
                # print(res)
                # return
            else:
                
                result['status'] = 0
                result['msg'] = "Insufficient wallet balance of members id being activated"
                # result['alertMsg'] = "some error occured from our end"
                
                return JsonResponse(result)
                
          
            
            if res:

                # print("cam here")
                try:
                    
      
                    
                    objw=TransactionHistoryOfCoin.objects.create(
                            cointype='USD',
                            memberid=toBeActivatedMember,
                            name=toBeActivatedMember.username,
                            hashtrxn='peerActivate',
                            amount=package,
                            coinvalue=90,
                            trxndate=datetime.now(),
                            status=1,
                            coinvaluedate=datetime.now(),
                            total=package,
                            amicoinvalue=90,
                            amifreezcoin=float(90),
                            amivolume=90,
                            totalinvest=package,
                            tran_type='DEBIT',
                        )
                    print("wallet entry done")

               
                    
                    # rimberioBonus=RimberioCoinDistribution.objects.filter(task='activateId').first().coin_reward
                    # getmultiplier=AllPackageDetails.objects.filter(package_price=package).first().multiplier

                    # RimberioWallet.objects.create(amount=rimberioBonus*getmultiplier,remark=f"rimberio bonus for package activation  is {rimberioBonus*getmultiplier}",trans_for="packageactivation",tran_by=toBeActivatedMember,trans_from=toBeActivatedMember,trans_to=toBeActivatedMember,trans_date=datetime.now(),trans_type='CREDIT',package_id=res)

                
                    # print("came here")
                    # assignSocialJobs(toBeActivatedMember,res)
                    
                    # distribute downline rimberiocoin
                    # print("came here")
                    # print("came here=========================================>")
                    # newMemId=str(toBeActivatedMember.memberid)
                    # invwalletId=str(res.id)
                    # try:
                    #     with connection.cursor() as cursor:
                    #         cursor.callproc('rimberio_coin_distribution_activateid', [
                    #                 newMemId,
                    #                 1*getmultiplier,
                    #                 'IdActivationDownlineDistribution',
                    #                 invwalletId
                                   
                                    
                                    
                                
                    #         ])
                            
                    #     # print("entry done")


                            
                    # except Exception as e:
                    #     print('Error occurred:', str(e))
                    #     # return "Error: Please try again later"
                    
            
                    
                except Exception as e:
                    
                    print(e)
                    logger.error(f"{datetime.now()}: An error occurred: %s", str(e))
                    # if objw:
                        
                    #     objw.delete()
                        
                    # if res:
                    #     res.delete()
                    
                    
                    
                    
                    result['status'] = 0
                    result['msg'] = "some error occured from our end"
                    result['alertMsg'] = "some error occured from our end"
                    
                    return JsonResponse(result)
                
                
                
                
                # result['status'] = 1
                # result['msg'] = "You Package has been activatd successfully"
                # result['alertMsg'] = "You Package has been activated successfully"
                
                    # sendMail(request,email=request.POST.get('email'),subject="Topup Success",template='successfullTopup',additionalParams={'withdrawal_amt': enteredAmount})
                return JsonResponse({'success': True,'msg': f'{toBeActivatedMember.username} account has been activated successfully'})

            

            
            else:
                # result['status'] = 0
                # result['message'] = "You Package activation has been failed"
                
                return JsonResponse({'success': True,'msg': 'some error occured please try again later'})

        else:
            return JsonResponse({'success': False,'msg': 'Invalid amount'})

    
    
    return render(request,'zqUsers/member/peeractivationnew.html',{
        'allPs':AllPackageDetails.objects.all()
    })


@login_required                

def filter_level_bonus(request):
    print("came here====")
    level = str(request.GET.get('level'))
    print(level)
    if level and level !='all':
        print("came here=====>")
        # filtered_data = Income2.objects.filter(position=int(level),point=int(level),intronewid=request.user.introducerid)
        filtered_data = Income2.objects.filter(position=int(level),introname=request.user.username)
        # filtered_data1 = Income2.objects.filter(point=str(1),intronewid=request.user.introducerid)
        # print( filtered_data)
        total=filtered_data.aggregate(Sum('rs'))['rs__sum'] or 0
    elif level and level=='all':
        filtered_data = Income2.objects.filter(introname=request.user.username)
        total=filtered_data.aggregate(Sum('rs'))['rs__sum'] or 0
    else:
        filtered_data = []
        total=0
    # print("came here")
    # print(filtered_data)
    # html = render_to_string('zqUsers/member/partials/levelIncPartial.html', {'allTrans': filtered_data})
    return render(request,'partials/levelIncPartial.html',context={
        'allTrans':filtered_data,
        'total':total
    })

@login_required                

def fiterlevelTeam(request):
    # print("came here====")
    level = str(request.GET.get('level'))
    # print(level)
    
    lt = get_introducer_hierarchy(request.user.username)
    # print(lt)
    # print("*****", lt)
    i=0
    # print(type(lt))
    # print(lt[0])
    
    if level and level !='all':
        # print("came here=====>")
        
        # print(lt)
        # filtered_data = Income2.objects.filter(position=int(level),point=int(level),intronewid=request.user.introducerid)
        filtered_data = [member for member in lt if int(member[1]) == int(level)]

        # filtered_data1 = Income2.objects.filter(point=str(1),intronewid=request.user.introducerid)
        # print( filtered_data)
        # total=filtered_data.aggregate(Sum('rs'))['rs__sum'] or 0
    elif level and level=='all':
        filtered_data = lt
        # total=filtered_data.aggregate(Sum('rs'))['rs__sum'] or 0
    else:
        filtered_data = []
        # total=0
    # print("came here")
    # print(filtered_data)
    # html = render_to_string('zqUsers/member/partials/levelIncPartial.html', {'allTrans': filtered_data})
    context = {'lt': filtered_data, 'i':i}
    return render(request,'partials/levelTeamPartial.html',context)


@login_required                
def adCenter(request, index = 0):
    
    rows = AllQuestions.objects.all()
    total_rows = rows.count()

    # print(request.user.memberid,"******")
    
    if request.method == 'POST':
        try:
            # Retrieve question_id and selected_choice from POST data
            
            # data=json.load(data)
            # data = json.loads(request.body)
            # print
            question_id = request.POST.get('question_id')
            selected_choice = request.POST.get('selected_choice')

            question = AllQuestions.objects.get(id=question_id)
            
            # Save submitted data to SubmittedData model
            SubmittedData.objects.create(
                submitted_by=request.user.memberid,
                question_inp=question.question,
                selected_choice=selected_choice
            )
            
            # Move to the next question
            index = int(request.POST.get('index', 0)) + 1
            
            if index < total_rows:
                # Fetch the next question
                next_question = rows[index]
                data = {
                    'question': next_question.question,
                    'choice1': next_question.choice1,
                    'choice2': next_question.choice2,
                    'choice3': next_question.choice3,
                    'choice4': next_question.choice4,
                    'question_id': next_question.id,  # Include the ID of the next question
                    'index': index
                }
                print(data['question'], data['choice1'], data['choice2'], data['choice3'], data['choice4'], data['question_id'], data['index'] )
                return JsonResponse(data)
            else:
                # All questions answered
                # survey has been submitted
                
                print("survey has been completed it came here")
                sureveeyReward=5
                
                allDirects=ZqUser.objects.filter(introducerid=request.user.memberid).count() 
                allPackages=InvestmentWallet.objects.filter(txn_by=request.user).count()
                
                if allPackages>0:
                    if allDirects==1:
                        communityBuildingBonus=CommunityBuildingBonus.objects.get(referral_requirement=1).stage_bonus
                    elif allDirects==2:
                        communityBuildingBonus=CommunityBuildingBonus.objects.get(referral_requirement=2).stage_bonus
                    elif allDirects>2:
                        communityBuildingBonus=CommunityBuildingBonus.objects.get(referral_requirement=3).stage_bonus
                    
                    
                    try:
                        inv=InvestmentWallet.objects.filter(txn_by=request.user).first()
                        invId=inv.id
                        
                        roiEnts=ROIDailyCustomer.objects.filter(userid=request.user.memberid,investment_id=invId).count()
                        newobjs=ROIDailyCustomer(userid=request.user,remark=f'ad bonus for {sureveeyReward}',total_sbg=sureveeyReward,roi_sbg=sureveeyReward,roi_date=datetime.now(),status=1,daily_amount=sureveeyReward,roi_days=roiEnts+1,investment_id=inv,usd_rate=0,zaan_rate=0,roi_sbg_usd=sureveeyReward,zaan_value_in_usd=sureveeyReward)
                        newobjs.save()
                        
                        if allDirects:
                            communityIncomeEntry=CommunityBuildingIncome(introid=request.user.id,intronewid=request.user,introname=request.user.username,rs=communityBuildingBonus,package_usd=inv.amount,rs_usd=communityBuildingBonus,status=1,point=0,package=inv.amount,nextsunday=datetime.now(),members=request.user,custid=inv.id,custnewid=request.user.memberid,custname=request.user.username,paidstatus=1,last_paid_date=datetime.now())
                            communityIncomeEntry.save()
                            
                        rimberioBonus=RimberioCoinDistribution.objects.filter(task='socialJobSubmission').first().coin_reward
                        RimberioWallet.objects.create(amount=rimberioBonus,remark=f"rimberio bonus for social job submission is {rimberioBonus}",trans_for="socialJobSubmission",tran_by=request.user,trans_from=request.user,trans_to=request.user,trans_date=datetime.now(),trans_type='CREDIT')

                    except Exception as e:
                        print(e)
                        
                else:
                    
                    rimberioBonus=RimberioCoinDistribution.objects.filter(task='socialJobSubmission').first().coin_reward
                    RimberioWallet.objects.create(amount=rimberioBonus,remark=f"rimberio bonus for social job submission is {rimberioBonus}",trans_for="socialJobSubmission",tran_by=request.user,trans_from=request.user,trans_to=request.user,trans_date=datetime.now(),trans_type='CREDIT')

                    
 
                return JsonResponse({'completed': True})
        except Exception as e:
            # Log and handle any errors
            print(f"Error: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    
    if index < total_rows:
        question = rows[index]
        return render(request, 'zqUsers/member/adCenter.html', {'question': question, 'index': index})
    else:
        
        # survey has been submitted
        print("survey has been completed it came here to redirect here")

        return redirect('newmemberDashboard')


@login_required                
def distributeSurveyReward(memberId):
    
    surveyBonus=5
    
    ROIDailyCustomer.objects.filter(userid=memberId).count()
    
    newSurveyRewatdEntry=ROIDailyCustomer(userid=memberId,remark=f'ad bonus for survey is {surveyBonus}$ ',total_sbg=surveyBonus,roi_sbg=surveyBonus,roi_date=datetime.now(),status=1,daily_amount=surveyBonus,roi_days=roiEnts+1,investment_id=obj,usd_rate=USDRate,zaan_rate=ZQLRate,roi_sbg_usd=datROIUSD,zaan_value_in_usd=obj.zaan_value_in_usd)

    
@login_required   
def changePassowrd(request):
    
    if request.method == 'POST':
        print("came here")
        form = CustomPasswordChangeForm(request.user, request.POST)
        print(request.POST)
        if form.is_valid():
            print(form.errors)
            user = form.save()
            update_session_auth_hash(request, user)  # Update the session with the new password
            messages.success(request, 'Your password was successfully updated!')
            return redirect('index')  # Redirect to the same page after successful password change
        else:
            messages.error(request, 'Credentials are invalid.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, "zqUsers/member/changePassword.html", {'form':form})

@login_required    
def adsTeam(request):
    
    return render(request,"zqUsers/member/adsTeam.html")
 
@login_required    
def kycPage(request):
    
    return render(request,"zqUsers/member/kycPage.html")
@login_required    
def spendRitcoins(request):
    
    return render(request,"zqUsers/member/spendRitcoins.html")




@login_required
def redeemRitcoins(request):
    
    if request.method == "POST":
        billamount=request.POST.get("billAmount")
        if billamount:
            try:
                billamount=float(billamount)
                
            except Exception as e:
                messages.error(request, "Please enter correct bill amount")
                return redirect("redeemRitcoins")
            
        else:
            
            messages.error(request, "Please enter correct bill amount")
            return redirect("redeemRitcoins")
        if "youtube_image" in request.FILES:  # Ensure the file is uploaded
            lolimage = request.FILES["youtube_image"]
           
            # Validate image type (allow only images)
            valid_extensions = ["image/jpeg", "image/png", "image/jpg"]
            if lolimage.content_type not in valid_extensions:
                messages.error(request, "Only JPG and PNG images are allowed.")
                return redirect("redeemRitcoins")

            # Validate file size (max 5MB)
            max_size = 5 * 1024 * 1024  # 5MB
            if lolimage.size > max_size:
                messages.error(request, "File size should not exceed 5MB.")
                return redirect("redeemRitcoins")

            # Save the image to the database
            redemption = RedeemedRitcoins(redeemed_by=request.user, image=lolimage,amount=billamount)
            redemption.save()

            messages.success(request, "Redemption request submitted successfully!")
            # return redirect("redeemRitcoins")
        else:
            messages.error(request, "No image was uploaded.")


    getallhistory=RedeemedRitcoins.objects.filter(redeemed_by=request.user)
    return render(request, "zqUsers/member/redeem-ritcoins.html",{
        "getallhistory":getallhistory
    })

@login_required    
def redeemCoins(request,site):
    
    return render(request,"zqUsers/member/redeem-coins.html",context={
        'site':site,
    })


@login_required     
def directTeam(request):
    # userid = request.user.memberid
    dt = ZqUser.objects.filter(introducerid = request.user)
    i = 0
    print(dt)
    context = {'dt': dt, 'i':i}
    return render(request,"zqUsers/member/directTeam.html", context)

@login_required 
def levelTeam(request):
    # lt = get_introducer_hierarchy(request.user.memberid)
    lt = get_introducer_hierarchy(request.user.username)
    # print(lt)
    # print("*****", lt)
    i=0
    # print(type(lt))
    # print(lt[0])
    context = {'lt': lt, 'i':i}
    return render(request,"zqUsers/member/levelTeam.html", context)


@login_required     
def directBonus(request):
    allDirectBonus=Income1.objects.filter(intronewid=request.user.memberid).order_by('-srno')
    
    if allDirectBonus.count()>0:
        gtf=allDirectBonus.first().rs
        
    else:
        gtf=0
    allreards=DirectReferalRewards.objects.filter(ref_requirement__gt=1)
    # getallents=[]
    # for reward in allreards:
    #     getent=Income1.objects.filter(intronewid=request.user.memberid)
    # # getalldicts=[ reward for reward in allrewards]
    
    
    return render(request,"zqUsers/member/directBonus.html",context={
        'allDirectBonus':gtf,
        'allRefRewards':enumerate(allreards),
    })


@login_required 
def levelBonus(request):
    
    totalDirects=ZqUser.objects.filter(introducerid=request.user,status=1).count()
    allTrans=Income2.objects.filter(intronewid=request.user.memberid)
    # print("came")
    # print(allTrans)
    return render(request,"zqUsers/member/levelBonus.html",context={
        'allTrans':allTrans,
        'total':allTrans.aggregate(Sum('rs'))['rs__sum'] or 0,
        'total_direct_members':totalDirects,
    })

@login_required    
def clubBonus(request):
    # allDirectBonus=ClubMembersIncome.objects.filter(memberid=request.user.memberid)
    club1Mems=ClubMembersIncome.objects.filter(memberid=request.user.memberid)
    return render(request,"zqUsers/member/clubBonus.html",context={
        # 'allDirectBonus':allDirectBonus
    })

@login_required 
def adBonus(request):
    
    return render(request,"zqUsers/member/adBonus.html")

@login_required     
def adsTeam(request):
    
    return render(request,"zqUsers/member/adsTeam.html")


@login_required

def addWalletAddress(request):
    
    if  request.user.withdrawal_usdt_address:
        return redirect('withdrawal')
    
    
    
    if request.method == "POST":
        # print(request.POST)
        getTransHash=request.POST.get('TransHash')
        getUSDTWDADD=request.POST.get('usdtWalletAdd')
        print(getTransHash,getUSDTWDADD)
        if (getTransHash and len(getTransHash)>5) and (getUSDTWDADD and len(getUSDTWDADD)>5):
            # print(getTransHash)
            # print(request.user)
            request.user.withdrawal_usdt_address=getTransHash
            request.user.withdrawal_tron_address=getUSDTWDADD
            request.user.save()
            # return redirect('withdrawal')
            return JsonResponse({'success': True,'msg': f'Wallet address updated successfully'})

        else:
            # messages.error(request, 'Please enter a valid address')
            return JsonResponse({'success': False,'msg': f'Please enter a valid address'})

            # return redirect('addWalletAddress')
    return render(request,"zqUsers/member/addWalletAddress.html",context={
        
        })

@login_required 
def withdrawal(request):
    
    
    if not request.user.withdrawal_usdt_address:
        return redirect('addWalletAddress')
    
    allWds=WalletAMICoinForUser.objects.filter(memberid=request.user.memberid).exclude(currency='INR')
    
    
    allWdsRT=RimberioWallet.objects.filter(tran_by=request.user.memberid,trans_for='withdraw')

    return render(request,"zqUsers/member/withdrawal.html",context={
        
        'allWds':enumerate(allWds),
        'allWdsINR':enumerate(allWdsRT),
      
    })
    
@login_required 
def groupwithdarwals(request):
    
    # allWds=WalletAMICoinForUser.objects.filter(memberid=request.user.memberid).exclude(currency='INR')
    
    
    # allWdsINR=WalletAMICoinForUser.objects.filter(memberid=request.user.memberid,currency='INR')
    allWdsINR=[]
    # totalIncome=0
    if request.user.doesMemberHaveAssocialtedIds():
        # print(self.associated_users.all())
        # print(request.user.associated_users.all())
        for user in request.user.associated_users.all():
            # print(user)
             for wd in WalletAMICoinForUser.objects.filter(memberid=user,currency='INR'):
                 allWdsINR.append(wd)
            # totalIncome+=user.totalWithdrawals()

    # return float(totalIncome)
    # # print(allWdsINR)
    # acConfirmObj=AccountComfirmation.objects.filter(uploaded_by=request.user.memberid)
    # allBanks=BankList.objects.all()
    # # print(allBanks)
    
    # if acConfirmObj.count()>0:
    #     acConfirmObj=acConfirmObj.first()
    # else:
        # acConfirmObj=None
        
        
    
    return render(request,"zqUsers/member/groupwithdrawals.html",context={
        
        # 'allWds':enumerate(allWds),
        'allWdsINR':enumerate(allWdsINR),
        # 'acConfirmObj':acConfirmObj,
        # 'allBanks':allBanks,
    })
    

def get_busd_price(request):
    # response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=binancecoin&vs_currencies=usd')
    response =  requests.get('https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=usd')
    data = response.json()
    busd_price = data['tether']['usd']
    # busd_price = data['binancecoin']['usd']
    # print(busd_price)
    # tBNB_price=int(100000)
    return JsonResponse({'price': busd_price})




def get_usdt_price():
    response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=usd')

    data = response.json()
    busd_price = data['tether']['usd']
    # print(busd_price)
    # tBNB_price=int(100000)
    return busd_price


def get_price(request, blockchain):
    if blockchain == 'ethereum':
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd')
        price = response.json()['ethereum']['usd']
    elif blockchain == 'bsc':
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=binancecoin&vs_currencies=usd')
        price = response.json()['binancecoin']['usd']
    # Add more cases for other blockchains
    else:
        return JsonResponse({'error': 'Unsupported blockchain'}, status=400)

    return JsonResponse({'price': price})

@login_required 
@csrf_exempt
def verify_transaction(request):
    print("came here==========")
    if request.method == 'POST':
    # if True:
        print("came after post")
        data = json.loads(request.body)
        transaction_hash = data.get('transactionHash')
        tranTimeCoinValue = data.get('tranTimeCoinValue')
        coinName = data.get('coinName')
        cryptoAmount = data.get('cryptoAmount')
        transactionAmountInUsd = data.get('amount')
        # print(transaction_hash,tranTimeCoinValue,coinName,cryptoAmount)
      
        
        # time.sleep(15)
        web3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))  # BSC Testnet RPC URL
      
        try:
            transaction_receipt = None
            while not transaction_receipt:
                try:
                    transaction_receipt = web3.eth.get_transaction_receipt(transaction_hash)
                    time.sleep(5)  # wait for 5 seconds before checking again
                except:
                    pass  # 
           
            
            if transaction_receipt['status'] == 1:
                
                transaction = web3.eth.get_transaction(transaction_hash)
            # print(transaction)
                if transaction:
                    # Verify the transaction details (e.g., sender, recipient, amount)
                    # Add your own logic to verify the transaction and update the user's wallet
                    sender = transaction['from']
                    recipient_contract = transaction['to']
                    input_data = transaction['input']
                    usdt_contract_address = '0x55d398326f99059fF775485246999027B3197955'
                    
                    bscscan_api_key = ""

                    abi_url = f"https://api.bscscan.com/api?module=contract&action=getabi&address={usdt_contract_address}&apikey={bscscan_api_key}"
                    response = requests.get(abi_url)
                
                    if response.status_code == 200:
                        data = response.json()
                        if data['status'] == '1': # Ensure the API call was successful
                            contract_abi = json.loads(data['result'])
                    amount = web3.from_wei(transaction['value'], 'ether')
                    amountInUSD = amount*tranTimeCoinValue
                    
                    usdt_contract = web3.eth.contract(address=recipient_contract, abi=contract_abi)
                    
                    function_name, function_params = usdt_contract.decode_function_input(input_data)
                    
                    recipient=function_params['recipient']
                    
                    if recipient.lower() == '0x83c2cc4E02b329710c5b39f5AF2c5A5922c16756'.lower():  # Your testnet receiving address
                        
                        
                        
                        try:
                            
                            
                            doesTransAlreadyExists=TransactionHistoryOfCoin.objects.filter(memberid_id=request.user.memberid,hashtrxn=transaction_hash)
                            
                            # print(doesTransAlreadyExists.count())
                            if doesTransAlreadyExists.count()>0:
                                
                                return JsonResponse({'success': False,'error': 'Transaction already exist'})
                            
                            else:
                            
                            
                                newTran=TransactionHistoryOfCoin.objects.create(
                                    cointype=coinName,
                                    memberid_id=request.user.memberid,
                                    name=sender.lower(),
                                    hashtrxn=transaction_hash,
                                    amount=amountInUSD,
                                    coinvalue=tranTimeCoinValue,
                                    trxndate=datetime.now(),
                                    status=1,
                                    coinvaluedate=datetime.now(),
                                    total=amountInUSD,
                                    amicoinvalue=tranTimeCoinValue,
                                    amifreezcoin=float(cryptoAmount),
                                    amivolume=cryptoAmount,
                                    totalinvest=amountInUSD,
                                    tran_type='CREDIT',
                                )
                                
                                # newTran.save()
                            
                            
                            
                            objw = WalletTab.objects.create(
                            # col2=topupInitiatedByUser,
                                col3="Deposit",
                                col4="ZQL Coin " + str(amountInUSD) + " is used for topup of " +request.user.email ,
                                amount=amountInUSD,
                                user_id=request.user,
                                txn_date=datetime.now(),
                                txn_type="CREDIT",
                                zql_rate=0,
                                usd_rate=0,
                                usd_value_of_zaan=amountInUSD
                            )
                        
                            objw.save()
                            
                        except Exception as e:
                            
                            print(e)
                            return JsonResponse({'success': False})
                        
                        
                        # package=float(amount)*float(100000)
                        # if activateMemberId(request,package):
                            
                            
                        return JsonResponse({'success': True,'msg': 'Funds added to your   wallet successfully'})
                            
                            
                            # wallet entry
                            
                            
                            
                            
                        # print("transaction verified")

                        
                        # else:
                        #     return JsonResponse({'success': False,'error': 'some error occured while activating your account'})
                            
                    else:
                        return JsonResponse({'success': False, 'error': 'Recipient address mismatch.'})
                else:
                    return JsonResponse({'success': False, 'error': 'Transaction not found.'})
                
                
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@login_required 
def verifyTransaction(request):
    return verify_transaction(request)
 
 
def get_usdt_abi(request):
    usdt_contract_address = '0x55d398326f99059fF775485246999027B3197955'
    bscscan_api_key = ""

    abi_url = f"https://api.bscscan.com/api?module=contract&action=getabi&address={usdt_contract_address}&apikey={bscscan_api_key}"
    response = requests.get(abi_url)

    if response.status_code == 200:
        data = response.json()
        if data['status'] == '1':  # Ensure the API call was successful
            contract_abi = json.loads(data['result'])
            return JsonResponse({'abi': contract_abi})
        else:
            return JsonResponse({'error': 'Failed to retrieve ABI'}, status=500)
    else:
        return JsonResponse({'error': 'Failed to retrieve ABI'}, status=500)
 
    

@login_required 
@csrf_exempt
def withdraw(request):
    if request.method == 'POST':
       
        data=json.loads(request.body)
        result={}
        
        
       
        if data.get('type')  == 'USD' and  data.get('what_for') == 'sendOTPWalletWd':
            
            withdrawaddress=data.get('walletAdd') 
            withdrawAmount=data.get('amount') 

            if  not withdrawAmount or float(withdrawAmount)<0:
                
                return JsonResponse({'success': False, 'error': 'please enter valid amount.'})
            # print('came')
            if not withdrawaddress:
                
                return JsonResponse({'success': False, 'error': 'please enter valid withdarwal address.'})


            try:
                if send_otp(request,email=request.user.email,subject='Withdrawal initiation from wallet',template="zqUsers/emailtemps/walletwd.html",whatfor='WALLETWITHDRAWAL'):
                        return JsonResponse({'success': True, 'error': 'please enter otp sent to your email.'})
                    
                else:
                    return JsonResponse({'success': False, 'error': 'something went wrong'})
                print('to send otp')   
            except Exception as e:
                print(str(e))
                    
       
        if data.get('type')  == 'USD'  and not (  data.get('what_for') == 'sendOTPWalletWd'):
            
            
            
            enterdOTP=data.get('wtdotp')
            # print(enterdOTP)
            if not enterdOTP:
                return JsonResponse({'success': False, 'error': 'Please enter valid otp.'})
            
            if enterdOTP != str(request.session.get('WALLETWITHDRAWALOTP')):
                
                return JsonResponse({'success': False, 'error': 'Please enter correct otp.'})
                      
            

        
            data = json.loads(request.body)
            
            user_address = data.get('account')

            # tBNBPrice= get_usdt_price()
            coinName='USDT'
            EntAmountInDollar = data.get('amount')
            # AmountToBeTransfered = float(EntAmountInDollar)*0.9
            AmountToBeTransfered = float(EntAmountInDollar)
            # adminCharg = float(EntAmountInDollar)*0.1
            # amount = float(AmountToBeTransfered)/tBNBPrice
 
            if request.user.is_withdrawal_blocked:
                return JsonResponse({'success': False, 'error': 'withdrawas have been blocked for your account please contact us on support '})


            
            if float(EntAmountInDollar)<=0:
                
                    return JsonResponse({'success': False, 'error': 'Invalid entered amount for withdrawal .'})

            if  float(EntAmountInDollar)>float(request.user.totalWithdrawalableBalance()):
            # if  float(EntAmountInDollar)>float(request.user.totalWithdrawalableBalance()):
                
                    return JsonResponse({'success': False, 'error': 'Invalid entered amount for withdrawal .'})


            try:
               

                # user_address=Web3.to_checksum_address(user_address)
                # website_address=Web3.to_checksum_address(website_address)
                
   
                
                                 
                
                # if True:
                    
                    
                newTran=TransactionHistoryOfCoin.objects.create(
                                cointype=coinName,
                                memberid_id=request.user.memberid,
                                name=request.user.email,
                                hashtrxn="",
                                amount=EntAmountInDollar,
                                coinvalue=0,
                                trxndate=datetime.now(),
                                status='pending',
                                coinvaluedate=datetime.now(),
                                total=AmountToBeTransfered,
                                amicoinvalue=0,
                                amifreezcoin=float(EntAmountInDollar),
                                amivolume=EntAmountInDollar,
                                totalinvest=0,
                                tran_type='DEBIT',
                            )
                            
                    # newTran.save()

                obj_wallet_ami_coin = WalletAMICoinForUser.objects.create(
                    email=request.user.email,
                    amicoin=EntAmountInDollar,
                    amicoinin_doller=EntAmountInDollar,
                    paystatus="success",
                    remark="success",
                    receivedate=datetime.now(),
                    trxndate=datetime.now(),
                    # trxnid=result['pay_id'],
                    trxnid="",
                    status=0,
                    withrawal_add=user_address,
                    withdrawal_bank_name=user_address,
                    admin_charge=0,
                    requested_amount=EntAmountInDollar,
                    total_value=AmountToBeTransfered,
                    memberid=request.user,
                    total_value_zaan=0,
                    withdrawl_time_zaan_rate=0,
                    transactionId=newTran,
                    currency="USDT",
                )
                    
                    
                return JsonResponse({'success': True, 'message':f'withdrawal  of {withdrawAmount} USDT  requested successfully'}) 

            
                    
                  
                 
                 
                 
                 
                # else:
                #     return JsonResponse({'success': False, 'error': 'withdrawal failed transaction not found'})                       
                            
                            
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        
        
        
        
        elif data.get('type') == 'RT' and  data.get('what_for') == 'withdrawFund':
            
    
            withdrawAmount=float(data.get('amount') )
            withdrawWalletAdd=data.get('account') 
            
            # print(withdrawAmount,withdrawWalletAdd)
            # return
            
            if withdrawWalletAdd == "" or len(str(withdrawWalletAdd))<10: 
                
                return JsonResponse({
                    'success':False,
                    'error':'Please enter valid wallet address'
                })
            if withdrawAmount<0 or (withdrawAmount > float(request.user.totalRimberioWalletBalance())):
                
                return JsonResponse({
                    'success':False,
                    'error':'Please enter valid amount to withdraw fund'
                })
            
       
            if request.user.is_withdrawal_blocked:
                return JsonResponse({
                                    'success':False,
                                    'error':'withdrawals have been blocked for this account'
                                })
                            
                            
                            
                            
            try:
                

                                
                    newrimberiocoinentry=RimberioWallet.objects.create(amount=withdrawAmount,remark="",trans_for="withdraw",tran_by=request.user,trans_from=request.user,trans_to=request.user,trans_date=datetime.now(),trans_type='DEBIT',address=withdrawWalletAdd)

                    return JsonResponse({'success': True, 'message':f'{withdrawAmount} ritcoins withdrawal to wallet requested successfully'}) 

            except Exception as e:
                print(str(e)) 
     
   
            
           
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'})
    
def randomPinCode():
    pin_codes=['110001', '400001', '700001', '600001', '560001', '380001', '500001', '411001', '208001', '380006', '800001', '695001', '302001', '600005', '641001', '834001', '600006', '560002', '560003', '500003', '500004', '560004', '560005', '600010', '641002', '641003', '641004', '641005', '641006', '641007', '641008', '641009', '641010', '641011', '641012', '641013', '641014', '641015', '641016', '641017', '641018', '641019', '641020', '641021', '641022', '641023', '641024', '641025', '641026', '641027', '641028', '641029', '641030', '641031', '641032', '641033', '641034', '641035', '641036', '641037', '641038', '641039', '641041', '641042', '641043', '641044', '641045', '641046', '641047', '641048', '641049', '641050', '641062']
    return random.choice(pin_codes)

 
def generate_random_address():
        fake = Faker('en_IN')  # 'en_IN' locale for Indian addresses

        address = {
            'street_address': fake.street_address(),
            'city': fake.city(),
            'state': fake.state(),
            'pin_code': fake.postcode()
        }

        return address

@login_required 
def sendOTPForPhoneVerification(request,phone_number,full_name):
    
    

        
        url=""
        
        headers={
            'Accept':'application/json',
        }
        
        
        # randPinCode=getRandomPinCode()
        
        # full_name=full_name.strip()
        name_parts = full_name.split()
        # print(name_parts)
    
    # Check if the name contains at least two parts
        if len(name_parts) < 2:
               first_name = name_parts[0]
               last_name = name_parts[0]
        else:
            
            first_name = name_parts[0]
            last_name = name_parts[-1]
            
        fake = Faker('en_IN')   
        data={
            'mobile_number':str(phone_number),
            'first_name':first_name,
            'last_name':last_name,
            'address1':f'{fake.street_address()},{fake.city()}',
            'address2':f'{fake.state()}',
            'pin_code':f'{randomPinCode()}'
            # 'pin_code':'fake.postcode()'
        }
        
        
        
        response=requests.post(url,data=data,headers=headers)
        print(response.json())
        if response.status_code!=200:
            

            return {
                'status':False,
                'msg':'Something went wrong'
            }
        
        else:
            
            # {'status_id': 2, 'status': 2, 'response_code': '', 'message': 'Already Registered'}
            respRes=response.json()
            
            if respRes['status']==0 and respRes['status_id']==1 :
                
                return {
                    'status':True,
                    'msg':'OTP successfully sent to your mobile number'
                }
            
            
            
            
            elif respRes['status']==2 and respRes['message']=='Already Registered':
                
                # print("came here")
                try:
                    acConfobj=AccountComfirmation.objects.create(phone_number=phone_number,pob_name=full_name,is_phone_verified=1,uploaded_by=request.user)
                except Exception as e:
                    print(e)
                return{
                    'status':True,
                    'msg':'Already Registered'
                }
            elif  respRes['status']==2 and respRes['message']=='The entered name is invalid, please correct and try again':
                
                return {
                    'status':False,
                    'msg':'Please enter a valid name'
                }    
            else:
                
                return {
                    'status':False,
                    'msg':'Something went wrong please try after siem time'
                }
                
@login_required 
def verifyOTPForPhoneVerification(request,phone_number,full_name,OTP):
    
    
    respRes={}
    if request.method=='POST':
        
        

        url=""
        
        headers={
            'Accept':'application/json',
        }
        
        data={
            'mobile_number':phone_number,
            'otp':OTP
            
        }
        
        
        try:
            response=requests.post(url,data=data,headers=headers)
            
            if response.status_code!=200:
                
                respRes['status']=0
                respRes['spanmsg']=''
                respRes['msg']='Something went wrong'
                return respRes
                
            result=response.json()

            if result['status']==0 :
                
                try:
                    acConfobj=AccountComfirmation.objects.create(phone_number=phone_number,pob_name=full_name,is_phone_verified=1,uploaded_by=request.user)

                    
                    # acConfObj=AccountComfirmation.objects.get(uploaded_by=request.user.memberid)
                    # acConfObj.is_phone_verified=True
                    # acConfObj.save()
                    
                    respRes['status']=1
                    respRes['spanmsg']='Phone number verified successfully'
                    respRes['msg']='Phone number verified successfully'
                except Exception as e:
                    respRes['status']=0
                    respRes['spanmsg']='some error occured'
                    respRes['msg']='some error occured'
                    

                return respRes
        # return JsonResponse(respRes)
                
            else:
                respRes['status']=0
                respRes['spanmsg']=''
                respRes['msg']='Invalid OTP'
                return respRes
                
            
        except Exception as e:
            # print(e)
            respRes['status']=0
            respRes['spanmsg']=''
            respRes['msg']='Something went wrong'
            return  respRes
    

@login_required 
def addBenificiary(request,accountHolder,BankName,IFSC,accountNumber,confirmAccountNumber,phone_number,bankNameId):
    
    
        print("came here=====add benificiary")
        print(phone_number)
        print(len(phone_number.strip()))
        # return
        
        phone_num=phone_number.strip()
        url=""
        
        headers={
            'Accept':'application/json',
        }
        
        data={
            'mobile_number':str(phone_num),
            'account_number':str(accountNumber),
            'beneficiary_name':str(accountHolder),
            'ifsc':IFSC,
            'bank_id':BankName,
            
            # 'pin_code':'fake.postcode()'
        }
        
        
        response=requests.post(url,data=data,headers=headers)
        
        print(response.text)
        # return
        # print( response.status_code)
        apiResp=response.json()
        # print( apiResp['errors'])
        # print( 'errors' in apiResp)
        if response.status_code!=200:
            
            if 'errors' in apiResp:
                # print("ifsc" in apiResp['errors'])
                if "ifsc" in apiResp['errors']:
                    # print("cam ehre")
                    # print(apiResp["errors"]["ifsc"])
                    return {
                    'status':False,
                    'msg':"Invalid IFSC code"
                    }
                    
                elif "account_number" in apiResp['errors']:
                    return {
                        'status':False,
                        'msg':'Invalid account number'
                        }
                elif "mobile_number" in apiResp['errors']:
                    return {
                        'status':False,
                        'msg':'Invalid mobile number'
                        }
                
                else:
                    
                    return {
                        'status':False,
                        'msg':'Something went wrong'
                    }
            
        else:
            
            apiRes=response.json()
            
            if apiRes['status']==0  :
                
                try:
                    acObj=AccountComfirmation.objects.get(uploaded_by=request.user.memberid)
                    bankName=BankList.objects.get(id=bankNameId).bank_name
                    # print(bankName)
                    # return
                    # print("came here")
                    acObj.pob_bankId=apiRes['beneficiary_id']
                    acObj.pob_name=accountHolder
                    acObj.pob_number=accountNumber
                    acObj.pob_ifsc=IFSC
                    acObj.pob_upload_date=datetime.now()
                    acObj.pob_bankName=bankName
                    acObj.is_kyc_verfied=1
                    acObj.save()
                except Exception as e:
                    print(e)
                
                
                return {
                    'status':True,
                    'msg':'Bank added successfully'
                }
                
            else:
                return {
                'status':False,
                'msg':'Something went wrong'
                }
        
@login_required        
def withdrawFund(request,amount,regBankId):
    
    
        # print("came inside withdraw fund")
        
        try:
            
            usd_rate=CustomCoinRate.objects.filter(coin_name='USD').order_by('-id').first().amount
            usdRateInINR=float(usd_rate)
            totalAmountInINR=amount*usdRateInINR
            print(totalAmountInINR)
            
            admincaharge=float(AdminWithdrawalCharge.objects.get(id=1).chargeInPercent)
            admincahargeAmount=totalAmountInINR*(admincaharge)
            totalAmountTobeSentInr=totalAmountInINR*(1-admincaharge)
            admincahargeUSD=amount*(admincaharge)
            
            totalAmountTobeSent=totalAmountInINR*(1-admincaharge)
            totalAmountTobeUSDT=amount*(1-admincaharge)
            # print(usdRateInINR,totalAmountInINR,admincaharge,admincahargeAmount,totalAmountTobeSent)
            # print(int(totalAmountTobeSent))
        
        except Exception as e:
            print(e)
    
    
        # return
        url=""
        
        headers={
            'Accept':'application/json',
        }
        
        
        acConfObj=AccountComfirmation.objects.get(id=regBankId)
        
        data={
            'mobile_number':acConfObj.phone_number,
            'beneficiary_id':acConfObj.pob_bankId,
            # 'beneficiary_name':acConfObj.accountHolder,
            'amount':int(totalAmountTobeSent),
            'channel_id':2,
            'client_id':f'{request.user.memberid}',
            'provider_id':39
            
            # 'pin_code':'fake.postcode()'
        }
        
        try:
        
            response=requests.post(url,data=data,headers=headers)
            print(response)
        except Exception as e:
            print(e)
        # print()
        # print( response.status_code)
        apiResp=response.json()
        print(apiResp)
        # print( apiResp['errors'])
        # print( 'errors' in apiResp)
        if response.status_code!=200:
            
            return {
                    'status':False,
                    'msg':"Something went wrong please try after some time"
                    }
            
            # if 'errors' in apiResp:
            #     # print("ifsc" in apiResp['errors'])
            #     if "ifsc" in apiResp['errors']:
            #         # print("cam ehre")
            #         # print(apiResp["errors"]["ifsc"])
            #         return {
            #         'status':False,
            #         'msg':"Invalid IFSC code"
            #         }
                    
            #     elif "account_number" in apiResp['errors']:
            #         return {
            #             'status':False,
            #             'msg':'Invalid account number'
            #             }
            #     elif "mobile_number" in apiResp['errors']:
            #         return {
            #             'status':False,
            #             'msg':'Invalid mobile number'
            #             }
                
            #     else:
                    
            #         return {
            #             'status':False,
            #             'msg':'Something went wrong'
            #         }
            
        else:
            
            apiRes=response.json()
     
        
        
        # {'status': 1, 'status_id': 3, 'payid': 8951998, 'message': 'Process', 'orderid': '', 'txnid': '', 'utr': '', 'amount': '11', 'transaction_date': '2024-06-08 11:11:41'}
            
            if apiRes['status']== 0 or apiRes['status']== 1 :
                   
                try:
                    
                                
                    newTran=TransactionHistoryOfCoin.objects.create(
                        cointype='USD',
                        memberid_id=request.user.memberid,
                        name=request.user.username,
                        hashtrxn=apiRes['payid'],
                        amount=amount,
                        coinvalue=usdRateInINR,
                        trxndate=datetime.now(),
                        status=1,
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
                        email=request.user.email,
                        amicoin=totalAmountInINR,
                        amicoinin_doller=amount,
                        paystatus="success",
                        remark="success",
                        receivedate=datetime.now(),
                        trxndate=datetime.now(),
                        # trxnid=result['pay_id'],
                        trxnid=apiRes['payid'],
                        status=1,
                        withrawal_add=acConfObj.pob_number,
                        withdrawal_bank_name=acConfObj.pob_bankName,
                        admin_charge=math.ceil(admincahargeAmount),
                        requested_amount=totalAmountInINR,
                        total_value= math.floor(totalAmountTobeSent),
                        memberid=request.user,
                        total_value_zaan=0,
                        withdrawl_time_zaan_rate=0,
                        transactionId=newTran,
                        currency='INR',
                    )
                        
                        # obj_wallet_ami_coin.save()
                        
                        
                                
                    objw = WalletTab.objects.create(
                        # col2=topupInitiatedByUser,
                        col3="Withdrawal",
                        col4="ZQL Coin " + str(amount) + " has been withdrawn " +request.user.email ,
                        amount=amount,
                        user_id=request.user,
                        txn_date=datetime.now(),
                        txn_type="DEBIT",
                        zql_rate=0,
                        usd_rate=0,
                        usd_value_of_zaan=0
                        )
                    
                    
                    return {
                    'status':True,
                    'msg':'Withdtawal placed successfully funds will be transferred to your bank account within 24 hours'
                    }
                

                except Exception as e:
                    print(e)
                    return {
                        'status':True,
                        'msg':'something went wrong please try after some time'
                        }
                
                
                # {'status': 2, 'status_id': 2, 'message': 'Low Balance, Refill your Account or check Amount (100 - 5000)'}
                
            elif apiRes['status'] == 2 and apiRes['message'] == 'Low Balance, Refill your Account or check Amount (100 - 5000)' :
                
                
                
                return {
                'status':False,
                'msg':"Reciver's bank is currently facing high payment failures.Please try after some time.."
                }
                
            else:
                
                return {
                    'status':False,
                    'msg':"some error occured while facilitating your transaction please try after sometime"
                    }
                
        

def WithdrawShifra(request):


    result={}
    totalBalance = request.user.totalWalletBalance()
    if request.method == "POST":
        # ZQLRate=CustomCoinRate.objects.order_by('-id').first().amount
        # ZQLRate=CustomCoinRate.objects.order_by('-id').first().amount
        # ZQLRate=CustomCoinRate.objects.filter(coin_name='ZQL').order_by('-id').first().amount
        # ZQLRate=float(CustomCoinRate.objects.filter(coin_name='ZQL').order_by('-id').first().amount)
        USDRate=float(CustomCoinRate.objects.filter(coin_name='USD').order_by('-id').first().amount)
        Client_id = request.user.memberid
        userid = request.user.id
     
        entAmount = request.POST.get('amount')
        # Amount = entAmount

        BankName = request.POST.get('Bankname')
        # print("Bank name", BankName)
        print("came  to paymentTrasnfer")
        result = PaymentTransfer(request,userid, BankName, Client_id,entAmount, ZQLRATE, totalBalance)
        # print(result)
        if result:
            response_data = {'message': "Withdrawal successful"}
            return JsonResponse({
                'status':1,
                'msg':'Withdrawal successful !'
            }) 
        else:
            response_data = {'message': "Error processing withdrawal"}
            return JsonResponse({
                'status':0,
                'msg':'Error processing withdrawal !'
            }) 

        return JsonResponse(response_data)

    else:
        response_data = {'message': "Something went wrong"} 
        return JsonResponse({
                'status':0,
                'msg':'Something went wrong!'
            }) 


def PaymentTransfer(request,userid, BankName, Client_id,Amount, ZQLRate, totalBalance):

    AmountINZAAN = float(Amount)/float(ZQLRATE)
    # dollarValueInINR=90
    dollarValueInINR=float(CustomCoinRate.objects.filter(coin_name='USD').order_by('-id').first().amount)
    AmountININR = float(Amount)*float(dollarValueInINR)
    totalBalance = request.user.totalWalletBalance()
    # print(dollarValueInINR)
    # print(AmountININR)
    # return
    if userid and BankName and Client_id and Amount:
        try:
            user = ZqUser.objects.get(id = userid)
        except:
            user = None
        if user:
            userName = user.username
        else:
            return

        ben_detail = AccountComfirmation.objects.filter(uploaded_by=user.memberid, pob_bankName__iexact=BankName)

        if ben_detail.count()>0:
            bankObj=ben_detail.first()
            benId = bankObj.pob_bankId
        else:
            return

        amountInZAAN=AmountINZAAN
        # print("balance ccnt")
        if float(Amount)<=float(totalBalance):
        
            try:
                  
                    # print("wallet entry done")

                    obj_wallet_ami_coin = WalletAMICoinForUser.objects.create(
                        email=user.email,
                        amicoin=ZQLRATE,
                        amicoinin_doller=Amount,
                        paystatus="Pending",
                        remark="Request Pending",
                        receivedate=datetime.now(),
                        trxndate=datetime.now(),
                        # trxnid=result['pay_id'],
                        trxnid='',
                        status=0,
                        withrawal_add='',
                        withdrawal_bank_name=BankName,
                        admin_charge=0,
                        requested_amount=Amount,
                        total_value=Amount,
                        memberid=user,
                        total_value_zaan=AmountINZAAN,
                        withdrawl_time_zaan_rate=ZQLRATE
                    )
                    
                    obj_wallet_ami_coin.save()
                
           
            except Exception as e:
                    
                    print("some error occured",e)
                    return False
                    
                # print("Transaction ststus before",tranStatus)

            # print(" came to tranStatus")
            tranStatus=PaymentTransferMain(request,obj_wallet_ami_coin.id, float(Amount),BankName)
            if tranStatus:
                
            
                return True
            
            else:
                return False
            
            
          
        else:
            return False
    else:
        # print("Please select all fields..")
        return False
    


def PaymentTransferMain(request,wdId,amount,BankName):

    # print("came here")
    # return
    try:
        walletAMITranObj=WalletAMICoinForUser.objects.get(id=wdId)
        # print(walletAMITranObj)
    except:
        return False
    
    # print("gaiankkk")
    userid=walletAMITranObj
    # print(walletAMITranObj.memberid.memberid )     

    user = ZqUser.objects.get(memberid = walletAMITranObj.memberid.memberid)
    # user = request.user
    Client_id=user.memberid
    # print(user.username)

    
    Amount=float(walletAMITranObj.total_value)
    # Amount=amount
    totalBalance=float(user.totalWalletBalance())
    
    if not float(Amount)<=float(totalBalance):
        print("Insufficient Wallet Balance")
        return False
        
    
    # print("cam again")
    # ZQLRate=CustomCoinRate.objects.order_by('-id').first().amount
    # ZQLRate=CustomCoinRate.objects.filter(coin_name='ZQL').order_by('-id').first().amount
    # ZQLRate=float(CustomCoinRate.objects.filter(coin_name='ZQL').order_by('-id').first().amount)
    USDRate=float(CustomCoinRate.objects.filter(coin_name='USD').order_by('-id').first().amount)    
    BankName=walletAMITranObj.withdrawal_bank_name
    # BankName=BankName
    # print(BankName)
    AmountINZAAN = float(Amount)/float(ZQLRATE)
    dollarValueInINR=CustomCoinRate.objects.filter(coin_name='USD').order_by('-id').first().amount
    AmountININR = float(Amount)*float(dollarValueInINR)

    # print(BankName,Client_id,Amount)
    # return
    
    # print("=========================>lllll")
    
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
       
        print("=========================>mmmmmmm")
        AccountComfirmationObj = AccountComfirmation.objects.filter(uploaded_by=user.memberid, pob_bankName__iexact=BankName)

        Mobile_number = user.phone_number
     
        ben_detail = AccountComfirmationObj

        if ben_detail.count()>0:
            bankObj=ben_detail.first()
            benId = bankObj.pob_bankId
        else:
            return False
        

        # print("came")
        # print("=========================>nnnnn")
        base_url = ""
        delete_beneficiary_url = base_url + "delete_beneficiary"
        transfer_url = base_url + "transfer"
        # print("Transfer url",transfer_url)
        headers = {
            "Accept": "application/json",
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
            
            

            objw = WalletTab.objects.create(
                        # col2=topupInitiatedByUser,
                        col3="Withdrawal",
                        col4="ZQL Coin " + str(AmountINZAAN) + " is used for topup of " +user.email ,
                        amount=AmountINZAAN,
                        user_id=user,
                        txn_date=datetime.now(),
                        txn_type="DEBIT",
                        zql_rate=ZQLRATE,
                        usd_rate=USDRATE,
                        usd_value_of_zaan=float(AmountINZAAN)*ZQLRATE
                    )
                    
            objw.save()
            walletAMITranObj.status=1
            walletAMITranObj.save()
            return True

        
                    

        elif result['status']==2:
            print(result.message)
            return False
            
 
    else:
        print("Please select all fields..")
        return False




@login_required 
def walletHistory(request):
    
    # if not request.user.username == 'Hemant':
        
    allDs = request.user.transaction_history.filter(tran_type='CREDIT')
    getWallAdd=DepositWallet.objects.all().order_by('-id').first().address


    return render(request,"zqUsers/member/walletHistory.html",context={
        'allDs':allDs,
        'wallAdd':getWallAdd,
    })


    
 
@login_required 
def rimberiowallet(request):
    
    allTrans = request.user.RimberioWallet_tranby_member.all()

    return render(request,"zqUsers/member/rimberiowallet.html",context={
        'allTrans':allTrans,
        'title':'All coin earnings'
    })
    
 
 
@login_required 
def rimberiowalletsocialjobs(request):
    
    allTrans = RimberioWallet.objects.filter(trans_for='socialJobSubmission',tran_by=request.user)

    return render(request,"zqUsers/member/rimberiowallet.html",context={
        'allTrans':allTrans,
        'title':'Socialjob coin earnings'
    })
    
 
 
@login_required 
def rimberiowalletlevel(request):
    
    # allTrans = request.user.RimberioWallet_tranby_member.all()
    allTrans = RimberioWallet.objects.filter(remark='direct income',tran_by=request.user)

    return render(request,"zqUsers/member/rimberiowallet.html",context={
        'allTrans':allTrans,
        'title':'Level Account Activation coin earnings',
        'whatFor':'direct',
    })
    
@login_required 
def rimberiowalletlevelSocialJobs(request):
    
    # allTrans = request.user.RimberioWallet_tranby_member.all()
    allTrans = RimberioWallet.objects.filter(trans_for='IdActivationDownlineDistribution',tran_by=request.user)

    return render(request,"zqUsers/member/rimberiowallet.html",context={
        'allTrans':allTrans,
        'title':'Level Account Activation coin earnings'
    })
    
@login_required 
def rimberiowalletpackageactivation(request):
    
    # allTrans = request.user.RimberioWallet_tranby_member.all()
    allTrans = RimberioWallet.objects.filter(remark='ritcoins reward for activating your account is 100000',tran_by=request.user)

    return render(request,"zqUsers/member/rimberiowallet.html",context={
        'allTrans':allTrans,
        'title':'Package activation coin reward'
    })
    
 
 
@login_required 
def rimberiowalletsocialjobslevel(request):
    
    # allTrans = request.user.RimberioWallet_tranby_member.all()
    allTrans = RimberioWallet.objects.filter(trans_for='SocialJobSubmitDownlineDistribution',tran_by=request.user)

    return render(request,"zqUsers/member/rimberiowallet.html",context={
        'allTrans':allTrans,
        'title':'Team Social Job Submission coin reward'
    })
    

 
def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    print(ext)
    valid_extensions = ['.jpg', '.jpeg', '.png']
    if ext.lower() not in valid_extensions:
        
        print("Unsupported file extension.")
        return False
    
    else:
        return True


@login_required 
def custom_logout(request):
    logout(request)
    return redirect('login')



@login_required 
def quiz_view(request):
    questions = Question.objects.all()
    return render(request, 'quiz/quiz.html', {'questions': questions})


# @login_required 
def preConfirmEmail(request):
        return render(request, 'zqUsers/member/preemailconfirmlogin.html')
 
 
@login_required    
def magicbonus(request):
        # currentDate=datetime.now()
        # if is_naive(currentDate):
        #     currentDate=make_aware(currentDate)
            
        # allTrans=MagicalIncome.objects.filter(intronewid=request.user.memberid,last_paid_date__lt=currentDate)
        # print(allTrans.aggregate(Sum('rs'))['rs__sum'] or 0)
            # lt = get_introducer_hierarchy(request.user.memberid)
    totalDirects=ZqUser.objects.filter(introducerid=request.user,status=1).count()

    lt = get_introducer_hierarchy(request.user.username)
   
    # allMagicIncomesTotal=[ tuple(list(tp).append(tp[0].getMagicalBonusTotal(request.user)))  for tp in lt]
    allMagicIncomesTotal = [ tuple(list(tp) + [tp[0].getMagicalBonusTotal(request.user)]) for tp in lt if tp[0].getMagicalBonusTotal(request.user)>0]
    # allMagicIncomesTotal = [ tuple(list(tp) + []) for tp in lt if >0]

            
            
        
        

    allMb=0
    for mb in allMagicIncomesTotal:
        allMb+=mb[2]
    
    allMagicIncomesTotalNew=[]
    for lst in allMagicIncomesTotal:
        # newlst=list(lst)
        getrate=MagicBonusDetails.objects.filter(level=lst[1])
        if getrate.count()>0:
            rt=getrate.first().bonus_percent
            allMagicIncomesTotalNew.append(list(lst)+[rt])
    # for b in allMagicIncomesTotal:
        
    # print(allMagicIncomesTotalNew)
    # print(allMagicIncomesTotal)
    i=0
   
    # context = {'lt': lt, 'i':i}
    context = {'lt': allMagicIncomesTotalNew, 'i':i, 'total':allMb,'total_direct_members':totalDirects}

    return render(request, 'zqUsers/member/magicbonus.html',context)


   
@login_required    
def viewMagicBonusDetails(request,memid):
#    print(memid)
    user=ZqUser.objects.get(id=memid)
    # print(user)
    
    currDate=datetime.now()    
    totalBonus=0
    if is_naive(currDate):
        currDate=make_aware(currDate)
        
    allSjs= MagicalIncome.objects.filter(members=user,intronewid=request.user.memberid)
    allValid=[]
    for sj in   allSjs:
        sjRoidate=sj.last_paid_date
        if is_naive(sjRoidate):
            sjRoidate=make_aware(sjRoidate)
            
        if  sjRoidate<currDate:
            allValid.append(sj)
                
                
    # print("came hee")      
    # print(allValid)    
    #     return  totalBonus
    # getAllMBonus=
    
    # print(getAllMBonus)
    print("came to redraw")
    return render(request,'partials/magicincpartial.html',context={
        'allTrans':allValid,
        # 'total':total
    })

    # return render(request, 'zqUsers/member/magicIncDetailed.html' ,{
    #     'allTrans':allValid,
       
    # })
    
    
@login_required    
def bonusReport(request):
       
    # Fetch the package activation date from the user session
    activation_date = request.user.activationdate
    today = datetime.now().date()
    def format_date(date):
        return date.strftime('%Y-%m-%d') if date else None
    # Filter income records from the activation date to today
    direct_income = request.user.income1_intros.filter(last_paid_date__range=[activation_date, today]).values('rs', 'last_paid_date')
    level_income = request.user.income2_intros.filter(last_paid_date__range=[activation_date, today]).values('rs', 'last_paid_date')
    magic_income = request.user.magicalIncome_intros.filter(last_paid_date__range=[activation_date, today]).values('rs', 'last_paid_date')
    community_building_income = request.user.communitybuilding_receiver.filter(bonus_received_date__range=[activation_date, today]).values('received_bonus', 'bonus_received_date')
    club_income = request.user.clubIncomeMember_zquser.filter(activation_date__range=[activation_date, today]).values('bonus_income', 'activation_date')
    social_income = request.user.roiDailyMember_zquser.filter(roi_date__range=[activation_date, today]).values('roi_sbg', 'roi_date')

    # Combine the incomes for the same date
    income_data = list(direct_income) + list(level_income) + list(magic_income) + list(community_building_income) + list(social_income)+ list(club_income)
    combined_data = {}
     # Process direct income
    for income in direct_income:
        date =format_date(income['last_paid_date'])
        if date not in combined_data:
            combined_data[date] = {
                'direct_income': 0,
                'level_income': 0,
                'magic_income': 0,
                'community_building_income': 0,
                'club_income': 0,
                'social_income': 0
            }
        combined_data[date]['direct_income'] += income['rs']

    # Process level income
    for income in level_income:
        date = format_date(income['last_paid_date'])
        if date not in combined_data:
            combined_data[date] = {
                'direct_income': 0,
                'level_income': 0,
                'magic_income': 0,
                'community_building_income': 0,
                'club_income': 0,
                'social_income': 0
            }
        combined_data[date]['level_income'] += income['rs']

    # Process magic income
    for income in magic_income:
        date = format_date(income['last_paid_date'])
        if date not in combined_data:
            combined_data[date] = {
                'direct_income': 0,
                'level_income': 0,
                'magic_income': 0,
                'community_building_income': 0,
                'club_income': 0,
                'social_income': 0
            }
        combined_data[date]['magic_income'] += income['rs']

    # Process community building income
    for income in community_building_income:
        date =format_date(income['bonus_received_date'])
        if date not in combined_data:
            combined_data[date] = {
                'direct_income': 0,
                'level_income': 0,
                'magic_income': 0,
                'community_building_income': 0,
                'club_income': 0,
                'social_income': 0
            }
        combined_data[date]['community_building_income'] += income['received_bonus']

    # Process club income
    for income in club_income:
        date = format_date(income['activation_date'])
        if date not in combined_data:
            combined_data[date] = {
                'direct_income': 0,
                'level_income': 0,
                'magic_income': 0,
                'community_building_income': 0,
                'club_income': 0,
                'social_income': 0
            }
        combined_data[date]['club_income'] += income['bonus_income']

    # Process social income
    for income in social_income:
        date =format_date( income['roi_date'])
        if date not in combined_data:
            combined_data[date] = {
                'direct_income': 0,
                'level_income': 0,
                'magic_income': 0,
                'community_building_income': 0,
                'club_income': 0,
                'social_income': 0
            }
        combined_data[date]['social_income'] += income['roi_sbg']
   
    
    data = []
    for date, income in combined_data.items():
        if any(income.values()):  # Include date if at least one field is non-zero
            data.append({'date': date, **income})
    # print(data)
    # return JsonResponse()
    return render(request, 'zqUsers/member/bonusReport.html',context={'data': enumerate(data)})
        
    
    
@login_required    
def socialmedia(request):
    
    
        result={}
        
        
        doesuserhavesubmittedform=SubmittedDataForSocialMedia.objects.filter(uploadedby=request.user)
        if doesuserhavesubmittedform.count()>0:
            if  doesuserhavesubmittedform.first().status:
                # messages.warning(request, '')
                return redirect('activation')
        
        if request.method=='POST' :

            if request.POST.get('socialJobTaskSubmit')=='submitted':
                
                print("came here")
                form = SubmittedDataForSocialMediaForm(request.POST, request.FILES)
        
                
             
              
               
                if form.is_valid():
               
                    
                                    
                        
                    if 'youtube_image' in request.FILES:
                        # whatFor='youtube'
                        ytImage=request.FILES.get('youtube_image')

                    if 'insta_image' in request.FILES:
                        # whatFor='instagram'
                        instaUpload=request.FILES.get('insta_image')
                    #  return
                    
                    # it is telegram image
                    if 'twitter_image' in request.FILES:
                        # whatFor='twitter'
                        twitterUpload=request.FILES.get('twitter_image')
               
                                
                    try:
                        
                        # if packageId:
                        #     invObj=InvestmentWallet.objects.get(id=packageId)
                            
                        # else:
                        #     invObj=None 
                        
                        print("came here")
                        saveData=SubmittedDataForSocialMedia(twitter_image=twitterUpload,youtube_image=ytImage,insta_image=instaUpload,uploadedby=request.user,whatfor="",status=1)
                        
                        saveData.save()
                        print('data is saved successfully')
                        # assignTask=AssignedSocialJob.objects.get(id=assignedTaskId)
                        # assignTask.status=True
                        # assignTask.save()
                        # print(f"Data is {saveData.uploaddate},{saveData.uploaddate},{saveData.uploadedby.username} ")
                        
                    except Exception as e:
                        print(str(e))
                        
            
    
        
        
                    messages.success(request,'social tasks submitted successfully')
                    return redirect('activation')
       

                
                    
                else:
                    
                    messages.error(request,'Please submit all tasks')
                    socialJobIns=SocialJobs.objects.all().order_by('-id').first()
                    return render(request, 'zqUsers/member/socialmedia.html',context={
                        'form':form,
                        'ytUrl':socialJobIns.youtube_link,
                        'facebook':socialJobIns.fb_link,
                        'twitter':socialJobIns.twitter_link,
                        'instagram':socialJobIns.insta_link,
                        'greviews':socialJobIns.greview_link,
                        'surveyId':socialJobIns.id,
                        'packageId':1,
                        'assignedTaskId':1
                    })
                    
                    #  return
            else:
                
               
              
                
                # socialJobId=request.POST.get('socialJobId')
                # packageId=request.POST.get('packageId')
                # assignedTaskId=request.POST.get('assignedTaskId')
                allUrls=SocialJobs.objects.all().order_by('-id').first()
                # print(socialJobId,packageId)
                return render(request, 'zqUsers/member/socialmedia.html',context={
                    'ytUrl':allUrls.youtube_link,
                    'facebook':allUrls.fb_link,
                    'twitter':allUrls.twitter_link,
                    'instagram':allUrls.insta_link,
                    'greviews':allUrls.greview_link,
                    'surveyId':1,
                    'packageId':1,
                    'assignedTaskId':1,
                })
            
                
                
        allUrls=SocialJobs.objects.all().order_by('-id').first()
            
        return render(request, 'zqUsers/member/socialmedia.html',context={
            'ytUrl':allUrls.youtube_link,
            'facebook':allUrls.fb_link,
            'twitter':allUrls.twitter_link,
            'instagram':allUrls.insta_link,
            'greviews':allUrls.greview_link,})
        
        
        

# @login_required    
def mailConfirmPage(request):
        return render(request, 'zqUsers/member/mailConfirmPage.html')

@login_required    
def coutdownkyc(request):
    
    
    # print(f"{request.user.memberid} is associated id {request.user.isGroupedId()}")
    allPackages=InvestmentWallet.objects.filter(txn_by_id=request.user.memberid)
    allSocialJobs=SocialJobs.objects.all()

            
    current_date = timezone.now()
    
    allPs=InvestmentWallet.objects.filter(txn_by_id=request.user.memberid)
    
    
    allvalidAssignedJobs=[]
    allvalidAssignedGroupJobs=[]
    
    if allPs.count()>0:
        for package in allPs:
            
            allAssigndJobs=AssignedSocialJob.objects.filter(assigned_to=request.user.memberid,valid_upto__gt=current_date,package_id=package.id)
            
            if allAssigndJobs.count()>0:
                if allAssigndJobs.order_by('id').first().package_id.group_id:
                    allvalidAssignedGroupJobs.append(allAssigndJobs.order_by('id').first())
                else:
                    allvalidAssignedJobs.append(allAssigndJobs.order_by('id').first())
            
    else:
        
        allAssigndJobs=AssignedSocialJob.objects.filter(assigned_to=request.user.memberid,valid_upto__gt=current_date)
            
        if allAssigndJobs.count()>0:
    # print(AssignedSocialJob.objects.filter(assigned_to=request.user.memberid,valid_upto__gt=current_date).order_by('id').first())
            allvalidAssignedJobs.append(allAssigndJobs.order_by('id').first() )


    if allvalidAssignedGroupJobs:
        allvalidAssignedJobs.append(allvalidAssignedGroupJobs[0])
    allSubmittedJobs=[]
    allCompletedSocialJobs=ROIDailyCustomer.objects.filter(userid=request.user.memberid).order_by('-roi_date')
    # roi_date_instance = ROIDailyCustomer.objects.filter(userid=request.user.memberid, id=154536).first()

    allValidJobsTillNow=[]
    allGroupedJobs=[]
    for sjb in  allCompletedSocialJobs:
        
        
        if timezone.is_naive(sjb.roi_date):
                sjb.roi_date = make_aware(sjb.roi_date, timezone.get_current_timezone())

        current_datetime = timezone.now()
        
        if timezone.is_naive(current_datetime):
            
            current_datetime = make_aware(current_datetime, timezone.get_current_timezone())
        
        if sjb.roi_date<current_datetime:
            # allValidJobsTillNow.append(sjb)
            sjb.job_status=1
        else:
            sjb.job_status=0
            
        allValidJobsTillNow.append(sjb)
        
     

    return render(request, 'zqUsers/member/coutdownkyc.html',{
            'subscriptions':allvalidAssignedJobs,
            # 'allSubmittedSurveys':enumerate(SubmittedDataForSocialMedia.objects.filter(uploadedby=request.user.memberid).order_by('-uploaddate')),
            'allSubmittedSurveys':enumerate(allValidJobsTillNow)
        })
   
@login_required    
def groupcoutdownkyc(request):
    
    
    
    allAssociatedUsers=ZqUser.objects.filter(associated_id=request.user.memberid)
    allPackages=[]
    
    for user in allAssociatedUsers:
        
        for inv in InvestmentWallet.objects.filter(txn_by=user):
            # print(f"{user.memberid} is associated id {user.isGroupedId()}")
            allPackages.append(inv)
       
    # print("came here")     
    # print(allPackages)     
    allSocialJobs=SocialJobs.objects.all()
    # if allPackages.count()>0:
    #     isPaidUser=True
    # else:
    #     isPaidUser=False
    
    # if isPaidUser:
        
    #     for package in allPackages:
    #         for socialjob in  allSocialJobs:
    #             assignedJobsForThisPackage=AssignedSocialJob.objects.filter(assigned_to=request.user.memberid,package_id=package.id,social_job_id=socialjob.id).count()
    #             if assignedJobsForThisPackage>0:
    #                 continue
    #             else:
    #                 allPreviousPackagesCount=AssignedSocialJob.objects.filter(assigned_to=request.user.memberid,package_id=package.id)
                    
    #                 if allPreviousPackagesCount.count()>0:
                        
    #                     lastObj=allPreviousPackagesCount.order_by('-id').first()
    #                     newEntryForThisPackage=AssignedSocialJob(assigned_to=request.user,package_id=package,social_job_id=socialjob,valid_from=lastObj.valid_upto,valid_upto=lastObj.valid_upto+timedelta(days=5)+ timedelta(days=2))
    #                     newEntryForThisPackage.save()
    #                 else:
    #                     newEntryForThisPackage=AssignedSocialJob(assigned_to=request.user,package_id=package,social_job_id=socialjob,valid_from=package.txn_date,valid_upto=package.txn_date+timedelta(days=5)+ timedelta(days=2))
    #                     newEntryForThisPackage.save()
                        
                
    # else:
        
    #         for socialjob in  allSocialJobs:
                
    #             assignedJobsForThisPackage=AssignedSocialJob.objects.filter(assigned_to=request.user.memberid,social_job_id=socialjob.id).count()
    #             if assignedJobsForThisPackage>0:
    #                 continue
    #             else:
    #                 allPreviousPackagesCount=AssignedSocialJob.objects.filter(assigned_to=request.user.memberid)
    #                 if allPreviousPackagesCount.count()>0:
    #                     lastObj=allPreviousPackagesCount.order_by('-id').first()
    #                     newEntryForThisPackage=AssignedSocialJob(assigned_to=request.user,social_job_id=socialjob,valid_from=lastObj.valid_upto,valid_upto=lastObj.valid_upto+timedelta(days=5)+ timedelta(days=2))
    #                     newEntryForThisPackage.save()
    #                 else:
    #                     newEntryForThisPackage=AssignedSocialJob(assigned_to=request.user,social_job_id=socialjob,valid_from=request.user.date_joined,valid_upto=request.user.date_joined+timedelta(days=5)+ timedelta(days=2))
    #                     newEntryForThisPackage.save()
                        
            
    current_date = timezone.now()
    
    # allPs=InvestmentWallet.objects.filter(txn_by_id=request.user.memberid)
    allPs=allPackages
    
    # print(allPs)
    
    
    allvalidAssignedJobs=[]
    
    if len(allPs)>0:
        for package in allPs:
            
            allAssigndJobs=AssignedSocialJob.objects.filter(assigned_to=package.txn_by.memberid,valid_upto__gt=current_date,package_id=package.id)
            
            if allAssigndJobs.count()>0:
                allvalidAssignedJobs.append(allAssigndJobs.order_by('id').first())
            
    else:
        
        allAssigndJobs=AssignedSocialJob.objects.filter(assigned_to=request.user.memberid,valid_upto__gt=current_date)
            
        if allAssigndJobs.count()>0:
    # print(AssignedSocialJob.objects.filter(assigned_to=request.user.memberid,valid_upto__gt=current_date).order_by('id').first())
            allvalidAssignedJobs.append(allAssigndJobs.order_by('id').first() )

    # print("to be printed")
    # print(allvalidAssignedJobs)
    # print("to be printed")
    
    
    # allCompletedSocialJobs=AssignedSocialJob.objects.filter(assigned_to=request.user.memberid,status=1).order_by('-valid_from')
    # allCompletedSocialJobs=ROIDailyCustomer.objects.filter(userid=request.user.memberid).order_by('-roi_date')
    # print(ROIDailyCustomer.objects.filter(userid=request.user.memberid,id=154536).first().roi_date) #2024-06-27 00:00:00
    # print()
    
    # current_datetime = timezone.now()
    # print(datetime.now()) #2024-06-27 14:44:40.600576
    
    allSubmittedJobs=[]
    allCompletedSocialJobs=[]
    # allCompletedSocialJobs=ROIDailyCustomer.objects.filter(userid=request.user.memberid).order_by('-roi_date')
    
    for user in allAssociatedUsers:
        for rdi in ROIDailyCustomer.objects.filter(userid=user.memberid).order_by('-roi_date'):
           allCompletedSocialJobs.append(rdi) 
        
    # roi_date_instance = ROIDailyCustomer.objects.filter(userid=request.user.memberid, id=154536).first()

    allValidJobsTillNow=[]

    for sjb in  allCompletedSocialJobs:
        
        
        if timezone.is_naive(sjb.roi_date):
                sjb.roi_date = make_aware(sjb.roi_date, timezone.get_current_timezone())

        current_datetime = timezone.now()
        
        if timezone.is_naive(current_datetime):
            
            current_datetime = make_aware(current_datetime, timezone.get_current_timezone())
        
        if sjb.roi_date<current_datetime:
            # allValidJobsTillNow.append(sjb)
            sjb.job_status=1
        else:
            sjb.job_status=0
            
        allValidJobsTillNow.append(sjb)
        
     
    # if request.user.doesMemberHaveAssocialtedIds():
    allvalidAssignedJobs=[allvalidAssignedJobs[0]]
    # else:
            
    # print(allCompletedSocialJobs)
    return render(request, 'zqUsers/member/coutdownkyc.html',{
            'subscriptions':allvalidAssignedJobs,
            # 'allSubmittedSurveys':enumerate(SubmittedDataForSocialMedia.objects.filter(uploadedby=request.user.memberid).order_by('-uploaddate')),
            'allSubmittedSurveys':enumerate(allValidJobsTillNow)
        })
   
    
@login_required    
def community(request):
        return render(request, 'zqUsers/member/community.html')
    
    


def get_introducer_hierarchy(member_id):
    # print(member_id)
    # Initialize the hierarchy list
    hierarchy = []

    # Retrieve the member with the given ID
    # member = ZqUser.objects.get(memberid=member_id)
    # print(member_id)
    member = ZqUser.objects.get(username=member_id)
    # print(member)
    # Add the member to the hierarchy with level 0
    hierarchy.append((member, 0))

    # Retrieve all the members introduced by the current member recursively
    def get_indirect_introducers(member, level):
        # Retrieve the indirect introducers of the current member
        # introducers = member.introduced_users.all()
        introducers = member.introducer_usernames.all()
        
        # Increment the level for the next level of introducers
        level += 1
        
        # Iterate over the indirect introducers
        for introducer in introducers:
            # Add the introducer to the hierarchy with its level
            # print(introducer.memberid)
            if introducer:
                hierarchy.append((introducer, level))
            else:
                break
            
            # Recursively call the function to get the introducers of the current introducer
            get_indirect_introducers(introducer, level)

    # Call the function to get the indirect introducers of the current member
    get_indirect_introducers(member, 0)

    return hierarchy


def CompletedTasks(request):
    return render(request, 'zqUsers/member/completedSocialJobs.html')



@login_required
def makePayment(request):
    
    # data = json.loads(request.body)
    # print(data)
    # result={}
    # amount=request.POST.get('amount')
    
    # if request.method=='POST':
    #     Entamount=float(request.POST.get('amount'))
    #     print(Entamount)
    # # return
    
    # print(amount)
    # return
    # current_user = request.user
    # userid = request.user.id
    
    
    # if current_user.first_name:
    #     uName=current_user.first_name
    # else:
    #     uName=current_user.username
        
    # if current_user.phone_number:
    #     uPhone=current_user.phone_number
    # else:
    #     uPhone='0123456789'
        
    # print("count is",uPhone.count())
    # return
    if request.method == "POST":
        
        result={}
        Entamount=float(request.POST.get('amount'))
        print(Entamount)
        
        current_user = request.user
        userid = request.user.id
        
        
        if current_user.first_name:
            uName=current_user.first_name
        else:
            uName=current_user.username
            
        if current_user.phone_number:
            uPhone=current_user.phone_number
        else:
            uPhone='0123456789'
        
        # logger.error(f"{datetime.now()} An error occurred: %s", 'LOL')
        url = "https://api.ekqr.in/api/create_order" 

        # usrName = current_user.first_name 
        # print(amoEntamountunt)

        payload ={
            "key" : "",
            "customer_name": uName,
            "customer_email": current_user.email,
            "client_txn_id": f"{current_user.id}_{uuid.uuid4()}_{timezone.now().strftime('%Y%m%d%H%M%S')}",
            "amount": str(Entamount),
            "p_info": "Product Name",
            "customer_mobile": uPhone,
            "redirect_url": ""+reverse('checkPayment'),
        }
        # print(request.POST.get('amount'))
        headers ={
            'content-type' : "application/json"
        }
        
        try:
            
            # print(uPhone)
            # response = requests.post(url, headers=headers, json=payload)
            response = requests.request("POST", url, headers=headers, json=payload)
            
            # print(response.status_code)
            
            # return
            if response.status_code == 200:
                res = response.json()
                print(res)
                print(res['msg']=='Merchant not Found or Logout.')
                # print(res['status']==False)
                if res['status'] is False and res['msg'].strip()=='Merchant not Found or Logout.':
                    # print("came hee")
                    result['status']=0
                    result['msg']='This payment mode is not available right now please try after sometime'
                    return JsonResponse(result)
                
                if res['status']==True:
            
                        try:
                            # print(result.get('status'))
                            if res.get('status'):
                            # print()
                                request.session['client_txn_id'] = payload['client_txn_id']
                                saveQr=QrTransDetails(memberid=request.user.memberid,client_txn_id=payload['client_txn_id'],amount=float(Entamount))
                                # print(request.session.get('client_txn_id'))
                                saveQr.save()
                                result['status']=1
                                result['msg']="success"
                                result['url']=res['data']['payment_url']

                                return JsonResponse(result) 
                            else:
                                
                                result['status']=0
                                result['msg']="some error occured from our side please try after some time"
                                return JsonResponse(result)
                                # result['url']=result['data']['payment_url']

                                # return JsonResponse(result) 
                        except Exception as e:
                            # logger.error("An error occurred: %s", str(e))
                            # print(str(e))
                            logger.error(f"{datetime.now()}: An error occurred: %s", str(e))
                            result['status']=0
                            result['msg']="some error occured from our side please try after some time"
                            return JsonResponse(result)
                
                
                
                else:
                    result['status']=0
                    result['msg']='This payment mode is not available right now please try after sometime '
                    return JsonResponse(result)
                       
                    
            else:
                
                logger.error(f"{datetime.now()} :An error occurred: %s", str(e))
                result['status']=0
                result['msg']='This payment mode is not available right now please try after sometime'
                return JsonResponse(result)
                        


        except Exception as e:
            logger.error(f"{datetime.now()} :An error occurred: %s", str(e))
            result['status']=0
            result['msg']='This payment mode is not available right now please try after sometime'
            return JsonResponse(result)
                

    # else:
    #     result['status']=0
    #     result['message']='This payment mode is not available right now please try after sometime'
    return redirect('walletHistory')  
    # return render(request, "AdminDashboard/student.html", {'curr_user':curr_user})
    # return HttpResponse('lllllllllllllllllll')



def get_web3():
    
    RPC_URL = "https://blockchain.ramestta.com"
    web3 = Web3(Web3.HTTPProvider(RPC_URL))

    syncing_status = web3.eth.syncing
    if syncing_status:
        RPC_URL = "https://blockchain2.ramestta.com"
    web3 = Web3(Web3.HTTPProvider(RPC_URL))

    # Apply PoA middleware
    web3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
    
    # Check if web3 is connected
    if not web3.is_connected():
        raise ConnectionError("Failed to connect to the blockchain")
        # return False
    return web3
    


def get_wallet_balance(wallet_address):
    """
    Calculates the total balance of a wallet on the Ramestta blockchain.

    Parameters:
    - wallet_address (str): The address of the wallet.

    Returns:
    - float: The wallet balance in RAMA (or Ether).
    """
    try:
        # RPC URL for the Ramestta blockchain
        RPC_URL = "https://blockchain2.ramestta.com"
        web3 = Web3(Web3.HTTPProvider(RPC_URL))

        # Apply PoA middleware
        web3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

        # Check connection
        if not web3.is_connected():
            raise ConnectionError("Failed to connect to the blockchain")

        # Get balance in Wei (smallest denomination of RAMA/Ether)
        balance_in_wei = web3.eth.get_balance(wallet_address)

        # Convert Wei to RAMA/Ether
        balance_in_rama = web3.from_wei(balance_in_wei, 'ether')

        return float(balance_in_rama)

    except Exception as e:
        print(f"Error fetching wallet balance: {e}")
        raise

def get_rama_price():
    # Replace with your CoinMarketCap API Key
    api_key = ""
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

    # Parameters for the API call
    parameters = {
        "symbol": "RAMA",  # Replace with the symbol for RAMA
        "convert": "USDT"
    }

    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": api_key,
    }

    try:
        # Make the API call
        response = requests.get(url, headers=headers, params=parameters)
        data = response.json()
        # print(data)
        
        # Parse and return the price in USDT
        if "data" in data and "RAMA" in data["data"]:
            price = data["data"]["RAMA"]["quote"]["USDT"]["price"]
            # print(f"Current RAMA Price in USDT: ${price}")
            return price
        else:
            # print("Unable to fetch RAMA price.")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None






def verify_RAMA_transaction(tx_hash):
    
    
    print("Waiting for transaction to be confirmed...")
# def get_web3():
    web3=get_web3()

    try:
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        print('status is',receipt.status)
        if receipt.status == 1:
            # Transaction is confirmed
            transaction = web3.eth.get_transaction(tx_hash)

            # Extract relevant information
            sender_address = transaction['from']
            recipient_address = transaction['to']
           
            amount_in_tokens=transaction['value']
            # gas_used = receipt.gasUsed  # Gas used from receipt
            # gas_cost = Decimal(gas_used) * Decimal(gas_price) / Decimal(1e18)  # Gas cost in ETH
            balance_after_tx = Decimal(amount_in_tokens) / Decimal(1e18)  # Approximation

            print({
                    'SENDER_ADDRESS':sender_address,
                    'RECEPIENT_ADDRESS':recipient_address,
                    'TRANSFERRED_AMOUNT':balance_after_tx,
                        
                    }
                )
            # print(f"Transaction confirmed: {tx_hash} and amount is {balance_after_tx} | Block: {receipt.blockNumber}")
            # return tx_hash.hex()
            return {
                    'SENDER_ADDRESS':sender_address,
                    'RECEPIENT_ADDRESS':recipient_address,
                    'TRANSFERRED_AMOUNT':balance_after_tx,
                        
                    }
        
        
        else:
            raise ValueError(f"Transaction {tx_hash.hex()} failed")

    except TimeExhausted:
        print("Transaction confirmation timed out")
        return False




def verify_USDT_transaction(transaction_hash):
    # print("came here==========")
    if True:
    
      
        
        # time.sleep(15)
        web3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))  # BSC Testnet RPC URL
      
        try:
            transaction_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash, timeout=30)

            
            if transaction_receipt['status'] == 1:
                
                transaction = web3.eth.get_transaction(transaction_hash)
            # print(transaction)
                if transaction:
                    # Verify the transaction details (e.g., sender, recipient, amount)
                    # Add your own logic to verify the transaction and update the user's wallet
                    sender = transaction['from']
                    recipient_contract = transaction['to']
                    input_data = transaction['input']
                    usdt_contract_address = '0x55d398326f99059fF775485246999027B3197955'
                    
                    bscscan_api_key = ""

                    abi_url = f"https://api.bscscan.com/api?module=contract&action=getabi&address={usdt_contract_address}&apikey={bscscan_api_key}"
                    response = requests.get(abi_url)
                
                    if response.status_code == 200:
                        data = response.json()
                        if data['status'] == '1': # Ensure the API call was successful
                            contract_abi = json.loads(data['result'])
                    amount = web3.from_wei(transaction['value'], 'ether')
                    # gtamount = Decimal(amount) / Decimal(10**18)

                    # amountInUSD = amount*tranTimeCoinValue
                    # print('amount is ',gtamount)
                    
                    usdt_contract = web3.eth.contract(address=recipient_contract, abi=contract_abi)
                    
                    function_name, function_params = usdt_contract.decode_function_input(input_data)
                    
                    recipient=function_params['recipient']
                    transAmount=function_params['amount']
                    gtamount = Decimal(transAmount) / Decimal(10**18)
                    # print(function_params)
                    # return function_params
                    
                    if recipient:  # Your testnet receiving address
                        
                        
                        
                        try:
                            
                            # print('====')
                            # print('amount is ',gtamount)
                            # print("transaction verified")
                            return {
                                'SENDER_ADDRESS': sender,
                                'RECIPIENT_ADDRESS': recipient.lower(),
                                'TRANSFERRED_AMOUNT': gtamount,
                            }
                            
                        except Exception as e:
                            
                            print(e)
                            return False
                        
                        

                            

                            
                    else:
                        return False
                else:
                    return False
                
                
            
        except Exception as e:
            return False







@login_required

def depositFund(request):
    
    
    if request.method=="POST":
        getTransHash=request.POST.get('TransHash')
        
        if not getTransHash and not len(getTransHash)>15:
                return JsonResponse({'success': False,'msg': f'Invalid transaction hash '})
            
            
        try:
            
            # VERIFY TRANSACTION HASH
            
            getWallAdd=DepositWallet.objects.all().order_by('-id').first().address
            
            print('came here to verify')
            try:
                get_trans=verify_USDT_transaction(getTransHash)
            except Exception as e:
                print(str(e))
                
            
            if get_trans and get_trans['RECEPIENT_ADDRESS']==getWallAdd :
                print('addrss is same')
                # check if a trans already does not exists
                
                # check whether transaction already exists
                
                try:
                    getallcounts=TransactionHistoryOfCoin.objects.filter(hashtrxn=getTransHash.strip()).count()
                    if getallcounts>0:
                        print('duplictat hash')
                        return JsonResponse({'success': False,'msg': f'Transcation already added to sender wallet'})
                    
                
                except Exception as e:
                    print(str(e))
                    
                
                print('duplicate hash chcked')
                try:
                
              
                    newWalletTabEntry=WalletTab.objects.create(
                        col2=request.user.email,
                        col3='Deposit',
                        col4=f"{ get_trans['TRANSFERRED_AMOUNT'] } usdt has been added to your wallet",
                        amount=get_trans['TRANSFERRED_AMOUNT'],
                        user_id=request.user,
                        txn_date=datetime.now(),
                        txn_type='CREDIT',
                        zql_rate=0,
                        usd_rate=0,
                        usd_value_of_zaan=0
                    )

                    # newWalletTabEntry.save()
                    
                    
                            
                    newTran=TransactionHistoryOfCoin.objects.create(
                            cointype="RITCOIN",
                            memberid=request.user,
                            name=request.user.email,
                            hashtrxn=getTransHash.strip(),
                            amount=get_trans['TRANSFERRED_AMOUNT'],
                            coinvalue=0,
                            trxndate=datetime.now(),
                            status='pending',
                            coinvaluedate=datetime.now(),
                            total=get_trans['TRANSFERRED_AMOUNT'],
                            amicoinvalue=0,
                            amifreezcoin=float(get_trans['TRANSFERRED_AMOUNT']),
                            amivolume=get_trans['TRANSFERRED_AMOUNT'],
                            totalinvest=get_trans['TRANSFERRED_AMOUNT'],
                            tran_type='CREDIT',
                        )
                        
                        
                        
                        
                
                        
                    # newTran.save()
                    print('Transaction saved sucessfully')
                    
                    
                except Exception as e:
                    print(str(e))
                
                return JsonResponse({'success': True,'msg': f'Transaction verification requested successfully.Funds will be added to your wallet within 24 hours'}) 

                
                
            else:
                print(get_trans)
                
            
                return JsonResponse({'success': False,'msg': f'Invalid transaction hash '}) 
                 

        
    
          
            
            # return redirect('walletHistory')


        except Exception as e:
            
            
            return JsonResponse({'success': False,'msg': f'Something went wrong please try after sometime'}) 

    

        
            
        # MAKE A TRANSACTION ENTRY
            
        # return JsonResponse({'success': True,'msg': f'hash is {getTransHash}'})
    
    
    return JsonResponse({'success': True,'msg': f'method not allowed'})

    
 
# @login_required

def checkPayment(request):
#  print("came here again=====================>")
    # logger.error("Came here again===============")
    # logger.error("User is %s", request.user.memberid)

    # print(request.GET.get('client_txn_id'))
    result = {}
    # client_txn_Id = request.session.get('client_txn_id')
    client_txn_Id =request.GET.get('client_txn_id')
    meber=QrTransDetails.objects.get(client_txn_id=client_txn_Id)
    
    user=ZqUser.objects.get(memberid=meber.memberid)
    # print(user.memberid)
    # logger.error("Client txn id is %s", client_txn_Id)

    # print(request.user.memberid)
    # print("Client txn id is:", client_txn_Id)
    # client_txn_Id=request.GET.get('client_txn_id')

    url = ""

    payload ={
        "key": "",
        "client_txn_id": client_txn_Id,
        "txn_date": date.today().strftime('%d-%m-%Y'),
    }
 
 

    headers = {
        'Content-Type': 'application/json'
    }
 
 
    time.sleep(5)
    try:
        response = requests.request("POST", url, headers=headers, json=payload)
        # response = requests.post(url, headers=headers, json=payload)
        # print("response is")
        # print(response.text)
    except Exception as e:
        print(str(e))
        logger.error(f"An error occurred: Transaction failed. Error: {response.text}")



    
    if response.status_code == 200:
        # print("Inside status code")
        APIresult = response.json()
        # print(result)
        # print("status is",result['status'],'and type is',type(result['status']))
        # datavalue=len(result['data'])
        # loopCount=0
        
        if APIresult['status'] is False and APIresult['msg']=="Record not found":
            
            msg='Payment not done'
                # msg=f"Transaction successfull {ZQLCoinamount} zaan coins added to your wallet successfully "
            messages.warning(request, msg)
            # return redirect('myAdd')
            return redirect('walletHistory')
        
        if APIresult['status'] is True and APIresult['data']['status']=="failure":
            
            msg=APIresult['data']['remark']
                # msg=f"Transaction successfull {ZQLCoinamount} zaan coins added to your wallet successfully "
            messages.warning(request, msg)
            # return redirect('myAdd')
            return redirect('walletHistory')
    
        

      

        if APIresult['status'] and APIresult['data']  and APIresult['data']['status']=="success":
            # print("Inside status success")

            # ZQLRate=CustomCoinRate.objects.get(id=1).amount
            # ZQLRate=CustomCoinRate.objects.order_by('-id').first().amount
            ZQLRate=1
            USDRate=float(CustomCoinRate.objects.filter(coin_name='USD').order_by('-id').first().amount)
            # ZQLRate=CustomCoinRate.objects.order_by('-id').first().amount
            Coinamount = APIresult['data']['amount']
            ZQLCoinamount = float(APIresult['data']['amount'])*(1/(float(ZQLRate)*float(USDRate)))
            USDCoinamount = float(Coinamount)/(USDRate)
            
            
            try:
                # Create an instance
            
                transaction = INRTransactionDetails(
                    customer_name=APIresult['data']['customer_name'],
                    upi_txn_id=APIresult['data']['customer_vpa'],
                    status= APIresult['data']['status'],
                    txnAt=APIresult['data']['createdAt'],
                    amount = Coinamount,
                    client_txn_id = APIresult['data']['client_txn_id'],
                    zaan_coin_value=ZQLRate,
                    conversion_usd_value=USDRate,
                
                    memberId=user,
                    )
                
                
                transaction.save()
         
                 
                newWalletTabEntry=WalletTab.objects.create(
                                col2=user.email,
                                col3='Deposit',
                                col4=f'{USDCoinamount} usdt has been added to your wallet',
                                amount=USDCoinamount,
                                user_id=user,
                                txn_date=datetime.now(),
                                txn_type='CREDIT',
                                zql_rate=ZQLRate,
                                usd_rate=USDRate,
                                usd_value_of_zaan=USDCoinamount
                            )

                newWalletTabEntry.save()
                
                
                    
                newTran=TransactionHistoryOfCoin.objects.create(
                    cointype="USD",
                    memberid=user,
                    name=user.email,
                    hashtrxn=client_txn_Id,
                    amount=USDCoinamount,
                    coinvalue=USDRate,
                    trxndate=datetime.now(),
                    status='success',
                    coinvaluedate=datetime.now(),
                    total=USDCoinamount,
                    amicoinvalue=USDRate,
                    amifreezcoin=float(USDCoinamount),
                    amivolume=USDCoinamount,
                    totalinvest=USDCoinamount,
                    tran_type='CREDIT',
                )
                
                
                
                
           
                
                newTran.save()
                
                # add member to a club
                if int(USDCoinamount) == 550:
                    ClubMembers.objects.create(memberid=user,club='club1',club_added_date=datetime.now())
                elif  int(USDCoinamount) == 1100:
                    ClubMembers.objects.create(memberid=user,club='club2',club_added_date=datetime.now())
                elif int(USDCoinamount) == 2750:
                    ClubMembers.objects.create(memberid=user,club='club3',club_added_date=datetime.now())

            
                    
    
                msg=f"Transaction successfull {USDCoinamount} USD added to your wallet successfully "
                messages.success(request, msg)
                
                return redirect('walletHistory')


            except Exception as e:
                # print(e)
                logger.error(f"{datetime.now()}: An error occurred: %s", str(e))
                result['status']=0
                msg='Some erorr occured from our side'
                # msg=f"Transaction successfull {ZQLCoinamount} zaan coins added to your wallet successfully "
                messages.warning(request, msg+str(e))
                # return redirect('myAdd')
                return redirect('walletHistory')


        else:
          
            remark = result['data'].get('remark', 'Transaction failed without a specific remark')
            # print(f"Transaction failed. Remark: {remark}")
            result['status']=0
            result['message']='Something went wrong'
                    # result['url']=result['data']['payment_url']
            msg=f"some error occured while processing your transaction if funds has been debited it will be processed within a few hours  status unsucessfull"
            messages.warning(request, msg)
                
            return redirect('walletHistory')
            # return JsonResponse(result) 


    else:
        logger.error(f"{datetime.now()} :An error occurred: Transaction failed. Error: {response.text}")
        # print(f"")
        result['status']=0
        result['msg']="transaction failed"
                  
        msg=f"some error occured while processing your transaction if fund has been debited it will be processed within a few hours "
        messages.warning(request, msg)
                
        return redirect('walletHistory') 
    


def testWalletTopup(request):
    
    return render(request,'zqUsers/member/testWalletTopup.html')

def linkExpired(request):
    

    return render(request,'zqUsers/member/linkExpired.html')

def unconfirmedEmail(request):
    

    return render(request,'zqUsers/member/unconfirmedEmail.html')


@login_required                
def activate_id_TOPUPByMember(request, amount,activationMember):
    

        
        if int(amount) >= 0 and activationMember.status == 0:
        # if int(amount) >= 0 :
           
            try:
                    
                    print('Came here=======================')
                    with connection.cursor() as cursor:
                        # cursor.execute("EXEC activate_id @memberid=%s, @package=%s, @comment='Self id activation', @activation_by='User', @activation_time_no_of_btc=0, @activation_time_no_of_trx=0, @activation_time_no_of_eth=0, @btc_rate=0, @trx_rate=0, @eth_rate=0;", [memberid, num])
                        res=cursor.execute("CALL activate_id(%s, %s, 'Self id activation', 'User', 0, 0, 0, 0, 0, 0,%s,%s,%s);", (activationMember.memberid, amount,0,0,amount))
                        # print(res)
                        str_result = "Success"
                        
                        return res
                        # print('Came here=======================')
                        
            except Exception as e:
                # print(e)
                logger.error(f"{datetime.now()}:An error occurred: %s", str(e))
                return 0
                # return e
                
        else:
        #    print("=========================rinvestment")
           
        #    print("status is ",_userinformation.status )
            
           if activationMember.status == 1:
               
                # print("===================came for reinvestment")
                try:
                    with connection.cursor() as cursor:
                        
                        # CREATE DEFINER=`zaanqueriladmin`@`%` PROCEDURE `reinvestproc`(IN `_memberid` VARCHAR(255), IN `_package` FLOAT, IN `comment` VARCHAR(255), IN `activation_by` VARCHAR(255), IN `activation_time_no_of_btc` FLOAT, IN `activation_time_no_of_trx` FLOAT, IN `activation_time_no_of_eth` FLOAT, IN `btc_rate` FLOAT, IN `eth_rate` FLOAT, IN `trx_rate` FLOAT)
                        # res=cursor.execute("CALL activate_id(%s, %s, 'Self id activation', 'User', 0, 0, 0, 0, 0, 0);", (request.user.memberid, num))

                        res=cursor.execute("CALL reinvestproc (%s, %s, 'Self id activation', 'User', 0, 0, 0,0, 0, 0,%s,%s,%s);", [activationMember.memberid, amount,0,0,amount])
                        # print("retune====================================")
                        # print(res)
                        return res
                except Exception as e:
                    # print(e)
                    logger.error(f"{datetime.now()}: An error occurred: %s", str(e))
                    #  return e
                    return 0


def send_otp(request,email,subject,template,whatfor,context={}):
    
    
   
    # print('came to send otp')
    randNum=random.randint(100000,999999)
    context['OTP']=str(randNum)

   
    html_content = render_to_string(template, context)
    
    
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
        # print('came to send///////////')
        if sendEmail.send():
            
            if whatfor=="ACTIVATEPEERID":
                
                print(randNum)
                request.session['ACTIVATEPEERID'] = randNum
                return True
               
            elif whatfor=="WALLETWITHDRAWAL":
                
                print(randNum)
                request.session['WALLETWITHDRAWALOTP'] = randNum
                return True
               
            
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
def activateAnyMembersId(request):
    
    # print("came here")
 
    if request.method == 'POST':
 
        result={}
        TOTALWALLETBALANCE=request.user.totalWalletBalance()
        # print(TOTALWALLETBALANCE)
        data = json.loads(request.body)
        # print(data)
        package = float(data.get('Package'))
        memberId = data.get('Username')
        type = data.get('type')
        # print(package,memberId)
        
        if type=='sendOTP':
            try:
                if send_otp(request,email=request.user.email,subject="OTP to verify peer account activation",template="zqUsers/emailtemps/peerIdActivation.html",whatfor="ACTIVATEPEERID"):
                    
                    result['status']=1
                    result['msg']='OTP sent successfully'
                    return JsonResponse(result)
                
                else:
                    result['status']=0
                    result['msg']='something went wrong while sending otp'
                    return JsonResponse(result)
            except Exception as e:
                print(e)
                result['status']=0
                result['msg']='something went wrong while sending otp'
                return JsonResponse(result)
                    
        
        # check whether otp is in session
        
        if 'ACTIVATEPEERID' in request.session:
            
            userEnteredOTP=data.get('otp').strip()

            sessionOTP=str(request.session.get('ACTIVATEPEERID'))
            if (userEnteredOTP!=sessionOTP):
                
                result['status']=0
                result['msg']='Incorrect otp'
                return JsonResponse(
                    result
                )
        else:
            
            result['status']=0
            result['msg']='unauthenticated otp'
            return JsonResponse(
                result
            )
                
  
        try:
            toBeActivatedMember=ZqUser.objects.get(username=memberId)
        except:
            toBeActivatedMember=None
        
        if not toBeActivatedMember:
            result['status'] = 0
            result['msg'] = "No member found associated with this username"
            
            return JsonResponse(result)

        
        if package and float(package)>0 and package<=TOTALWALLETBALANCE:
            
            # first amount  worth package to be debited from payee wallet
            
            try:
            
                # debitFromPayeeWallet = WalletTab.objects.create(
                #             # col2=topupInitiatedByUser,
                #             col3="TOPUPFORPEER",
                #             col4= str(package) + " $ used for peers topup of " +toBeActivatedMember.username ,
                #             amount=package,
                #             user_id=request.user,
                #             txn_date=datetime.now(),
                #             txn_type="DEBIT",
                #             zql_rate=0,
                #             usd_rate=0,
                #             usd_value_of_zaan=package
                #         )
                
                
                
                # debitFromPayeeWallet=TransactionHistoryOfCoin.objects.create(
                #             cointype=coinName,
                #             memberid_id=request.user,
                #             name=request.user.username,
                #             hashtrxn=transaction_hash,
                #             amount=amountInUSD,
                #             coinvalue=tranTimeCoinValue,
                #             trxndate=datetime.now(),
                #             status=1,
                #             coinvaluedate=datetime.now(),
                #             total=amountInUSD,
                #             amicoinvalue=tranTimeCoinValue,
                #             amifreezcoin=float(cryptoAmount),
                #             amivolume=cryptoAmount,
                #             totalinvest=amountInUSD,
                #             tran_type='CREDIT',
                #         )
                
                debitFromPayeeWallet=TransactionHistoryOfCoin.objects.create(
                            cointype='USD',
                            memberid=request.user,
                            name=request.user.username,
                            hashtrxn='success',
                            amount=package,
                            coinvalue=90,
                            trxndate=datetime.now(),
                            status='success',
                            coinvaluedate=datetime.now(),
                            total=package,
                            amicoinvalue=90,
                            amifreezcoin=float(90),
                            amivolume=90,
                            totalinvest=package,
                            tran_type='DEBIT',
                        )
                
                creditToReceiverWallet=TransactionHistoryOfCoin.objects.create(
                            cointype='USD',
                            memberid=toBeActivatedMember,
                            name=toBeActivatedMember.username,
                            hashtrxn='PEER TOPUP',
                            amount=package,
                            coinvalue=90,
                            trxndate=datetime.now(),
                            status='success',
                            coinvaluedate=datetime.now(),
                            total=package,
                            amicoinvalue=90,
                            amifreezcoin=float(90),
                            amivolume=90,
                            totalinvest=package,
                            tran_type='CREDIT',
                        )
                            
                        # newTran.save()
                # creditToReceiverWallet = WalletTab.objects.create(
                #             # col2=topupInitiatedByUser,
                #             col3="Deposit",
                #             col4= str(package) + " $  has been deposited to your wallet by " +request.user.username ,
                #             col5= "TOPUPFORPEER" ,
                #             amount=package,
                #             user_id=toBeActivatedMember,
                #             txn_date=datetime.now(),
                #             txn_type="CREDIT",
                #             zql_rate=0,
                #             usd_rate=0,
                #             usd_value_of_zaan=package
                #         )
                
            except Exception as e:
                print(e)
                    
            
            
            print("came here to check if fund====")
            
            if package<=float(toBeActivatedMember.totalWalletBalance()):
                res=activate_id_TOPUPByMember(request=request,amount=package,activationMember=toBeActivatedMember)
                
            else:
                
                result['status'] = 0
                result['msg'] = "Insufficient wallet balance of members id being activated"
                # result['alertMsg'] = "some error occured from our end"
                
                return JsonResponse(result)
                
          
            
            if res:

                # print("cam here")
                try:
                    
                    # objw = WalletTab.objects.create(
                    #     # col2=topupInitiatedByUser,
                    #     col3="TOPUP",
                    #     col4=str(package) + " $ is used for topup of " +toBeActivatedMember.username ,
                    #     amount=package,
                    #     user_id=toBeActivatedMember,
                    #     txn_date=datetime.now(),
                    #     txn_type="DEBIT",
                    #     zql_rate=0,
                    #     usd_rate=0,
                    #     usd_value_of_zaan=package
                    # )
                    
                    # objw.save()
                    
                    objw=TransactionHistoryOfCoin.objects.create(
                            cointype='USD',
                            memberid=toBeActivatedMember,
                            name=toBeActivatedMember.username,
                            hashtrxn='peerActivate',
                            amount=package,
                            coinvalue=90,
                            trxndate=datetime.now(),
                            status=1,
                            coinvaluedate=datetime.now(),
                            total=package,
                            amicoinvalue=90,
                            amifreezcoin=float(90),
                            amivolume=90,
                            totalinvest=package,
                            tran_type='DEBIT',
                        )
                    # print("wallet entry done")

                    newInvestmentWalletEntry=InvestmentWallet.objects.create(
                        txn_by=toBeActivatedMember,
                        amount=package,
                        remark=f'{package}$ is added  to your investment wallet',
                        txn_date=datetime.now(),
                        txn_type='CREDIT',
                        zaan_rate=0,
                        usd_rate=0,
                        zaan_value_in_usd=package,
                        activated_by=request.user,
                    )
                    
                    newInvestmentWalletEntry.save()
                    
                    # rimberioBonus=RimberioCoinDistribution.objects.filter(task='activateId').first().coin_reward

                    # RimberioWallet.objects.create(amount=rimberioBonus,remark=f"rimberio bonus for package activation  is {rimberioBonus}",trans_for="packageactivation",tran_by=toBeActivatedMember,trans_from=toBeActivatedMember,trans_to=toBeActivatedMember,trans_date=datetime.now(),trans_type='CREDIT',package_id=newInvestmentWalletEntry)

                
                    # print("came here")
                    # assignSocialJobs(toBeActivatedMember,newInvestmentWalletEntry)
                    
                    # distribute downline rimberiocoin
                    # print("came here")
                    # print("came here=========================================>")
                    # newMemId=str(toBeActivatedMember.memberid)
                    # invwalletId=str(newInvestmentWalletEntry.id)
                    # try:
                    #     with connection.cursor() as cursor:
                    #         cursor.callproc('rimberio_coin_distribution_activateid', [
                    #                 newMemId,
                    #                 1,
                    #                 'IdActivationDownlineDistribution',
                    #                 invwalletId
                                   
                                    
                                    
                                
                    #         ])
                            
                    #     # print("entry done")


                            
                    # except Exception as e:
                    #     print('Error occurred:', str(e))
                    #     # return "Error: Please try again later"
                    
            
                    
                except Exception as e:
                    
                    print(e)
                    logger.error(f"{datetime.now()}: An error occurred: %s", str(e))
                    if objw:
                        
                        objw.delete()
                        
                    if newInvestmentWalletEntry:
                        newInvestmentWalletEntry.delete()
                    
                    
                    
                    
                    result['status'] = 0
                    result['msg'] = "some error occured from our end"
                    result['alertMsg'] = "some error occured from our end"
                    
                    return JsonResponse(result)
                
                
                
                
                # result['status'] = 1
                # result['msg'] = "You Package has been activatd successfully"
                # result['alertMsg'] = "You Package has been activated successfully"
                
                    # sendMail(request,email=request.POST.get('email'),subject="Topup Success",template='successfullTopup',additionalParams={'withdrawal_amt': enteredAmount})
                return JsonResponse({'success': True,'msg': f'{toBeActivatedMember.username} Id has been activated successfully'})

            
                
                # if sendEMail(request,request.user.email,subject='Activation Request for Mining Machine',template='newMemPanel/emailtemps/machineActivationRequest.html',context={'activatedmachineName':activatedMachineName},whatFor='activationRequest'):

                #     result['status'] = 1
                #     result['msg'] = "Your Machine has been Activated successfully"
                #     result['alertMsg'] = "Your Machine has been Activated successfully"
                    
                #     # sendMail(request,email=request.POST.get('email'),subject="Topup Success",template='successfullTopup',additionalParams={'withdrawal_amt': enteredAmount})
                #     return JsonResponse(result)
            
            
            
            
            else:
                # result['status'] = 0
                # result['message'] = "You Package activation has been failed"
                
                return JsonResponse({'success': True,'msg': 'some error occured please try again later'})

        else:
            return JsonResponse({'success': False,'msg': 'Invalid amount'})


def topUpMemberId(request):
    
    
    return render(request,'zqUsers/member/topupMemberId.html')




# @login_required 
def dummyWitdrawal(request):
    
    allWds=WalletAMICoinForUser.objects.filter(memberid=request.user.memberid)
    acConfirmObj=AccountComfirmation.objects.filter(uploaded_by=request.user.memberid).first()
    return render(request,"zqUsers/member/withdrawalold.html",context={
        
        'allWds':enumerate(allWds),
        'acConfirmObj':acConfirmObj
    })
    

 
@login_required                

def sendAssignedJobToUserMail(request):
    print("came jere")
    
    current_date = timezone.now()
    allPackages=InvestmentWallet.objects.filter(txn_by=request.user)
    # totalBonus=0
    
    data= json.loads(request.body)
    jobId=data.get('socialJobId')
    
    if allPackages.count()>0:
            
            
            for package in allPackages:
                    
                # print(AssignedSocialJob.objects.filter(assigned_to=self,status=0,package_id=package,valid_from__lt=current_date,valid_upto__gt=current_date).first())
                try:
                    # lastestAssignedJob=AssignedSocialJob.objects.filter(assigned_to=self,status=0,package_id=package,valid_from__lt=current_date,valid_upto__gt=current_date).order_by('id').first()
                    # print(lastestAssignedJob)
                    # allJobs=AssignedSocialJob.objects.filter(assigned_to=request.user,package_id=package,valid_from__lt=current_date,valid_upto__gt=current_date).order_by('id').first()
                    allJobs=AssignedSocialJob.objects.filter(id=jobId).order_by('id').first()
                    # allJobs=AssignedSocialJob.objects.get(id=470)
                    print(allJobs)
                    # print(allJobs.check_token)
                    # print(allJobs.status)
                    if  allJobs.check_token and allJobs.status  :
                        
                      
                        return render(request,'zqUsers/member/socialJobMailsentSuccess.html',context={
                                'whatfor':'jobAlreadyCompleted'
                            })
                    
                    validFromDate=allJobs.valid_from
                    validTillDate=allJobs.valid_upto
                
                    nowDateTime=datetime.now()
                    # timedelta(days=5)+ timedelta(days=2)
                    if is_naive(validFromDate):
                    
                        validFromDate = make_aware(validFromDate)
                    if is_naive(nowDateTime):
                        nowDateTime = make_aware(nowDateTime)
                    if is_naive(validTillDate):
                        validTillDate = make_aware(validTillDate)
                        
                    sendMailVaidFrom=validTillDate-timedelta(days=2)
                    
                    if sendMailVaidFrom<nowDateTime<validTillDate:
                    # if True:
                        print("came here")
                        if sendMailVerificationEmailForSocialMedia(request,request.user.id,allJobs.id):
                            
                            return JsonResponse({
                                'status':1,
                                'msg':'Social job sent to your email successfully please click on it to get  rewarded'
                            })
                            # print("mail sent successfully")
                            # return render(request,'zqUsers/member/socialJobMailsentSuccess.html',context={
                            #     'whatfor':'mailSent'
                            # })
                        else:
                             return JsonResponse({
                                'status':0,
                                'msg':'Something went wrong'
                            })
    

                    # print(self.prepaid_memberid.filter(memberid=self.memberid,assigned_task_id=lastestAssignedJob.id,given_date__lt=current_date).count())
                    # totalBonus+=float(self.prepaid_memberid.filter(memberid=self,assigned_task_id=lastestAssignedJob,given_date__lt=current_date).aggregate(Sum('bonus'))['bonus__sum'] or 0)
                    # print(totalBonus)
                except Exception as e:
                    print(e)
        
    else:
        allJobs=AssignedSocialJob.objects.filter(assigned_to=request.user,status=0,valid_from__lt=current_date,valid_upto__gt=current_date).order_by('id').first()
        validFromDate=allJobs.valid_from
        validTillDate=allJobs.valid_upto
    
        nowDateTime=datetime.now()
        # timedelta(days=5)+ timedelta(days=2)
        if is_naive(validFromDate):
        
            validFromDate = make_aware(validFromDate)
        if is_naive(nowDateTime):
            nowDateTime = make_aware(nowDateTime)
        if is_naive(validTillDate):
            validTillDate = make_aware(validTillDate)
            
        sendMailVaidFrom=validTillDate-timedelta(days=2)
        
        if sendMailVaidFrom<nowDateTime<validTillDate:
        
            if sendMailVerificationEmailForSocialMedia(request,request.user.id,allJobs.id):

                 return JsonResponse({
                                'success':1,
                                'msg':'Social job sent to your email successfully please click on it to get  rewarded'
                            })
            else:
                 return JsonResponse({
                                'success':0,
                                'msg':'something went wrong'
                            })
    # allJobs=AssignedSocialJob.objects.filter(assigned_to=request.user).order_by('-id').first()
    
 

def sendMailVerificationEmailForSocialMedia(request, user_id,assignedSocialJobId):
    
    # print("came here")
    user = ZqUser.objects.get(pk=user_id)
    # token = email_verification_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    asid = urlsafe_base64_encode(force_bytes(assignedSocialJobId))

    # token = long_email_verification_token.make_token(user)
    html_content = render_to_string('zqUsers/emailtemps/sendMailForSocialJob.html',{
                'user': user,
                'domain': request.META['HTTP_HOST'],
                # 'domain': 'www.rimberio.world',
                'uid': uid,
                'asid': asid,
                'token': email_verification_token.make_token(user),
            })
    # print(f"https://{domain}{% url 'submit_social_job' uidb64=uid asidb64=asid token=token %}")
    # return


    with get_connection(  
                        
        host=settings.EMAIL_HOST, 
        port=settings.EMAIL_PORT,  
        username=settings.EMAIL_HOST_USER, 
        password=settings.EMAIL_HOST_PASSWORD, 
        use_tls=settings.EMAIL_USE_TLS  
    ) as connection:  
        subject = "Social Job Sumbission"  
        email_from = "noreply@ritcoin.exchange" 
        recipient_list = [user.email]  
        # recipient_list = ['amrevrp@gmail.com']  
        # message ="This is testing email" 
        body=html_content 
        sendEmail=EmailMessage(subject, body, email_from, recipient_list, connection=connection)
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


# this is new changed to social_job afterwards

def submit_social_job(request, uidb64,asidb64 ,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        asid = force_str(urlsafe_base64_decode(asidb64))
        try:
            user = ZqUser.objects.get(id=uid)
        except Exception as e:
            
            return HttpResponse('Submission link is invalid!')
            
        if asid:
            try:
                assignedJobId=AssignedSocialJob.objects.get(id=asid)
            except Exception as e:
                return HttpResponse('Submission link is invalid!')
        else:
            return HttpResponse('Submission link is invalid!')
            
                
        # else:
            # assignedJobId=N
        # print(assignedJobId)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist,assignedJobId.DoesNotExist):
        # user = None
        assignedJobId = None
        

    if user and assignedJobId  and  not assignedJobId.check_token and not  assignedJobId.status and email_verification_token.check_token(user, token):
        
        
        if user.doesMemberHaveAssocialtedIds():
            
            isactive=True
            totalEarnedAmount=submit_social_job_associated_Ids(request, user.id,assignedJobId)
            
            if totalEarnedAmount>0:
                return render(request,'zqUsers/member/submitSocialJobThroughLink.html',context={
                            'amount':totalEarnedAmount,
                            'isactive':isactive
                        })
            else:
                
                return render(request,'zqUsers/member/failurejobsubmission.html')
        
        
        elif assignedJobId.package_id.group_id:
            print("came here inside group")
            isactive=True
            totalEarnedAmount=submit_social_job_group_Ids(request, user.id,assignedJobId)
            if totalEarnedAmount>0:
                return render(request,'zqUsers/member/submitSocialJobThroughLink.html',context={
                            'amount':totalEarnedAmount,
                            'isactive':isactive
                        })
            else:
                return render(request,'zqUsers/member/failurejobsubmission.html')


        else:
            
            getMultiplier=AllPackageDetails.objects.filter(package_price=assignedJobId.package_id.amount).first().multiplier
            
            # print(getMultiplier)
            
            # return
            
            totalJobBonus=5*int(getMultiplier)
            if  user.username != 'vagak6':
                assignedJobId.check_token=True
                assignedJobId.save()
                
            
            validTillDate=assignedJobId.valid_upto
            if is_naive(validTillDate):
                validTillDate = make_aware(validTillDate)
            
            try:
                
                # print(assignedJobId.package_id)
                # return
                # if assignedJobId.package_id:
                if int(assignedJobId.package_id.id)>0:
                    isactive=True
                    roiEnts=ROIDailyCustomer.objects.filter(userid=user.memberid,investment_id=assignedJobId.package_id).count()
                    
                    newobjs=ROIDailyCustomer(userid=user,remark=f'social job submission bonus ${totalJobBonus}',total_sbg=totalJobBonus,roi_sbg=totalJobBonus,roi_date=validTillDate,status=1,daily_amount=totalJobBonus,roi_days=roiEnts+1,investment_id=assignedJobId.package_id,usd_rate=0,zaan_rate=0,roi_sbg_usd=totalJobBonus,zaan_value_in_usd=totalJobBonus,assigned_job_id=assignedJobId)
                    newobjs.save()
                    
                 
                   
                    # distribute magical income
                    userMemId=str(user.memberid)
                    assJId=int(assignedJobId.id)
                    try:
                        with connection.cursor() as cursor:
                            cursor.callproc('MagicalIncome', [
                                    userMemId,
                                    totalJobBonus,
                                    assJId,
                                    assignedJobId.valid_upto
                                    
                                
                            ])

                    except Exception as e:
                        print('Error occurred:', str(e))
                        # return "Error: Please try again later"
                        
                   
                    try:   
                        # Distribute community building Bonus
                        # get activation date
                        userActivationDate=user.activationdate
                        if is_naive(userActivationDate):
                    
                            userActivationDate = make_aware(userActivationDate)
                        
                        # check active totaldirects within 7 days
                        totalActiveRefers=ZqUser.objects.filter(introducerid=user.memberid,status=1,activationdate__lt=userActivationDate+timedelta(days=7)).count()
                        
                        if totalActiveRefers>0:
                            if totalActiveRefers == 1:
                                communityIncome=float(CommunityBuildingBonus.objects.get(referral_requirement=1).stage_bonus)*int(getMultiplier)
                            elif totalActiveRefers == 2:
                                communityIncome=float(CommunityBuildingBonus.objects.get(referral_requirement=2).stage_bonus)*int(getMultiplier)
                            else:
                                communityIncome=float(CommunityBuildingBonus.objects.get(referral_requirement=3).stage_bonus)*int(getMultiplier)
                                
                                
                                

                            #  entry for community building Bonus
                            communityBuildingBonus=CommunityBuildingIncome.objects.create(
                                bonus_received_from=user,
                                receiver_memberid=user,
                                received_bonus = communityIncome,
                                calculated_on = totalJobBonus,
                                calculated_on_referrals = totalActiveRefers,
                                job_submission_date = datetime.now(),
                                bonus_received_date = validTillDate,
                                social_job_id=assignedJobId
                                
                            )
                            
                            # Rimberio coin distribution for social job
                        rimberioBonus=RimberioCoinDistribution.objects.filter(task='socialJobSubmission').first().coin_reward*int(getMultiplier)

                        rimbobj=RimberioWallet.objects.create(amount=rimberioBonus,remark=f"rimberio bonus for social job submission is {rimberioBonus}",trans_for="socialJobSubmission",tran_by=user,trans_from=user,trans_to=user,trans_date=datetime.now(),trans_type='CREDIT',package_id=assignedJobId.package_id,social_job_id=assignedJobId)
                            # print(rimbobj)
                            # print(rimberioBonus)
                            
                            # return
                            # downline coin distribution downline
                        newMemId=str(user.memberid)
                        packageIdIs=str(assignedJobId.package_id.id)
                        assignedJobIdIs=str(assignedJobId.id)
                        try:
                            with connection.cursor() as cursor:
                                cursor.callproc('rimberio_coin_distribution_downline', [
                                        newMemId,
                                        1*int(getMultiplier),
                                        'SocialJobSubmitDownlineDistribution',
                                        packageIdIs,
                                        assignedJobIdIs
                                        
                                        
                                    
                                ])
                                
                            # print("entry done")


                                
                        except Exception as e:
                            print('Error occurred:', str(e))
                            # return "Error: Please try again later"
                        
        
                            
                            
                            
                    except Exception as e:
                        print(f"Error Occured: {str(e)}")
                    
                    # print(totalJobBonus)
                    # return      
                        
                else:
                    rimberioBonus=RimberioCoinDistribution.objects.filter(task='socialJobSubmission').first().coin_reward

                    RimberioWallet.objects.create(amount=rimberioBonus,remark=f"rimberio bonus for social job submission is {rimberioBonus}",trans_for="socialJobSubmission",tran_by=user,trans_from=user,trans_to=user,trans_date=datetime.now(),trans_type='CREDIT',package_id=assignedJobId.package_id,social_job_id=assignedJobId)
                    isactive=False
                assignedJobId.status=True
                assignedJobId.completion_date=timezone.now()
                assignedJobId.save()
                
                return render(request,'zqUsers/member/submitSocialJobThroughLink.html',context={
                    'amount':totalJobBonus,
                    'isactive':isactive
                    
                    
                    })
            except Exception as e:
                print(str(e))
                return render(request,'zqUsers/member/failurejobsubmission.html')
        
        # return redirect('submittedSocialJobThroughLink')
            
    else:
        return HttpResponse('Submission link is invalid!')




 
 
 
 
 
def submit_social_job_associated_Ids(request, userId,associatedJobId):
   
       
    associteduser = ZqUser.objects.get(id=userId)
    assignedJobId=associatedJobId
    allAssociatedIds=list(ZqUser.objects.filter(associated_id=associteduser.memberid))
    # print(allAssociatedIds)
    allAssociatedIds.append(associteduser)
    allAssignedJobs=[]
    current_date = timezone.now()
    totalJobsEarnings=0
    try:
        for user in allAssociatedIds:
            
            allAssignedJobsToUser=AssignedSocialJob.objects.filter(assigned_to=user.memberid,valid_from__lt=current_date,valid_upto__gt=current_date)
            # print(allAssignedJobsToUser)
            # return
            for assignedJobId in allAssignedJobsToUser:
            
                validFromDate=assignedJobId.valid_from
                validTillDate=assignedJobId.valid_upto
                        
                nowDateTime=datetime.now()
                # timedelta(days=5)+ timedelta(days=2)
                if is_naive(validFromDate):
                
                    validFromDate = make_aware(validFromDate)
                if is_naive(nowDateTime):
                    nowDateTime = make_aware(nowDateTime)
                if is_naive(validTillDate):
                    validTillDate = make_aware(validTillDate)
                    
                jobCompltionUntil=validTillDate-timedelta(days=2)
                
                if jobCompltionUntil<nowDateTime<validTillDate:
                    
                    # print("came to check if job has already been taken")
                    
                    if user and assignedJobId  and  not assignedJobId.check_token and not  assignedJobId.status :
                        # Handle the social job submission logic here
                        # For example, render a form or process the job submission
                       
                        totalJobBonus=5
                        assignedJobId.check_token=True
                        assignedJobId.save()
                        
                        try:
                            if assignedJobId.package_id:
                                # print("came for entry")
                                # return
                                roiEnts=ROIDailyCustomer.objects.filter(userid=user.memberid,investment_id=assignedJobId.package_id).count()
                                newobjs=ROIDailyCustomer(userid=user,remark=f'social job submission bonus $5',total_sbg=totalJobBonus,roi_sbg=totalJobBonus,roi_date=validTillDate,status=1,daily_amount=totalJobBonus,roi_days=roiEnts+1,investment_id=assignedJobId.package_id,usd_rate=0,zaan_rate=0,roi_sbg_usd=totalJobBonus,zaan_value_in_usd=totalJobBonus,assigned_job_id=assignedJobId)
                                newobjs.save()
                                totalJobsEarnings+=int(newobjs.total_sbg)
                                userMemId=str(user.memberid)
                                assJId=int(assignedJobId.id)
                                # distribute magical income
                                try:
                                    with connection.cursor() as cursor:
                                        cursor.callproc('MagicalIncome', [
                                                userMemId,
                                                totalJobBonus,
                                                assJId,
                                                validTillDate
                                                
                                            
                                        ])


                                except Exception as e:
                                    print('Error occurred:', str(e))
                                    # return "Error: Please try again later"
                                    
                                
                                try:   
                                    # Distribute community building Bonus
                                    # get activation date
                                    userActivationDate=user.activationdate
                                    if is_naive(userActivationDate):
                                
                                        userActivationDate = make_aware(userActivationDate)
                                    
                                    # check active totaldirects within 7 days
                                    totalActiveRefers=ZqUser.objects.filter(introducerid=user.memberid,status=1,activationdate__lt=userActivationDate+timedelta(days=7)).count()
                                    
                                    if totalActiveRefers>0:
                                        if totalActiveRefers == 1:
                                            communityIncome=float(CommunityBuildingBonus.objects.get(referral_requirement=1).stage_bonus)
                                        elif totalActiveRefers == 2:
                                            communityIncome=float(CommunityBuildingBonus.objects.get(referral_requirement=2).stage_bonus)
                                        else:
                                            communityIncome=float(CommunityBuildingBonus.objects.get(referral_requirement=3).stage_bonus)
                                            
                                        #  entry for community building Bonus
                                        communityBuildingBonus=CommunityBuildingIncome.objects.create(
                                            bonus_received_from=user,
                                            receiver_memberid=user,
                                            received_bonus = communityIncome,
                                            calculated_on = totalJobBonus,
                                            calculated_on_referrals = totalActiveRefers,
                                            job_submission_date = datetime.now(),
                                            bonus_received_date = validTillDate,
                                            social_job_id=assignedJobId
                                            
                                        )
                                        
                                        
                                        # Rimberio coin distribution for social job
                                        rimberioBonus=RimberioCoinDistribution.objects.filter(task='socialJobSubmission').first().coin_reward

                                        RimberioWallet.objects.create(amount=rimberioBonus,remark=f"rimberio bonus for social job submission is {rimberioBonus}",trans_for="socialJobSubmission",tran_by=user,trans_from=user,trans_to=user,trans_date=datetime.now(),trans_type='CREDIT',package_id=assignedJobId.package_id,social_job_id=assignedJobId)

                                        # downline coin distribution downline
                                        newMemId=str(user.memberid)
                                        packageIdIs=str(assignedJobId.package_id.id)
                                        assignedJobIdIs=str(assignedJobId.id)
                                        try:
                                            with connection.cursor() as cursor:
                                                cursor.callproc('rimberio_coin_distribution_downline', [
                                                        newMemId,
                                                        1,
                                                        'SocialJobSubmitDownlineDistribution',
                                                        packageIdIs,
                                                        assignedJobIdIs
                                                        
                                                        
                                                    
                                                ])
                                                
                                            # print("entry done")


                                                
                                        except Exception as e:
                                            print('Error occurred:', str(e))
                                            # return "Error: Please try again later"
                                        
                        

                                                    
                                except Exception as e:
                                    print(f"Error Occured: {str(e)}")
                                                

                            else:
                                rimberioBonus=RimberioCoinDistribution.objects.filter(task='socialJobSubmission').first().coin_reward

                                RimberioWallet.objects.create(amount=rimberioBonus,remark=f"rimberio bonus for social job submission is {rimberioBonus}",trans_for="socialJobSubmission",tran_by=user,trans_from=user,trans_to=user,trans_date=datetime.now(),trans_type='CREDIT',package_id=assignedJobId.package_id,social_job_id=assignedJobId)

                            assignedJobId.status=True
                            assignedJobId.completion_date=timezone.now()
                            
                            assignedJobId.save()
                        except Exception as e:
                            print(e)
                        
                        # return redirect('submittedSocialJobThroughLink')
                        # return True
                    # else:
                    #     return False
                    elif user and assignedJobId and assignedJobId.check_token  and assignedJobId.status :
                        continue
                
                else:
                    continue  

        return totalJobsEarnings

    except Exception as e:
        print(str(e))
        return totalJobsEarnings
    

    # if user and assignedJobId  and  not assignedJobId.check_token and not  assignedJobId.status and email_verification_token.check_token(user, token):
    #     # Handle the social job submission logic here
    #     # For example, render a form or process the job submission
    #     totalJobBonus=5
    #     assignedJobId.check_token=True
    #     assignedJobId.save()
        
    #     try:
    #         if assignedJobId.package_id:
    #             roiEnts=ROIDailyCustomer.objects.filter(userid=user.memberid,investment_id=assignedJobId.package_id).count()
    #             newobjs=ROIDailyCustomer(userid=user,remark=f'social job submission bonus $5',total_sbg=totalJobBonus,roi_sbg=totalJobBonus,roi_date=assignedJobId.valid_upto,status=1,daily_amount=totalJobBonus,roi_days=roiEnts+1,investment_id=assignedJobId.package_id,usd_rate=0,zaan_rate=0,roi_sbg_usd=totalJobBonus,zaan_value_in_usd=totalJobBonus,assigned_job_id=assignedJobId)
    #             newobjs.save()
                
    #             # distribute magical income
    #             try:
    #                 with connection.cursor() as cursor:
    #                     cursor.callproc('MagicalIncome', [
    #                             user.memberid,
    #                             totalJobBonus,
    #                             assignedJobId.id,
    #                             assignedJobId.valid_upto
                                
                            
    #                     ])


    #             except Exception as e:
    #                 print('Error occurred:', str(e))
    #                 # return "Error: Please try again later"
                    
                 
    #             try:   
    #                 # Distribute community building Bonus
    #                 # get activation date
    #                 userActivationDate=user.activationdate
    #                 if is_naive(userActivationDate):
                
    #                     userActivationDate = make_aware(userActivationDate)
                    
    #                 # check active totaldirects within 7 days
    #                 totalActiveRefers=ZqUser.objects.filter(introducerid=user.memberid,status=1,activationdate__lt=userActivationDate+timedelta(days=7)).count()
                    
    #                 if totalActiveRefers>0:
    #                     if totalActiveRefers == 1:
    #                         communityIncome=float(CommunityBuildingBonus.objects.get(referral_requirement=1).stage_bonus)
    #                     elif totalActiveRefers == 2:
    #                         communityIncome=float(CommunityBuildingBonus.objects.get(referral_requirement=2).stage_bonus)
    #                     else:
    #                         communityIncome=float(CommunityBuildingBonus.objects.get(referral_requirement=3).stage_bonus)
                            
    #                     #  entry for community building Bonus
    #                     communityBuildingBonus=CommunityBuildingIncome.objects.create(
    #                         bonus_received_from=user,
    #                         receiver_memberid=user,
    #                         received_bonus = communityIncome,
    #                         calculated_on = totalJobBonus,
    #                         calculated_on_referrals = totalActiveRefers,
    #                         job_submission_date = datetime.now(),
    #                         bonus_received_date = assignedJobId.valid_upto,
    #                         social_job_id=assignedJobId
                            
    #                     )
                        
    #             except Exception as e:
    #                 print(f"Error Occured: {str(e)}")
                    
                
                    
                
                
                    
    #         else:
    #             rimberioBonus=RimberioCoinDistribution.objects.filter(task='socialJobSubmission').first().coin_reward

    #             RimberioWallet.objects.create(amount=rimberioBonus,remark=f"rimberio bonus for social job submission is {rimberioBonus}",trans_for="socialJobSubmission",tran_by=user,trans_from=user,trans_to=user,trans_date=datetime.now(),trans_type='CREDIT')

    #         assignedJobId.status=True
    #         assignedJobId.save()
    #     except Exception as e:
    #         print(e)
        
    #     return redirect('submittedSocialJobThroughLink')
    # else:
    #     return HttpResponse('Submission link is invalid!')
    
def submit_social_job_group_Ids(request, userId,associatedJobId):
   
       
    associteduser = ZqUser.objects.get(id=userId)
    assignedJobId=associatedJobId
    # allAssociatedIds=list(ZqUser.objects.filter(associated_id=associteduser.memberid))
    allAssociatedIds=[]
    # print(allAssociatedIds)
    allAssociatedIds.append(associteduser)
    allAssignedJobs=[]
    current_date = timezone.now()
    totalJobsEarnings=0
    
    # print(allAssociatedIds)
    
    
    try:
        for user in allAssociatedIds:
            
            # print(assignedJobId.package_id.id)
            allGroupedIds=InvestmentWallet.objects.filter(txn_by=associteduser,group_id=assignedJobId.package_id.group_id)
            # print(allGroupedIds.count())
            # print("came here============>a")
            # return
            for package in allGroupedIds:
                allAssignedJobsToUser=AssignedSocialJob.objects.filter(assigned_to=user.memberid,package_id=package.id,valid_from__lt=current_date,valid_upto__gt=current_date)
                # print(allAssignedJobsToUser)
                # return
                for assignedJobId in allAssignedJobsToUser:
                
                    validFromDate=assignedJobId.valid_from
                    validTillDate=assignedJobId.valid_upto
                            
                    nowDateTime=datetime.now()
                    # timedelta(days=5)+ timedelta(days=2)
                    if is_naive(validFromDate):
                    
                        validFromDate = make_aware(validFromDate)
                    if is_naive(nowDateTime):
                        nowDateTime = make_aware(nowDateTime)
                    if is_naive(validTillDate):
                        validTillDate = make_aware(validTillDate)
                        
                    jobCompltionUntil=validTillDate-timedelta(days=2)
                    
                    if jobCompltionUntil<nowDateTime<validTillDate:
                        
                        # print("came to check if job has already been taken")
                        
                        if user and assignedJobId  and  not assignedJobId.check_token and not  assignedJobId.status :
                            # Handle the social job submission logic here
                            # For example, render a form or process the job submission
                        
                            totalJobBonus=5
                            assignedJobId.check_token=True
                            assignedJobId.save()
                            
                            try:
                                if assignedJobId.package_id:
                                    # print("came for entry")
                                    # return
                                    roiEnts=ROIDailyCustomer.objects.filter(userid=user.memberid,investment_id=assignedJobId.package_id).count()
                                    newobjs=ROIDailyCustomer(userid=user,remark=f'social job submission bonus $5',total_sbg=totalJobBonus,roi_sbg=totalJobBonus,roi_date=validTillDate,status=1,daily_amount=totalJobBonus,roi_days=roiEnts+1,investment_id=assignedJobId.package_id,usd_rate=0,zaan_rate=0,roi_sbg_usd=totalJobBonus,zaan_value_in_usd=totalJobBonus,assigned_job_id=assignedJobId)
                                    newobjs.save()
                                    totalJobsEarnings+=int(newobjs.total_sbg)
                                    # distribute magical income
                                    userMemId=str(user.memberid)
                                    assJId=int(assignedJobId.id)
                                    try:
                                        with connection.cursor() as cursor:
                                            cursor.callproc('MagicalIncome', [
                                                    userMemId,
                                                    totalJobBonus,
                                                    assJId,
                                                    validTillDate
                                                    
                                                
                                            ])


                                    except Exception as e:
                                        print('Error occurred:', str(e))
                                        # return "Error: Please try again later"
                                        
                                    
                                    try:   
                                        # Distribute community building Bonus
                                        # get activation date
                                        userActivationDate=user.activationdate
                                        if is_naive(userActivationDate):
                                    
                                            userActivationDate = make_aware(userActivationDate)
                                        
                                        # check active totaldirects within 7 days
                                        totalActiveRefers=ZqUser.objects.filter(introducerid=user.memberid,status=1,activationdate__lt=userActivationDate+timedelta(days=7)).count()
                                        
                                        if totalActiveRefers>0:
                                            if totalActiveRefers == 1:
                                                communityIncome=float(CommunityBuildingBonus.objects.get(referral_requirement=1).stage_bonus)
                                            elif totalActiveRefers == 2:
                                                communityIncome=float(CommunityBuildingBonus.objects.get(referral_requirement=2).stage_bonus)
                                            else:
                                                communityIncome=float(CommunityBuildingBonus.objects.get(referral_requirement=3).stage_bonus)
                                                
                                            #  entry for community building Bonus
                                            communityBuildingBonus=CommunityBuildingIncome.objects.create(
                                                bonus_received_from=user,
                                                receiver_memberid=user,
                                                received_bonus = communityIncome,
                                                calculated_on = totalJobBonus,
                                                calculated_on_referrals = totalActiveRefers,
                                                job_submission_date = datetime.now(),
                                                bonus_received_date = validTillDate,
                                                social_job_id=assignedJobId
                                                
                                            )
                                            
                                            
                                            # Rimberio coin distribution for social job
                                            rimberioBonus=RimberioCoinDistribution.objects.filter(task='socialJobSubmission').first().coin_reward
                                            RimberioWallet.objects.create(amount=rimberioBonus,remark=f"rimberio bonus for social job submission is {rimberioBonus}",trans_for="socialJobSubmission",tran_by=user,trans_from=user,trans_to=user,trans_date=datetime.now(),trans_type='CREDIT',package_id=assignedJobId.package_id,social_job_id=assignedJobId)

                                            # RimberioWallet.objects.create(amount=rimberioBonus,remark=f"rimberio bonus for social job submission is {rimberioBonus}",trans_for="socialJobSubmission",tran_by=user,trans_from=user,trans_to=user,trans_date=datetime.now(),trans_type='CREDIT',package_id=assignedJobId.package_id,social_job_id=assignedJobId)

                                            # downline coin distribution downline
                                            newMemId=str(user.memberid)
                                            packageIdIs=str(assignedJobId.package_id.id)
                                            assignedJobIdIs=str(assignedJobId.id)
                                            try:
                                                with connection.cursor() as cursor:
                                                    cursor.callproc('rimberio_coin_distribution_downline', [
                                                            newMemId,
                                                            1,
                                                            'SocialJobSubmitDownlineDistribution',
                                                            packageIdIs,
                                                            assignedJobIdIs
                                                            
                                                            
                                                        
                                                    ])
                                                    
                                                # print("entry done")


                                                    
                                            except Exception as e:
                                                print('Error occurred:', str(e))
                                                # return "Error: Please try again later"
                                            
                            

                                                        
                                    except Exception as e:
                                        print(f"Error Occured: {str(e)}")
                                                    

                                else:
                                    rimberioBonus=RimberioCoinDistribution.objects.filter(task='socialJobSubmission').first().coin_reward

                                    RimberioWallet.objects.create(amount=rimberioBonus,remark=f"rimberio bonus for social job submission is {rimberioBonus}",trans_for="socialJobSubmission",tran_by=user,trans_from=user,trans_to=user,trans_date=datetime.now(),trans_type='CREDIT',package_id=assignedJobId.package_id,social_job_id=assignedJobId)

                                assignedJobId.status=True
                                assignedJobId.completion_date=timezone.now()
                                
                                assignedJobId.save()
                            except Exception as e:
                                print(e)
                            
                            # return redirect('submittedSocialJobThroughLink')
                            # return True
                        # else:
                        #     return False
                        elif user and assignedJobId and assignedJobId.check_token  and assignedJobId.status :
                            continue
                    
                    else:
                        continue  

            
        return totalJobsEarnings

    except Exception as e:
        print(str(e))
        return totalJobsEarnings
    

    # if user and assignedJobId  and  not assignedJobId.check_token and not  assignedJobId.status and email_verification_token.check_token(user, token):
    #     # Handle the social job submission logic here
    #     # For example, render a form or process the job submission
    #     totalJobBonus=5
    #     assignedJobId.check_token=True
    #     assignedJobId.save()
        
    #     try:
    #         if assignedJobId.package_id:
    #             roiEnts=ROIDailyCustomer.objects.filter(userid=user.memberid,investment_id=assignedJobId.package_id).count()
    #             newobjs=ROIDailyCustomer(userid=user,remark=f'social job submission bonus $5',total_sbg=totalJobBonus,roi_sbg=totalJobBonus,roi_date=assignedJobId.valid_upto,status=1,daily_amount=totalJobBonus,roi_days=roiEnts+1,investment_id=assignedJobId.package_id,usd_rate=0,zaan_rate=0,roi_sbg_usd=totalJobBonus,zaan_value_in_usd=totalJobBonus,assigned_job_id=assignedJobId)
    #             newobjs.save()
                
    #             # distribute magical income
    #             try:
    #                 with connection.cursor() as cursor:
    #                     cursor.callproc('MagicalIncome', [
    #                             user.memberid,
    #                             totalJobBonus,
    #                             assignedJobId.id,
    #                             assignedJobId.valid_upto
                                
                            
    #                     ])


    #             except Exception as e:
    #                 print('Error occurred:', str(e))
    #                 # return "Error: Please try again later"
                    
                 
    #             try:   
    #                 # Distribute community building Bonus
    #                 # get activation date
    #                 userActivationDate=user.activationdate
    #                 if is_naive(userActivationDate):
                
    #                     userActivationDate = make_aware(userActivationDate)
                    
    #                 # check active totaldirects within 7 days
    #                 totalActiveRefers=ZqUser.objects.filter(introducerid=user.memberid,status=1,activationdate__lt=userActivationDate+timedelta(days=7)).count()
                    
    #                 if totalActiveRefers>0:
    #                     if totalActiveRefers == 1:
    #                         communityIncome=float(CommunityBuildingBonus.objects.get(referral_requirement=1).stage_bonus)
    #                     elif totalActiveRefers == 2:
    #                         communityIncome=float(CommunityBuildingBonus.objects.get(referral_requirement=2).stage_bonus)
    #                     else:
    #                         communityIncome=float(CommunityBuildingBonus.objects.get(referral_requirement=3).stage_bonus)
                            
    #                     #  entry for community building Bonus
    #                     communityBuildingBonus=CommunityBuildingIncome.objects.create(
    #                         bonus_received_from=user,
    #                         receiver_memberid=user,
    #                         received_bonus = communityIncome,
    #                         calculated_on = totalJobBonus,
    #                         calculated_on_referrals = totalActiveRefers,
    #                         job_submission_date = datetime.now(),
    #                         bonus_received_date = assignedJobId.valid_upto,
    #                         social_job_id=assignedJobId
                            
    #                     )
                        
    #             except Exception as e:
    #                 print(f"Error Occured: {str(e)}")
                    
                
                    
                
                
                    
    #         else:
    #             rimberioBonus=RimberioCoinDistribution.objects.filter(task='socialJobSubmission').first().coin_reward

    #             RimberioWallet.objects.create(amount=rimberioBonus,remark=f"rimberio bonus for social job submission is {rimberioBonus}",trans_for="socialJobSubmission",tran_by=user,trans_from=user,trans_to=user,trans_date=datetime.now(),trans_type='CREDIT')

    #         assignedJobId.status=True
    #         assignedJobId.save()
    #     except Exception as e:
    #         print(e)
        
    #     return redirect('submittedSocialJobThroughLink')
    # else:
    #     return HttpResponse('Submission link is invalid!')
    
           
    
def submittedSocialJobThroughLink(request):
    
    return render(request,'zqUsers/member/submitSocialJobThroughLink.html',context={
        'amount':5
    })



def assignSocialJobs(user,package):
    
        allDummyUsersForTesting=ZqUser.objects.filter(id=user.id)
        # allDummyUsersForTesting=ZqUser.objects.filter(is_dummy=True,username='vagak1')
        for user in allDummyUsersForTesting:
            
            
            allPackages=InvestmentWallet.objects.filter(txn_by=user,id=package.id)
            allSocialJobs=SocialJobs.objects.all()
            if allPackages.count()>0:
                isPaidUser=True
            else:
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
 
 

def sendTestmail(request, user_id):
    user = ZqUser.objects.get(pk=user_id)
    # token = email_verification_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    # asid = urlsafe_base64_encode(force_bytes(assignedSocialJobId))

    # token = long_email_verification_token.make_token(user)
    html_content = render_to_string('zqapp/emailtemps/regisuccess.html',{
                'user': user,
                'domain': request.META['HTTP_HOST'],
                # 'domain': 'www.rimberio.world',
                'uid': uid,
                # 'asid': asid,
                'token': email_verification_token.make_token(user),
            })


    with get_connection(  
                        
        host=settings.EMAIL_HOST, 
        port=settings.EMAIL_PORT,  
        username=settings.EMAIL_HOST_USER, 
        password=settings.EMAIL_HOST_PASSWORD, 
        use_tls=settings.EMAIL_USE_TLS  
    ) as connection:  
        subject = "Social Job Sumbission"  
        email_from = "noreply@ritcoin.exchange" 
        recipient_list = [user.email]  
        # message ="This is testing email" 
        body=html_content 
        sendEmail=EmailMessage(subject, body, email_from, recipient_list, connection=connection)
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


def sendMailToUser(request):
    
    if sendTestmail(request, request.user.id) :
        print("mail sent")
    else:
        print("LOOOO")
 
@login_required        
def userProfile(request):
    return render(request,'zqUsers/member/userProfile.html')


# @login_required        
def connectwallet(request):
    return render(request,'zqUsers/member/connectwall.html')


@login_required 
def sendSocialJob(request):
    
    if request.method=='POST':
        print("came ere")
        return HttpResponse("LOL")