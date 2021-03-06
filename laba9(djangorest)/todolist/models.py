from django.db import models
from django.contrib.auth.models import User

class Tasklist(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey('auth.User', null=False,  default='', related_name='lists', on_delete=models.CASCADE) ###У списка задач есть поле владелец


    def __str__(self):
        return "{}".format(self.name)

class TaskType(models.Model): ###Модель тегов
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=200, blank=True)
    description = models.TextField(max_length=1000, blank=True)
    completed = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    date_modified = models.DateField(auto_now=True)
    tasklist = models.ForeignKey(Tasklist, null=True, related_name='tasks', on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', null=False, default='', related_name='tasks', on_delete=models.CASCADE) ###У задачи есть поле владелец
    tags = models.ManyToManyField(TaskType, related_name='tasks') ###У задачи есть поле теги

    PRIORITY = (
        ('h', 'High'),
        ('m', 'Medium'),
        ('l', 'Low'),
        ('n', 'None')
    )

    priority = models.CharField(max_length=1, choices=PRIORITY, default='n')

    def __str__(self):
        return "{}".format(self.name)
