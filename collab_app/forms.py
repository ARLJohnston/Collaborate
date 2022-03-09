from django import forms
from collab_app.models import UserProfile, Forum, University, Category, Page, Comment, Like

class CommentForm(forms.ModelForm):
    pass

class PostForm(forms.ModelForm):
    pass

class CategoryForm(forms.ModelForm):
    pass

class UniversityForm(forms.ModelForm):
    pass

class UserForm(forms.ModelForm):
    pass

class UserProfileForm(forms.ModelForm):
    pass