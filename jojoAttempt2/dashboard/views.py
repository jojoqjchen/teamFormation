from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User


# Create your views here.
@login_required
def user_profile(request):
    user = User.objects.get(username = request.user)
    return render(request, 'dashboard/user_profile.html', {'user':user, 'username': request.user})
