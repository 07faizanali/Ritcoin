from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import connection
from django.contrib.auth.hashers import make_password
# from wallet.models import InvestmentWallet
from django.db.models import Sum
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import datetime,date,timedelta
from django.utils.timezone import make_aware,is_naive


class ZqUser(AbstractUser):
    
    email = models.EmailField(unique=True)
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    opid = models.TextField(blank=True, null=True)
    memberid = models.CharField(max_length=20,unique=True)
    spillid = models.TextField(null=True)
    plain_password = models.CharField(max_length=255,null=True)
    # introducerid = models.CharField(max_length=20,null=True)
    introducerid = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, to_field='memberid', related_name='introduced_users')
    associated_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, to_field='memberid',db_column='associated_id' ,related_name='associated_users')
    introducer_username = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, to_field='username',db_column='introducer_username' ,related_name='introducer_usernames')
    
    gender = models.TextField(blank=True, null=True)
    # username = models.TextField(blank=True, null=True)
    father_spouse_name = models.TextField(db_column='Father_Spouse_name', blank=True, null=True)  # Field name made lowercase.
    dob = models.DateField(auto_now_add=True)
    country = models.TextField(blank=True, null=True)
    local_currency = models.CharField(blank=True, null=True, max_length=255)
    address = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=50, null=True)
    pincode = models.IntegerField(null=True)
    mobile = models.TextField(blank=True, null=True)
    # email = models.TextField()
    joindate = models.DateTimeField(auto_now_add=True)
    nominee = models.TextField(null=True)
    age = models.FloatField(null=True)  # Field name made lowercase.
    relation = models.TextField(null=True)
    # status = models.BooleanField()
    status = models.BooleanField(default=False)
    userType=models.CharField(max_length=50,default='member')

    bankname = models.TextField( null=True)  # Field name made lowercase.
    branchname = models.TextField(null=True)  # Field name made lowercase.
    accountholder = models.TextField(null=True)  # Field name made lowercase.
    accountno = models.IntegerField(default=0)  # Field name made lowercase.
    accounttype = models.TextField(null=True)  # Field name made lowercase.
    ifsc = models.TextField( null=True)  # Field name made lowercase.
    pan = models.TextField( null=True)  # Field name made lowercase.
    rank = models.IntegerField(default=0)
    bankaccountno = models.TextField( null=True)  # Field name made lowercase.
    pinused = models.IntegerField(null=True)
    position = models.IntegerField(default=0)
    dsiid = models.TextField( null=True)  # Field name made lowercase.
    uid = models.IntegerField(default=0)
    activationdate = models.DateTimeField(null=True)
    aadhaar = models.TextField(null=True)
    
    # image = 
    bank_img = models.TextField(blank=True, null=True)
    pan_img = models.TextField(blank=True, null=True)
    aadhaar_img = models.TextField(blank=True, null=True)
   
    
    
    kyc_status = models.BooleanField(default=False)
    registrationtype = models.TextField(db_column='RegistrationType', blank=True, null=True)  # Field name made lowercase.
    topnewid = models.TextField(db_column='Topnewid', blank=True, null=True)  # Field name made lowercase.
    profile_pic = models.TextField(db_column='Profile_pic', blank=True, null=True)  # Field name made lowercase.
    pin_amount = models.FloatField(db_column='Pin_Amount',default=0)  # Field name made lowercase.
    poolnumber = models.IntegerField(null=True)
    uid1 = models.IntegerField(null=True)
    position1 = models.IntegerField(null=True)
    spillid1 = models.TextField(blank=True, null=True)
    isleader = models.IntegerField(db_column='isLeader',null=True)  # Field name made lowercase.
    zqcoin_address = models.TextField (null=True)
    tron_address = models.TextField(null=True)
    btc_address = models.TextField(null=True)
    eth_address = models.TextField(null=True)
    bnb_address = models.TextField(null=True)
    usdt_address = models.TextField(null=True)
    withdrawal_zqcoin_address = models.TextField(null=True)
    withdrawal_tron_address = models.TextField(null=True)
    withdrawal_eth_address = models.TextField(null=True)
    withdrawal_bnb_address = models.TextField(null=True)
    withdrawal_usdt_address = models.TextField(null=True)
    withdrawal_btc_address = models.TextField(null=True)
    
    intro_email = models.TextField()
    activation_time_btc_rate = models.FloatField(null=True)
    activation_time_trx_rate = models.FloatField(null=True)
    activation_time_eth_rate = models.FloatField(null=True)
    activation_by = models.TextField(blank=True, null=True)
    activation_time_no_of_btc = models.FloatField(null=True)
    activation_time_no_of_trx = models.FloatField(null=True)
    activation_time_no_of_eth = models.FloatField(null=True)
    is_verfied = models.BooleanField(default=False)
    #  = models.BooleanField(default=False)
    txn_password=models.CharField(max_length=255,null=True)
    phone_number=models.CharField(max_length=15,null=True)
    is_mining_activated=models.BooleanField(default=False)
    is_dummy=models.BooleanField(default=False)
    is_blocked=models.BooleanField(default=False)
    is_withdrawal_blocked=models.BooleanField(default=False)
    

    
    def doesMemberHaveAssocialtedIds(self):
        allIds=ZqUser.objects.filter(associated_id=self)
        
        if allIds.count()>0:
            return True
        return False
    
    def isGroupedId(self):
        if self.associated_id:
            return True
        else:
            return False
       

    
    def groupIncome(self):
        
        totalIncome=0
        if self.doesMemberHaveAssocialtedIds():
            # print(self.associated_users.all())
            for user in self.associated_users.all():
                # print(user)
                totalIncome+=user.totalWalletBalance()
      
        
        return float(totalIncome)
                
    def totalGroupInvestments(self):
        totalIncome=0
        if self.doesMemberHaveAssocialtedIds():
            # print(self.associated_users.all())
            for user in self.associated_users.all():
                # print(user)
                totalIncome+=user.totalInvestments()
      
        
        return float(totalIncome)
        
    def totalGroupDirectIncome(self):
        totalIncome=0
        if self.doesMemberHaveAssocialtedIds():
            # print(self.associated_users.all())
            for user in self.associated_users.all():
                # print(user)
                totalIncome+=user.totalDirectIncome()
      
        return float(totalIncome)
        
    def totalGroupLevelIncome(self):
        totalIncome=0
        if self.doesMemberHaveAssocialtedIds():
            # print(self.associated_users.all())
            for user in self.associated_users.all():
                # print(user)
                totalIncome+=user.totalLevelIncome()
      
        return float(totalIncome)
       
     
    def totalGroupCommunityBuildingIncome(self): 
        totalIncome=0
        if self.doesMemberHaveAssocialtedIds():
            # print(self.associated_users.all())
            for user in self.associated_users.all():
                # print(user)
                totalIncome+=user.CommunityBuildingIncome()
      
        return float(totalIncome)
        
    def totalGroupRimberioWalletBalance(self): 
        totalIncome=0
        if self.doesMemberHaveAssocialtedIds():
            # print(self.associated_users.all())
            for user in self.associated_users.all():
                # print(user)
                totalIncome+=user.totalRimberioWalletBalance()
      
        return float(totalIncome)
        
    def totalGroupMagicalBonus(self): 
        totalIncome=0
        if self.doesMemberHaveAssocialtedIds():
            # print(self.associated_users.all())
            for user in self.associated_users.all():
                # print(user)
                totalIncome+=user.totalMagicalIncome()
      
        return float(totalIncome)
        
    def totalGroupClubBonus(self): 
        totalIncome=0
        if self.doesMemberHaveAssocialtedIds():
            # print(self.associated_users.all())
            for user in self.associated_users.all():
                # print(user)
                totalIncome+=user.totalClubBonus()
      
        return float(totalIncome)  
        
        
    def totalGroupSocailJobBonus(self): 
        totalIncome=0
        if self.doesMemberHaveAssocialtedIds():
            # print(self.associated_users.all())
            for user in self.associated_users.all():
                # print(user)
                totalIncome+=user.totalMiningBonus()
      
        return float(totalIncome)
        
    def totalGroupPrepaidBonus(self): 
        totalIncome=0
        if self.doesMemberHaveAssocialtedIds():
            # print(self.associated_users.all())
            for user in self.associated_users.all():
                # print(user)
                totalIncome+=user.totalPrepaidBonus()
      
        return float(totalIncome)
    
    def totalGroupWithdrawal(self): 
        totalIncome=0
        if self.doesMemberHaveAssocialtedIds():
            # print(self.associated_users.all())
            for user in self.associated_users.all():
                # print(user)
                totalIncome+=user.totalWithdrawals()
      
        return float(totalIncome)
        
    
    def totalSelfInvs(self):
        totalInvestments=float(InvestmentWallet.objects.filter(txn_by=self,activated_by=self).aggregate(Sum('amount'))['amount__sum'] or 0)
        return totalInvestments
    
    
    def totalInvestments(self):
        
        totalInvAmount=InvestmentWallet.objects.filter(txn_by=self).aggregate(Sum('amount'))['amount__sum'] or 0
        print('total investments are',totalInvAmount)
        return totalInvAmount

   
    
    def getMagicalBonusTotal(self,member):
        
        
        # if self.doesMemberHaveAssocialtedIds();
        currDate=datetime.now()    
        totalBonus=0
        if is_naive(currDate):
            currDate=make_aware(currDate)
            
        allSjs=  MagicalIncome.objects.filter(members=self,intronewid=member)
        for sj in   allSjs:
            sjRoidate=sj.last_paid_date
            if is_naive(sjRoidate):
                sjRoidate=make_aware(sjRoidate)
                
            if  sjRoidate<currDate:
                totalBonus+=sj.rs
                
                
            
          
        return  totalBonus


       
    
    def totalPeerInvestments(self):
        
        return InvestmentWallet.objects.filter(txn_by=self).exclude(activated_by=self).aggregate(Sum('amount'))['amount__sum'] or 0

        # return InvestmentWallet.objects.filter(txn_by=self,activated_by=self).aggregate(Sum('amount'))['amount__sum'] or 0
    
 

    def totalDirectIncome(self):
        totalDirectAmount=Income1.objects.filter(intronewid=self).aggregate(Sum('rs'))['rs__sum'] or 0
        print('total direct income is',totalDirectAmount)
        return totalDirectAmount
    
    def CommunityBuildingIncome(self):
        
        currDate=datetime.now() 
        totalBonus=0
        if is_naive(currDate):
            currDate=make_aware(currDate)
            
        allSjs= self.communitybuilding_receiver.all()
        for sj in   allSjs:
            sjRoidate=sj.bonus_received_date
            if is_naive(sjRoidate):
                sjRoidate=make_aware(sjRoidate)
                
            if  sjRoidate<currDate:
                totalBonus+=sj.received_bonus
                
                
            
          
        return   totalBonus
        
        # return self.communitybuilding_receiver.filter(bonus_received_date__lt=datetime.now()).aggregate(Sum('received_bonus'))['received_bonus__sum'] or 0
        # return 0
    
  
    def totalRimberioWalletBalance(self):
        # print(self.totalRimberioWalletBalance(),'is total ritcoins')
        TOTALCREDITS=self.RimberioWallet_tranby_member.filter(trans_type='CREDIT').aggregate(Sum('amount'))['amount__sum'] or 0
        TOTALDEBTS=self.RimberioWallet_tranby_member.filter(trans_type='DEBIT').aggregate(Sum('amount'))['amount__sum'] or 0
        # print(tbl)
        return float(TOTALCREDITS-TOTALDEBTS)
    
  
    def totalMagicalIncome(self):
        
        currDate=datetime.now()    
        totalBonus=0
        if is_naive(currDate):
            currDate=make_aware(currDate)
            
        allSjs= self.magicalIncome_intros.all()
        for sj in   allSjs:
            sjRoidate=sj.last_paid_date
            if is_naive(sjRoidate):
                sjRoidate=make_aware(sjRoidate)
                
            if  sjRoidate<currDate:
                totalBonus+=sj.rs
                
                
            
          
        return  totalBonus
        # return  0
        # return self.magicalIncome_intros.all().aggregate(Sum('rs'))['rs__sum'] or 0
        # return self.magicalIncome_intros.filter(last_paid_date__lt=datetime.now()).aggregate(Sum('rs'))['rs__sum'] or 0
    
  
    def totalLevelIncome(self):
        # print(Income2.objects.filter(intronewid=self.memberid).aggregate(Sum('rs_usd'))['rs_usd__sum'])
        return Income2.objects.filter(intronewid=self.memberid).aggregate(Sum('rs'))['rs__sum'] or 0
    
    
    def totalClubBonus(self):
        # print("===========")
        # print(self.clubIncomeMember_zquser.all().aggregate(Sum('bonus_income'))['bonus_income__sum'])
        return float(self.clubIncomeMember_zquser.all().aggregate(Sum('bonus_income'))['bonus_income__sum'] or 0)
    
  
    def totalMiningBonus(self):
        currDate=datetime.now()
        
        totalBonus=0
        if is_naive(currDate):
            currDate=make_aware(currDate)
            
        allSjs= ROIDailyCustomer.objects.filter(userid=self)
        for sj in   allSjs:
            sjRoidate=sj.roi_date
            if is_naive(sjRoidate):
                sjRoidate=make_aware(sjRoidate)
                
            if  sjRoidate<currDate:
                totalBonus+=sj.roi_sbg
                
                
            
          
        return   totalBonus
        # return ROIDailyCustomer.objects.filter(userid=self,roi_date__lt=currDate).aggregate(Sum('roi_sbg'))['roi_sbg__sum'] or 0
    
 
    def totalPendingWithdrawl(self):
        return WalletAMICoinForUser.objects.filter(memberid=self,paystatus='pending').aggregate(Sum('total_value_zaan'))['total_value_zaan__sum'] or 0
    
    
    def allTopUpsByPeer(self):
        # return self.wallettab_member.filter(txn_type='CREDIT',col3="Deposit",col5="TOPUPFORPEER").aggregate(Sum('amount'))['amount__sum'] or 0
        getTm= float(InvestmentWallet.objects.filter(txn_by=self).exclude(activated_by=self).aggregate(Sum('amount'))['amount__sum'] or 0)
        
        print('total is',getTm)
        return getTm
    
    

    
    def allTopUpsForPeer(self):
        # allTopUps=self.wallettab_member.filter(txn_type='DEBIT',col3="TOPUPFORPEER").aggregate(Sum('amount'))['amount__sum'] or 0
        allTopUps=float(InvestmentWallet.objects.filter(activated_by=self).exclude(txn_by=self).aggregate(Sum('amount'))['amount__sum'] or 0)
        # print(allTopUps)
        # print("prit al topups are",allTopUps)
        return float(allTopUps)
    
    
    def totalAllBonus(self):
        allDirectIncome=self.totalDirectIncome()
        totalLevelIncome=self.totalLevelIncome()
        totalROI=self.totalMiningBonus()
        totalClubBonus=self.totalClubBonus()
        totalMagicalIncome=self.totalMagicalIncome()
        CommunityBuildingIncome=self.CommunityBuildingIncome()
        
        return allDirectIncome+totalLevelIncome+totalROI+totalClubBonus+totalMagicalIncome+CommunityBuildingIncome
    

    
    def totalApprovedWithdrawl(self):
        return WalletAMICoinForUser.objects.filter(memberid=self,paystatus='success').aggregate(Sum('total_value_zaan'))['total_value_zaan__sum'] or 0
    
   

        
    def totalCreditAmount(self):
        return self.wallettab_member.filter(txn_type='CREDIT').exclude(col3='DIRECT INCOME').exclude(col3='LEVEL INCOME').aggregate(Sum('amount'))['amount__sum'] or 0
    
    
    def totalPeerTopupsN(self):
        return float(self.transaction_history.filter(tran_type='DEBIT',hashtrxn='peerActivate',status=1).aggregate(Sum('amount'))['amount__sum'] or 0)

    def totalDepositsWithoutPeer(self):
            return self.transaction_history.filter(tran_type='CREDIT',status='success').exclude(hashtrxn='PEER TOPUP').aggregate(Sum('amount'))['amount__sum'] or 0

        
    def totalDeposits(self):
        # if self.username == 'Hemant':
        #     return self.transaction_history.filter(tran_type='CREDIT').aggregate(Sum('amount'))['amount__sum'] or 0
        
        return self.transaction_history.filter(tran_type='CREDIT',status='success').aggregate(Sum('amount'))['amount__sum'] or 0
    
    def totalDirectCoins(self):
        # if self.username == 'Hemant':
        #     return self.transaction_history.filter(tran_type='CREDIT').aggregate(Sum('amount'))['amount__sum'] or 0
            # def totalRimberioWalletBalance(self):
        # print(self.totalRimberioWalletBalance(),'is total ritcoins')
        tbl=self.RimberioWallet_tranby_member.filter(remark='direct income').aggregate(Sum('amount'))['amount__sum'] or 0
        print(tbl)
        return float(tbl)
        # return self.transaction_history.filter(tran_type='CREDIT',status='success').aggregate(Sum('amount'))['amount__sum'] or 0
    
    def totalDepositsByAdmin(self):
        return self.transaction_history.filter(tran_type='CREDIT',deposit_by_admin=True,status='success').aggregate(Sum('amount'))['amount__sum'] or 0

    def totalRemainingTopupFund(self):
        ...

    def totalAdminWithdrawals(self):
            return self.walletAMICoinMember_zquser.filter(remark='admin_withdrawal').aggregate(Sum('amicoinin_doller'))['amicoinin_doller__sum'] or 0
   
    def totalSelfWithdrawals(self):
            return float(self.totalWithdrawals()-self.totalAdminWithdrawals())
 
    def totalDebitAmount(self):
        return self.wallettab_member.filter(txn_type='DEBIT').exclude(col3='DIRECT INCOME').exclude(col3='LEVEL INCOME').aggregate(Sum('amount'))['amount__sum'] or 0
    
 
    def totalWithdrawals(self):
        return self.walletAMICoinMember_zquser.all().aggregate(Sum('amicoinin_doller'))['amicoinin_doller__sum'] or 0
    
    
    
    def totalWalletBalance(self):
    
        allDirectIncomes=float(self.totalDirectIncome())       
        totalWithdrawals=float(self.totalWithdrawals())
        totalSelfDeposits= self.transaction_history.filter(tran_type='CREDIT',status='success').exclude(hashtrxn='PEER TOPUP').aggregate(Sum('amount'))['amount__sum'] or 0
        totalPeerDeposits= self.transaction_history.filter(tran_type='CREDIT',status='success',hashtrxn='PEER TOPUP').aggregate(Sum('amount'))['amount__sum'] or 0
       
        # totalDeposits=float(self.totalDeposits())       
        totalSelfInvestments=float(InvestmentWallet.objects.filter(txn_by=self,activated_by=self).aggregate(Sum('amount'))['amount__sum'] or 0)
        totalPeerInvestment=float(self.totalPeerInvestments())
        totalallTopUpsForPeer=float(self.allTopUpsForPeer())
        # totalallTopUpsByPeer=float(self.allTopUpsByPeer())
        # totalPeerTopupsN=float(self.totalPeerTopupsN())
  
        inZAAN=round(totalSelfDeposits+totalPeerDeposits+allDirectIncomes-totalSelfInvestments-totalPeerInvestment-totalWithdrawals-totalallTopUpsForPeer, 2)
        
        if inZAAN<0:
            inZAAN=0
        
        return inZAAN
    
    
    def totalRealWalletBalance(self):
        
        # ZQLRate=
        # ZQLRate=CustomCoinRate.objects.order_by('-id').first().amount
        credit=self.totalCreditAmount()
        debit=self.totalDebitAmount()
        # totalROI=self.totalMiningBonus()
        # totalROI=float(self.totalMiningBonus())
        allDirectIncomes=float(self.totalDirectIncome())
        allLevelIncomes=float(self.totalLevelIncome())
        allMagicalIncomes=float(self.totalMagicalIncome())
        allCommunityBuildingIncome=float(self.CommunityBuildingIncome())
        alltotalMiningIncome=float(self.totalMiningBonus())
        totalWithdrawals=float(self.totalWithdrawals())
        totalDeposits=float(self.totalDeposits())
        # totalInvestments=float(self.totalInvestments())
        totalInvestments=float(InvestmentWallet.objects.filter(txn_by=self,activated_by=self).aggregate(Sum('amount'))['amount__sum'] or 0)
        totalPeerInvestment=float(self.totalPeerInvestments())
        totalallTopUpsForPeer=float(self.allTopUpsForPeer())
        totalallTopUpsByPeer=float(self.allTopUpsByPeer())
        totalClubBonus=float(self.totalClubBonus())
        
        if self.doesMemberHaveAssocialtedIds():
            groupTotalIncome=self.groupIncome()
            
        else:
            groupTotalIncome=0
        
        allLevelIncomes=self.totalLevelIncome()
        

        
        
        inZAAN=round(totalallTopUpsByPeer+allDirectIncomes+totalClubBonus+groupTotalIncome+allLevelIncomes+allMagicalIncomes+allCommunityBuildingIncome+alltotalMiningIncome+totalDeposits-totalInvestments-totalPeerInvestment-totalWithdrawals-totalallTopUpsForPeer, 2)
      
        
        return inZAAN
    
    
    
    def totalWithdrawalableBalance(self):
        
        # print("came her")
        
        # totalDeposits
        
        totalWalletBalance=float(self.totalWalletBalance())
        # totalInvestments=float(InvestmentWallet.objects.filter(txn_by=self,activated_by=self).aggregate(Sum('amount'))['amount__sum'] or 0)
        # totalallTopUpsForPeer=float(self.allTopUpsForPeer())
        # totalAdminWithdrawals=float(self.totalAdminWithdrawals())
        # totalDeposits=float(self.totalDeposits())
        
        # totalAdminDeposits=self.transaction_history.filter(tran_type='CREDIT',deposit_by_admin=True,status='success').aggregate(Sum('amount'))['amount__sum'] or 0
        totalRemaining=float(self.totalRemainingAdminDeposits())
        allTotalBonus=float(self.totalAllBonus())
        # if (totalDeposits-totalAdminDeposits)>0:
        
        # print(totalRemaining)
        # print(allTotalBonus)
        
        print('withdrawable balance is,',totalWalletBalance-totalRemaining)
        if totalRemaining>0:
            # return totalDeposits-totalRemaining+allTotalBonus
            return totalWalletBalance-totalRemaining
        else:
            return totalWalletBalance
        
        
  

    
    def totalRealWithdrawalableBalance(self):
        
        # print("came her")
        
        totalWalletBalance=float(self.totalWalletBalance())
        totalInvestments=float(InvestmentWallet.objects.filter(txn_by=self,activated_by=self).aggregate(Sum('amount'))['amount__sum'] or 0)
        totalallTopUpsForPeer=float(self.allTopUpsForPeer())
        totalAdminWithdrawals=float(self.totalAdminWithdrawals())

        totalAdminDeposits=self.transaction_history.filter(tran_type='CREDIT',deposit_by_admin=True,status='success').aggregate(Sum('amount'))['amount__sum'] or 0
        totalWithdrawableBalance=totalWalletBalance
        if totalInvestments<totalAdminDeposits:
            
          
            if totalallTopUpsForPeer>0:
                remainingAdminBalance=(totalAdminDeposits-totalInvestments-totalallTopUpsForPeer-totalAdminWithdrawals)
                # print("reaming balance is",remainingAdminBalance)
                if remainingAdminBalance>0:
                    totalWithdrawableBalance=totalWalletBalance-remainingAdminBalance
                # else:
                #     totalWithdrawableBalance=totalWalletBalance
            else:
                remainingAdminBalance=(totalAdminDeposits-totalInvestments-totalAdminWithdrawals)
                
                if remainingAdminBalance>0:
                    totalWithdrawableBalance=totalWalletBalance-remainingAdminBalance
                # else:
                #     totalWithdrawableBalance=totalWalletBalance

     
        
        
        
        # print('came here')
        # if totalWithdrawableBalance<0:
        #     totalWithdrawableBalance=0
        
        return totalWithdrawableBalance
    
    
    def totalRemainingAdminDeposits(self):
     
        totalInvestments=float(InvestmentWallet.objects.filter(txn_by=self,activated_by=self).aggregate(Sum('amount'))['amount__sum'] or 0)
        totalallTopUpsForPeer=float(self.allTopUpsForPeer())
        
        # print("all topus for per are",totalallTopUpsForPeer)
        totalAdminWithdrawals=float(self.totalAdminWithdrawals())

        totalAdminDeposits=self.transaction_history.filter(tran_type='CREDIT',deposit_by_admin=True,status='success').aggregate(Sum('amount'))['amount__sum'] or 0
        
        if totalAdminDeposits>0:
        
            if totalallTopUpsForPeer>0:
                remainingAdminBalance=(totalAdminDeposits-totalInvestments-totalallTopUpsForPeer-totalAdminWithdrawals)
                if remainingAdminBalance>0:
                    totalWithdrawableBalance=remainingAdminBalance
                else:
                    totalWithdrawableBalance=0
                # else:
                #     totalWithdrawableBalance=totalWalletBalance
            else:
                remainingAdminBalance=(totalAdminDeposits-totalInvestments-totalAdminWithdrawals)
                
                if remainingAdminBalance>0:
                    totalWithdrawableBalance=remainingAdminBalance
                else:
                    totalWithdrawableBalance=0
                  
        else:
            totalWithdrawableBalance=0
              

        return totalWithdrawableBalance

            
    
    def totalPrepaidBonus(self):
        current_date = timezone.now()
        allPackages=InvestmentWallet.objects.filter(txn_by=self)
        totalBonus=0
        # print(allPackages.count()>0)
        # print(self.memberid)
        if allPackages.count()>0:
            
            
            for package in allPackages:
                    
                # print(AssignedSocialJob.objects.filter(assigned_to=self,status=0,package_id=package,valid_from__lt=current_date,valid_upto__gt=current_date).first())
                try:
                    # lastestAssignedJob=AssignedSocialJob.objects.filter(assigned_to=self,status=0,package_id=package,valid_from__lt=current_date,valid_upto__gt=current_date).order_by('id').first()
                    lastestAssignedJob=AssignedSocialJob.objects.filter(assigned_to=self,package_id=package,valid_from__lt=current_date,valid_upto__gt=current_date).order_by('id').first()
                    # print(lastestAssignedJob)
                    # print(self.prepaid_memberid.filter(memberid=self.memberid,assigned_task_id=lastestAssignedJob.id,given_date__lt=current_date).count())
                    totalBonus+=float(self.prepaid_memberid.filter(memberid=self,assigned_task_id=lastestAssignedJob,given_date__lt=current_date).aggregate(Sum('bonus'))['bonus__sum'] or 0)
                    # print(totalBonus)
                except Exception as e:
                    print(e)
        
        # else:
            # lastestAssignedJob=AssignedSocialJob.objects.filter(assigned_to=self,status=0,valid_from__lt=current_date,valid_upto__gt=current_date).order_by('id').first()

        return totalBonus

        
    
    def isClubMem(self):
        memClub=ClubMembers.objects.filter(memberid=self)
    
        if memClub.count()>0:
            
            return True
        else:
            return False
    
    def totalDirectMems(self):
        # print("came here")
        # print(ZqUser.objects.filter(introducerid=self).count())
        return ZqUser.objects.filter(introducerid_id=self.memberid).count()
    
    def totalDirectActivMems(self):
        # print("came here")
        # print(ZqUser.objects.filter(introducerid=self).count())
        return ZqUser.objects.filter(introducerid_id=self.memberid,status=1).count()
    
    def totalAllMems(self):
        # print("came here")
        # print(ZqUser.objects.filter(introducerid=self).count())
        return self.totalDirectMems()+self.totalLevelTeam()
    
    def totalToups(self):
        # print("came here")
        # print(ZqUser.objects.filter(introducerid=self).count())
        return InvestmentWallet.objects.filter(txn_by=self).count()
    
    def totalCoins(self):
        return RimberioWallet.objects.filter(txn_by=self).count()
    

   
  
    def get_introducer_hierarchy(self,member_id):
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


 
        
    def totalLevelActiveTeam(self):
        lt = self.get_introducer_hierarchy(self.username)
        unique_users = list({user for user, _ in lt if user.status})
        if len(unique_users)>0:
            return len(unique_users)-1
        else:
            return 0
    def totalLevelTeam(self):
        lt = self.get_introducer_hierarchy(self.username)
        unique_users = list({user for user, _ in lt})
        
        return len(unique_users)-1
        
      


    def save(self, *args, **kwargs):
       
        
        if not self.pk:  # Check if the object is being created for the first time
          
        # super().save(*args, **kwargs)
            last_member = ZqUser.objects.order_by('-memberid').first()  # Get the last member
            if last_member:
                last_member_id = int(last_member.memberid[3:])  # Extract the numeric part
                new_member_id = last_member_id + 1
                self.memberid = 'RBO{:06d}'.format(new_member_id)  # Format the new member id
            else:
                self.memberid = 'RBO000001'  # If there are no existing members
                
            # if self.password:
            #     self.password = make_password(self.password)
        # self.full_clean() 
        super().save(*args, **kwargs)  # Call the save method of the superclass


    class Meta:
        managed = False
        db_table = 'zqusers_zquser'
        ordering = ['-date_joined'] 




