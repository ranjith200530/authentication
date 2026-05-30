from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
import re

from . import models
# Create your views here.

def logoutpage(request):

    logout(request)

    return redirect("loginpage")

def loginpage(req):
    if req.user.is_authenticated:
        return redirect("home")
    if req.method=="POST":
        username=req.POST.get("username")
        password=req.POST.get("password")
        
        user=authenticate(req,
                          username=username,
                          password=password)
        if user:
            login(req,user)
            return redirect("home")
        else:
            return render(req,"index.html",{"error":"invalid username or password"})
    return render(req,"index.html")

def registerpage(req):
    if req.method=="POST":
        username=req.POST.get("username")
        password=req.POST.get("password")
        password2=req.POST.get("repassword")
        
        if username=="":
            return render(req,"registerpage.html",{"error":"Please enter username"})
        if len(password)<6:
            return render(req,"registerpage.html",{"error":"Password must br greater than 6 characters"})
        if password!=password2:
            return render(req,"registerpage.html",{"error":"Please enter password correct"})
        # checking whether a user with the username exits or not
        if User.objects.filter(username=username).exists():
            return render(req,"registerpage.html",{"error":"user alreadt exists"})
          # USER EXISTS CHECK
        if User.objects.filter(username=username).exists():

            return render(req, "registerpage.html", {
                "error": "User already exists"
            })

        # UPPERCASE CHECK
        if not re.search(r"[A-Z]", password):

            return render(req, "registerpage.html", {
                "error": "Password must contain uppercase letter"
            })

        # LOWERCASE CHECK
        if not re.search(r"[a-z]", password):

            return render(req, "registerpage.html", {
                "error": "Password must contain lowercase letter"
            })

        # NUMBER CHECK
        if not re.search(r"[0-9]", password):

            return render(req, "registerpage.html", {
                "error": "Password must contain a number"
            })

        # SPECIAL CHARACTER CHECK
        if not re.search(r"[@#$%^&*!]", password):

            return render(req, "registerpage.html", {
                "error": "Password must contain special character"
            })

            
        user = User.objects.create_user(
            username=username,
            password=password
        )
        login(req,user)
        return redirect("home")
    return render(req,"registerpage.html")



def home(req):
    if req.user.groups.filter(name="Admin").exists():
        task=models.Todo.objects.all()
        name="Admin"
        

    elif req.user.groups.filter(name="Manager").exists():
        task=models.Todo.objects.all()
        name="Manager"

    elif req.user.groups.filter(name="users").exists():
        name="Normal user"
        task=models.Todo.objects.filter(user=req.user)
    return render(req,"home.html",{"task":task,"name":name,  "is_admin": req.user.groups.filter(name="Admin").exists(),})








def edit(req,id):
    task = get_object_or_404(models.Todo, id=id)
    if req.method=="POST":
        new_title=req.POST.get('title')
        task.title=new_title
        task.save()
        return redirect("home")
    return render(req,"edit.html",{'task':task})

def delete(req,id):
    task = get_object_or_404(models.Todo, id=id)
    task.delete()
    return redirect("home")

def add(req):
    if req.method=="POST":
        title=req.POST.get("title")
        models.Todo.objects.create(title=title,user=req.user)
        
        return redirect("home")
