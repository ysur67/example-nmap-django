# Generated by Django 3.1.12 on 2021-10-01 19:40

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Наименование задачи')),
                ('ip_range', models.CharField(max_length=200, verbose_name='Диапазон адресов')),
                ('result', djongo.models.fields.JSONField(blank=True, default={}, verbose_name='Результат выполнения задачи')),
                ('status', models.CharField(blank=True, choices=[('created', 'Создан'), ('started', 'Запущен'), ('stopped', 'Остановлен'), ('finished', 'Выполнен')], default='created', max_length=100, verbose_name='Текущий статус задачи')),
            ],
        ),
    ]
