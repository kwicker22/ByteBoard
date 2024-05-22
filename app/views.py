from django.shortcuts import render, redirect
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
        else:
            messages.info(request, "Username OR Password is incorrect")
    return render(request, "login.html", context)


@login_required(login_url="login/")
def logoutUser(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login/")
def base(request):
    context = {}
    return render(request, "base.html", context)


@login_required(login_url="login/")
def home(request):
    jobs = Job.objects.filter(is_published=True)
    context = {"jobs": jobs}
    return render(request, "home.html", context)


# User ONLY ///////////////////////////////////////////////////////////////////////////////
@unauthenticated_user
def registerApplicantPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            group = Group.objects.get(name="user")
            messages.success(request, (f"Account was created for {group}"))
            return redirect("login")

    context = {"form": form}
    return render(request, "register.html", context)


@login_required(login_url="login/")
def userView(request):
    jobs = Applicant.objects.filter(user=request.user)
    applications = []
    for each in jobs:
        applications.append(each.job)
    context = {"applications": applications}
    return render(request, "userdashboard.html", context)


# Recruiter Only ////////////////////////////////////////////////////////////////////////////////////


def registerRecruiter(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            group = Group.objects.get(name="user")
            messages.success(request, (f"Account was created for {group}"))
            return redirect("login")

    context = {"form": form}
    return render(request, "recruiter_register.html", context)


def recruiterDash(request):
    jobs = Job.objects.filter(company=request.user)
    context = {"jobs": jobs}
    return render(request, "recruiterdashboard.html", context)


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
            messages.success(request, (f"Job was created for {request.user}"))
            return redirect("recruiterdash")

    context = {"form": form}
    return render(request, "joblisting.html", context)


def deleteJob(request):
    messages.success(request, ("Job has been successfully deleted"))
    job_listing = Job.objects.get(id=request.job.id)
    if request.method == "POST":
        form = deleteJob(request.Post)
        if form.is_valid():
            form.save()
            job_listing.delete()
            messages.success(request, ("Job listing has been deleted"))
            return redirect("recruiter")

    context = {"form": form}
    return render(request, ".html", context)