class AllPackageDetails(models.Model):
    # cointype = models.CharField(max_length=100)

    package_name = models.CharField(max_length=100)
    package_price = models.FloatField()
    multiplier = models.IntegerField()
    added_date = models.DateTimeField()
 
    
    class Meta:
        db_table = 'all_package_details'
        managed=False  



       
class TransactionHistoryOfCoin(models.Model):
    cointype = models.CharField(max_length=100)
    memberid = models.ForeignKey(ZqUser, on_delete=models.CASCADE, to_field='memberid', related_name='transaction_history')

    name = models.CharField(max_length=255)
    hashtrxn = models.CharField(max_length=255)
    amount = models.FloatField()
    coinvalue = models.FloatField()
    trxndate = models.DateTimeField()
    status = models.CharField(max_length=100)
    coinvaluedate = models.DateTimeField()
    total = models.FloatField()
    amicoinvalue = models.FloatField()
    amifreezcoin = models.FloatField()
    amivolume = models.FloatField()
    totalinvest = models.FloatField()
    tran_type = models.CharField(max_length=100,null=True)
    deposit_by_admin = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'wallet_transactionhistoryofcoin'
        managed=False  


class MemberHierarchy(models.Model):
    # Define fields that match the structure of your temporary table
    member_id = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    referral_email = models.CharField(max_length=100, unique=True)
    date_of_reg = models.DateField()
    level = models.IntegerField()
    sbg_coin = models.IntegerField()
    status = models.IntegerField()

    class Meta:
        managed = False  # Specify managed = False to prevent Django from managing the table
        db_table = 'MemberHierarchy'

    @classmethod
    def fetch_data(cls):
        # Use a raw SQL query to fetch data from the temporary table
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM MemberHierarchy")
            rows = cursor.fetchall()
        return rows


