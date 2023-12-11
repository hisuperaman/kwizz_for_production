from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from login.models import User
from django.views.decorators.csrf import csrf_exempt
import json
from host.models import Quiz

def username_required(view_func):
    def inner(request, *args, **kwargs):
        if request.session.get("uid"):
            user = User.objects.filter(user_uid=request.session.get("uid")).first()
            if user is None:
                request.session.pop("uid")
                return redirect(reverse("login:index"))
            if user.user_username is None:
                return redirect(reverse("login:welcome"))
        return view_func(request, *args, **kwargs)
    return inner

# Create your views here.
@username_required
def index(request):
    if request.session.get("uid"):
        my_template = "home/index.html"
        
        return render(request, my_template)
    
    return redirect(reverse("login:index"))

@csrf_exempt
def getHostQuizHeldStatus(request):
    if request.method=="POST":
        quiz_code = json.loads(request.body)["quiz_code"]
        host_id = quiz_code.split(" ")[0]
        quiz_id = quiz_code.split(" ")[1]

        host_quiz = Quiz.objects.get(quiz_host_id=host_id, quiz_id=quiz_id)
        quiz_is_held = host_quiz.quiz_is_held

        return JsonResponse({"quiz_is_held": quiz_is_held})

    return redirect(reverse("home:index"))