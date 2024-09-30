from django.shortcuts import render,redirect
from django.contrib import messages
from django.urls import reverse
from validate_email import validate_email
from .models import Profile
from .forms import LoginForm, SignUpForm, TasksForm
from django.core.mail import EmailMessage
from django.conf import settings
from .decorators import auth_user_should_not_access
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str,DjangoUnicodeDecodeError
from .utils import generate_token
import threading
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()

# Create your views here.
class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('Activation.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[user.email]
                         )

    if not settings.TESTING:
        EmailThread(email).start()

# @auth_user_should_not_access
def Login(request):
    form = SignUpForm()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user and not user.is_email_verified:
            messages.error(request, 'Email is not verified, please check your email inbox')
            return render(request, 'Login.html')

        if not user:
            messages.error(request, 'Invalid credentials, try again')
            return render(request, 'Login.html')

        login(request, user)

        return redirect(reverse('Dash'))

    return render(request, 'Login.html', {'form':form})

# @auth_user_should_not_access
def Register(request):
    form = SignUpForm()

    if request.method == "POST":
        context = {'has_error': False}
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if len(password1) < 6:
            messages.error(request, 'Password should be at least 6 characters for greater security')
            return redirect('Register')

        if password1 != password2:
            messages.error(request, 'Password Mismatch! Your Passwords Do Not Match')
            return redirect('Register')

        if not validate_email(email):
            messages.error(request, 'Password Mismatch! Your Passwords Do Not Match')
            return redirect('Register')

        if not username:
            messages.error(request, 'Username is required!')
            return redirect('Register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is taken! Choose another one')

            return render(request, 'Register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is taken! Choose another one')

            return render(request, 'Register.html')

        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email)
        user.set_password(password1)
        user.save()

        if not context['has_error']:
            send_activation_email(user, request)

            messages.success(request, 'Sign Up Successful! We sent you an email to verify your account')
            return redirect('Register')

    return render(request, 'Register.html', {'form':form})

def Logout(request):
    
    logout(request)
    messages.success(request, 'Successfully Logged Out!')

    return redirect(reverse('Login'))

def ActivateUser(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))

        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.success(request, 'Email Verified! You can now Log in')
        return redirect(reverse('Login'))

    return render(request, 'Activation Failed.html', {"user": user})



from django.shortcuts import render
from .models import Tasks, UserSubscription
def Dashboard(request):
    subscribed_courses = UserSubscription.objects.filter(user=request.user).select_related('module','transaction')
    user_favorites = request.session.get('user_favorites', [])
    
    context = {'subscribed_courses': subscribed_courses, 'user_favorites': user_favorites}
    return render(request, 'Dashboard.html', context)



def Dash(request):
    return render(request,'dash.html')

from .models import Tasks
def task_list(request):
    tasks=Tasks.objects.all()
    print(tasks)
    return render(request,'Tasks.html', {'tasks': tasks})


# def Tasks_status(request):
#     return render(request,'Tasks_status.html')


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Tasks

@login_required
def accept_task(request, task_id):
    task = get_object_or_404(Tasks, task_id=task_id)
    if task.is_available:
        task.is_available = False
        task.accepted_by = request.user  # Associate the task with the logged-in user
        task.save()
        return redirect('user_tasks')  # Redirect to user's tasks page after accepting
    else:
        return render(request, 'Tasks.html')  # Optional template if the task is no longer available

@login_required
def user_tasks(request):
    tasks = Tasks.objects.filter(accepted_by=request.user)
    return render(request, 'user_tasks.html', {'tasks': tasks})


from django.db.models import Count

def home(request):
    
    
    return render(request, 'index.html')



def adv(request):
   
      
     return render(request,'advanced.html')