class Investment(models.Model):
    user = models.ForeignKey(ZqUser,to_field='memberid', on_delete=models.CASCADE)
    investment_amount = models.FloatField()
    start_time = models.DateTimeField(auto_now_add=True)
    current_return = models.FloatField(default=0)  
    
    class Meta:
        db_table = 'daily_roi' 
        managed=False 
        
    def save(self, *args, **kwargs):
        # Check if ZqUser instance is provided, if not, fetch ZqUser using memberid
        if not isinstance(self.user, ZqUser):
            try:
                self.user = ZqUser.objects.get(memberid=self.user)
            except ZqUser.DoesNotExist:
                raise ValueError("ZqUser with memberid '{}' does not exist".format(self.user))
        
        super().save(*args, **kwargs)
    
    
class ROIRates(models.Model):
    
    rate = models.FloatField()
    set_date = models.DateTimeField()
    # current_return = models.FloatField(default=0)  
    
    # def isROIHasBeenDistributedForGivenDate(self,roiDate):
    #     return ROIDailyCustomer.objects.filter(roi_date=roiDate).count()>0
    
    
    class Meta:
        managed=False
        db_table = 'roi_rates' 
    

class DownlineLevel(models.Model):
    
    memberid = models.ForeignKey(ZqUser, on_delete=models.CASCADE, related_name='downline_levels')

    # memberid = models.CharField(max_length=100)
    email = models.EmailField()
    membername = models.CharField(max_length=100)
    # introducerid = models.CharField(max_length=100)
    introducerid = models.ForeignKey(ZqUser, on_delete=models.CASCADE, related_name='introduced_downlines')

    status = models.BooleanField(default=False)
    pinamount = models.CharField(max_length=100,null=True)
    joindate = models.DateTimeField()
    levelno = models.IntegerField(default=1)  # Changed LevelNo to levelno to follow Python naming convention

    def __str__(self):
        return
    class Meta:
        managed = False    
    
