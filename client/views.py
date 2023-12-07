from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from host.models import Quiz
from .models import ClientQuiz
from django.contrib import messages
import json
import requests
from host.serializers import QuizSerializer
from .serializers import ClientQuizSerializer
from django.views.decorators.csrf import csrf_exempt
from login.models import User
from .models import ClientQuiz
from django.utils import timezone
from datetime import datetime, timedelta
import math


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
        if(request.method=="POST"):
            quizCode = request.POST['quiz_code']

            quizID = quizCode.split(' ')[1]
            hostID = quizCode.split(' ')[0]

            return redirect(reverse("client:join", kwargs={"host_id": hostID ,"quiz_id": quizID}))

        quizCode = request.GET.get('quiz_code', False)

        if not quizCode:
            return redirect(reverse("home:index"))

        quizID = quizCode.split(' ')[1]
        hostID = quizCode.split(' ')[0]

        try:
            stored_quizCode = Quiz.objects.get(quiz_id=quizID, quiz_host_id=hostID, quiz_visible=True, quiz_is_held=False)
            return JsonResponse({"message": "Quiz found!"})

        except Quiz.DoesNotExist:
            return JsonResponse({"message": "Quiz not found!"})

    return redirect(reverse("home:index"))

@username_required
def join(request, host_id, quiz_id):
    if request.session.get("uid"):
        context = {
            "host_id": host_id,
            "quiz_id": quiz_id
        }
        
        current_user = User.objects.get(user_uid=request.session.get("uid"))
        current_user_username = current_user.user_username
        if(current_user_username == host_id):
            return redirect(reverse("home:index"))
        
        try:
            Quiz.objects.get(quiz_host_id=host_id, quiz_id=quiz_id, quiz_visible=True, quiz_is_held=False)
        except Quiz.DoesNotExist:
            return redirect(reverse("home:index"))

        return render(request, "client/index.html", context=context)

    return redirect(reverse("home:index"))


@username_required
def result(request, host_id, quiz_id):
    if request.session.get("uid"):
        my_template = "client/result.html"

        user = get_object_or_404(User, user_uid=request.session.get("uid"))
        if user.user_username==host_id:
            return redirect(reverse("home:index"))


        # getting time spent
        quiz_info = ClientQuiz.objects.filter(clientquiz_host_id=host_id, clientquiz_quiz_id=quiz_id, user=user).last()
        time_spent = quiz_info.clientquiz_time_taken.total_seconds()
        minutes = int(time_spent) // 60
        seconds = int(time_spent) % 60

        time_spent = f"{'0' if minutes<10 else ''}{minutes}:{'0' if seconds<10 else ''}{seconds}"
        

        total_questions = quiz_info.clientquiz_total_questions
        correct_answers = quiz_info.clientquiz_correct_answers
        percentage = math.floor((correct_answers/total_questions)*100)
        attempted_questions = quiz_info.clientquiz_attempted_questions
        unattempted_questions = total_questions - attempted_questions

        # getting host_quiz is_held attribute
        host_quiz = Quiz.objects.get(quiz_host_id=host_id, quiz_id=quiz_id)
        quiz_is_held = host_quiz.quiz_is_held

        context = {
            "host_id": host_id,
            "quiz_id": quiz_id,
            "time_spent": time_spent,
            "total_questions": total_questions,
            "correct": correct_answers,
            "percentage": percentage,
            "attempted_questions": attempted_questions,
            "unattempted_questions": unattempted_questions,
            "quiz_is_held": quiz_is_held
        }

        return render(request, my_template, context=context)
        
    return redirect(reverse("home:index"))


@username_required
def result_info(request, host_id, quiz_id):
    if request.session.get("uid"):
        my_template = "result_info.html"

        client_id = User.objects.get(user_uid=request.session.get("uid")).user_username
        context = {
            "host_id": host_id,
            "quiz_id": quiz_id,
            "client_id": client_id
        }

        host_quiz = get_object_or_404(Quiz, quiz_host_id=host_id, quiz_id=quiz_id)
        if not host_quiz.quiz_is_held:
            return redirect(reverse("home:index"))

        return render(request, my_template, context=context)
    
    return redirect(reverse("home:index"))


@csrf_exempt
def get_quiz(request):
    host_id = request.POST['host_id']
    quiz_id = request.POST['quiz_id']
    quiz = get_object_or_404(Quiz, quiz_host_id=host_id, quiz_id=quiz_id)
    # quizzes = Quiz.objects.all()
    
    serializer = QuizSerializer(quiz)
    # print(serializer.data)
    return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def get_client_quiz(request):
    host_id = request.POST['host_id']
    quiz_id = request.POST['quiz_id']
    client_id = request.POST['client_id']

    client = User.objects.get(user_username=client_id)

    try:
        client_quiz = ClientQuiz.objects.get(clientquiz_host_id=host_id, clientquiz_quiz_id=quiz_id, user=client)
        serializer = ClientQuizSerializer(client_quiz)
        # print(serializer.data)
        return JsonResponse(serializer.data, safe=False)

    except ClientQuiz.DoesNotExist:
        # print("Not found")
        return JsonResponse({"unsuccessful": True})
    # quizzes = Quiz.objects.all()

