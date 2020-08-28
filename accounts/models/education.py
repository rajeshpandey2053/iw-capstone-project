from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class College(models.Model):
    college_name = models.CharField(max_length=150)
    college_short_form = models.CharField(max_length=150, blank=False, null=True)

    def __str__(self):
        return self.college_short_form


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
    # SEMESTERS = [(1, 'semester 1'),(2,'semester 2'),(3,'semester 3'),(4,'semester 4'),(5,'semester 5'),(6,
    # 'semester 6'),(7,'semester 7'),(8,'semester 8')] YEARS = [(1,'year 1'),(2,'year 2'),(3,'year 3'),(4,'year 4')]
    semester = models.IntegerField(blank=True, null=True)
    year = models.IntegerField()
    college = models.CharField(max_length=30)
    faculty = models.ForeignKey(Faculty, related_name='education_faculty', on_delete=models.PROTECT)
    university = models.ForeignKey(University, related_name='education_University', on_delete=models.PROTECT)

    def __str__(self):
        return f"year:{self.year} sem:{self.semester}"

