from django.shortcuts import render, redirect
from .models import Contact

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def services(request):
    return render(request, "services.html")

def contact(request):
    if request.method == "POST":
        Contact.objects.create(
            name=request.POST["name"],
            email=request.POST["email"],
            message=request.POST["message"]
        )
        return redirect("contact")
    return render(request, "contact.html")