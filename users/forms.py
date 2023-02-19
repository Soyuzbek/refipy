import random

from django import forms
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _


class ApplicationForm(forms.Form):
    email = forms.EmailField(label=_('email'))
    referral_code = forms.IntegerField(
        label=_('referral code'),
        min_value=100_000,
        max_value=999_999,
        required=False,
    )

    def save(self):
        confirmation_code = random.randint(100_000, 999_999)
        cache.set(
            key=f'confirm_{self.cleaned_data["email"]}',
            value={
                'confirmation_code': confirmation_code,
                'referral_code': self.cleaned_data.get('referral_code'),
            },
            timeout=60 * 2,
        )


class ConfirmationForm(forms.Form):
    email = forms.EmailField(label=_('email'))
    confirmation_code = forms.IntegerField(
        label=_('confirmation code'),
        min_value=100_000,
        max_value=999_999,
    )

    def clean(self):
        email = self.cleaned_data['email']
        confirmation_code = self.cleaned_data['confirmation_code']
        if not cache.get(f'confirm_{email}'):
            self.add_error('email', _('Email could not found or confirmation code is expired'))
        else:
            if cache.get(f'confirm_{email}')['confirmation_code'] != confirmation_code:
                self.add_error('confirmation_code', _("Didn't match!"))

        return self.cleaned_data

    def save(self):
        return
