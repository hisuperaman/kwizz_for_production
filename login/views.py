from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
import requests
from .models import User
import os

from .oauth_variables import *
# from .client_credentials import *

CLIENT_ID = os.getenv("CLIENT_ID", 123)
CLIENT_SECRET = os.getenv("CLIENT_SECRET", 123)

# Create your views here.
def index(request):
    if not request.session.get("uid"):
        my_template = "login/index.html"
        context = {}
        return render(request, my_template, context)
    return redirect(reverse("home:index"))

def login(request):
    if not request.session.get("uid"):
        url = f"{AUTHORIZATION_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={scopes}"
        return redirect(url)
    return redirect(reverse("login:index"))

def callback(request):
    code = request.GET['code']

    token_params = {
        "code": code,
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI
    }

    try:
        token_response = requests.post(TOKEN_URL, data=token_params)
    except Exception as e:
        print(e)

    access_token = token_response.json()["access_token"]

    headers = {
            "Authorization": f"Bearer {access_token}"
        }
    user_info_response = requests.get("https://www.googleapis.com/oauth2/v3/userinfo", headers=headers)

    user_info = user_info_response.json()

    db_user_info = User.objects.values_list("user_uid", flat=True)

    if user_info["sub"] not in db_user_info:
        User.objects.create(user_uid=user_info["sub"], user_name=user_info["name"], user_email=user_info["email"], user_pfp=user_info["picture"])
        request.session["uid"] = user_info["sub"]
        return redirect(reverse("login:welcome"))

    request.session["uid"] = user_info["sub"]

    user_uid = request.session["uid"]
    user_username = User.objects.filter(user_uid=user_uid).first().user_username
    request.session["username"] = user_username


    return redirect(reverse("home:index"))

def logout(request):
    if request.session.get("uid"):
        request.session.clear()

    return redirect(reverse("login:index"))


def welcome(request):
    if request.method=="POST":
        username = request.POST["username"]
        username = username.strip()
        username = username.lower()
        user = User.objects.filter(user_uid=request.session["uid"]).first()
        user.user_username = username
        user.save()

        request.session["username"] = username

        return redirect(reverse("home:index"))

    if (not request.session.get("username")) and request.session.get("uid"):
        my_template = "login/welcome.html"

        context = {

        }

        return render(request, my_template, context=context)
    
    return redirect(reverse("home:index"))

def username_exists(request):
    username = request.GET["username"]
    users = User.objects.filter(user_username=username).first()
    
    if users is not None:
        return JsonResponse({"exists": True})

    return JsonResponse({"exists": False})