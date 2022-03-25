from django import forms
from django.contrib.auth.models import User
from collab_app.models import UserProfile, Forum, University, Category, Page, Comment, Like


class CommentForm(forms.ModelForm):
    body = forms.CharField(max_length=Comment.NAME_MAX_LENGTH, help_text="Reply...")

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Comment
        fields = ('body',)


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    #  text entry for users
    title = forms.CharField(max_length=Page.TITLE_MAX_LENGTH, help_text="Please enter the title of the page.")
    image = forms.ImageField() # [HOT-FIX: removed args] upload_to='image', blank=True, help_text="Upload a picture."
    text = forms.CharField(max_length=Page.TEXT_MAX_LENGTH, help_text="Type in here.")

    class Meta:
        model = Page
        exclude = ('category', 'user')

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # If url is not empty and doesn't start with 'http://', # then prepend 'http://'.
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url

        return cleaned_data


class UniversityForm(forms.ModelForm):
    name = forms.CharField(max_length=University.NAME_MAX_LENGTH)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = University
        fields = ('name',)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(widget=forms.EmailInput())
    biography = forms.CharField(widget=forms.TextInput())

    class Meta:
        model = User
        fields = ('username', 'password',)

    pass


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture', 'biography','email',)
