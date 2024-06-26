# Generated by Django 5.0.4 on 2024-04-09 22:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Retailer',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('user.useraccount',),
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('ACCEPTED', 'ACCEPTED'), ('REJECTED', 'REJECTED')], default='PENDING', max_length=9)),
                ('required', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.product')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.route')),
                ('retailer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='retailer.retailer')),
            ],
        ),
    ]
