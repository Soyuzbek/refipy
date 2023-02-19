from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser):
    email = models.EmailField(
        _('email'),
        unique=True,
        error_messages={
            'unique': _('A user with that email already exists.'),
        },
    )
    referer = models.ForeignKey('User', models.SET_NULL, 'referee_set', null=True, blank=True)
    referral_code = models.PositiveBigIntegerField(_('referral code'), null=True, blank=True)
    score = models.PositiveSmallIntegerField(_('score'), default=0)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Email this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
