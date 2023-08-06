from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import random

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from django.conf import settings


class CustomManager(BaseUserManager):
    def create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('email address is required')
        
        if not username:
            raise ValueError('user must have an username')
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(make_password(password))
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must be have is_staff True")

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must be have is_superuser True")

        if extra_fields.get('is_active') is not True:
            raise ValueError("Superuser must be have is_active True")
        
        if extra_fields.get('is_admin') is not True:
            raise ValueError("Superuser must be have is_admin True")
        
        user = self.create_user(email, username, password, **extra_fields)

        return user

    


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE = (
        ("visitor", "visitor"),
        ("developer", "developer"),
    )
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'
    user_type = models.CharField(max_length=100, choices=USER_TYPE, default=USER_TYPE[0])
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_verify = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = CustomManager()

    def __str__(self) -> str:
        return str(self.email)


class Verification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='verification')
    account_code = models.CharField(max_length=20, blank=True, null=True)
    verify_code = models.CharField(max_length=10)

    def __str__(self):
        return str(self.user.email)
    
    @receiver(post_save, sender=User)
    def create_verification(sender, instance, created, **kwargs):
        if created:
            current_user = Verification.objects.create(user=instance)

            # sending email 
            ac_code = ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(4)])
            current_user.account_code = ac_code
            # send  email
            user_email = current_user.user.email
            get_username = current_user.user.username
            # end split
            code_num = ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
            # save random number to database
            current_user.verify_code = code_num
            # end saving
            subject = "Verify your email address"
            # html_message = render_to_string('accounts/email.html')
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user_email]
            # send_mail( subject, html_message, email_from, recipient_list )
            sitename = SaveDomain.objects.all().order_by('-id').first()
            context = ({
                'username': get_username,
                'code': code_num,
                'domain': sitename.get_domain()
            })
            text_content = render_to_string('account/email.txt', context)
            html_content = render_to_string('account/email.html', context)
            email = EmailMultiAlternatives(subject=subject, body=text_content, from_email=email_from, to=recipient_list, reply_to=[email_from,])
            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=False)
            # end here

    @receiver(post_save, sender=User)
    def save_verification(sender, instance, **kwargs):
        instance.verification.save()
        



    

class SaveDomain(models.Model):
    domain = models.CharField(max_length=255)

    def get_domain(self, *args, **kwargs):
        if self.domain:
            return self.domain
        else:
            return None