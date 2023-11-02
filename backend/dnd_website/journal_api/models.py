from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db.models.signals import *
from tinymce.models import HTMLField


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    # def create_user(self, username, email=None, password=None, **extra_fields):
    #     extra_fields.setdefault('is_staff', False)
    #     extra_fields.setdefault('is_superuser', False)
    #     return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(username, email, password, **extra_fields)

class Account(AbstractUser):
    email = models.EmailField(unique=True)
    slug = models.SlugField(max_length=150, db_index=True, blank=True, null=True)
    avatar = models.ImageField(upload_to='images/user_avatars/%Y/%m/%d/', blank=True)
    confirmation_code = models.CharField(max_length=6, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email",]


    class Meta:
        db_table = "Account"
        verbose_name = "Account"
        verbose_name_plural = "Account"

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    

    def __str__(self):
        return f'{self.id} - {self.username}'


class Notification(models.Model):
    NOTIFICATION_TYPE = (('post_reaction', 'post_reaction'),
                         ('post_comment', 'post_comment'),
                         ('comment_reply', 'comment_reply'),
                         ('comment_reaction', 'comment_reaction'),
                         ('subscribe', 'subscribe'))
    
    created_datetime = models.DateTimeField(auto_now_add=True)
    seen_datetime = models.DateTimeField(blank=True, null=True)
    seen = models.BooleanField(default=False)
    notification_type= models.CharField(max_length=50, choices = NOTIFICATION_TYPE)
    receiver = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='notifications')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, blank=True, related_name='post_notifications')
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, blank=True, related_name='comment_notifications')
    post_reaction = models.ForeignKey('PostReaction', on_delete=models.CASCADE, null=True, blank=True, related_name='post_reaction_notifications')
    comment_reaction = models.ForeignKey('CommentReaction', on_delete=models.CASCADE, null=True, blank=True, related_name='comment_reaction_notifications')
    subscription = models.ForeignKey('Subscription', on_delete=models.CASCADE, null=True, blank=True, related_name='subscription_notifications')

    class Meta:
        ordering = ['-created_datetime']
        db_table = "Notification"
        verbose_name = "Notification"
        verbose_name_plural = "Notification"

    def __str__(self):
        return f'{self.id} - {self.notification_type} to {self.receiver.username}'

     

class Subscription(models.Model):
    subscription_reciever = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='account_subscription_reciever')
    subscriber = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='account_subscriber')
    subscription_datetime = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "Subscription"
        verbose_name = "Subscription"
        verbose_name_plural = "Subscription"
    
    def __str__(self):  
        return f'Subscription_reciever @{self.subscription_reciever.username} - subscriber @{self.subscriber.username}'
        

class Post(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    description = models.CharField(max_length=500)
    body = HTMLField()
    thumbnail = models.ImageField(upload_to='images/post_thumbnail/%Y/%m/%d/', blank=True, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    is_draft = models.BooleanField(default=False)
    is_publish = models.BooleanField(blank=True, default=True)
    publish_datetime = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey('Account', null=True, on_delete=models.SET_DEFAULT, default="user doesn't exist")
    tags = models.ManyToManyField('Tag', blank=True)
    commented = models.BooleanField(default=False)
    reacted = models.BooleanField(default=False)
    num_comments = models.IntegerField(default=0, blank=True)
    allow_comments = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.id} - {self.title}'

    class Meta:
        ordering = ['-created_datetime']
        db_table = "Post"
        verbose_name = "Post"
        verbose_name_plural = "Post"

class PostReaction(models.Model):
    REACTION_CHOICES = (('like', 'Like'),('dislike', 'Dislike'))
    reaction_type = models.CharField(max_length=10, blank=True, null=True, choices = REACTION_CHOICES)  #like or dislike
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post_reactions', null=True, blank=True)
    reacted_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('Account', on_delete=models.SET_DEFAULT, default=None)

    def __str__(self):
        return f'{self.post}/{self.reaction_type}'
    
    class Meta:
        db_table = "Post_reaction"
        verbose_name = "Post_reaction"
        verbose_name_plural = "Post_reaction"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=75, unique=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.name}'
    
    def get_absolute_url(self):
        return f'/{self.slug}/'

    class Meta:
        db_table = "Tag"
        verbose_name = "Tag"
        verbose_name_plural = "Tag"


class Comment(models.Model):
    status = models.CharField(max_length=5, choices=(('n','normal'), ('b','banned'), ('d','deleted')), default='n')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')    
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='replies', blank=True)
    author = models.ForeignKey('Account', on_delete=models.SET_DEFAULT, default="user doesn't exist")    
    text = models.TextField(blank=True)
    created_datetime = models.DateTimeField(auto_now_add=True)    
    updated_datetime = models.DateTimeField(auto_now=True)
    report_reasons = models.ManyToManyField('ReportReason', through="CommentReport", blank=True)
    replies_count = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return f'{self.id} - {self.text}'
    
    class Meta:
        db_table = "Comment"
        verbose_name = "Comment"
        verbose_name_plural = "Comment"
        ordering = ['-created_datetime'] #likes it's second param to ordering

class CommentReaction(models.Model):
    REACTION_CHOICES = (('like', 'Like'),('dislike', 'Dislike'))
    reaction_type = models.CharField(max_length=10, blank=True, null=True, choices = REACTION_CHOICES)  #like or dislike
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='comment_reactions', null=True, blank=True)
    reacted_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('Account', on_delete=models.SET_DEFAULT, default="user doesn't exist")

    def __str__(self):
        return f'{self.comment}/{self.reaction_type}'
    
    class Meta:
        db_table = "Comment_reaction"
        verbose_name = "Comment_reaction"
        verbose_name_plural = "Comment_reaction"

class ReportReason(models.Model):
    formulation = models.CharField(max_length=250, unique=True)
    
    def __str__(self):
        return f'{self.id} -{self.formulation}'
    
    class Meta:
        db_table = "Report_reason"
        verbose_name = "Report_reason"
        verbose_name_plural = "Report_reasons"

class CommentReport(models.Model):
    report_comment_formulation = models.TextField()
    report_reason = models.ForeignKey('ReportReason', on_delete=models.CASCADE, )
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, )

    def __str__(self):
        return f'{self.comment}/{self.report_reason}'
    
    class Meta:
        db_table = "Comment_report"
        verbose_name = "Comment_report"
        verbose_name_plural = "Comment_report"
    