class NewLogin(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.CharField(max_length=255)
    emailid = models.EmailField()
    password = models.CharField(max_length=255)
    reg_date = models.DateField()
    status = models.IntegerField()
    type = models.CharField(max_length=255)
    lastlogin = models.DateTimeField()
    currentlogin = models.DateTimeField()

    class Meta:
        db_table = 'newlogin'
        managed=False 


class PackageAssign(models.Model):
    PackageIssueId = models.AutoField(primary_key=True)
    MemberNewId = models.CharField(max_length=50)
    MemberId = models.IntegerField()
    MemberName = models.CharField(max_length=255)
    MemberIntroId = models.CharField(max_length=50)
    MemberIntroName = models.CharField(max_length=255)
    MemberRegisDate = models.DateField()
    Package = models.IntegerField()
    DSI = models.IntegerField()
    PV = models.IntegerField()
    CapLimit = models.CharField(max_length=255)
    PackageIssueDate = models.DateField()
    PackagePin = models.CharField(max_length=255)
    packageid = models.IntegerField()  # Add this field if it exists in your database

    class Meta:
        db_table = 'PackageAssign'
        managed=False 
        
     
class TempDailyROI(models.Model):
    userid = models.CharField(max_length=100)
    roi_date = models.DateField()
    roi_sbg = models.FloatField()
    total_sbg = models.FloatField()
    roi_days = models.IntegerField()
    remark = models.CharField(max_length=255)

    def __str__(self):
        
        return f"ROI for {self.userid} on {self.roi_date}"
    class Meta:
        managed = False
    
    
    
class InvestmentWallet(models.Model):
    id = models.AutoField(primary_key=True)
    txn_by = models.ForeignKey(ZqUser, on_delete=models.CASCADE, to_field='memberid',db_column='txn_by_id', related_name='investmentwallet_member')
    amount = models.FloatField()
    zaan_rate = models.FloatField(default=0)
    usd_rate = models.FloatField(default=0)
    zaan_value_in_usd = models.FloatField(default=0)
    remark=models.TextField(blank=True,null=True)
    activated_by = models.ForeignKey(ZqUser, on_delete=models.SET_NULL, to_field='memberid',db_column='activated_by', related_name='activatedbytopup_member',null=True)
    # group_id= models.IntegerField(null=True)
    # group_id = models.ForeignKey(ZqUser, on_delete=models.SET_NULL, to_field='memberid',db_column='activated_by', related_name='activatedbytopup_member',null=True)
    group_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, to_field='id',db_column='group_id', related_name='inv_groups')

    txn_date = models.DateTimeField(auto_now_add=True)
    txn_type = models.CharField(max_length=255,default='CREDIT')
    class Meta:
        managed = False
        # managed
        db_table = 'wallet_investmentwallet'
        ordering = ['-txn_date']

    # def __str__(self):
