# Generated by Django 3.0.8 on 2020-09-11 17:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('idx', models.AutoField(primary_key=True, serialize=False)),
                ('channel_name', models.CharField(blank=True, max_length=100, null=True)),
                ('channel_id', models.CharField(max_length=200)),
                ('channel_description', models.CharField(blank=True, max_length=3000, null=True)),
                ('channel_start_date', models.DateField(blank=True, null=True)),
                ('processed', models.BooleanField(blank=True, null=True)),
                ('upload_id', models.CharField(blank=True, max_length=1000, null=True)),
                ('hidden_subscriber', models.BooleanField(blank=True, null=True)),
                ('thumbnail_url', models.CharField(blank=True, max_length=200, null=True)),
                ('temp', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'db_table': 'channel',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idx', models.IntegerField(blank=True)),
                ('phone', models.CharField(blank=True, max_length=45, null=True)),
                ('on_subscribe', models.BooleanField(blank=True, null=True)),
                ('own_channel', models.ForeignKey(blank=True, db_column='own_channel', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.Channel')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
