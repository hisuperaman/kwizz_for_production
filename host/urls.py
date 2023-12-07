from django.urls import path
from . import views

app_name = "host"
urlpatterns = [
    path("", views.index, name="index"),
    path("new_quiz/", views.new_quiz, name="new_quiz"),

    path("responses/<str:host_id>/<int:quiz_id>/", views.responses, name="responses"),
    path("preview/<str:host_id>/<int:quiz_id>/", views.preview, name="preview"),
    
    path("result_info/<str:host_id>/<int:quiz_id>/<str:client_id>/", views.result_info, name="result_info"),

    path("socket.io/", views.socketio_view, name="socket"),
    path("start_quiz/", views.start_quiz, name="start_quiz"),
    path("leave/", views.leave, name="leave"),
    path("getTimerValue/", views.getTimerValue, name="getTimerValue"),
    path("clearQuizSession/", views.clearQuizSession, name="clearQuizSession"),
    path("submitQuiz/", views.submitQuiz, name="submitQuiz"),

    path("getJoinedUsers/", views.getJoinedUsers, name="getJoinedUsers"),
    path("getPassedUsers/", views.getPassedUsers, name="getPassedUsers"),

    path("getUserData/", views.getUserData, name="getUserData"),

    path("getPreviouslyHeldQuizzes/", views.getPreviouslyHeldQuizzes, name="getPreviouslyHeldQuizzes"),
    path("getToBeHeldQuizzes/", views.getToBeHeldQuizzes, name="getToBeHeldQuizzes"),

    path("getToBeHeldQuizCount/", views.getToBeHeldQuizCount, name="getToBeHeldQuizCount"),
    path("getPreviouslyHeldQuizCount/", views.getPreviouslyHeldQuizCount, name="getPreviouslyHeldQuizCount"),

    path("deleteQuiz/", views.deleteQuiz, name="deleteQuiz"),
    path("editQuiz/", views.editQuiz, name="editQuiz"),

    path("changeQuizVisibility/", views.changeQuizVisibility, name="changeQuizVisibility"),
]