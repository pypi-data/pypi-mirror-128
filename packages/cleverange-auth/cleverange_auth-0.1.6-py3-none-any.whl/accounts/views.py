from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from accounts.forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from accounts.models import SaveDomain
from django.contrib.auth import get_user_model
User = get_user_model()

from django.conf import settings

class RegisterTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        # save the domain name from the request
        SaveDomain.objects.get_or_create(domain=str(request.get_host()))
        # let check the current user is authenticated or not
        if request.user.is_authenticated:
            return redirect('/')
        else:
            form = RegisterForm()
            context = {
                'form': form
            }
            return render(request, 'account/register-new.html', context)
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_PATH)
        else:
            form = RegisterForm()
            if request.method == 'post' or request.method == 'POST':
                form = RegisterForm(request.POST)
                if form.is_valid():
                    try:
                        user = form.save()
                        get_user_verification_obj = user.verification
                        acc_code = get_user_verification_obj.account_code
                        return redirect(reverse('accounts:verify', kwargs={'account_code': acc_code}))
                    except:
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            context = {'form': form}
            return render(request, 'account/register-new.html', context)


def account_verification(request, account_code):
    try:
        if request.user.is_authenticated:
            return redirect('accounts:register')
        else:
            if account_code:
                get_user = User.objects.get(verification__account_code=account_code)
                get_code = get_user.verification.verify_code
                if request.method == 'post' or request.method == 'POST':
                    check_code = request.POST.get('code')
                    if get_code == check_code:
                        get_user.is_active = True
                        get_user.is_verify = True
                        get_user.save()
                        return redirect('accounts:login')
                    else:
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

                context = {}
                return render(request, 'account/verification-new.html', context)
            else:
                return redirect('accounts:register')
    except:
        return render(request, 'account/verification-new.html')



class LoginTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_PATH)
        else:
            return render(request, 'account/login-new.html')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_PATH)
        else:
            if request.method == 'post' or request.method == 'POST':
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect(settings.LOGIN_REDIRECT_PATH)
            return render(request, 'account/login-new.html')



