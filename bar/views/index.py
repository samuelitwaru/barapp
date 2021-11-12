from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms import LoginForm


@login_required
def index(request):
    return redirect('bar:create_orders')

def login_view(request):
    _next = request.GET.get("next", "bar:create_orders")
    if request.method == "POST":
        form = LoginForm(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)

        if user:
            login(request, user)
            return redirect(_next)
        else:
            messages.error(request, f"User not found!", extra_tags="danger")
            return redirect("bar:login")
    else:
        if get_user(request).is_authenticated:
            return redirect('bar:create_orders')

        form = LoginForm()
        context = {"form": form}
        return render(request, 'index/login.html', context)


def forgot_password(request):
    forgot_password_form = ForgotPasswordForm()
    if request.method == "POST":
        forgot_password_form = ForgotPasswordForm(request.POST)
        if forgot_password_form.is_valid():
            cleaned_data = forgot_password_form.cleaned_data
            user = cleaned_data.get("email")
            # set auth token
            set_user_token(user)
            # send email
            send_auth_mail(user.username)
            # send_auth_mail.delay(user.email)
            messages.info(request, f"An email with password reset instructions has been sent to '{user.username}'. Login to your this email to continue.")
            return redirect("bar:create_orders")

    context = {"forgot_password_form": forgot_password_form}
    return render(request, "auth/forgot-password.html", context) 



def logout_view(request):
    logout(request)
    return redirect('bar:login')