class QrTransDetails(models.Model):
    id = models.AutoField(primary_key=True)
    memberid = models.CharField(max_length=255)
    client_txn_id = models.TextField()
    amount = models.FloatField()
  
    class Meta:
        managed = False
        # managed
        db_table = 'qr_trans_details'

class LevelBonusDetails(models.Model):
    level=models.IntegerField()
    required_directs=models.IntegerField()
    income_rate=models.FloatField(default=0)
    
    
    class Meta:
        managed = False
        db_table = 'level_income'
        
class MagicBonusDetails(models.Model):
    level=models.IntegerField()
    required_directs=models.IntegerField()
    bonus_percent=models.FloatField(default=0)
    
    
    class Meta:
        managed = False
        db_table = 'magical_bonus'
 
class Income2(models.Model):
    srno = models.AutoField(primary_key=True)
    introid = models.IntegerField()
    # intronewid = models.CharField(max_length=255)
    intronewid = models.ForeignKey(ZqUser,to_field='memberid', db_column='intronewid',on_delete=models.CASCADE,related_name='income2_intros')

    introname = models.CharField(max_length=255)
    
    rs = models.FloatField()
    rs_usd = models.FloatField(default=0)
    zaan_rate = models.FloatField(default=0)
    usd_rate = models.FloatField(default=0)
    package_usd = models.FloatField(default=0)
    date = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    status = models.IntegerField()
    point = models.IntegerField()
    package = models.FloatField()
    nextsunday = models.DateField()
    # members = models.CharField(max_length=255)
    members = models.ForeignKey(ZqUser,to_field='memberid', on_delete=models.CASCADE,db_column='members' ,related_name='income2_members')
    package_id = models.ForeignKey(InvestmentWallet,to_field='id', on_delete=models.CASCADE,db_column='package_id' ,related_name='income2_packageid',null=True)
    multiplier = models.IntegerField()
    # position = models.IntegerField()
    position = models.IntegerField()
    custid = models.IntegerField()
    custnewid = models.CharField(max_length=255)
    custname = models.CharField(max_length=255)
    paidstatus = models.IntegerField()
    last_paid_date = models.DateField()

    class Meta:
        db_table = 'income2'
        managed=False 
        
class LevelIncomeBonus(models.Model):
    srno = models.AutoField(primary_key=True)
    introid = models.IntegerField()
    # intronewid = models.CharField(max_length=255)
    intronewid = models.ForeignKey(ZqUser,to_field='memberid', db_column='intronewid',on_delete=models.CASCADE,related_name='income2new_intros')

    introname = models.CharField(max_length=255)
    
    rs = models.FloatField()
    rs_usd = models.FloatField(default=0)
    zaan_rate = models.FloatField(default=0)
    usd_rate = models.FloatField(default=0)
    package_usd = models.FloatField(default=0)
    date = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    status = models.IntegerField()
    point = models.IntegerField()
    package = models.FloatField()
    nextsunday = models.DateField()
    # members = models.CharField(max_length=255)
    members = models.ForeignKey(ZqUser,to_field='memberid', on_delete=models.CASCADE,db_column='members' ,related_name='ncome2new_members')

    position = models.IntegerField()
    custid = models.IntegerField()
    custnewid = models.CharField(max_length=255)
    custname = models.CharField(max_length=255)
    paidstatus = models.IntegerField()
    last_paid_date = models.DateField()
    package_id = models.IntegerField()

    class Meta:
        db_table = 'level_income_bonus'
        managed=False 
        

        
class WalletAMICoinForUser(models.Model):
    email = models.EmailField()
    amicoin = models.FloatField()
    amicoinin_doller = models.FloatField()
    paystatus = models.CharField(max_length=100)
    remark = models.CharField(max_length=255)
    receivedate = models.DateTimeField()
    approve_date = models.DateTimeField()
    trxndate = models.DateTimeField()
    trxnid = models.CharField(max_length=255)
    status = models.IntegerField()
    withrawal_add = models.CharField(max_length=255)
    admin_charge=models.FloatField(default=0)
    requested_amount=models.FloatField(default=0)
    total_value=models.FloatField(default=0)
    currency=models.CharField(max_length=20,null=True)
    # memberid=models.CharField(max_length=15)
    memberid = models.ForeignKey(ZqUser,to_field='memberid', db_column='memberid',on_delete=models.CASCADE,related_name='walletAMICoinMember_zquser')

    total_value_zaan=models.FloatField(null=True)
    withdrawl_time_zaan_rate=models.FloatField(blank=True)
    withdrawal_bank_name=models.CharField(max_length=255,null=True,blank=True)
    transactionId = models.ForeignKey(TransactionHistoryOfCoin,to_field='id', db_column='transactionId',on_delete=models.CASCADE,related_name='walletami_tranhistory')

    # memberid=models.CharField(max_length=15)

    class Meta:
        # db_table = 'walletAMICoin_for_user'
        db_table = 'walletamicoin_for_user'
        managed=False 
        
    
    
