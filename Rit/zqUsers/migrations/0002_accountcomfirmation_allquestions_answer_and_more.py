# Generated by Django 5.0.6 on 2024-06-06 12:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zqUsers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountComfirmation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poi_name', models.CharField(max_length=50, null=True)),
                ('poi_type', models.CharField(max_length=20, null=True)),
                ('poi_number', models.CharField(max_length=50, null=True)),
                ('poi_image', models.FileField(null=True, upload_to='static/uploadedDocuments/')),
                ('poa_name', models.CharField(max_length=50, null=True)),
                ('poa_number', models.CharField(max_length=50, null=True)),
                ('poa_image', models.FileField(null=True, upload_to='static/uploadedDocuments/')),
                ('pob_name', models.CharField(max_length=50, null=True)),
                ('pob_bankId', models.IntegerField(null=True)),
                ('pob_bankName', models.CharField(max_length=50, null=True)),
                ('ifsc', models.CharField(max_length=50, null=True)),
                ('pob_number', models.CharField(max_length=50, null=True)),
                ('pob_image', models.FileField(null=True, upload_to='static/uploadedDocuments/')),
                ('pob_ifsc', models.CharField(max_length=30, null=True)),
                ('poi_upload_date', models.DateTimeField(auto_now_add=True)),
                ('poa_upload_date', models.DateTimeField(auto_now_add=True)),
                ('pob_upload_date', models.DateTimeField(auto_now_add=True)),
                ('poi_status', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(3)])),
                ('poa_status', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(3)])),
                ('pob_status', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(3)])),
                ('is_phone_verified', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'account_confirmation',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AllQuestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200, unique=True)),
                ('choice1', models.CharField(max_length=200)),
                ('choice2', models.CharField(max_length=200)),
                ('choice3', models.CharField(max_length=200)),
                ('choice4', models.CharField(max_length=200)),
                ('correct_option', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'AllQuestions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('is_correct', models.BooleanField(default=False)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AssignedSocialJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateTimeField()),
                ('valid_upto', models.DateTimeField()),
                ('status', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'assigned_social_jobs',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AvailableMiningMachine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('activation_cost', models.FloatField()),
                ('machine_code', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'availabe_mining_machines',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BankList',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('bank_id', models.IntegerField()),
                ('bank_name', models.CharField(max_length=255)),
                ('bank_code', models.CharField(max_length=255)),
                ('master_ifsc', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'Bank_List',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BuyAndSellTrade',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('quantity', models.FloatField()),
                ('type', models.CharField(max_length=20)),
                ('rate', models.FloatField()),
                ('status', models.BooleanField()),
                ('trade_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'buy_and_sell_trades',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ClubMembers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('club', models.CharField(max_length=255)),
                ('club_added_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'club_member_details',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ClubMembersIncome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_activation_amount', models.IntegerField()),
                ('bonus_income', models.FloatField()),
                ('bonus_percent', models.FloatField()),
                ('activation_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'club_member_income',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ClubsBonus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('club_name', models.CharField(max_length=255)),
                ('bonus', models.FloatField()),
            ],
            options={
                'db_table': 'clubs_bonus',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CommunityBuildingBonus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage', models.IntegerField()),
                ('stage_name', models.CharField(max_length=255)),
                ('stage_bonus', models.FloatField()),
                ('referral_requirement', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'community_building_bonus',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CommunityBuildingIncome',
            fields=[
                ('srno', models.AutoField(primary_key=True, serialize=False)),
                ('introid', models.IntegerField()),
                ('introname', models.CharField(max_length=255)),
                ('rs', models.FloatField()),
                ('package_usd', models.FloatField(default=0)),
                ('rs_usd', models.FloatField(default=0)),
                ('date', models.IntegerField(default=1)),
                ('month', models.IntegerField(default=5)),
                ('year', models.IntegerField(default=2024)),
                ('status', models.IntegerField()),
                ('point', models.IntegerField()),
                ('package', models.FloatField()),
                ('nextsunday', models.DateField()),
                ('zaan_rate', models.FloatField(default=0)),
                ('usd_rate', models.FloatField(default=0)),
                ('position', models.IntegerField(default=1)),
                ('custid', models.IntegerField()),
                ('custnewid', models.CharField(max_length=255)),
                ('custname', models.CharField(max_length=255)),
                ('paidstatus', models.IntegerField()),
                ('last_paid_date', models.DateField()),
            ],
            options={
                'db_table': 'communitybuildingbonus',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DownlineLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('membername', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=False)),
                ('pinamount', models.CharField(max_length=100, null=True)),
                ('joindate', models.DateTimeField()),
                ('levelno', models.IntegerField(default=1)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('investment_amount', models.FloatField()),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('current_return', models.FloatField(default=0)),
            ],
            options={
                'db_table': 'daily_roi',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MagicalIncome',
            fields=[
                ('srno', models.AutoField(primary_key=True, serialize=False)),
                ('introid', models.IntegerField()),
                ('introname', models.CharField(max_length=255)),
                ('rs', models.FloatField()),
                ('package_usd', models.FloatField(default=0)),
                ('rs_usd', models.FloatField(default=0)),
                ('date', models.IntegerField()),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
                ('status', models.IntegerField()),
                ('point', models.IntegerField()),
                ('package', models.FloatField()),
                ('nextsunday', models.DateField()),
                ('zaan_rate', models.FloatField(default=0)),
                ('usd_rate', models.FloatField(default=0)),
                ('position', models.IntegerField()),
                ('custid', models.IntegerField()),
                ('custnewid', models.CharField(max_length=255)),
                ('custname', models.CharField(max_length=255)),
                ('paidstatus', models.IntegerField()),
                ('last_paid_date', models.DateField()),
            ],
            options={
                'db_table': 'magicincome',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MemberHierarchy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_id', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100, unique=True)),
                ('referral_email', models.CharField(max_length=100, unique=True)),
                ('date_of_reg', models.DateField()),
                ('level', models.IntegerField()),
                ('sbg_coin', models.IntegerField()),
                ('status', models.IntegerField()),
            ],
            options={
                'db_table': 'MemberHierarchy',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NewLogin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('userid', models.CharField(max_length=255)),
                ('emailid', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=255)),
                ('reg_date', models.DateField()),
                ('status', models.IntegerField()),
                ('type', models.CharField(max_length=255)),
                ('lastlogin', models.DateTimeField()),
                ('currentlogin', models.DateTimeField()),
            ],
            options={
                'db_table': 'newlogin',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PackageAssign',
            fields=[
                ('PackageIssueId', models.AutoField(primary_key=True, serialize=False)),
                ('MemberNewId', models.CharField(max_length=50)),
                ('MemberId', models.IntegerField()),
                ('MemberName', models.CharField(max_length=255)),
                ('MemberIntroId', models.CharField(max_length=50)),
                ('MemberIntroName', models.CharField(max_length=255)),
                ('MemberRegisDate', models.DateField()),
                ('Package', models.IntegerField()),
                ('DSI', models.IntegerField()),
                ('PV', models.IntegerField()),
                ('CapLimit', models.CharField(max_length=255)),
                ('PackageIssueDate', models.DateField()),
                ('PackagePin', models.CharField(max_length=255)),
                ('packageid', models.IntegerField()),
            ],
            options={
                'db_table': 'PackageAssign',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='QrTransDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('memberid', models.CharField(max_length=255)),
                ('client_txn_id', models.TextField()),
                ('amount', models.FloatField()),
            ],
            options={
                'db_table': 'qr_trans_details',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('worth_zaan', models.FloatField()),
                ('expire_date', models.DateTimeField(null=True)),
                ('is_scratched', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'rewards',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RimberioCoinDistribution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin_reward', models.IntegerField()),
                ('task', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'rimberio_coin_distribution',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RimberioWallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remark', models.TextField(null=True)),
                ('amount', models.FloatField()),
                ('trans_for', models.CharField(max_length=255)),
                ('trans_date', models.DateTimeField()),
                ('trans_type', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'rimberio_wallet_history',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ROIRates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField()),
                ('set_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'roi_rates',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SocialJobs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sociallink', models.TextField()),
                ('whatfor', models.CharField(max_length=255, null=True)),
                ('fb_link', models.CharField(max_length=255, null=True)),
                ('insta_link', models.CharField(max_length=255, null=True)),
                ('twitter_link', models.CharField(max_length=255, null=True)),
                ('youtube_link', models.CharField(max_length=255, null=True)),
                ('greview_link', models.CharField(max_length=255, null=True)),
                ('uploaddate', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'sociallinks',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SubmittedData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_by', models.CharField(max_length=255)),
                ('question_inp', models.CharField(max_length=255)),
                ('selected_choice', models.CharField(default=0, max_length=255)),
            ],
            options={
                'db_table': 'SubmittedData',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SubmittedDataForSocialMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('whatfor', models.CharField(max_length=255)),
                ('greview_image', models.FileField(null=True, upload_to='taskImages/')),
                ('facebook_image', models.FileField(null=True, upload_to='taskImages/')),
                ('twitter_image', models.FileField(null=True, upload_to='taskImages/')),
                ('insta_image', models.FileField(null=True, upload_to='taskImages/')),
                ('youtube_image', models.FileField(null=True, upload_to='taskImages/')),
                ('uploaddate', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'submittedimagesforsocialmedia',
                'ordering': ['id'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TempDailyROI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(max_length=100)),
                ('roi_date', models.DateField()),
                ('roi_sbg', models.FloatField()),
                ('total_sbg', models.FloatField()),
                ('roi_days', models.IntegerField()),
                ('remark', models.CharField(max_length=255)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TransactionHistoryOfCoin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cointype', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=255)),
                ('hashtrxn', models.CharField(max_length=255)),
                ('amount', models.FloatField()),
                ('coinvalue', models.FloatField()),
                ('trxndate', models.DateTimeField()),
                ('status', models.CharField(max_length=100)),
                ('coinvaluedate', models.DateTimeField()),
                ('total', models.FloatField()),
                ('amicoinvalue', models.FloatField()),
                ('amifreezcoin', models.FloatField()),
                ('amivolume', models.FloatField()),
                ('totalinvest', models.FloatField()),
                ('tran_type', models.CharField(max_length=100, null=True)),
            ],
            options={
                'db_table': 'wallet_transactionhistoryofcoin',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UploadedImages',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('uploaded_image', models.FileField(null=True, upload_to='static/uploadedDocuments/')),
                ('doc_type', models.CharField(max_length=255)),
                ('doc_number', models.CharField(max_length=255)),
                ('upload_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'uploaded_images',
                'ordering': ['id'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserActivatedMachineDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('hasActivatedAntiminerS21', models.BooleanField(default=False)),
                ('hasActivatedAntiminerRPRO', models.BooleanField(default=False)),
                ('hasActivatedAntiminerT9', models.BooleanField(default=False)),
                ('S21_activation_date', models.DateTimeField(blank=True, null=True)),
                ('hasActivatedT9PROHYD', models.BooleanField(default=False)),
                ('hasActivatedS9jPRO', models.BooleanField(default=False)),
                ('hasActivatedS9jPROA', models.BooleanField(default=False)),
                ('S9jPRO_activation_date', models.DateTimeField(blank=True, null=True)),
                ('RPRO_activation_date', models.DateTimeField(blank=True, null=True)),
                ('T9_activation_date', models.DateTimeField(blank=True, null=True)),
                ('T9PROHYD_activation_date', models.DateTimeField(blank=True, null=True)),
                ('S9jPROA_activation_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'user_activated_machine_details',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserBankDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('bank_name', models.CharField(max_length=255)),
                ('ifsc', models.CharField(max_length=255)),
                ('accNo', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'UserBankDetails',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Withdrawal_Type',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('withdrawal_mode', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'Withdrawal_Type',
                'managed': False,
            },
        ),
        migrations.AlterModelOptions(
            name='income1',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='income2',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='roidailycustomer',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='walletamicoinforuser',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='zquser',
            options={'managed': False, 'ordering': ['-date_joined']},
        ),
        migrations.AlterModelTable(
            name='tradingtransaction',
            table='trading_transactions',
        ),
    ]
