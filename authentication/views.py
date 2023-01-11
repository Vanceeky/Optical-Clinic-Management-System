from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm

from django.contrib.auth.models import Group

from .decorators import allowed_users, unauthenticated_user, admin_only
from django.contrib.auth.decorators import login_required

from authentication.token import account_activation_token 
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from django.core.mail import EmailMessage  
from django.contrib.auth import get_user_model

# Create your views here.


@unauthenticated_user
def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    context = {
        "form": form, 
        "msg": msg
    }
    return render(request, "authentication/login.html", context)

@unauthenticated_user
def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # default to non-active
            user.is_active = False
            user.save()
    


            #customer = Group.objects.get_or_create(name='user')
            #customer[0].user_set.add(user)

             # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('authentication/acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()
          
            #return HttpResponse('Please confirm your email address to complete the registration') 
            msg = 'User created - please <a href="/login">login</a>.'
            #return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    context = {
        "form": form, 
        "msg": msg, 
        "success": success
    }

    return render(request, "authentication/register.html", context)


def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        customer = Group.objects.get_or_create(name='user')
        customer[0].user_set.add(user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!')  


