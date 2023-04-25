from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import Profile

def index(request):

    context = {}

    return render(request, 'index.html', context)

def signup(request):

    context = {}

    if request.method == "POST":
        # After submitting the form in signup.html, there are
        # several fields with unique names that store user's inputs.
        # I'm using here these fields' names to get these inputs
        # and use them to create new user.
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:

            # Check if username or email has been taken.
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Taken")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Taken")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username,
                                                email=email,
                                                password=password)
                user.save()

                # log user in and redirect to settings page

                # create a Profile object for the user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('signup')

        else:
            messages.info(request, "Passwords Not Matching")
            return redirect('signup')

    else:
        return render(request, 'signup.html', context)

def signin(request):
    