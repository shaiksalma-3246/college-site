from django.db import models
from django.contrib.auth.models import User
class Subject(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Experiment(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='experiments'
    )
    title = models.CharField(max_length=200)
    aim = models.TextField()
    code = models.TextField()
    explanation = models.TextField()
    output = models.TextField()
    result = models.TextField()
    viva_questions = models.TextField()

    def __str__(self):
        return self.title


class Student(models.Model):
    roll_no = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.roll_no


class LabSession(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject.name} - {self.date}"


class LabMark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(LabSession, on_delete=models.CASCADE)
    marks = models.IntegerField()

    class Meta:
        unique_together = ('student', 'session')

    def __str__(self):
        return f"{self.student.roll_no} - {self.session.date}"
