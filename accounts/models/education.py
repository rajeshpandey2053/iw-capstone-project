from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class University(models.Model):
    university_name = models.CharField(max_length=150)
    uni_short_form = models.CharField(max_length=150, blank=False, null=True)

    def __str__(self):
        return self.uni_short_form


class Faculty(models.Model):
    faculty_name = models.CharField(max_length=150)
    fac_short_form = models.CharField(max_length=100)

    def __str__(self):
        return self.fac_short_form


class Education(models.Model):
    semester = models.CharField(max_length=100, blank=True, null=True)
    year = models.CharField(max_length=100)
    college = models.CharField(max_length=200, blank=True, null=True)
    faculty = models.ForeignKey(
        Faculty, related_name='education_faculty', on_delete=models.PROTECT)
    university = models.ForeignKey(
        University, related_name='education_University', on_delete=models.PROTECT)

    def __str__(self):
        return f"year:{self.year} sem:{self.semester}"
