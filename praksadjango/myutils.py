from django.shortcuts import redirect
from django.urls import reverse

def redirect_with_next(request, fallback_url_name):
    next_url = request.GET.get('next')
    print(next_url)
    if next_url:
        return redirect(next_url)
    return redirect("/registration")
