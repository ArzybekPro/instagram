from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    profile_image=models.FileField(
        upload_to='profile_image/',
        blank=True,
        null=True,
    )
    full_name=models.CharField(
        max_length=100
    )
    description=models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    phone_number=models.CharField(
        max_length=20,
        blank=True,
        null=True,
        
    )
    GENDERS=(
        ('women','women'),
        ('men','men'),
        ('another','another')
    )
    gender = models.CharField(
        choices=GENDERS,
        default='another',
        max_length=20,
        blank=True,
        null=True
        
    )
    relationship=models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    occupation=models.CharField(
        max_length=60,
        blank=True,
        null=True
    )
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name='пользователь'
        verbose_name_plural='пользователи'


class Followers(models.Model):
    to_user = models.ForeignKey(
        User,
        related_name="followers",
        on_delete=models.CASCADE
        )
    from_user = models.ForeignKey(
        User,
        related_name="followings",
        on_delete=models.CASCADE
        )