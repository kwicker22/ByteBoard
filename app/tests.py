from django.test import TestCase
from .models import *
from django.contrib.auth.models import User


# Create your tests here.


class Sitetest(TestCase):
    def test_create_job(self):
        user = User.objects.create(username="Kera", password="123password")
        job = createJob(
            user,
            "Bass Camp",
            "python dev",
            "dev python",
            "saltillo",
            "ms",
            "Full time",
            10,
            True,
            "2024-05-21",
        )

        self.assertEqual(job.company, user)
        self.assertEqual(job.company_description, "Bass Camp")
        self.assertEqual(job.title, "python dev")
        self.assertEqual(job.description, "dev python")
        self.assertEqual(job.city, "saltillo")
        self.assertEqual(job.state, "ms")
        self.assertEqual(job.job_type, "Full time")
        self.assertEqual(job.salary, 10)
        self.assertEqual(job.is_published, True)
        self.assertEqual(job.date_published, "2024-05-21")
