# Generated by Django 4.0.3 on 2022-04-05 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auctionbid_authgroup_authgrouppermissions_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boodleuser',
            fields=[
                ('userid', models.AutoField(primary_key=True, serialize=False)),
                ('displayname', models.CharField(max_length=255)),
                ('pword', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'boodleuser',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('storeid', models.AutoField(primary_key=True, serialize=False)),
                ('storename', models.CharField(max_length=255)),
                ('storedesc', models.CharField(max_length=700)),
            ],
            options={
                'db_table': 'store',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Userfavorites',
            fields=[
                ('favoriteid', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'userfavorites',
                'managed': False,
            },
        ),
    ]
