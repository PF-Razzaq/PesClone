# Generated by Django 5.0.4 on 2024-05-08 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pes', '0011_alter_pesevents_eventdate'),
    ]

    operations = [
        migrations.CreateModel(
            name='PesExecutor',
            fields=[
                ('ExecutorID', models.BigAutoField(primary_key=True, serialize=False)),
                ('Username', models.CharField(max_length=50)),
                ('Password', models.CharField(max_length=50)),
                ('Status', models.IntegerField()),
                ('ExecutorOverrideID', models.IntegerField(blank=True, null=True)),
                ('LastAccessed', models.DateTimeField(blank=True, null=True)),
                ('LoginCount', models.DecimalField(blank=True, decimal_places=0, max_digits=18, null=True)),
                ('LanguageID', models.CharField(blank=True, max_length=2, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'PesExecutor',
            },
        ),
    ]