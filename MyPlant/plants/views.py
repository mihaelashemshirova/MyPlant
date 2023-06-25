from django.shortcuts import render, redirect
from MyPlant.plants.forms import PlantCreateForm, ProfileCreateForm, PlantEditForm, PlantDeleteForm, ProfileDeleteForm, \
    ProfileEditForm
from .models import Plant
from .templatetags.custom_tags import get_profile


def index(request):
    return render(request, 'common/home-page.html')


def catalogue(request):
    plants = Plant.objects.all()

    context = {
        'plants': plants,
    }
    return render(request, 'common/catalogue.html', context)


def profile_create(request):
    form = ProfileCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('catalogue')

    context = {
        'form': form,
    }
    return render(request, 'profile/create-profile.html', context)


def profile_details(request):
    plants = Plant.objects.all()
    context = {
        'plants': plants
    }
    return render(request, 'profile/profile-details.html', context)


def profile_edit(request):
    profile = get_profile()

    if request.method == 'GET':
        form = ProfileEditForm(instance=profile)
    else:
        form = ProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile-details')

    context = {
        'profile': profile,
        'form': form
    }
    return render(request, 'profile/edit-profile.html', context)


def profile_delete(request):
    profile = get_profile()
    plant = Plant.objects.all()

    if request.method == 'POST':
        form = ProfileDeleteForm(request.POST, instance=profile)
        form.save()
        for i in plant:
            plant_form = PlantDeleteForm(request.POST, instance=i)
            plant_form.save()

        return redirect('index')

    context = {
        'profile': profile
    }

    return render(request, 'profile/delete-profile.html', context)


def plant_create(request):
    form = PlantCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('catalogue')
    context = {
        'form': form,
    }
    return render(request, 'plants/create-plant.html', context)


def plant_details(request, pk):
    plant = Plant.objects.filter(pk=pk).get()
    context = {
        'plant': plant
    }
    return render(request, 'plants/plant-details.html', context)


def plant_edit(request, pk):
    plant = Plant.objects.filter(pk=pk).get()
    form = PlantEditForm(request.POST or None, instance=plant)
    if form.is_valid():
        form.save()
        return redirect('catalogue')

    context = {
        'form': form,
        'plant': plant
    }
    return render(request, 'plants/edit-plant.html', context)


def plant_delete(request, pk):
    plant = Plant.objects.filter(pk=pk).get()
    form = PlantDeleteForm(request.POST or None, instance=plant)
    if form.is_valid():
        form.save()
        return redirect('catalogue')
    context = {
        'form': form,
        'plant': plant
    }
    return render(request, 'plants/delete-plant.html', context)
