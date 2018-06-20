from django.db import models

# Create your models here.

class Shifts(models.Model):
    name = models.CharField(max_length=20, unique=True)
    onduty = models.CharField(max_length=5)
    offduty = models.CharField(max_length=5)
    hours = models.FloatField(null=True)

class Employees(models.Model):
    uid = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=20)

class Arrangement(models.Model):
    date = models.DateField()
    shift = models.ForeignKey(to="Shifts", to_field='name', on_delete=models.CASCADE)
    number = models.IntegerField()

class Schedule(models.Model):
    date = models.DateField()
    shift = models.ForeignKey(to="Shifts", to_field='name', on_delete=models.CASCADE)
    employee = models.ForeignKey(to="Employees", to_field='uid', on_delete=models.CASCADE)

class Vacation(models.Model):
    date = models.DateField()
    employee = models.ForeignKey(to='Employees', to_field='uid', on_delete=models.CASCADE)

class Workhours(models.Model):
    employee = models.ForeignKey(to='Employees', to_field='uid', on_delete=models.CASCADE)
    month = models.IntegerField()
    workhours = models.FloatField(null=True)