from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Need, Action


@login_required
def index(request):
    needs = Need.objects.filter(user=request.user)
    return render(request, 'needs/index.html', {'needs': needs})


@csrf_exempt
@login_required
def add_need(request):
    if request.method == 'POST':
        name = request.POST['need-name']
        negative_need = (request.POST['need-type'] == 'negative')
        decay_time_value = request.POST['decay-time-value']
        decay_time_unit = request.POST['decay-time-unit']

        decay_time = float(decay_time_value) * int(decay_time_unit)

        new_need = Need(
            user=request.user,
            name=name,
            max_level=decay_time,
            current_level=decay_time,
            negative_need=negative_need
        )
        new_need.save()

    return HttpResponseRedirect(reverse('index'))


@csrf_exempt
@login_required
def add_action(request):
    if request.method == 'POST':
        name = request.POST['action-name']
        related_need = get_object_or_404(Need, id=request.POST['related-need'])
        need_impact = int(request.POST['need-impact'])

        new_action = Action(
            name=name,
            value=need_impact,
            related_need=related_need
        )
        new_action.save()

    return HttpResponseRedirect(reverse('index'))


@csrf_exempt
@login_required
def delete_need(request, need_id):
    need = get_object_or_404(Need, id=need_id)

    if request.method == 'POST':
        need.delete()
        return JsonResponse({'message': 'Need deleted successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)


@login_required
def enact_action(request, action_id):
    action = get_object_or_404(Action, id=action_id)
    need = action.related_need

    if need.negative_need:
        updated_level = need.max_level * \
            ((need.get_level() - action.value) / 100)
    else:
        updated_level = need.max_level * \
            ((need.get_level() + action.value) / 100)

    need.current_level = updated_level
    need.save()

    return HttpResponseRedirect(reverse('index'))


def login_view(request):
    if request.method == 'POST':

        # Attempt to sign user in
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'needs/login.html', {
                'message': 'Invalid username and/or password.',
            })
    else:
        return render(request, 'needs/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']

        # Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'needs/register.html', {
                'message': 'Passwords must match.',
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
            })

        # Validate unique email
        if User.objects.filter(email=email).exists():
            return render(request, 'needs/register.html', {
                'message': 'Email already in use.',
                'first_name': first_name,
                'last_name': last_name,
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                email, password, first_name=first_name, last_name=last_name)
        except IntegrityError:
            return render(request, 'needs/register.html', {
                'message': 'An error occurred. Please try again later.',
            })

        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'needs/register.html')
