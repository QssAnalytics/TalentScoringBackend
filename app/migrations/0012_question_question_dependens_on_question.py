# Generated by Django 4.1.7 on 2023-07-04 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_rename_question_idd_answer_questionidd'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_dependens_on_question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question_depend', to='app.question'),
        ),
    ]