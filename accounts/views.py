from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.utils.translation import ugettext_lazy


def login_page(request):

    if request.user.is_authenticated():
        return redirect('/')

    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    error = None
    if username and password:
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
            else:
                error = ugettext_lazy(u'Account is disabled')
        else:
            error = ugettext_lazy(u'Invalid login or password')

    return render(
        request,
        'pages/login/login.html',
        {
            'login_form': AuthenticationForm,
            'error': error,
        }
    )


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))
