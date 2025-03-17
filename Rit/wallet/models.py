
from zqUsers.models import ZqUser
# from wallet.models import CustomCoinRate
# Create your models here.
from django.db import models

# ZQLRate=CustomCoinRate.objects.order_by('-id').first().amount



# class TransactionHistoryOfCoin(models.Model):
#     cointype = models.CharField(max_length=100)
#     memberid = models.ForeignKey(ZqUser, on_delete=models.CASCADE, to_field='memberid', related_name='transaction_history')

#     # memberid = models.ForeignKey(ZqUser, on_delete=models.CASCADE,db_column='memberid', related_name='user_trans_memid')

#     # memberid = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     hashtrxn = models.CharField(max_length=255)
#     amount = models.FloatField()
#     coinvalue = models.FloatField()
#     trxndate = models.DateTimeField()
#     status = models.CharField(max_length=100)
#     coinvaluedate = models.DateTimeField()
#     total = models.FloatField()
#     amicoinvalue = models.FloatField()
#     amifreezcoin = models.FloatField()
#     amivolume = models.FloatField()
#     totalinvest = models.FloatField()
#     tran_type = models.CharField(max_length=100,null=True)
#     transactionId = models.ForeignKey(WalletAMICoinForUser,to_field='id', db_column='transactionId',on_delete=models.CASCADE,related_name='walletami_tranhistory')

    # transactionId=models.ForeignKey(WalletAMICoinForUser, on_delete=models, to_field='memberid', related_name='transaction_history')

    # def __str__(self):
    #     return f"{self.memberid} - {self.cointype}"
    
    # def save(self, *args, **kwargs):
    #     # Check if ZqUser instance is provided, if not, fetch ZqUser using memberid
    #     if not isinstance(self.memberid, ZqUser):
    #         try:
    #             self.memberid = ZqUser.objects.get(memberid=self.memberid)
    #         except ZqUser.DoesNotExist:
    #             raise ValueError("ZqUser with memberid '{}' does not exist".format(self.user))
        
    #     super().save(*args, **kwargs)

class CustomCoinRate(models.Model):
    status = models.IntegerField()
    no_of_coin = models.IntegerField()
    coin_name = models.CharField(max_length=100)
    create_by = models.CharField(max_length=255)
    amount = models.FloatField()
    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.coin_name
    
    
    class Meta:
        # db_table = 'UserBankDetails'
        managed=False

# class OTP(models.Model):
#     id = models.AutoField(primary_key=True)
#     memberid = models.ForeignKey(ZqUser, on_delete=models.CASCADE, to_field='memberid', related_name='otp_member')

#     # memberid = models.CharField(max_length=255)
#     otp = models.CharField(max_length=255)
#     otp_time = models.DateTimeField()
#     status = models.IntegerField()
#     retry = models.IntegerField()
#     type = models.CharField(max_length=255)
#     remark = models.CharField(max_length=255)

#     def __str__(self):
#         return f"OTP {self.id} for member {self.memberid}"
    
    
#     class Meta:
#         # db_table = 'UserBankDetails'
#         managed=False
    
# class WalletTab(models.Model):
#     id = models.AutoField(primary_key=True)
#     col2 = models.CharField(max_length=255)
#     col3 = models.CharField(max_length=255)
#     col4 = models.CharField(max_length=255,null=True)
#     col5 = models.CharField(max_length=255,null=True)
#     col6 = models.TextField(max_length=255,null=True)
#     col7 = models.CharField(max_length=255,null=True)
#     amount = models.FloatField()
#     # user_id = models.CharField(max_length=255)
#     user_id = models.ForeignKey(ZqUser, on_delete=models.CASCADE, to_field='memberid', related_name='wallettab_member')
#     txn_date = models.DateTimeField()
#     txn_type = models.CharField(max_length=255)

#     def __str__(self):
#         return f"Transaction {self.id} for user {self.user_id}"


class Income2Master(models.Model):
    id = models.AutoField(primary_key=True)
    level = models.IntegerField()
    income = models.FloatField()
    levelname = models.CharField(max_length=255)

    class Meta:
        db_table = 'Income2Master'
        managed=False
               
        
# class Income2(models.Model):
#     srno = models.AutoField(primary_key=True)
#     introid = models.IntegerField()
#     intronewid = models.CharField(max_length=255)
#     introname = models.CharField(max_length=255)
#     rs = models.FloatField()
#     date = models.IntegerField()
#     month = models.IntegerField()
#     year = models.IntegerField()
#     status = models.IntegerField()
#     point = models.IntegerField()
#     package = models.FloatField()
#     nextsunday = models.DateField()
#     members = models.CharField(max_length=255)
#     position = models.IntegerField()
#     custid = models.IntegerField()
#     custnewid = models.CharField(max_length=255)
#     custname = models.CharField(max_length=255)
#     paidstatus = models.IntegerField()
#     last_paid_date = models.DateField()

#     class Meta:
#         db_table = 'Income2'
        
        
# class Income1(models.Model):
#     srno = models.AutoField(primary_key=True)
#     introid = models.IntegerField()
#     intronewid = models.CharField(max_length=255)
#     # intronewid = models.ForeignKey(ZqUser,to_field='memberid', db_column='intronewid',on_delete=models.CASCADE,related_name='income1_intros')

