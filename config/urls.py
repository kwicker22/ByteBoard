from django.contrib import admin
from django.urls import path
from app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("register/", registerApplicantPage, name="register"),
    path("login/", loginPage, name="login"),
    path("logout/", logoutUser, name="logout"),
    path("user/", userView, name="userdash"),
    path("recruiter/", recruiterDash, name="recruiterdash"),
    path("create_job/", JobListing, name="create-job"),
    path("recruiter_register/", registerRecruiter, name="recruiter_register"),
    path("update/<int:id>/", updateJob, name="update"),
    path("home/jobs/apply/<int:id>", applyforJob, name="apply"),
    path("delete/<int:id>/", deleteJob, name="delete"),
    path("home/jobs", search_result_view, name="job_view"),
    path("applicants/<int:id>/", viewApplicant, name="applicants"),
    path("resume/<int:id>/", resume, name="resume"),
    path("home/", home, name="home"),
    path("", base, name="base"),
    path("admin/", admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
