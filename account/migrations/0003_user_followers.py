# Generated by Django 4.2.1 on 2023-05-18 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_follow_delete_customusermanager_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(to='account.follow'),
        ),
    ]