from django.contrib import messages
from django.shortcuts import render

def bake_view(request):

    messages.success(request, "Baked successfully.")

    return render(request, "bake.html")