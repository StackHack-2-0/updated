from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegisterForm, ProfileRegisterForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.forms import modelformset_factory
from django.db import IntegrityError, transaction
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from .models import *

def home(request):
    if request.user.is_authenticated:
        profile_instance = Profile.objects.get(user=request.user)
        if profile_instance.verified:
            return(render(request, "client/home.html", {}))
        else: 
            return redirect(reverse_lazy('client:preview'))
    else:
        return(render(request, "client/home.html", {}))
def menu(request):
    if request.user.is_authenticated:
        profile_instance = Profile.objects.get(user=request.user)
        if profile_instance.verified:
            return(render(request, "client/menu.html", {}))
        else: 
            return redirect(reverse_lazy('client:preview'))
    else:
        return(render(request, "client/menu.html", {}))

def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('client:home'))

def LoginPage(request):
    form = LoginForm(request.POST or None)
    context = {"form": form}
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect(reverse_lazy('client:home'))
        else:
            print("Error")
    return(render(request, "client/login.html", context))

def SignUpPage(request):
    if request.method  == 'POST':
        form = UserRegisterForm(request.POST or None)
        p_reg_form = ProfileRegisterForm(request.POST,request.FILES or None)
        # print(form)
        # print(p_reg_form)
        if form.is_valid() and p_reg_form.is_valid():
            user = form.save()
            user.refresh_from_db()
            p_reg_form_instance = p_reg_form.save(commit=False)
            p_reg_form_instance.user = user
            p_reg_form_instance.email = user.email
            # random = (int(p_reg_form_instance.mobile) * 25)%300 
            # p_reg_form_instance.registration_id = random
            p_reg_form_instance.save()

            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'],)
            login(request, user)
            return redirect(reverse_lazy('client:preview'))
        else:
            form = UserRegisterForm(request.POST,request.FILES or None)
            p_reg_form = ProfileRegisterForm(request.POST,request.FILES or None)
            context = {
                'form': form,
                'p_reg_form': p_reg_form,
            }
    else:
        form = UserRegisterForm()
        p_reg_form = ProfileRegisterForm()
        context = {
                'form': form,
                'p_reg_form': p_reg_form,
            }
    return render(request, 'client/register.html', context)

def profile(request):
    if request.user.is_authenticated:
        profile_instance = Profile.objects.get(user=request.user)
        if profile_instance.verified:
            form_instance = Profile.objects.get(user=request.user)
            context = { 'form' : form_instance}
            return render(request, 'client/profile.html', context)
        else: 
            return redirect(reverse_lazy('client:preview'))
    else:
        return redirect(reverse_lazy('client:home'))

def preview(request):
    form_instance = Profile.objects.get(user=request.user)
    context = { 'form' : form_instance}
    return render(request, 'client/preview.html', context)

def submit(request):
    if request.method  == 'POST':
        profile_instance = Profile.objects.get(user=request.user)
        profile_instance.verified = True
        random = (int(profile_instance.mobile) * 25)%300
        profile_instance.registration_id = random
        profile_instance.save()
        return redirect(reverse_lazy('client:profile'))

def update(request):
    if request.method  == 'POST':
        form_instance = Profile.objects.get(user=request.user)
        p_reg_form = ProfileRegisterForm(request.POST, request.FILES or None , instance=form_instance)
        if p_reg_form.is_valid():
            form_instance.save()
            return redirect(reverse_lazy('client:preview'))
        else:
            p_reg_form = ProfileRegisterForm(request.POST,request.FILES or None)
            context = {
                'form': p_reg_form,
            }
            return render(request, 'client/update.html', context)
    else:
        form_instance = Profile.objects.get(user=request.user)
        form = ProfileRegisterForm(instance=form_instance)
        context = { 'form' : form}
        return render(request, 'client/update.html', context)