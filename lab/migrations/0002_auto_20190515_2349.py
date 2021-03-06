# Generated by Django 2.2.1 on 2019-05-15 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('submission', '0001_initial'),
        ('lab', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='labsubmissionproblemsubmission',
            name='problem_submission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='submission.ProblemSubmission'),
        ),
        migrations.AddField(
            model_name='labsubmission',
            name='lab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab.Lab'),
        ),
        migrations.AddField(
            model_name='labsubmission',
            name='problem_submissions',
            field=models.ManyToManyField(blank=True, related_name='lab_submissions', through='lab.LabSubmissionProblemSubmission', to='submission.ProblemSubmission'),
        ),
    ]
