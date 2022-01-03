from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, ProfileRegisterForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from event.models import Event, Car, Candidate
from django.contrib.auth.models import User


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Uwierzytelnienie zakończyło się powodzeniem.")
                else:
                    return HttpResponse('Konto jest zablokowane.')
            else:
                return HttpResponse('Nieprawidłowe dane uwierzytelniające.')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    candidate = Candidate.objects.filter(user_id=request.user.id)[:1]
    events = Event.objects.all()
    cars = Car.objects.all()
    price = 0
    car_exist = 0
    carid = 0
    lenregevent = 0
    lendecevent = 0

    if candidate:
        if candidate.get().type == candidate.get().types[0][0]:
            price = 39
        else:
            price = 149
    for car in cars:
        if car.owner.id == request.user.id:
            car_exist = 1
            carid = car.id
        if request.user in car.reserved.all():
            car_exist = 2
            carid = car.id
    return render(request, 'account/dashboard.html', {'section': 'dashboard',
                                                      'events': events,
                                                      'cars': cars,
                                                      'car_exist': car_exist,
                                                      'carid': carid,
                                                      'lenregevent': lenregevent,
                                                      'lendecevent': lendecevent,
                                                      'price': price})


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileRegisterForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_profile = profile_form.save(commit=False)
            new_profile = Profile.objects.create(user=new_user,
                                                 phone_number=new_profile.phone_number,
                                                 city=new_profile.city,
                                                 gender=new_profile.gender)
            new_profile.save()
            return render(request, 'account/register_done.html', {'new_user': new_user, 'new_profile': new_profile})
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileRegisterForm()
        return render(request, 'account/register.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def edit(request):
    if request.method =='POST':
        user_form = UserEditForm(instance=request.user.profile, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def profile(request, id):
    user = User.objects.get(id=id)
    return render(request, 'account/profile.html', {'user': user})


@login_required
def notifications(request, id):
    user = User.objects.get(id=id)
    return render(request, 'account/show_notifications.html', {'user': user})
