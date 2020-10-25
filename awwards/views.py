
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.contrib.auth import authenticate, login
# from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserUpdateForm,ProfileUpdateForm
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
# from .token_generator import account_activation_token
def home(request):
    return render(request,"home.html")

# def login(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         return redirect(request,'/')
    
#     return render(request, '/registration/login.html')
        
@login_required
def logout(request):
    django_logout(request)
    return  HttpResponseRedirect('/')

@login_required
@csrf_protect
def profile(request):
    # images = Post.objects.all()
    # post = Post.objects.filter(author=request.user).order_by('-date_posted')
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        # 'images': images,
        # 'posts' : post
    }

    return render(request, 'profile/profile.html', context)