from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render

def bake():
    return True

def bake_view(request):
    if request.method == "POST":
        if bake():
            messages.success(request, "Baked successfully.")
        else:
            messages.error(request, "Baked failed.")
        
        return redirect("bake_view")
    
    return render(request, "bake.html")