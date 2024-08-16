import json
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from myapp.models import Task , Contact
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import TokenGenerator,generate_token
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.views.generic import View



# Create your views here.




# sign up 
def signup(request):
    if request.method=="POST":
        email=request.POST['email']
        username=request.POST["name"]
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password!=confirm_password:
            messages.warning(request,"Password is Not Matching")
            return render(request,'signup.html')                   
        try:
            if User.objects.get(username=email):
                # return HttpResponse("email already exist")
                messages.info(request,"Email is Taken")
                return render(request,'signup.html')
        except Exception as identifier:
            pass
        user = User.objects.create_user(username,email,password)
        user.is_active=True
        user.save()
        return redirect('/login')
    return render(request,"signup.html")


# sign in
def handlelogin(request):
    if request.method=="POST":

        username=request.POST['username']
        userpassword=request.POST['pass']
        myuser=authenticate(username=username,password=userpassword)

        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Success")
            return redirect('/home')

        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/login')

    return render(request,'login.html')  

# logout
def handlelogout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('/')



def index(request):
    return render(request, "index.html")

@login_required(login_url='/login')
def home(request):
    task = Task.objects.filter(user=request.user).all()
    return render(request,"index.html", {'task':task})
    

@login_required(login_url='/login')
def addTask(request):
    if request.method == 'POST':
        print(request.POST.get('title'))
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')

        # Create a Task and associate it with the current user
        task = Task.objects.create(
            title=title, 
            description=description, 
            due_date=due_date, 
            user=request.user
        )
        task.save()

        return redirect('/home')

    return render(request, 'addtask.html')

@login_required(login_url='/login')
def editTask(request, task_id):
    task = get_object_or_404(Task, task_id=task_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        
        
        task.title = title;
        task.description = description;
        task.due_date = due_date;
        task.complete = 'complete' in request.POST
        task.save()
        return redirect('/home')
    else:
        return render(request, 'edittask.html', {'task': task})
    
@login_required(login_url='/login')
def completeTask(request, task_id):
    task = Task.objects.get(pk=task_id)
    task.complete = True
    task.save()
    return redirect('/home')    

def calender(request) :
    return render(request, 'calender.html')

def about(request) :
    return render(request, "aboutus.html")


def contact(request) :
    if(request.method == 'POST') :
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        contact = Contact.objects.create(
            name = name,
            email = email,
            message = message,
            user = request.user,
        )
        contact.save()
        messages.success(request, "Your query has been submitted. We'll reach out to you soon!")
        
        return redirect('/home')
    
    return render(request, 'contactus.html')

class RequestResetEmailView(View):
    def get(self,request):
        return render(request,'request-reset-email.html')
    
    def post(self,request):
        email=request.POST['email']
        user=User.objects.filter(email=email)

        if user.exists():
            # current_site=get_current_site(request)
            email_subject='[Reset Your Password]'
            message=render_to_string('reset-user-password.html',{
                'domain':'127.0.0.1:8000',
                'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token':PasswordResetTokenGenerator().make_token(user[0])
            })

            email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
            email_message.send()

            # messages.info(request,f"WE HAVE SENT YOU AN EMAIL WITH INSTRUCTIONS ON HOW TO RESET THE PASSWORD {message} " )
            return render(request,'request-reset-email.html')
        else:
            messages.error(request, "No user exists with the provided email.")
            return render(request,'request-reset-email.html')

class SetNewPasswordView(View):
    def get(self,request,uidb64,token):
        context = {
            'uidb64':uidb64,
            'token':token
        }
        try:
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)

            if  not PasswordResetTokenGenerator().check_token(user,token):
                messages.warning(request,"Password Reset Link is Invalid")
                return render(request,'request-reset-email.html')

        except DjangoUnicodeDecodeError as identifier:
            messages.error(request,"Invalid link.")
            return render(request,'request-reset-email.html')

        return render(request,'set-new-password.html',context)

    def post(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password!=confirm_password:
            messages.warning(request,"Password is Not Matching")
            return render(request,'set-new-password.html',context)
        
        try:
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,"Password Reset Success Please Login with NewPassword")
            return redirect('/login/')

        except DjangoUnicodeDecodeError as identifier:
            messages.error(request,"Something Went Wrong")
            return render(request,'set-new-password.html',context)

