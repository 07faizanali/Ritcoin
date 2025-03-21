# Generated by Django 5.0.6 on 2024-06-12 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zqUsers', '0003_alter_income1_table_alter_income2_table_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminWithdrawalCharge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chargeInPercent', models.FloatField()),
            ],
            options={
                'db_table': 'admin_withdrawal_charge',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='prepaidSocialMediaBonus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bonus', models.FloatField()),
                ('given_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'prepaid_social_media_bonus',
                'managed': False,
            },
        ),
        migrations.AlterModelTable(
            name='banklist',
            table='bank_list',
        ),
    ]
