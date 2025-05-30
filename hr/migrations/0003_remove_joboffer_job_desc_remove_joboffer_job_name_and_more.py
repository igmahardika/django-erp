# Generated by Django 5.2.1 on 2025-05-22 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0002_alter_employee_options_alter_jobapplicant_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='joboffer',
            name='job_desc',
        ),
        migrations.RemoveField(
            model_name='joboffer',
            name='job_name',
        ),
        migrations.RemoveField(
            model_name='joboffer',
            name='job_open_from',
        ),
        migrations.RemoveField(
            model_name='joboffer',
            name='job_open_to',
        ),
        migrations.AddField(
            model_name='joboffer',
            name='actual_handling_duration',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='case_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='customer',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='duration',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='duration_waneda',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='end_pause_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='issue_classification',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='last_action',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='odp_or_bts',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='pause_duration',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='power_after',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='power_before',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='priority',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='problem_summary',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='root_cause',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='severity_level',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='site_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='start_escalation_waneda',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='start_pause_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='technician',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
