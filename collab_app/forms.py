from django import forms
from collab_app.models import UserProfile, Forum, University, Category, Page, Comment, Like

class CommentForm(forms.ModelForm):
    class Meta:
        # Provide an association between the ModelForm and a model

        model = Comment
        fields = ('body',)
    pass

class PostForm(forms.ModelForm):
    pass

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    forum = forms.ForeignKey(Forum, on_delete=models.CASCADE)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

     # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)
    pass

class UniversityForm(forms.ModelForm):
    class Meta:
        # Provide an association between the ModelForm and a model
        model = University
        fields = ('name',)

    pass

class UserForm(forms.ModelForm):
    BIO_MAX_LENGTH = 500
    EMAIL_MAX_LENGTH = 254
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    password = forms.CharField(widget=forms.PasswordInput())
    picture = models.ImageField(upload_to='profile_images', blank=True)
    biography = models.CharField(max_length=BIO_MAX_LENGTH, unique=False, null=True)
    email = models.EmailField(max_length=EMAIL_MAX_LENGTH, unique=True, null=False)

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password','picture','biography')
    pass

# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ('picture','biography',)
#     pass