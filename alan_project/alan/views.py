from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.query import QuerySet
from .models import *

def about(request):
    return render(request, 'alan/about.html', {})

def index(request):
    response = "Alan says hey there world!"
    return render(request, 'alan/index.html', {'response':response})