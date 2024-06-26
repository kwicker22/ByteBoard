from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage


upload_storage = FileSystemStorage(location="/static", base_url="/uploads")


# Create your models here.

JobType = (
    ("1", "Full time"),
    ("2", "Part time"),
    ("3", "Internship"),
)


# class Category(models.Model):
#     name = models.CharField(max_length=50)

#     def __str__(self) -> str:
#         return self.name


class Job(models.Model):
    company = models.ForeignKey(User, related_name="company", on_delete=models.CASCADE)
    company_description = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=300)
    description = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    job_type = models.CharField(choices=JobType, max_length=9)
    # category = models.ForeignKey(
    #     Category, related_name="Category", on_delete=models.CASCADE
    # )
    salary = models.PositiveIntegerField()
    is_published = models.BooleanField(default=False)
    date_published = models.DateField()

    def __str__(self):
        return self.title


def createJob(
    company,
    company_description,
    title,
    description,
    city,
    state,
    job_type,
    salary,
    is_published,
    date_published,
):
    return Job.objects.create(
        company=company,
        company_description=company_description,
        title=title,
        description=description,
        city=city,
        state=state,
        job_type=job_type,
        salary=salary,
        is_published=is_published,
        date_published=date_published,
    )


class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    resume = models.ImageField(upload_to="", null=True, blank=True)

    def __str__(self):
        return self.job.title


def createApplicant(user, job, first_name, last_name, resume):
    return Applicant.objects.create(
        user=user, job=job, first_name=first_name, last_name=last_name, resume=resume
    )
