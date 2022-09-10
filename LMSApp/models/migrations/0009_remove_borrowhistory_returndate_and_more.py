# Generated by Django 4.1 on 2022-09-10 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0008_borrowhistory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='borrowhistory',
            name='returnDate',
        ),
        migrations.AlterField(
            model_name='borrowhistory',
            name='copy',
            field=models.ForeignKey(on_delete=models.SET('Deleted Copy'), to='models.copy'),
        ),
        migrations.CreateModel(
            name='Fines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('borrowInstance', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='models.borrowhistory')),
            ],
        ),
    ]