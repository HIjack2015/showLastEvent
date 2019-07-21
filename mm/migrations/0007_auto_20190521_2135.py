# Generated by Django 2.2.1 on 2019-05-21 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mm', '0006_event_threadid'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='looked',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='eventCount',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='followeds',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='follows',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='looked',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='playlistCount',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='vipType',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