#     introname = models.CharField(max_length=255)
#     rs = models.FloatField()
#     date = models.IntegerField()
#     month = models.IntegerField()
#     year = models.IntegerField()
#     status = models.IntegerField()
#     point = models.IntegerField()
#     package = models.FloatField()
#     nextsunday = models.DateField()
#     members = models.CharField(max_length=255)
#     # members = models.ForeignKey(ZqUser,to_field='memberid', on_delete=models.CASCADE,db_column='members' ,related_name='income1_members')

#     position = models.IntegerField()
#     custid = models.IntegerField()
#     custnewid = models.CharField(max_length=255)
#     custname = models.CharField(max_length=255)
#     paidstatus = models.IntegerField()
#     last_paid_date = models.DateField()

#     class Meta:
#         managed = False
#         db_table = 'Income1'
        
           
class SqlCommand:
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def ExecuteScalar(self):
        # Implement execution logic
        pass

    def Close(self):
        # Implement close logic
        pass
    

class SendOTP(models.Model):
    Srno = models.AutoField(primary_key=True)
    email = models.EmailField()
    otp = models.IntegerField()
    trxndate = models.DateTimeField()
    status = models.IntegerField()

    class Meta:
        db_table = 'send_otp'
        managed=False
        
        
        
# class WalletAMICoinForUser(models.Model):
#     email = models.EmailField()
#     amicoin = models.FloatField()
#     amicoinin_doller = models.FloatField()
#     paystatus = models.CharField(max_length=100)
#     remark = models.CharField(max_length=255)
#     receivedate = models.DateTimeField()
#     approve_date = models.DateTimeField()
#     trxndate = models.DateTimeField()
#     trxnid = models.CharField(max_length=255)
#     status = models.IntegerField()
#     withrawal_add = models.CharField(max_length=255)
#     admin_charge=models.FloatField(default=0)
#     requested_amount=models.FloatField(default=0)
#     total_value=models.FloatField(default=0)
#     # memberid=models.CharField(max_length=15)
#     memberid = models.ForeignKey(ZqUser,to_field='memberid', db_column='memberid',on_delete=models.CASCADE,related_name='walletAMICoinMember_zquser')

#     total_value_zaan=models.FloatField(null=True)
#     withdrawl_time_zaan_rate=models.FloatField(blank=True)
#     # memberid=models.CharField(max_length=15)

#     class Meta:
#         db_table = 'walletAMICoin_for_user'
        
    
class InterestRate(models.Model):
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)
    set_by=models.ForeignKey(ZqUser, on_delete=models.SET_NULL, to_field='memberid', related_name='InterestRate_memberid',null=True)


    def __str__(self):
        return f"Interest Rate: {self.rate}% ({self.start_date} - {self.end_date})"
    
    
    class Meta:
        # db_table = 'UserBankDetails'
        managed=False
    

# class InvestmentWallet(models.Model):
#     id = models.AutoField(primary_key=True)
#     txn_by = models.ForeignKey(ZqUser, on_delete=models.CASCADE, to_field='memberid', related_name='investmentwallet_member')
#     amount = models.FloatField()
#     remark=models.TextField(blank=True,null=True)
#     # col2 = models.CharField(max_length=255)
#     # col3 = models.CharField(max_length=255)
#     # col4 = models.CharField(max_length=255,null=True)
#     # col5 = models.CharField(max_length=255,null=True)
#     # col6 = models.TextField(max_length=255,null=True)
#     # col7 = models.CharField(max_length=255,null=True)
    
#     # user_id = models.CharField(max_length=255)
#     txn_date = models.DateTimeField()
#     txn_type = models.CharField(max_length=255)

#     def __str__(self):
#         return f"Transaction {self.id} for user {self.user_id}"


# class ROIDailyCustomer(models.Model):
#     id = models.IntegerField(primary_key=True)
#     # userid = models.CharField(max_length=50, null=True)
#     userid = models.ForeignKey(ZqUser,to_field='memberid', db_column='userid',on_delete=models.CASCADE,related_name='roiDailyMember_zquser')

#     remark = models.CharField(max_length=100, null=True)
#     total_sbg = models.FloatField(null=True)
#     roi_days = models.IntegerField(null=True)
#     roi_date = models.DateField(null=True)
#     status = models.IntegerField(null=True)
#     roi_sbg = models.FloatField(null=True)
#     daily_amount = models.FloatField(default=0)
#     investment_id = models.IntegerField(null=True)
    
#     class Meta:
#         db_table = 'roi_daily_customer'


class INRTransactionDetails(models.Model):
    customer_name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    txnAt = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    upi_txn_id =  models.CharField(max_length=100)
    client_txn_id = models.CharField(max_length=15)
    zaan_coin_value =  models.DecimalField(max_digits=10, decimal_places=2)
    conversion_usd_value =  models.DecimalField(max_digits=10, decimal_places=2)
    # user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # member_id = models.ForeignKey(ZqUser, on_delete=models.CASCADE, to_field='memberid', related_name='inrTransDetails_member')
    # memberId =  models.CharField(max_length=50)
    memberId = models.ForeignKey(ZqUser,to_field='memberid', db_column='memberId',on_delete=models.CASCADE,related_name='intrtranMember_zquser')

    # members = models.ForeignKey(ZqUser, on_delete=models.CASCADE, related_name='intrtranMember_zquser')

    
    class Meta:
        db_table = 'inr_transaction_details'
        managed=False


class BonusReward(models.Model):
    id = models.IntegerField(primary_key=True)
    bonus = models.FloatField(null=True, default=None)
    date_field = models.DateField(null=True, default=None)
    amount = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bonus_reward'