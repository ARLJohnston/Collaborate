from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse


class UserProfile(models.Model):
    BIO_MAX_LENGTH = 500
    EMAIL_MAX_LENGTH = 254
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    biography = models.CharField(max_length=BIO_MAX_LENGTH, unique=False, null=True)
    # This includes email validation
    email = models.EmailField(max_length=EMAIL_MAX_LENGTH, unique=True, null=False)


    def __str__(self):
        return self.user.username


class Forum(models.Model):  # General or universities
    NAME_MAX_LENGTH = 10
    # A forum name does not need to be unique
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=False, null=False, primary_key=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Forum, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class University(models.Model):
    NAME_MAX_LENGTH = 50
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True, primary_key=True)

    # One to one relationship with university
    #forum = models.OneToOneField(Forum, on_delete=models.CASCADE)

    # Many-to-many relationship with user
    user = models.ManyToManyField(UserProfile)

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(University, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'universities'

    def __str__(self):
        return self.name


class Category(models.Model):
    NAME_MAX_LENGTH = 10
    # A category name does not need to be unique
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=False, null=False)
    # Gets foreign key from Forum
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class ForumCategoryAssociation(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Page(models.Model):
    TEXT_MAX_LENGTH = 500
    TITLE_MAX_LENGTH = 40
    # ID attribute is automatically added by django
    # one-to-many relationship with category
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # one-to-many relationship with user
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    image = models.ImageField(upload_to='image', blank=True)
    text = models.CharField(max_length=TEXT_MAX_LENGTH)

    slug = models.SlugField(unique=True, null=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Page, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('page_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    NAME_MAX_LENGTH = 300
    body = models.CharField(max_length=NAME_MAX_LENGTH)
    pinned = models.BooleanField(blank=True)

    # one-to-many relationship with user
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=False)
    # one-to-many relationship with post
    post = models.ForeignKey(Page, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.body


class Like(models.Model):
    # one-to-many relationship with comment
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)

    # one-to-many relationship with post
    post = models.ForeignKey(Page, on_delete=models.CASCADE, null=True)

    # One-to-many relationship with user
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)