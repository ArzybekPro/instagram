from django.db import models
from apps.users.models import User
# Create your models here.
class Post(models.Model):
    title=models.CharField(
        max_length=20
    )
    description=models.CharField(
        max_length=290,
    )
    image=models.ImageField(
        upload_to='post_image/',
    )
    user=models.ForeignKey(
        User,
        related_name='user_name',
        on_delete=models.CASCADE
    )
    created=models.DateTimeField(
        auto_now_add=True
    )
    
    def __str__(self):
        return f'Заголовок:{self.title}, Описание:{self.description}'
    
    class Meta:
        verbose_name='пост'
        verbose_name_plural='посты'
    

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        related_name='comment_post',
        on_delete=models.CASCADE
    )
    user=models.ForeignKey(
        User, 
        related_name='comment_user',
        on_delete=models.CASCADE
        )
    text=models.CharField(
        max_length=200
    )
    created=models.DateTimeField(
        auto_now_add=True
    )
    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = 'Коментс'
        verbose_name_plural = 'Коменты'
    
    
    
class Like(models.Model):
    user=models.ForeignKey(
        User,
        related_name='like_post',
        on_delete=models.CASCADE
        )
    post = models.ForeignKey(
        Post,
        related_name='post_like',
        on_delete=models.CASCADE
        )
    
class LikeComment(models.Model):
    comment = models.ForeignKey(
        Comment, 
        related_name='like_comment',
        on_delete=models.CASCADE,
        )
    user = models.ForeignKey(
        User,
        related_name='like_comment_user',
        on_delete=models.CASCADE,
        )
    
class Chat(models.Model):
    from_user=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='from_user',
        verbose_name='Чат пользователя'
        )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='to_user',
        verbose_name='Чат к пользователя',
        )

    class Meta:
        verbose_name="Чат"
        verbose_name_plural="Чаты"

class Message(models.Model):
    chat=models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='message_chat',
        verbose_name='ID чата'
    )
    from_user=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chat_from_user',
        verbose_name="Сообщение от пользователя",
        )
    message=models.CharField(
        max_length=200,
        verbose_name='Сообщение'
    )
    created_at=models.TimeField(
        auto_now_add=True
    )
    def __str__(self):
        return f"{self.chat}"
    
    class Meta:
        verbose_name= "Сообщение в чате",
        verbose_name_plural= "Сообщение в чатах"