class WalletTab(models.Model):
    id = models.AutoField(primary_key=True)
    col2 = models.CharField(max_length=255)
    col3 = models.CharField(max_length=255)
    col4 = models.CharField(max_length=255,null=True)
    col5 = models.CharField(max_length=255,null=True)
    col6 = models.TextField(max_length=255,null=True)
    col7 = models.CharField(max_length=255,null=True)
    amount = models.FloatField()
    usd_rate = models.FloatField(default=0)
    zql_rate = models.FloatField(default=0)
    usd_value_of_zaan = models.FloatField(default=0)
    # user_id = models.CharField(max_length=255)
    user_id = models.ForeignKey(ZqUser, on_delete=models.CASCADE, to_field='memberid', related_name='wallettab_member')
    txn_date = models.DateTimeField()
    txn_type = models.CharField(max_length=255)
    
    class Meta:
        managed = False
        db_table = 'wallet_wallettab'
    

    def __str__(self):
        return f"Transaction {self.id} for user {self.user_id}"

       
 
class Income1(models.Model):
    srno = models.AutoField(primary_key=True)
    introid = models.IntegerField()
    # intronewid = models.CharField(max_length=255)
    intronewid = models.ForeignKey(ZqUser,to_field='memberid', db_column='intronewid',on_delete=models.CASCADE,related_name='income1_intros')

    introname = models.CharField(max_length=255)
    rs = models.FloatField()
    package_usd = models.FloatField(default=0)
    rs_usd = models.FloatField(default=0)
    date = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    year = models.IntegerField(default=0)
    status = models.IntegerField(default=1)
    point = models.IntegerField(default=1)
    package = models.FloatField()
    nextsunday = models.DateField(auto_now_add=True)
    zaan_rate = models.FloatField(default=0)
    usd_rate = models.FloatField(default=0)
    # members = models.CharField(max_length=255)
    members = models.ForeignKey(ZqUser,to_field='memberid', on_delete=models.CASCADE,db_column='members' ,related_name='income1_members')
    packageId = models.ForeignKey(InvestmentWallet,to_field='id', on_delete=models.CASCADE,db_column='packageId' ,related_name='income1_packageid',null=True)
    # multiplier = models.IntegerField()
    position = models.IntegerField(default=1)
    custid = models.IntegerField()
    custnewid = models.CharField(max_length=255)
    custname = models.CharField(max_length=255)
    paidstatus = models.IntegerField(default=1)
    last_paid_date = models.DateField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'income1'
 
 

class  SocialJobs(models.Model):
    
    sociallink = models.TextField()
    whatfor = models.CharField(max_length=255,null=True)
    # whatfor = models.CharField(max_length=255)
    fb_link = models.CharField(max_length=255,null=True)
    insta_link = models.CharField(max_length=255,null=True)
    twitter_link = models.CharField(max_length=255,null=True)
    youtube_link = models.CharField(max_length=255,null=True)
    greview_link = models.CharField(max_length=255,null=True)
    uploaddate = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        managed = False
        db_table = 'sociallinks'
 
    

class AccountComfirmation(models.Model):
    # addressProof = models.CharField(max_length=100)
    # addressProof = models.FileField(upload_to='static/uploadedDocuments/',null=True)
    # idProof = models.FileField(upload_to='static/uploadedDocuments/',null=True)
    poi_name=models.CharField(max_length=50,null=True)
    poi_type=models.CharField(max_length=20,null=True)
    poi_number=models.CharField(max_length=50,null=True)
    poi_image=models.FileField(upload_to='static/uploadedDocuments/',null=True)
    poa_name=models.CharField(max_length=50,null=True)
    poa_number=models.CharField(max_length=50,null=True)
    poa_image=models.FileField(upload_to='static/uploadedDocuments/',null=True)
    pob_name=models.CharField(max_length=50,null=True)
    pob_bankId=models.IntegerField(null=True)
    pob_bankName=models.CharField(max_length=50,null=True)
    ifsc=models.CharField(max_length=50,null=True)
    pob_number=models.CharField(max_length=50,null=True)
    pob_image=models.FileField(upload_to='static/uploadedDocuments/',null=True)
    pob_ifsc=models.CharField(max_length=30,null=True)
    poi_upload_date=models.DateTimeField(auto_now_add=True)
    poa_upload_date=models.DateTimeField(auto_now_add=True)
    pob_upload_date=models.DateTimeField(auto_now_add=True)
    poi_status=models.IntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(3)])
    poa_status=models.IntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(3)])
    pob_status=models.IntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(3)])
    is_phone_verified=models.BooleanField(default=False)
    is_kyc_verfied=models.BooleanField(default=False)
    phone_number=models.CharField(max_length=20,null=True)

    # poi_name=models.CharField(max_length=100)
    # uploaded_file = models.FileField(upload_to='static/uploadedDocuments/',null=True)
    uploaded_by =models.ForeignKey(ZqUser,to_field='memberid', on_delete=models.CASCADE,db_column='uploaded_by' ,related_name='ac_confirm_members',null=True)
    # type= models.CharField(max_length=50,null=True)
    # id_name= models.CharField(max_length=50,null=True)
    # id_number= models.CharField(max_length=50,null=True)
    class Meta:
        managed=False
        db_table = 'account_confirmation'
        
    # bankProof = models.CharField(max_length=100)
    # IdProof = models.CharField(max_length=100)
    # uploaded_by= models.CharField(max_length=100)
    # roi_date = models.DateField()
    # roi_sbg = models.FloatField()
    # total_sbg = models.FloatField()
    # roi_days = models.IntegerField()
    # remark = models.CharField(max_length=255)

    # def __str__(self):
        
    #     return f"ROI for {self.userid} on {self.roi_date}"
    
class UploadedImages(models.Model):
    id = models.IntegerField(primary_key=True)
    kyc_id = models.ForeignKey(AccountComfirmation,  to_field='id',on_delete=models.RESTRICT, db_column='kyc_id', related_name='kyc_id')
    uploaded_by = models.ForeignKey(ZqUser, to_field='memberid',on_delete=models.RESTRICT, db_column='uploaded_by', related_name='uploaded_by_user_images')
    uploaded_image=models.FileField(upload_to='static/uploadedDocuments/',null=True)
    doc_type=models.CharField(max_length=255)
    doc_number=models.CharField(max_length=255)
    upload_date=models.DateTimeField(null=True)


    class Meta:
        managed=False 
        db_table = 'uploaded_images'
        ordering = ['id'] 


class AssignedSocialJob(models.Model):
    assigned_to =models.ForeignKey(ZqUser, to_field='memberid',on_delete=models.RESTRICT, db_column='assigned_to', related_name='assigned_to_zquser')
    social_job_id = models.ForeignKey(SocialJobs,to_field='id' ,db_column='social_job_id',on_delete=models.RESTRICT, related_name='social_job_id_socialjobs')
    package_id = models.ForeignKey(InvestmentWallet,to_field='id' ,db_column='package_id',on_delete=models.RESTRICT, null=True, related_name='package_id_investamentwallet')
    valid_from = models.DateTimeField()
    valid_upto = models.DateTimeField()
    status = models.BooleanField(default=False)
    check_token = models.BooleanField(default=False)
    completion_date=models.DateTimeField(null=True)

    class Meta:
        managed=False
        db_table = 'assigned_social_jobs'

class ClubsBonus(models.Model):
    club_name= models.CharField(max_length=255)
    bonus=models.FloatField()
    club_newname=models.CharField(max_length=255)
    class Meta:
        managed=False
        db_table = 'clubs_bonus'
 
 

# ===================
class ClubMembers(models.Model):
    memberid =models.ForeignKey(ZqUser, to_field='memberid',on_delete=models.RESTRICT, db_column='memberid', related_name='club_members_memberid_zquser')
    # club = models.CharField(max_length=255)
    club =models.ForeignKey(ClubsBonus, to_field='id',on_delete=models.RESTRICT, db_column='club', related_name='clubmem_club_bonus')
    
    club_added_date = models.DateTimeField(auto_now_add=True)
    dummy_name=models.CharField(max_length=255,null=True)


    class Meta:
        managed=False
        db_table = 'club_member_details'


       
