from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
import re
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
    return render(req,"home.html")