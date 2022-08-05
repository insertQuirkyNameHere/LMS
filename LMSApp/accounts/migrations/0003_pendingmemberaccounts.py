# Generated by Django 4.1 on 2022-08-04 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_is_approved'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingMemberAccounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100, unique=True)),
            ],
        ),
    ]
