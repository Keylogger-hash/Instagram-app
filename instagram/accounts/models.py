from django.db import models
# from django.contrib.auth.models import BaseUserManager
# from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import PermissionsMixin
# from django.utils.translation import ugettext_lazy as _
#
#
# # Create your models here.
# class MyUserManager(BaseUserManager):
#
#     def _create_user(self,email,password,**extra_fields):
#         if not email:
#             raise ValueError('Email should be send')
#         email = self.normalize_email(email)
#         user = self.model(email,password,**extra_fields)
#         user.save()
#         return user
#
#     def create_superuser(self,email,password,**extra_fields):
#         extra_fields.setdefault('is_staff',True)
#         extra_fields.setdefault('is_active',True)
#         extra_fields.setdefault('is_superuser',True)
#
#         if extra_fields["is_staff"] is not True:
#             raise ValueError("Superuser must have is_staff=True")
#         if extra_fields["is_superuser"] is not True:
#             raise ValueError("Superuser must have is_superuser=True")
#
#         return self._create_user(email,password,**extra_fields)
#
#
# class User(AbstractUser,PermissionsMixin):
#     email = models.EmailField()
#     is_staff = models.BooleanField(
#         _('staff status'),
#         default=False,
#         help_text=_('Designates whether the user can log into this admin site.'),
#     )
#     is_active = models.BooleanField(
#         _('active'),
#         default=True,
#         help_text=_(
#             'Designates whether this user should be treated as active. '
#             'Unselect this instead of deleting accounts.'
#         ),
#     )
#     USERNAME_FIELD = 'email'
#     objects = MyUserManager()
#
#     def get_email(self):
#         return self.email
#
#     def get_full_name(self):
#         return self.email
#
#     def get_short_name(self):
#         return self.email
