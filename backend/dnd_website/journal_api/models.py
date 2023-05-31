from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.timezone import now


class Account(AbstractUser):
    email = models.EmailField(unique=True)
    slug = models.SlugField(max_length=150, db_index=True, blank=True, null=True)
    avatar = models.URLField(default='', blank=True)
    favorites_reaction = models.ManyToManyField('Reaction', related_name='favorites_reaction', blank=True)
    recent_reaction = models.ManyToManyField('Reaction', related_name='recent_reaction', blank = True)
    
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
    author = models.ForeignKey('Account', on_delete=models.SET_NULL, null=True )
    tags = models.ManyToManyField('Tag', blank=True)
    reactions = models.ManyToManyField('Reaction', through='PostReaction', blank=True)
    comments_count = models.IntegerField(default=0)
    commented = models.BooleanField(default=False)
    reacted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id} - {self.title}'

    def get_comments_count(self):
        return f'{self.comments.all().count()}'

    class Meta:
        ordering = ['-created_datetime']
        db_table = "Post"
        verbose_name = "Post"
        verbose_name_plural = "Post"

class Reaction(models.Model):
    reaction_name = models.CharField(max_length=250, unique=True)
    reaction_url = models.CharField(max_length=2048)
    reaction_category = models.ForeignKey('ReactionCategory', on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.id} - {self.reaction_name}'
    
    class Meta:
        db_table = "Reaction"
        verbose_name = "Reaction"
        verbose_name_plural = "Reaction"



class ReactionCategory(models.Model):
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.id} - {self.category_name}'
    
    class Meta:
        db_table = "Reaction_category"
        verbose_name = "Reaction_category"
        verbose_name_plural = "Reaction_category"

class PostReaction(models.Model):
    reaction = models.ForeignKey('Reaction', on_delete=models.CASCADE, )
    post = models.ForeignKey('Post', on_delete=models.CASCADE,)
    reacted_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('Account', on_delete=models.CASCADE, )

    def __str__(self):
        return f'{self.post}/{self.reaction}'
    
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


class AbstractComment(models.Model):
    # Abstract comment model
    status = models.CharField(max_length=5, choices=(('n','normal'), ('b','banned'), ('d','deleted')), default='n')
    comment_text = models.TextField()
    replies_count = models.IntegerField(default=0, blank=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    report_reasons = models.ManyToManyField('ReportReason', through="CommentReport", blank=True)
    #likes/dislikes

    def __str__(self):
        return f'{self.id} - {self.comment_text}'

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comment"
        abstract = True

class Comment(AbstractComment, MPTTModel):
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE,)
    author = models.ForeignKey('Account', on_delete=models.CASCADE, )
    parent = TreeForeignKey('self', related_name='children', blank=True, null=True, on_delete=models.SET_NULL)

    def get_childrens_comment_count(self):
        return f'{self.children.all().count()}'

    class Meta:
        ordering = ['-created_datetime'] #likes it's second param to ordering
        db_table = "Comment"
        verbose_name = "Comment"
        verbose_name_plural = "Comment"


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
    




