from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from .models import Quiz
from .serializers import QuizSerializer, UserSerializer
from .socketio import sio, update_room_count, timer_states
import json
from django.views.decorators.csrf import csrf_exempt
import asyncio
import time
from datetime import datetime, timedelta
from django.utils import timezone
from login.models import User
from client.models import ClientQuiz
from django.db.models import F, Avg, Max


def username_required(view_func):
    def inner(request, *args, **kwargs):
        if request.session.get("uid"):
            user = User.objects.filter(user_uid=request.session.get("uid")).first()
            if user.user_username is None:
                return redirect(reverse("login:welcome"))
        return view_func(request, *args, **kwargs)
    return inner


# Create your views here.
@username_required
def index(request):
    if request.session.get("uid"):
        quiz_code = ""
        quiz_running = False

        if request.session.get("quiz_end_time", False):
            if timezone.now() >= datetime.fromisoformat(request.session.get("quiz_end_time")):
                request.session.pop("quiz_start_time")
                request.session.pop("quiz_end_time")
                request.session.pop("quiz_code")
                
            
            quiz_running = True
            quiz_code = request.session.get("quiz_code", "")

        my_template = "host/manage_quiz.html"

        context = {
            "quiz_code": quiz_code,
            "title": "",
            "questions": {

            },
            "quiz_running": quiz_running,
        }
        
        return render(request, my_template, context)
    
    return redirect(reverse("login:index"))

@username_required
def new_quiz(request):
    if request.session.get("uid"):
        my_template = "host/new_quiz.html"
        context = {
            "data": "nothing"
        }

        if request.method=="POST":
            no_of_questions = int(request.POST['no_of_questions'])

            questions = {}
            for i in range(1, no_of_questions+1):
                questions[request.POST[f"question{i}"]] = {"choices": request.POST.getlist(f"question{i}_choice"), "correct_choice_idx": int(request.POST[f"question{i}_choice_correct"])}

            quiz_title = request.POST['quiz_title']
            
            if(request.POST['quiz_timer_minutes']=="other"):
                quiz_timer_minutes = request.POST['timerOther']
            else:
                quiz_timer_minutes = request.POST['quiz_timer_minutes']
                
            host_id = request.session["username"]

            # obtaining quiz_id
            filtered_data = Quiz.objects.filter(quiz_host_id=host_id)
            max_quiz_id = filtered_data.aggregate(Max("quiz_id"))["quiz_id__max"]
            quiz_id = max_quiz_id+1 if max_quiz_id is not None else 1000


            context = {
                "quiz_id": quiz_id,
                "quiz_title": quiz_title,
                "quiz_timer_minutes": quiz_timer_minutes,
                "quiz_questions": questions,
            }


            quiz_obj = Quiz(quiz_id=quiz_id, quiz_host_id=host_id, quiz_title=quiz_title, quiz_timer_minutes=quiz_timer_minutes)
            try:
                quiz_obj.save()
            except ValueError as e:
                return JsonResponse({"message": f"Quiz limit reached. Please delete some quizzes to create new one!", "error": True})

            questions_text = list(questions.keys())
            # print(questions)
            for i in range(no_of_questions):
                question = questions_text[i]
                question_obj = quiz_obj.question_set.create(question_id=i+1, question_text=question)
                
                choices_and_correct = questions[question]
                choices = choices_and_correct["choices"]
                choice_correct = choices_and_correct["correct_choice_idx"]
                j = 1
                for choice in choices:
                    if choices[choice_correct]==choice:
                        choice_obj = question_obj.choice_set.create(choice_id=j, choice_text=choice, is_correct_choice=True)
                    else:
                        choice_obj = question_obj.choice_set.create(choice_id=j, choice_text=choice)
                    j += 1
            
            return JsonResponse({"message": f"Quiz saved with QuizCode {host_id} {quiz_obj.quiz_id}!", "error": None})


        return render(request, my_template, context)
    
    return redirect(reverse("login:index"))


