from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username


class Forum(models.Model):  # General or universities
    NAME_MAX_LENGTH = 10
    # A forum name does not need to be unique
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=False, null=False)

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Forum, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class University(models.Model):
    NAME_MAX_LENGTH = 50
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)

    # One to one relationship with university
    forum = models.OneToOneField(Forum, on_delete=models.CASCADE)

    # Many-to-many relationship with user
    user = models.ManyToManyField(UserProfile)

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(University, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'universities'

    def __str__(self): return self.name


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

    def __str__(self): return self.name


class Page(models.Model):
    # ID attribute is automatically added by django
    # one-to-many relationship with category
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # one-to-many relationship with user
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    title = models.CharField(max_length=40)
    image = models.ImageField(upload_to='image', blank=True)
    text = models.CharField(max_length=500)

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Page, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    NAME_MAX_LENGTH = 300
    body = models.CharField(max_length=NAME_MAX_LENGTH)
    pinned = models.BooleanField(blank=True)

    # one-to-many relationship with user
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=False)
    # one-to-many relationship with post
    post = models.ForeignKey(Page, on_delete=models.CASCADE, null=False)

    def __str__(self): return self.body


class Like(models.Model):
    NAME_MAX_LENGTH = 128
    number = models.IntegerField(default=0)
    # one-to-many relationship with comment
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)

    # one-to-many relationship with post
    post = models.ForeignKey(Page, on_delete=models.CASCADE, null=True)

    # One-to-one relationship with user
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return "Number of likes %d" % self.number
