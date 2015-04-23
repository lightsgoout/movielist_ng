from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.urlresolvers import reverse
from django import forms
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


class RegistrationForm(forms.Form):
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=30, required=True)
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)

    def clean_email(self):
        email = self.cleaned_data['email']
        if MovielistUser.objects.filter(email=email).exists():
            raise forms.ValidationError(ugettext_lazy(u'Email already exists'))

        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if MovielistUser.objects.filter(username=username).exists():
            raise forms.ValidationError(ugettext_lazy(u'Username already exists'))

        return username

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        if cleaned_data['password1'] != cleaned_data['password2']:
            raise forms.ValidationError(ugettext_lazy(u'Passwords do not match'))

        return cleaned_data


def register(request):

    if request.user.is_authenticated():
        return redirect('/')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            MovielistUser.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
            )
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            return redirect(user.get_absolute_url())
        else:
            return render(
                request,
                'registration/registration_form.html',
                {
                    'form': form,
                }
            )
    return render(
        request,
        'registration/registration_form.html'
    )


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


class MovielistUserForm(forms.ModelForm):
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