class ClubMembersIncome(models.Model):
    total_activation_amount = models.IntegerField()
    bonus_income = models.FloatField()
    bonus_percent = models.FloatField()
    memberid =models.ForeignKey(ZqUser, to_field='memberid',on_delete=models.RESTRICT, db_column='memberid', related_name='clubIncomeMember_zquser')
    club_id =models.ForeignKey(ClubsBonus, to_field='id',on_delete=models.RESTRICT, db_column='club_id', related_name='clubinc_club_bonus')
    club_members_count=models.IntegerField()
    # referral_requirement = models.CharField(max_length=255)
    # activation_date = models.DateTimeField()
    activation_date = models.DateField()
    
    class Meta:
        managed=False
        db_table = 'club_member_income'
    


class SubmittedDataForSocialMedia(models.Model):
    
    
    
    # id = models.IntegerField(primary_key=True)
    # whatfor = models.ForeignKey(AccountComfirmation,  to_field='id',on_delete=models.RESTRICT, db_column='kyc_id', related_name='kyc_id')
    whatfor=models.CharField(max_length=255)
    # uploaded_by = models.ForeignKey(ZqUser, to_field='memberid',on_delete=models.RESTRICT, db_column='uploaded_by', related_name='uploaded_by_user_images')
    # greview_image=models.FileField(upload_to='taskImages/',null=True)
    # facebook_image=models.FileField(upload_to='taskImages/',null=True)
    twitter_image=models.FileField(upload_to='taskImages/',null=True)
    insta_image=models.FileField(upload_to='taskImages/',null=True)
    youtube_image=models.FileField(upload_to='taskImages/',null=True)
    uploadedby = models.ForeignKey(ZqUser, to_field='memberid',on_delete=models.RESTRICT, db_column='uploadedby', related_name='uploadedbysocialimages_user_images')
    # social_job_id=models.ForeignKey(SocialJobs, to_field='id',on_delete=models.RESTRICT, db_column='social_job_id', related_name='socialjobid_sociallinks')
    # package_id=models.ForeignKey(InvestmentWallet, to_field='id',on_delete=models.RESTRICT, db_column='package_id', related_name='socialid_investmentwallet',null=True)
    # assigned_task_id=models.ForeignKey(AssignedSocialJob, to_field='id',on_delete=models.RESTRICT, db_column='assigned_task_id', related_name='assigned_task_id_assignedTask',null=True)
    # doc_number=models.CharField(max_length=255)
    uploaddate=models.DateTimeField(null=True,auto_now_add=True)
    status=models.BooleanField(default=False)

    class Meta:
        managed=False 
        db_table = 'submittedimagesforsocialmedia'
        ordering = ['id'] 




class prepaidSocialMediaBonus(models.Model):
    assigned_task_id =models.ForeignKey(AssignedSocialJob, to_field='id',on_delete=models.RESTRICT, db_column='assigned_task_id', related_name='assigned_task_id_assignedtask')
    memberid = models.ForeignKey(ZqUser,to_field='memberid' ,db_column='memberid',on_delete=models.RESTRICT, related_name='prepaid_memberid')
    bonus = models.FloatField()
    given_date = models.DateTimeField()
    # valid_upto = models.DateTimeField()
    # status = models.BooleanField(default=False)

    class Meta:
        managed=False
        db_table = 'prepaid_social_media_bonus'



class UserActivatedMachineDetails(models.Model):
    id = models.AutoField(primary_key=True)
    # memberid = models.CharField(max_length=20, unique=True)
    activated_by = models.ForeignKey(ZqUser,to_field='memberid', on_delete=models.CASCADE,db_column='activated_by' ,related_name='machine_activated_by_user',null=True)

    hasActivatedAntiminerS21 = models.BooleanField(default=False)
    hasActivatedAntiminerRPRO = models.BooleanField(default=False)
    hasActivatedAntiminerT9 = models.BooleanField(default=False)
    S21_activation_date = models.DateTimeField(null=True, blank=True)
    hasActivatedT9PROHYD = models.BooleanField(default=False)
    hasActivatedS9jPRO = models.BooleanField(default=False)
    hasActivatedS9jPROA = models.BooleanField(default=False)
    S9jPRO_activation_date = models.DateTimeField(null=True, blank=True)
    RPRO_activation_date = models.DateTimeField(null=True, blank=True)
    T9_activation_date = models.DateTimeField(null=True, blank=True)
    T9PROHYD_activation_date = models.DateTimeField(null=True, blank=True)
    S9jPROA_activation_date = models.DateTimeField(null=True, blank=True)
   

    def __str__(self):
        return self.memberid

    class Meta:
        managed=False
        db_table = 'user_activated_machine_details'