@username_required
def preview(request, host_id, quiz_id):
    if request.session.get("uid"):
        my_template = "host/preview_quiz.html"

        context = {
            "host_id": host_id,
            "quiz_id": quiz_id
        }
        return render(request, my_template, context=context)
    
    return redirect(reverse("home:index"))
    


@username_required
def responses(request, host_id, quiz_id):
    if request.session.get("uid"):
        my_template = "host/responses.html"

        context = {
            "host_id": host_id,
            "quiz_id": quiz_id
        }
        return render(request, my_template, context=context)
    
    return redirect(reverse("home:index"))


@username_required
def result_info(request, host_id, quiz_id, client_id):
    if request.session.get("uid"):
        my_template = "result_info.html"

        client = User.objects.get(user_username=client_id)
        context = {
            "host_id": host_id,
            "quiz_id": quiz_id,
            "client_id": client_id
        }

        get_object_or_404(Quiz, quiz_host_id=host_id, quiz_id=quiz_id)

        return render(request, my_template, context=context)
    
    return redirect(reverse("home:index"))


# def get_all_quiz(request):
#     if request.session.get("uid"):
#         host_id = request.session["username"]
#         quizzes = Quiz.objects.filter(quiz_host_id=host_id).order_by("-quiz_publish_date")
        
#         serializer = QuizSerializer(quizzes, many=True)
#         # print(serializer.data)
#         return JsonResponse(serializer.data, safe=False)
    
#     return redirect(reverse("login:index"))

@csrf_exempt
def getPreviouslyHeldQuizzes(request):
    if request.session.get("uid"):
        data = json.loads(request.body)
        start = data["start"]

        host_id = request.session["username"]

        end = start+10
        total_quizzes = Quiz.objects.filter(quiz_host_id=host_id).count()

        if end<total_quizzes:
            quizzes = Quiz.objects.filter(quiz_host_id=host_id, quiz_is_held=True).order_by("-quiz_publish_date")[start:end]
        else:
            quizzes = Quiz.objects.filter(quiz_host_id=host_id, quiz_is_held=True).order_by("-quiz_publish_date")[start:]
        
        serializer = QuizSerializer(quizzes, many=True)
        # print(serializer.data)
        return JsonResponse(serializer.data, safe=False)
    
    return redirect(reverse("login:index"))

@csrf_exempt
def getToBeHeldQuizzes(request):
    if request.session.get("uid"):
        data = json.loads(request.body)
        start = data["start"]

        host_id = request.session["username"]

        end = start+10
        total_quizzes = Quiz.objects.filter(quiz_host_id=host_id).count()

        if end<total_quizzes:
            quizzes = Quiz.objects.filter(quiz_host_id=host_id, quiz_is_held=False).order_by("-quiz_publish_date")[start:end]
        else:
            quizzes = Quiz.objects.filter(quiz_host_id=host_id, quiz_is_held=False).order_by("-quiz_publish_date")[start:]
        
        serializer = QuizSerializer(quizzes, many=True)
        # print(serializer.data)
        return JsonResponse(serializer.data, safe=False)
    
    return redirect(reverse("login:index"))

def getToBeHeldQuizCount(request):
    total_quizzes = Quiz.objects.filter(quiz_host_id=request.session.get("username"), quiz_is_held=False).count()
    return JsonResponse({"total": total_quizzes})

def getPreviouslyHeldQuizCount(request):
    total_quizzes = Quiz.objects.filter(quiz_host_id=request.session.get("username"), quiz_is_held=True).count()
    return JsonResponse({"total": total_quizzes})


