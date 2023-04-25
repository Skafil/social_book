from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Profile

@login_required(login_url='signin')
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
                user_login = authenticate(username=username, password=password)
                login(request, user_login)


                # create a Profile object for the user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')

        else:
            messages.info(request, "Passwords Not Matching")
            return redirect('signup')

    else:
        return render(request, 'signup.html', context)

def signin(request):


    context = {}

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Credentials Invalid")
            return redirect('signin')

    return render(request, 'signin.html', context)

@login_required(login_url='signin')
def logouts(request):
    logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def settings(request):
    print("Request user: ", request.user)
    user_profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        bio = request.POST['bio']
        location = request.POST['location']
        
        # We need yet to add enctype in form because of file
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
        else:
            image = request.FILES.get('image')

        user_profile.profileimg = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()

        return redirect('settings')
    
    context = {
        'user_profile': user_profile,
    }

    return render(request, 'setting.html', context)