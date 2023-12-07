from login.models import User

def base_context(request):
    if request.session.get('uid'):
        user_info = User.objects.get(user_uid=request.session.get("uid"))
            
        context = {
            "user_uid": user_info.user_uid,
            "user_name": user_info.user_name,
            "user_username": user_info.user_username,
            "user_email": user_info.user_email,
            "user_pfp": user_info.user_pfp,

            "user_quizzes_hosted": user_info.user_quizzes_hosted,
            "user_quizzes_joined": user_info.user_quizzes_joined
        }
        
        return context

    return {"context": "nothing"}