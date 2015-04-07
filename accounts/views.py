from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.shortcuts import redirect, render
from django.utils import translation
from django.utils.translation import ugettext_lazy
from accounts.models import MovielistUser
from common.models import Country


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
            'error': error,
        }
    )


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


class MovielistUserForm(ModelForm):
    class Meta:
        model = MovielistUser
        fields = ['country', 'gender', 'date_of_birth', 'email']

    def clean_gender(self):
        try:
            return bool(int(self.data['gender']))
        except (ValueError, TypeError):
            return None


@login_required
def settings_personal(request):
    saved = False
    form = None
    if request.method == 'POST':
        form = MovielistUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            saved = True

    cur_language = translation.get_language()
    sort_field = 'name_ru' if cur_language == 'ru' else 'name_en'
    countries = Country.objects.all().order_by(sort_field).values_list('id', sort_field)
    return render(
        request,
        'pages/settings/settings_personal.html',
        {
            'countries': countries,
            'GENDER_MALE': MovielistUser.GENDER_MALE,
            'GENDER_FEMALE': MovielistUser.GENDER_FEMALE,
            'saved': saved,
            'form': form,
        }
    )


@login_required
def change_password(request):
    saved = False
    form = None
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            saved = True
    return render(
        request,
        'pages/settings/password_change.html',
        {
            'saved': saved,
            'form': form,
        }
    )
