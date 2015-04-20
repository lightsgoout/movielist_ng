from django import forms
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
import re
from django.utils.translation import ugettext_lazy
from imports import tasks
from imports.models import ImportListJob


class KinopoiskImportForm(forms.Form):
    kinopoisk_id = forms.CharField(max_length=64)

    def clean_kinopoisk_id(self):
        kinopoisk_id = self.cleaned_data['kinopoisk_id']
        result = re.match('http://www.kinopoisk.ru/user/(\d+)/', kinopoisk_id)
        if not result:
            raise forms.ValidationError(ugettext_lazy('Invalid url'))
        return result.group(1)


@login_required
def import_kinopoisk(request):
    form = None
    try:
        current_job = ImportListJob.objects.filter(
            user=request.user, finished=False
        ).latest('id')
    except ImportListJob.DoesNotExist:
        current_job = None

        if request.method == 'POST':
            form = KinopoiskImportForm(request.POST)
            if form.is_valid():
                kinopoisk_id = form.cleaned_data['kinopoisk_id']
                current_job = ImportListJob.objects.create(
                    user=request.user,
                    kinopoisk_id=kinopoisk_id,
                )
                tasks.kinopoisk_import_list.delay(request.user.id, kinopoisk_id)
                return redirect(reverse('import_kinopoisk'))

    return render(
        request,
        'pages/settings/import_kinopoisk.html',
        {
            'form': form,
            'current_job': current_job,
        }
    )
