from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import *
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decoraters import *
from django.contrib.auth.models import Group
from django.core.paginator import Paginator


# Login and Home and Logout //////////////////////////////////////////////////////////////////
@unauthenticated_user
def loginPage(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

    return render(request, "login.html", context)


@login_required(login_url="login/")
def logoutUser(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login/")
def home(request):
    context = {}
    return render(request, "home.html", context)


@unauthenticated_user
@login_required(login_url="login/")
def base(request):
    return redirect("home")


# User ONLY ///////////////////////////////////////////////////////////////////////////////
@unauthenticated_user
def registerApplicantPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect("login")

    context = {"form": form}
    return render(request, "register.html", context)


@login_required(login_url="login/")
def userView(request):
    applicant = Applicant.objects.filter(user=request.user)
    applications = []
    for each in applicant:
        applications.append(each.job)
    context = {"applications": applications}
    return render(request, "userdashboard.html", context)


# Recruiter Only ////////////////////////////////////////////////////////////////////////////////////


@unauthenticated_user
def registerRecruiter(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            group = Group.objects.get(name="user")

            return redirect("login")

    context = {"form": form}
    return render(request, "recruiter_register.html", context)


@login_required(login_url="login/")
def recruiterDash(request):
    my_list = []
    jobs = Job.objects.filter(company=request.user)
    applicants = Applicant.objects.filter(job__in=jobs)
    print(applicants)
    context = {"jobs": jobs, "applicants": applicants}
    return render(request, "recruiterdashboard.html", context)


def viewApplicant(request, id):
    job = Job.objects.get(id=id)
    applicants = Applicant.objects.filter(job=job)
    context = {"applicants": applicants}
    return render(request, "viewapplicants.html", context)


def resume(request, id):
    resume = Applicant.objects.get(id=id).resume
    context = {"resume": resume}
    return render(request, "resume.html", context)


@login_required(login_url="login/")
def JobListing(request):
    form = JobForm()

    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.is_published = True
            title = request.POST.get("title")
            city = request.POST.get("city")
            state = request.POST.get("state")
            job_type = request.POST.get("Job_type")
            salary = request.POST.get("salary")
            description = request.POST.get("description")
            date_published = request.POST.get("date_published")
            company_description = request.POST.get("company_description")
            createJob(
                request.user,
                company_description,
                title,
                description,
                city,
                state,
                job_type,
                salary,
                job.is_published,
                date_published,
            )

            return redirect("recruiterdash")

    context = {"form": form}
    return render(request, "joblisting.html", context)


@login_required(login_url="login/")
def deleteJob(request, id):
    job_listing = Job.objects.get(id=id)
    if request.method == "POST":
        job_listing.delete()

        return redirect("recruiterdash")

    context = {"job_listing": job_listing}
    return render(request, "deletejob.html", context)


@login_required(login_url="login/")
def updateJob(request, id):
    instance = Job.objects.get(id=id)
    form = JobEditForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()

        return redirect("recruiterdash")
    content = {"form": form}
    return render(request, "updatejob.html", content)


@login_required(login_url="login/")
def search_result_view(request):

    job_list = Job.objects.order_by("-date_published")
    print(job_list)

    if "job_title_or_company" in request.GET:
        job_title_or_company_name = request.GET["job_title_or_company"]

        if job_title_or_company_name:
            job_list = job_list.filter(
                title__icontains=job_title_or_company_name
            ) | job_list.filter(company_name__icontains=job_title_or_company_name)
            print(job_list)

    if "city_or_state" in request.GET:
        location = request.GET["city_or_state"]
        if location:
            job_list = job_list.filter(location__icontains=location)
            print(job_list)

    if "job_type" in request.GET:
        job_type = request.GET["job_type"]
        if job_type:
            job_list = job_list.filter(job_type__iexact=job_type)
            print(job_list)

    paginator = Paginator(job_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
    }
    return render(request, "jobview.html", context)


@login_required(login_url="login/")
def applyforJob(request, id):
    form = ApplicantForm()
    job_listing = Job.objects.get(id=id)
    user = request.user
    if request.method == "POST":
        form = ApplicantForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            resume = request.FILES.get("resume")

            createApplicant(user, job_listing, first_name, last_name, resume)
            print(user)

            return redirect("userdash")

    context = {"form": form}
    return render(request, "applyforjob.html", context)
