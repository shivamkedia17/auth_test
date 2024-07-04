from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from example.forms import FileForm

# Create your views here.

@login_required
def profile(request):
    return render(request, 'profile.html', {
        'download_form': FileForm(),
        'delete_form': FileForm(),
    })

def homepage(request):
    return profile(request)