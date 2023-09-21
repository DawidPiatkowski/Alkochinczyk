from django.shortcuts import render
from .models import Property

def board_view(request):
    properties = Property.objects.all()
    return render(request, "alkochinczyk/board_view.html", {'properties': properties})