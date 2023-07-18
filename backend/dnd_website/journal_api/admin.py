from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

class CustomAccountAdmin(UserAdmin):
    search_fields = ('username',)
    readonly_fields = ['slug']
    list_display = ['username', 'email', 'date_joined', 'is_staff', 'is_active']
    fieldsets = [
        (
            None,
            {
                "fields": ["username", "email", "password"],
            },
        ),
        (
            "Advanced info",
            {
                "classes": ["collapse"],
                "fields": ['slug', "avatar"],
            },
        ),
    ]



class PostReactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'reaction_type', 'author', 'reacted_at', 'post', ]

class CommentReactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'reaction_type', 'author', 'reacted_at', 'comment', ]

class PostReactionsInline(admin.TabularInline):
    model = models.PostReaction
    extra = 1

class CommentReactionsInline(admin.TabularInline):
    model = models.CommentReaction
    extra = 1


class CommentInline(admin.TabularInline):
    model = models.Comment
    extra = 1

class PostAdmin(admin.ModelAdmin):
    inlines = (PostReactionsInline, CommentInline)
    list_display = ['id','author','created_datetime', 'is_publish', 'title', 'description', ]

class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    prepopulated_fields = {'slug': ('name',)}

class CommentAdmin(admin.ModelAdmin):
    inlines = (CommentReactionsInline,)
    list_display = ['id', 'text', 'author', 'parent', 'created_datetime']
    list_filter = ('author', 'created_datetime')
    search_fields = ('text', 'author__username')
    ordering = ('-created_datetime',)
    readonly_fields = ('created_datetime',)

class ReportReasonAdmin(admin.ModelAdmin):
    list_display = ['id', 'formulation']


admin.site.register(models.Account, CustomAccountAdmin)
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.ReportReason, ReportReasonAdmin)
admin.site.register(models.PostReaction, PostReactionAdmin)
admin.site.register(models.CommentReaction, CommentReactionAdmin)