class TradingTransaction(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.FloatField(default=None, null=True)
    usd_rate_at_time = models.FloatField()
    type = models.CharField(max_length=50)
    amount_in_inr = models.FloatField()
    trans_rate_usd = models.FloatField()
    #  = models.ForeignKey(ZqUser, on_delete=models.RESTRICT)
    traded_by = models.ForeignKey(ZqUser,to_field='memberid', on_delete=models.CASCADE,db_column='traded_by' ,related_name='traded_by_user')
    tran_date = models.DateTimeField(null=True, blank=True)


    class Meta:
        db_table = 'trading_transactions'
        indexes = [
            models.Index(fields=['traded_by'])
        ]
        
        managed=False 


class AvailableMiningMachine(models.Model):
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    activation_cost = models.FloatField()
    machine_code = models.CharField(max_length=50)

    class Meta:
        managed=False
        db_table = 'availabe_mining_machines'

    # def __str__(self):
    #     return self.name


class BankList(models.Model):
    id = models.IntegerField(primary_key=True)
    bank_id = models.IntegerField()
    bank_name = models.CharField(max_length=255)
    bank_code = models.CharField(max_length=255)
    master_ifsc = models.CharField(max_length=255)

    class Meta:
        db_table = 'bank_list'
        managed=False


class Withdrawal_Type(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    # Brand_name = models.ForeignKey(ZqUser,to_field='memberid', on_delete=models.CASCADE,db_column='Brand_name' ,related_name='brand_name_member')
    Brand_name = models.OneToOneField(ZqUser,to_field='memberid', on_delete=models.CASCADE,db_column='Brand_name' ,related_name='brand_name_member')
    withdrawal_mode = models.CharField(max_length=100)

    class Meta:
        db_table = 'Withdrawal_Type'
        managed=False

class UserBankDetails(models.Model):
    # id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255)
    uploaded_by= models.ForeignKey(ZqUser,to_field='memberid', on_delete=models.CASCADE,db_column='uploaded_by' ,related_name='uploaded_by_user')
    ifsc = models.CharField(max_length=255)
    accNo = models.CharField(max_length=255)

    class Meta:
        db_table = 'UserBankDetails'
        managed=False
        

class RimberioWallet(models.Model):
    # id = models.AutoField(primary_key=True)
    # amount = models.CharField(max_length=255)
    # col3 = models.CharField(max_length=255)
    # col4 = models.CharField(max_length=255,null=True)
    # col5 = models.CharField(max_length=255,null=True)
    remark = models.TextField(null=True)
    # col7 = models.CharField(max_length=255,null=True)
    amount = models.FloatField()
    # usd_rate = models.FloatField(default=0)
    # zql_rate = models.FloatField(default=0)
    # usd_value_of_zaan = models.FloatField(default=0)
    trans_for = models.CharField(max_length=255)
    # tran_by = models.CharField(max_length=255)
    # trans_from = models.CharField(max_length=255)
    # trans_to =  models.CharField(max_length=255)
    
    tran_by = models.ForeignKey(ZqUser, on_delete=models.CASCADE, db_column='tran_by', to_field='memberid', related_name='RimberioWallet_tranby_member')
    trans_from = models.ForeignKey(ZqUser, on_delete=models.CASCADE, db_column='trans_from' ,to_field='memberid', related_name='RimberioWallet_tranfrom_member')
    trans_to = models.ForeignKey(ZqUser, on_delete=models.CASCADE, db_column='trans_to' ,to_field='memberid', related_name='RimberioWallet_tranto_member')
    
    trans_date = models.DateTimeField()
    status = models.BooleanField(default=False)
    trans_type = models.CharField(max_length=255)
    package_id = models.ForeignKey(InvestmentWallet, on_delete=models.CASCADE, db_column='package_id' ,to_field='id', related_name='rimbwallet_packageid',null=True)
    social_job_id = models.ForeignKey(AssignedSocialJob, on_delete=models.CASCADE, db_column='social_job_id' ,to_field='id', related_name='rimbwallet_socialjobid',null=True)
    # social_job_id = models.CharField(max_length=255,null=True)
    address = models.CharField(max_length=255,null=True)

    
    class Meta:
        managed = False
        db_table = 'rimberio_wallet_history'
    
class CoinReward(models.Model):
    

    coin_reward = models.FloatField()

    what_for = models.CharField(max_length=255)


    
    class Meta:
        managed = False
        db_table = 'coin_rewards'
    



class RimberioCoinDistribution(models.Model):
    
    coin_reward = models.IntegerField()
    task = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'rimberio_coin_distribution'
        managed=False
        
        
class CommunityBuildingBonus(models.Model):
    
    stage = models.IntegerField()
    stage_name = models.CharField(max_length=255)
    stage_bonus = models.FloatField()
    referral_requirement = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'community_building_bonus'
        managed=False


class AdminWithdrawalCharge(models.Model):
    chargeInPercent=models.FloatField()
    
    
    class Meta:
        db_table = 'admin_withdrawal_charge'
        managed=False  


class BuyAndSellTrade(models.Model):
    id = models.IntegerField(primary_key=True)
    memberid= models.ForeignKey(ZqUser,to_field='memberid', on_delete=models.CASCADE,db_column='memberid' ,related_name='trade_coin_user')

    # memberid = models.CharField(max_length=10)
    quantity = models.FloatField()
    type = models.CharField(max_length=20)
    rate = models.FloatField()
    status = models.BooleanField()
    trade_date = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'buy_and_sell_trades'
        managed=False
        

class Reward(models.Model):
    name = models.CharField(max_length=255)
    worth_zaan = models.FloatField()
    expire_date = models.DateTimeField(null=True)
    member = models.ForeignKey(ZqUser,to_field='memberid',db_column='member' ,on_delete=models.CASCADE, related_name='rewards_member_zquser')
    is_scratched=models.BooleanField(default=False)
    class Meta:
        db_table = 'rewards'
        managed=False


class AllQuestions(models.Model):
    question = models.CharField(max_length=200, unique=True)
    choice1 = models.CharField(max_length=200)
    choice2 = models.CharField(max_length=200)
    choice3 = models.CharField(max_length=200)
    choice4 = models.CharField(max_length=200)
    correct_option = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question
    class Meta:
        db_table = 'AllQuestions'
        managed=False      


class Question(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text
    
    class Meta:
        # db_table = 'SubmittedData'
        managed=False

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    
    class Meta:
        # db_table = 'SubmittedData'
        managed=False



 
class ROIDailyCustomer(models.Model):
    id = models.IntegerField(primary_key=True)
    # userid = models.CharField(max_length=50, null=True)
    userid = models.ForeignKey(ZqUser,to_field='memberid', db_column='userid',on_delete=models.CASCADE,related_name='roiDailyMember_zquser')

    remark = models.CharField(max_length=100, null=True)
    total_sbg = models.FloatField(null=True)
    zaan_rate = models.FloatField(default=0)
    usd_rate = models.FloatField(default=0)
    zaan_value_in_usd = models.FloatField(default=0)
    roi_sbg_usd = models.FloatField(default=0)
    roi_days = models.IntegerField(null=True)
    roi_date = models.DateTimeField(null=True)
    status = models.IntegerField(null=True)
    roi_sbg = models.FloatField(null=True)
    daily_amount = models.FloatField(default=0)
    investment_id = models.ForeignKey(InvestmentWallet,to_field='id', db_column='investment_id',on_delete=models.CASCADE,related_name='investment_id_invs')
    assigned_job_id = models.ForeignKey(AssignedSocialJob,to_field='id', db_column='assigned_job_id',on_delete=models.CASCADE,related_name='roidaily_assignedjobs')


    
    class Meta:
        db_table = 'roi_daily_customer'
        managed=False 

class CommunityBuildingIncome(models.Model):
    
    bonus_received_from =  models.ForeignKey(ZqUser,to_field='memberid', on_delete=models.CASCADE,db_column='bonus_received_from' ,related_name='communitybuilding_member')
    receiver_memberid =  models.ForeignKey(ZqUser,to_field='memberid', on_delete=models.CASCADE,db_column='receiver_memberid' ,related_name='communitybuilding_receiver')
    # intronewid = models.CharField(max_length=255)
    # intronewid = models.ForeignKey(ZqUser,to_field='memberid', db_column='intronewid',on_delete=models.CASCADE,related_name='communitybuildingincome_intros')

    # introname = models.CharField(max_length=255)
    received_bonus = models.FloatField()
    calculated_on = models.FloatField()
    calculated_on_referrals = models.IntegerField()
    social_job_id =models.ForeignKey(AssignedSocialJob, to_field='id',on_delete=models.RESTRICT, db_column='social_job_id', related_name='socialjobid_communitybuildingbonus')

    job_submission_date = models.DateTimeField(auto_now_add=True)
    bonus_received_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'communitybuildingbonus'
    
class MagicalIncome(models.Model):
    srno = models.AutoField(primary_key=True)
    introid = models.IntegerField()
    # intronewid = models.CharField(max_length=255)
    intronewid = models.ForeignKey(ZqUser,to_field='memberid', db_column='intronewid',on_delete=models.CASCADE,related_name='magicalIncome_intros',null=True)

    introname = models.CharField(max_length=255)
    rs = models.FloatField()
    package_usd = models.FloatField(default=0)
    rs_usd = models.FloatField(default=0)
    date = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    status = models.IntegerField()
    point = models.IntegerField()
    package = models.FloatField()
    nextsunday = models.DateField()
    zaan_rate = models.FloatField(default=0)
    usd_rate = models.FloatField(default=0)
    # members = models.CharField(max_length=255)
    members = models.ForeignKey(ZqUser,to_field='memberid', on_delete=models.CASCADE,db_column='members' ,related_name='magicalIncome_members',null=True)

    position = models.IntegerField()
    custid = models.IntegerField()
    custnewid = models.CharField(max_length=255)
    custname = models.CharField(max_length=255)
    paidstatus = models.IntegerField()
    last_paid_date = models.DateField()
    social_job_id =models.ForeignKey(AssignedSocialJob, to_field='id',on_delete=models.SET_NULL, db_column='social_job_id', related_name='socialjobid_magicbonus',null=True)

    class Meta:
        managed = False
        db_table = 'magicincome'
    


class DepositWallet(models.Model):
    address=models.CharField(max_length=255)

    class Meta:
        db_table = 'deposit_address'
        managed=False   

class SubmittedData(models.Model):
    submitted_by = models.CharField(max_length=255)
    question_inp = models.CharField(max_length=255)
    selected_choice = models.CharField(max_length=255, default=0)

    class Meta:
        db_table = 'SubmittedData'
        managed=False   
        
class DirectReferalRewards(models.Model):
    
    ref_requirement = models.IntegerField()
    referral_coins = models.IntegerField()
    ref_reward= models.IntegerField()
    # ref_image
    ref_image = models.CharField(max_length=255, default=0)

    class Meta:
        db_table = 'direct_referral_rewards'
        managed=False   
        
class RedeemedRitcoins(models.Model):
    
    # redeemed_by = models.CharField(max_length=255, default=0)
    # image = models.IntegerField()
    redeemed_by = models.ForeignKey(ZqUser, to_field='memberid',on_delete=models.RESTRICT, db_column='redeemed_by', related_name='redeemed_by_user_images')
    image=models.FileField(upload_to='media/uploadedImages/')
    amount= models.FloatField()
    given_discount= models.FloatField(null=True)
    ritcoin_worth= models.FloatField(null=True)
    status= models.BooleanField(default=0)
    upload_date= models.DateTimeField(auto_now_add=True)
    # ref_image
    approve_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'redeemed_ritcoins'
        managed=False   