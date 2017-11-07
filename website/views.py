from django.shortcuts import redirect

def login_redirect(request):
    if request.user.is_authenticated():
        return redirect('/home/most_liked')
    return redirect("/account/login")
