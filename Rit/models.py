# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('ZqusersZquser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Userinformation(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    opid = models.TextField(blank=True, null=True)
    memberid = models.TextField(blank=True, null=True)
    spillid = models.TextField(blank=True, null=True)
    introducerid = models.TextField(blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    username = models.TextField(blank=True, null=True)
    father_spouse_name = models.TextField(db_column='Father_Spouse_name', blank=True, null=True)  # Field name made lowercase.
    dob = models.DateField()
    country = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    pincode = models.IntegerField()
    mobile = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    joindate = models.DateTimeField()
    nominee = models.TextField(blank=True, null=True)
    age = models.FloatField(db_column='Age')  # Field name made lowercase.
    relation = models.TextField(blank=True, null=True)
    status = models.IntegerField()
    bankname = models.TextField(db_column='BankName', blank=True, null=True)  # Field name made lowercase.
    branchname = models.TextField(db_column='BranchName', blank=True, null=True)  # Field name made lowercase.
    accountholder = models.TextField(db_column='AccountHolder', blank=True, null=True)  # Field name made lowercase.
    accountno = models.IntegerField(db_column='AccountNo')  # Field name made lowercase.
    accounttype = models.TextField(db_column='AccountType', blank=True, null=True)  # Field name made lowercase.
    ifsc = models.TextField(db_column='IFSC', blank=True, null=True)  # Field name made lowercase.
    pan = models.TextField(db_column='PAN', blank=True, null=True)  # Field name made lowercase.
    rank = models.IntegerField()
    bankaccountno = models.TextField(db_column='BankAccountNo', blank=True, null=True)  # Field name made lowercase.
    pinused = models.TextField(blank=True, null=True)
    position = models.IntegerField()
    dsiid = models.TextField(db_column='DSIid', blank=True, null=True)  # Field name made lowercase.
    uid = models.IntegerField()
    activationdate = models.DateTimeField()
    aadhaar = models.TextField(blank=True, null=True)
    bank_img = models.TextField(blank=True, null=True)
    pan_img = models.TextField(blank=True, null=True)
    aadhaar_img = models.TextField(blank=True, null=True)
    kyc_status = models.IntegerField()
    registrationtype = models.TextField(db_column='RegistrationType', blank=True, null=True)  # Field name made lowercase.
    topnewid = models.TextField(db_column='Topnewid', blank=True, null=True)  # Field name made lowercase.
    profile_pic = models.TextField(db_column='Profile_pic', blank=True, null=True)  # Field name made lowercase.
    pin_amount = models.FloatField(db_column='Pin_Amount')  # Field name made lowercase.
    poolnumber = models.IntegerField()
    uid1 = models.IntegerField()
    position1 = models.IntegerField()
    spillid1 = models.TextField(blank=True, null=True)
    isleader = models.IntegerField(db_column='isLeader')  # Field name made lowercase.
    coin_address = models.TextField(blank=True, null=True)
    tron_address = models.TextField(blank=True, null=True)
    ethereum_address = models.TextField(blank=True, null=True)
    withdrawal_coin_address = models.TextField(blank=True, null=True)
    withdrawal_tron_address = models.TextField(blank=True, null=True)
    withdrawal_ethereum_address = models.TextField(blank=True, null=True)
    intro_email = models.TextField(blank=True, null=True)
    activation_time_btc_rate = models.FloatField()
    activation_time_trx_rate = models.FloatField()
    activation_time_eth_rate = models.FloatField()
    activation_by = models.TextField(blank=True, null=True)
    activation_time_no_of_btc = models.FloatField()
    activation_time_no_of_trx = models.FloatField()
    activation_time_no_of_eth = models.FloatField()

    class Meta:
        managed = False
        db_table = 'userinformation'


class ZqusersZquser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(unique=True, max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    is_email_verified = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zqusers_zquser'


class ZqusersZquserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    zquser = models.ForeignKey(ZqusersZquser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'zqusers_zquser_groups'
        unique_together = (('zquser', 'group'),)


class ZqusersZquserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    zquser = models.ForeignKey(ZqusersZquser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'zqusers_zquser_user_permissions'
        unique_together = (('zquser', 'permission'),)
