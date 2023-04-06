from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from . import models
from mptt.admin import MPTTModelAdmin

class AccountInline(admin.StackedInline):
    verbose_name_plural = 'Account'
    model = models.Account
    can_delete = False

class CustomizeUserAdmin (UserAdmin):
    inlines = [AccountInline, ]

class PostReactionAdmin(admin.ModelAdmin):
    list_display = ['reaction', 'post', 'author']

class PostAdmin(admin.ModelAdmin):
    list_display = ['id','author','created_at', 'title', 'description', ]

class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class CommentAdmin(MPTTModelAdmin):
    mptt_level_indent = 15

class ReportReasonAdmin(admin.ModelAdmin):
    list_display = ['id', 'formulation']

class ReactionCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name']

class ReactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'reaction_name', 'reaction_category', 'reaction_url']


admin.site.unregister(User)
admin.site.register(User, CustomizeUserAdmin)
admin.site.register(models.Account)

admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.ReportReason, ReportReasonAdmin)
admin.site.register(models.ReactionCategory, ReactionCategoryAdmin)
admin.site.register(models.Reaction, ReactionAdmin)
admin.site.register(models.PostReaction, PostReactionAdmin)
