# Generated by Django 4.1 on 2022-09-05 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0005_remove_book_genre_book_genre'),
    ]

    operations = [
        migrations.CreateModel(
            name='Copy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('isIssued', models.BooleanField(default=False)),
                ('issueDate', models.DateField()),
                ('returnDate', models.DateField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.book')),
                ('issuedTo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='models.member')),
            ],
        ),
    ]
