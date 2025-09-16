from django.db import models

class School(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=200)
    subjects = models.ManyToManyField(Subject, related_name='teachers', blank=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=200)
    roll_no = models.CharField(max_length=50, blank=True)
    school = models.ForeignKey(School, related_name='students', on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject, related_name='students', blank=True)

    def __str__(self):
        return f"{self.name} ({self.roll_no})" if self.roll_no else self.name