def start_quiz(request):
    if request.method=="POST":
        room = request.POST["quizCode"]

        timer_states.setdefault(room, {"running": True})
        # print(f"{timer_states} starting")

        host_id = room.split(" ")[0]
        quiz_id = room.split(" ")[1]

        quiz = Quiz.objects.get(quiz_id=quiz_id, quiz_host_id=host_id)
        quiz.quiz_visible = False
        quiz.save()

        # returns datetime.datetime object
        current_datetime = timezone.localtime()

        quiz_start_time = current_datetime
        request.session["quiz_start_time"] = quiz_start_time.isoformat()
        # print(request.session.get("quiz_start_time"))

        quiz_end_time = quiz_start_time + timedelta(seconds=int(request.POST["total_seconds"]))
        
        request.session["quiz_end_time"] = quiz_end_time.isoformat()

        request.session["quiz_code"] = f"{host_id}{quiz_id}"

        sio.emit("start_quiz", data={"start": True, "quiz_start_time": quiz_start_time.isoformat()}, room=room)
        

    return JsonResponse({"quiz_start_time": quiz_start_time.isoformat(), "quiz_end_time": quiz_end_time.isoformat()})


def getTimerValue(request):
    if(request.session.get("quiz_start_time")):
        time_difference = datetime.fromisoformat(request.session.get("quiz_end_time", 0)) - timezone.now()
        
        time_remaining = time_difference.total_seconds()

        return JsonResponse({"time_seconds": time_remaining})
    
    return JsonResponse({"time_seconds": False})

def clearQuizSession(request):
    if(request.session.get("quiz_start_time")):
        request.session.pop("quiz_start_time")
        request.session.pop("quiz_end_time")
        request.session.pop("quiz_code")
    
    return JsonResponse({"cleared": True})


def submitQuiz(request):

    room = request.GET["room"]

    host_id = room.split(" ")[0]
    quiz_id = room.split(" ")[1]

    timer_states.pop(room, None)

    # submitted quiz on client view
    sio.emit("submit_quiz", data={"stop": True}, room=room)

    # updating quiz meta data
    host_quiz = Quiz.objects.get(quiz_host_id=host_id, quiz_id=quiz_id)
    host_quiz.quiz_is_held = True
    host_quiz.save()

    # updating number of quizzes hosted by user
    user = User.objects.get(user_uid=request.session.get("uid"))
    user.user_quizzes_hosted += 1
    user.save()

    # print(user.user_quizzes_hosted)

    return JsonResponse({"stopped": True})


@csrf_exempt
def deleteQuiz(request):
    if request.method=="POST":
        quiz_code = json.loads(request.body)["quizCode"]
        host_id = quiz_code.split(" ")[0]
        quiz_id = quiz_code.split(" ")[1]

        host_quiz = Quiz.objects.get(quiz_host_id=host_id, quiz_id=quiz_id)
        host_quiz.delete()

        client_quiz =  ClientQuiz.objects.filter(clientquiz_host_id=host_id, clientquiz_quiz_id=quiz_id)
        client_quiz.delete()

        return JsonResponse({"message": f"Quiz deleted successfully!"})

    return redirect(reverse("host:index"))


@csrf_exempt
def changeQuizVisibility(request):
    if request.method=="POST":
        quiz_code = json.loads(request.body)["quizCode"]
        host_id = quiz_code.split(" ")[0]
        quiz_id = quiz_code.split(" ")[1]

        quiz_visible = json.loads(request.body)["quiz_visible"]

        quiz_obj = Quiz.objects.get(quiz_host_id=host_id, quiz_id=quiz_id)
        
        # print(quiz_visible)
        quiz_obj.quiz_visible = quiz_visible
        quiz_obj.save()

        sio.emit("visibility_changed", {"quiz_visible": quiz_visible}, room=quiz_code)

        return JsonResponse({"message": f"Quiz visibility changed!"})

    return redirect(reverse("host:index"))

