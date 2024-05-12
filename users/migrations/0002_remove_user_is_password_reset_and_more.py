# Generated by Django 5.0.4 on 2024-05-12 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_password_reset',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_login_time',
        ),
        migrations.RemoveField(
            model_name='user',
            name='verification_code',
        ),
        migrations.AddField(
            model_name='user',
            name='bot_id',
            field=models.IntegerField(default=1111111111, unique=True, verbose_name='Телеграмм id пользователя'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=35, null=True, verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status'),
        ),
    ]