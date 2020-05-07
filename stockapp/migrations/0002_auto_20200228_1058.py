# Generated by Django 3.0.3 on 2020-02-28 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpricetile',
            name='adj_close',
            field=models.DecimalField(decimal_places=16, max_digits=32),
        ),
        migrations.AlterField(
            model_name='historicalpricetile',
            name='close',
            field=models.DecimalField(decimal_places=16, max_digits=32),
        ),
        migrations.AlterField(
            model_name='historicalpricetile',
            name='high',
            field=models.DecimalField(decimal_places=16, max_digits=32),
        ),
        migrations.AlterField(
            model_name='historicalpricetile',
            name='low',
            field=models.DecimalField(decimal_places=16, max_digits=32),
        ),
        migrations.AlterField(
            model_name='historicalpricetile',
            name='open',
            field=models.DecimalField(decimal_places=16, max_digits=32),
        ),
        migrations.AlterField(
            model_name='livepricetile',
            name='price',
            field=models.DecimalField(decimal_places=16, max_digits=32),
        ),
    ]