def editQuiz(request):
    if request.method=="POST":
        # getting host_id and quiz_id
        quiz_id = request.POST["quiz_id"]
        host_id = request.POST["host_id"]

        quiz_obj = Quiz.objects.get(quiz_host_id=host_id, quiz_id=quiz_id)

        no_of_questions = int(request.POST['no_of_questions'])

        questions = {}
        for i in range(1, no_of_questions+1):
            questions[request.POST[f"question{i}"]] = {"choices": request.POST.getlist(f"question{i}_choice"), "correct_choice_idx": int(request.POST[f"question{i}_choice_correct"])}

        quiz_title = request.POST['quiz_title']
            
        if(request.POST['quiz_timer_minutes']=="other"):
            quiz_timer_minutes = request.POST['timerOther']
        else:
            quiz_timer_minutes = request.POST['quiz_timer_minutes']


        # updating quiz object
        quiz_obj.quiz_title = quiz_title
        quiz_obj.quiz_timer_minutes = quiz_timer_minutes

        try:
            quiz_obj.save()
        except ValueError as e:
            return JsonResponse({"message": f"Quiz limit reached. Please delete some quizzes to create new one!", "error": True})

        # deleting question_set, choice_set will also get deleted due to
        # models.CASCADE property
        quiz_obj.question_set.all().delete()

        questions_text = list(questions.keys())
        # print(questions)
        for i in range(no_of_questions):
            question = questions_text[i]
            question_obj = quiz_obj.question_set.create(question_id=i+1, question_text=question)
                
            choices_and_correct = questions[question]
            choices = choices_and_correct["choices"]
            choice_correct = choices_and_correct["correct_choice_idx"]
            j = 1
            for choice in choices:
                if choices[choice_correct]==choice:
                    choice_obj = question_obj.choice_set.create(choice_id=j, choice_text=choice, is_correct_choice=True)
                else:
                    choice_obj = question_obj.choice_set.create(choice_id=j, choice_text=choice)
                j += 1
            
        return JsonResponse({"message": f"Quiz edited with QuizCode {host_id} {quiz_obj.quiz_id}!", "error": None})   

    if request.GET.get("host_id") and request.GET.get("quiz_id") :
        my_template = "host/edit_quiz.html"

        quiz_id = request.GET.get("quiz_id")
        host_id = request.GET.get("host_id")

        quiz_obj = Quiz.objects.get(quiz_host_id=host_id, quiz_id=quiz_id)
        
        if quiz_obj.quiz_is_held==True or (quiz_obj.quiz_visible):
            return redirect(reverse("host:index"))

        context = {
            "quiz_id": quiz_id,
            "host_id": host_id
        }

        return render(request, my_template, context=context)

    return redirect(reverse("host:index"))


def getJoinedUsers(request):
    quiz_code = request.GET["quiz_code"]
    host_id = quiz_code.split(" ")[0]
    quiz_id = quiz_code.split(" ")[1]

    quiz = Quiz.objects.get(quiz_id=quiz_id, quiz_host_id=host_id)
    no_of_users = quiz.quiz_no_of_users

    return JsonResponse({"no_of_users": no_of_users})

def getPassedUsers(request):
    quiz_code = request.GET["quiz_code"]
    host_id = quiz_code.split(" ")[0]
    quiz_id = quiz_code.split(" ")[1]

    quiz = ClientQuiz.objects.filter(clientquiz_quiz_id=quiz_id, clientquiz_host_id=host_id).annotate(percentage=(F("clientquiz_correct_answers") * 100)/F("clientquiz_total_questions")).filter(percentage__gte=33)
    totalUsersPassed = quiz.count()

    averagePercentage = quiz.aggregate(avg_percentage=Avg('percentage'))

    return JsonResponse({"totalUsersPassed": totalUsersPassed, "averagePercentage": averagePercentage["avg_percentage"]})

@csrf_exempt
def leave(request):
    if request.method=="POST":
        room = json.loads(request.body)["room"]
        sid = json.loads(request.body)["sid"]
        # room = data["room"]
        # print("left")
        sio.leave_room(sid, room)

        update_room_count(room)

        return JsonResponse({"Done": True})
    return redirect(reverse("home:index"))


@csrf_exempt
def getUserData(request):
    username = json.loads(request.body)["username"]
    user = User.objects.get(user_username=username)

    serializer = UserSerializer(user)

    return JsonResponse(serializer.data, safe=False)


def socketio_view(request):
    return sio.manage(request)