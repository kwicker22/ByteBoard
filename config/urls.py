from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path("register/", registerApplicantPage, name="register"),
    path("login/", loginPage, name="login"),
    path("logout/", logoutUser, name="logout"),
    path("user/", userView, name="userdash"),
    path("recruiter/", recruiterDash, name="recruiterdash"),
    path("create_job/", JobListing, name="create-job"),
    path("recruiter_register/", registerRecruiter, name="recruiter_register"),
    path("home", home, name="home"),
    path("", base, name="base"),
    path("admin/", admin.site.urls),
    path("delete/", deleteJob, name="delete"),
]