@csrf_exempt
def get_all_client_quiz(request):
    host_id = request.POST['host_id']
    quiz_id = request.POST['quiz_id']
    start = int(request.POST['quiz_start_idx'])

    try:
        end = start+10
        total_quizzes = ClientQuiz.objects.filter(clientquiz_host_id=host_id, clientquiz_quiz_id=quiz_id).count()
        if end<total_quizzes:
            client_quiz = ClientQuiz.objects.filter(clientquiz_host_id=host_id, clientquiz_quiz_id=quiz_id).order_by("-clientquiz_end_time")[start:end]
        else:
            client_quiz = ClientQuiz.objects.filter(clientquiz_host_id=host_id, clientquiz_quiz_id=quiz_id).order_by("-clientquiz_end_time")[start:]
        serializer = ClientQuizSerializer(client_quiz, many=True)
        # print(serializer.data)
        return JsonResponse(serializer.data, safe=False)

    except ClientQuiz.DoesNotExist:
        # print("Not found")
        return JsonResponse({"unsuccessful": True})
    # quizzes = Quiz.objects.all()

@csrf_exempt
def get_all_client_quiz_count(request):
    host_id = json.loads(request.body)["host_id"]
    quiz_id = json.loads(request.body)["quiz_id"]
    
    total_quizzes = ClientQuiz.objects.filter(clientquiz_host_id=host_id, clientquiz_quiz_id=quiz_id).count()

    return JsonResponse({"total": total_quizzes})


@csrf_exempt
def get_client_quizzes(request):
    data = json.loads(request.body)
    start = data["start"]

    user = User.objects.get(user_uid = request.session.get("uid"))

    try:
        end = start+10
        total_quizzes = ClientQuiz.objects.filter(user=user).count()
        if end<total_quizzes:
            client_quiz = ClientQuiz.objects.filter(user=user).order_by("-clientquiz_end_time")[start:end]
        else:
            client_quiz = ClientQuiz.objects.filter(user=user).order_by("-clientquiz_end_time")[start:]
        serializer = ClientQuizSerializer(client_quiz, many=True)
        # print(serializer.data)
        return JsonResponse(serializer.data, safe=False)

    except ClientQuiz.DoesNotExist:
        # print("Not found")
        return JsonResponse({"unsuccessful": True})
    # quizzes = Quiz.objects.all()

def getClientQuizCount(request):
    user = User.objects.get(user_uid = request.session.get("uid"))
    total_quizzes = ClientQuiz.objects.filter(user=user).count()
    return JsonResponse({"total": total_quizzes})


def getQuizTitle(request):
    quiz_code = request.GET["quiz_code"]

    host_id = quiz_code.split(" ")[0]
    quiz_id = quiz_code.split(" ")[1]

    try:
        quiz = Quiz.objects.get(quiz_id=quiz_id, quiz_host_id=host_id)
        return JsonResponse({"quiz_title": quiz.quiz_title})

    except ClientQuiz.DoesNotExist:
        return JsonResponse({"unsuccessful": True})




@csrf_exempt
def submitQuiz(request):
    if request.method=="POST":
        data = json.loads(request.body)

        host_id = data["host_id"]
        quiz_id = data["quiz_id"]

        start_time = datetime.fromisoformat(data["quiz_start_time"])
        end_time = datetime.fromisoformat(data["quiz_end_time"])

        user_choices = data["user_choices"]

        time_taken = end_time - start_time

        user = User.objects.get(user_uid=request.session["uid"])

        # getting total questions
        host_quiz = Quiz.objects.get(quiz_host_id=host_id, quiz_id=quiz_id)
        total_questions = host_quiz.question_set.count()

        
        quiz = ClientQuiz.objects.create(user=user, clientquiz_quiz_id=quiz_id, clientquiz_host_id=host_id,
                                clientquiz_start_time=start_time,
                                clientquiz_end_time=end_time,
                                clientquiz_time_taken=time_taken,
                                clientquiz_total_questions=total_questions,
                                clientquiz_attempted_questions=0,
                                clientquiz_correct_answers=0)

        host_quiz = Quiz.objects.get(quiz_host_id=host_id, quiz_id=quiz_id)
        
        correct_answers = 0
        for question_id, choice_id in user_choices.items():
            question = quiz.clientquestion_set.create(clientquestion_question_id=question_id)
            
            host_question = host_quiz.question_set.get(question_id=question_id)
            host_correct_choice = host_question.choice_set.get(is_correct_choice=True).choice_id
            
            if choice_id == host_correct_choice:
                correct = True
                correct_answers += 1
            else:
                correct = False

            choice = question.clientchoice_set.create(clientchoice_choice_id=choice_id, is_correct_choice=correct)
        

        # getting attempted questions
        attempted_questions = quiz.clientquestion_set.count()

        # updating correct answers and attempted questions
        quiz.clientquiz_correct_answers = correct_answers
        quiz.clientquiz_attempted_questions = attempted_questions
        quiz.save()

        # updating number of users submitted the quiz
        host_quiz.quiz_no_of_users += 1
        host_quiz.save()

        # updating number of quizzes joined by user
        user.user_quizzes_joined += 1
        user.save()

        # print("Submitted")

    return JsonResponse({"message": "Quiz submitted successfully!"})

def getCurrentTime(request):
    return JsonResponse({"datetime": timezone.localtime().isoformat()})