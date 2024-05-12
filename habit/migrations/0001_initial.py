# Generated by Django 5.0.4 on 2024-05-08 08:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Название', max_length=250, verbose_name='Название привычки')),
                ('place', models.CharField(max_length=250, verbose_name='Место выполнения привычки')),
                ('time', models.TimeField(verbose_name='Время выполнения привычки')),
                ('action', models.CharField(max_length=250, verbose_name='Действие привычки')),
                ('is_pleasant_habit', models.BooleanField(verbose_name='Признак приятной привычки')),
                ('frequency', models.IntegerField(default=1, verbose_name='Периодичность (в днях)')),
                ('reward', models.CharField(max_length=200, verbose_name='Вознаграждение')),
                ('time_to_complete', models.IntegerField(verbose_name='Время на выполнение (в минутах)')),
                ('is_public', models.BooleanField(default=False, verbose_name='Признак публичности')),
                ('related_habit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='habit.habit', verbose_name='Связанная привычка')),
            ],
        ),
    ]