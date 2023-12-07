from django.urls import path, include
from . import views

app_name = "client"
urlpatterns = [
    path("", view=views.index, name="index"),
    path("join/<str:host_id>/<int:quiz_id>", view=views.join, name="join"),
    path("get_quiz/", view=views.get_quiz, name="get_quiz"),
    path("result/<str:host_id>/<int:quiz_id>", view=views.result, name="result"),
    path("result_info/<str:host_id>/<int:quiz_id>", view=views.result_info, name="result_info"),
    
    path("submitQuiz/", views.submitQuiz, name="submitQuiz"),
    path("getCurrentTime/", views.getCurrentTime, name="getCurrentTime"),

    path("get_client_quiz/", views.get_client_quiz, name="get_client_quiz"),
    path("get_all_client_quiz/", views.get_all_client_quiz, name="get_all_client_quiz"),
    path("get_client_quizzes/", views.get_client_quizzes, name="get_client_quizzes"),
    path("getQuizTitle/", views.getQuizTitle, name="getQuizTitle"),
    
    path("getClientQuizCount/", views.getClientQuizCount, name="getClientQuizCount"),
    
    path("get_all_client_quiz_count/", views.get_all_client_quiz_count, name="get_all_client_quiz_count"),
]