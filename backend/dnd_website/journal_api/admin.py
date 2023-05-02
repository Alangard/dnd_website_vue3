from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from mptt.admin import MPTTModelAdmin

class CustomAccountAdmin(UserAdmin):
    search_fields = ('username',)
    readonly_fields = ['slug']
    list_display = ['username', 'email', 'date_joined', 'is_staff']
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
                "fields": ['slug', "avatar", "favorites_reaction", "recent_reaction"],
            },
        ),
    ]



class PostReactionAdmin(admin.ModelAdmin):
    list_display = ['reaction', 'post', 'author']

class PostReactionsInline(admin.TabularInline):
    model = models.PostReaction
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

class CommentAdmin(MPTTModelAdmin):
    mptt_level_indent = 15

class ReportReasonAdmin(admin.ModelAdmin):
    list_display = ['id', 'formulation']

class ReactionCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name']

class ReactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'reaction_name', 'reaction_category', 'reaction_url']




admin.site.register(models.Account, CustomAccountAdmin)
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.ReportReason, ReportReasonAdmin)
admin.site.register(models.ReactionCategory, ReactionCategoryAdmin)
admin.site.register(models.Reaction, ReactionAdmin)
admin.site.register(models.PostReaction, PostReactionAdmin)

