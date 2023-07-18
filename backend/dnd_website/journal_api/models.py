from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db.models.signals import *


class Account(AbstractUser):
    email = models.EmailField(unique=True)
    slug = models.SlugField(max_length=150, db_index=True, blank=True, null=True)
    avatar = models.URLField(default='', blank=True)
    confirmation_code = models.CharField(max_length=6, null=True, blank=True)

    class Meta:
        db_table = "Account"
        verbose_name = "Account"
        verbose_name_plural = "Account"

    def __str__(self):
        return f'{self.username}'
    
    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)

class Post(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    description = models.CharField(max_length=500, blank=True)
    body = models.TextField(blank=True)
    thumbnail = models.URLField(blank=True, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    is_publish = models.BooleanField(default=True)
    publish_datetime = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey('Account', null=True, on_delete=models.SET_DEFAULT, default="user doesn't exist")
    tags = models.ManyToManyField('Tag', blank=True)
    commented = models.BooleanField(default=False)
    reacted = models.BooleanField(default=False)
    num_comments = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return f'{self.id} - {self.title}'

    class Meta:
        ordering = ['-created_datetime']
        db_table = "Post"
        verbose_name = "Post"
        verbose_name_plural = "Post"


class PostReaction(models.Model):
    REACTION_CHOICES = (('like', 'Like'),('dislike', 'Dislike'))
    reaction_type = models.CharField(max_length=10, null=True, choices = REACTION_CHOICES)  #like or dislike
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post_reactions')
    reacted_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('Account', on_delete=models.SET_DEFAULT, default="user doesn't exist")

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
    reaction_type = models.CharField(max_length=10, null=True, choices = REACTION_CHOICES)  #like or dislike
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='comment_reactions')
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
    




