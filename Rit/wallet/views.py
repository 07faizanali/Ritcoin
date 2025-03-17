from django.http import HttpResponse,JsonResponse
import json

from django.shortcuts import render,redirect
from zqUsers.models import ZqUser
import requests
from django.http import JsonResponse
import random
from datetime import datetime

from django.core.mail import EmailMessage,get_connection
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
# from .forms import ChangePasswordForm, LoginForm
# from .forms import UserForm
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.contrib.auth import update_session_auth_hash

from .models import *
# from .utils import send_verify_coin_mail
# from django.db import connection

# from .models import MemberHierarchy


  

@login_required   
  
def generate_wallet_address(currency):
    url = ' https://www.coinpayments.net/v1/get_deposit_address'
    API_KEY = 'bc1bfa3b7140715f11232b9791b130aaf9f7feeb48b6bcf8a94b0fff476ad162'
    API_SECRET = 'dfkdjfkdjfkdjfkfkdryeuryuiuriworriowofskdjfhskdf'


    payload = {
        'key': API_KEY,
        'secret': API_SECRET,
        'currency': currency,
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        data = response.json()
        
        # print(data)
        if data['error'] == 'ok':
            return data['result']['address']
        else:
            print(f"Error: {data['error']}")
    else:
        print(f"Request failed with status code {response.status_code}")


@login_required   

def getAddress(request):
    # Example usage
    wallet_address = generate_wallet_address('BTC')
    print(f"Generated USDT Wallet Address: {wallet_address}")



@login_required   

def myAdd(request):
  
    return render(request,'zqUsers/admin/myAdd.html')


@login_required   

def addNVerify(request):
    
    return render(request,'zqUsers/admin/addNVerify.html')


@login_required   

def withdrawl(request):
    
    return render(request,'zqUsers/admin/withdrawl.html')


@login_required   

def teamLevelWise(request):
    
    return render(request,'zqUsers/admin/teamLevelWise.html')

@login_required   

def levelIncome(request):
    
    return render(request,'zqUsers/admin/levelIncome.html')



@login_required   

def withdrawlTransaction(request):
    
    return render(request,'zqUsers/admin/withdrawlTransaction.html')


@login_required   

def directIncome(request):
    
    return render(request,'zqUsers/admin/directIncome.html')

@login_required   

def dailyROI(request):
    
    return render(request,'zqUsers/admin/dailyROI.html')




@login_required   

def accountTopup(request):
    
    return render(request,'zqUsers/admin/accountTopup.html')

@login_required   

def airdropReward(request):
    
    return render(request,'zqUsers/admin/airdropReward.html')

@login_required   

def wallet(request):
    
    return render(request,'zqUsers/admin/airdropReward.html')


@login_required   

def index(request):
    
    return render(request,'zqUsers/admin/index.html')




def get_verify_transaction(request):
    txnhash = request.POST.get('txnhash')
    types = request.POST.get('types')
    result = {}

    passamount = 0

    count_txnhash = TransactionHistoryOfCoin.objects.filter(hashtrxn=txnhash).count()
    contract = "TS7iegyYEfWZx4sVwiFPyBkdLXsqFQkrDN"

    if count_txnhash == 0:
        if types == "TRX":
            contract_ret = ""
            contract_address = ""
            contract_data_amount = 0
            timestamp_s = ""

            user_details = ZqUser.objects.get(memberid=request.user.memberid)
            client2 = requests.get(f"https://apilist.tronscan.org/api/transaction-info?hash={txnhash}")
            rresult = json.loads(client2.content)

            for key, value in rresult.items():
                if key == "timestamp":
                    timestamp_s = value
                elif key == "contractRet":
                    contract_ret = value
                elif key == "toAddress":
                    contract_address = value
                elif key == "contractData":
                    other_data = json.loads(value)
                    for sub_key, sub_value in other_data.items():
                        if sub_key == "amount":
                            amount_data = sub_value
                            contract_data_amount = round(float(amount_data) / 1000000, 2)

                if timestamp_s and contract_ret and contract_address and contract_data_amount:
                    break

            if contract_ret == "SUCCESS" and contract_address == user_details.tron_address:
                ts = float(timestamp_s)
                timestamp = ts / 1000
                ss = datetime.fromtimestamp(timestamp)
                coin_date = ss.strftime("%Y-%m-%d")

                old_coin_client = requests.get(f"http://api.coinlayer.com/{coin_date}?access_key=5f642740438cfd06236b40e9bb8a708b")
                result_old_coin = json.loads(old_coin_client.content)

                if result_old_coin["success"].lower() == "true":
                    users = ZqUser.objects.get(memberid=request.user.username)
                    coin_amount = float(contract_data_amount)
                    coin_values = result_old_coin["rates"]["TRX"]
                    trxndate = datetime.strptime(coin_date, "%Y-%m-%d")
                    status = contract_ret
                    coin_value_date = datetime.strptime(result_old_coin["date"], "%Y-%m-%d")
                    total_coin = coin_amount * coin_values
                    one_coin_value = CustomCoinRate.objects.all().first().amount
                    amicoin = (total_coin / one_coin_value) / 2
                    amivolume = amicoin * one_coin_value
                    total_invest = amicoin * 2
                    passamount = coin_amount

                    obj = TransactionHistoryOfCoin.objects.create(
                        cointype="TRX",
                        memberid=users.memberid,
                        name=users.email,
                        hashtrxn=txnhash,
                        amount=coin_amount,
                        coinvalue=coin_values,
                        trxndate=trxndate,
                        status=status,
                        coinvaluedate=coin_value_date,
                        total=total_coin,
                        amicoinvalue=one_coin_value,
                        amifreezcoin=amicoin,
                        amivolume=amivolume,
                        totalinvest=total_invest
                    )

                    result["status"] = 1
                    result["message"] = "Your transaction verify successfully"
                    # send_verify_coin_mail(total_invest, txnhash, users.email)
                else:
                    result["status"] = 0
                    result["message"] = f"Please try again {result_old_coin['success']} -date : {coin_date}"
            else:
                result["status"] = 0
                result["message"] = "Please enter correct transaction id"
        # Add the handling for other types here...

    else:
        result["status"] = 0
        result["message"] = "This transaction id is already verified"
        
    print(result)

    return JsonResponse(result)


