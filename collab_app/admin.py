from django.contrib import admin
from .models import UserProfile, Forum, University, Category, Page, ForumCategoryAssociation, Comment

class UserProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'email')

class ForumAdmin(admin.ModelAdmin):
    fields = ('name',)

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Forum, ForumAdmin)
admin.site.register(University)
admin.site.register(Category)
admin.site.register(Page)
admin.site.register(ForumCategoryAssociation)
admin.site.register(Comment)