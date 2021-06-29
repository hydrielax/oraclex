from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def prediction(request):
    context = {}
    return render(request, 'predict/index.html', context)