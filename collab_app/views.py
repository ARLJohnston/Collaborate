from ast import For
from sre_parse import CATEGORIES
from unicodedata import category
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse, resolve
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User

from collab_app.forms import FindUniversity, UserForm, UserProfileForm, UniversityForm, PageForm, CategoryForm, CommentForm
from collab_app.models import ForumCategoryAssociation, UserProfile, University, Category, Page, Comment, Forum

def styling_function(request, add_to_recent, context_dict):

    if(add_to_recent):
        context_dict["page"] = "collab_app:" + resolve(request.path_info).url_name
        recent = request.COOKIES.get("recent")
        if(recent):
            context_dict["recent"] = recent.split(",")

    try:
        username = request.user.username
        user_data = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user_data)
        context_dict["profile_picture"] =  user_profile.picture
    except: #User does not exist
        pass

def index(request):
    """Takes url request, returns Http response."""
    context_dict = {}

    styling_function(request, True, context_dict)

    return render(request, 'collab_app/index.html', context=context_dict)

def about(request):
    """Takes url request, returns about page"""
    context_dict = {}
    styling_function(request, True, context_dict)

    return render(request, 'collab_app/about.html', context=context_dict)

def contact_us(request):
    """Takes url request, returns contact-us page"""
    context_dict = {}
    styling_function(request, True, context_dict)

    return render(request, 'collab_app/contact_us.html', context=context_dict)

def sign_up(request):
    """Takes url request, returns sign-up page"""

    is_registered = False
    
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # If the two forms are valid...
        if user_form.is_valid()  and  profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()

            is_registered = True
            print("HERHEHRHEHRHERH")
                    
            return redirect(reverse('collab_app:login'))

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    #context_dict = {'user_form': user_form,'university_form' : university_form, 'profile_form': profile_form,  'registered': is_registered}
    context_dict = {'user_form': user_form, 'profile_form': profile_form,  'registered': is_registered}

    styling_function(request, True, context_dict)

    return render(request, 'collab_app/sign_up.html', context=context_dict)

def login_view(request):
    """Takes url request, returns login page"""
    # If the request is a HTTP POST, try to pull out the relevant information.
    context_dict = {}
    styling_function(request, True, context_dict)

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password) # Checks if valid password.
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
        # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return redirect(reverse('collab_app:index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Collaborate account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    
    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
    # No context variables to pass to the template system, hence the
    # blank dictionary object...
        return render(request, 'collab_app/login.html', context_dict)

def logout_view(request):
    """Takes URL request, returns logout page."""
    if request.method == 'POST':
        logout(request)
        return redirect('collab_app:index')
    return render(request, 'collab_app/logout.html')

def my_account_redirect(request):
    """Takes url request, redirects to slug account"""
    if not request.user.is_authenticated:
        return HttpResponse("User not authenticated.")

    else:
        username = request.user.username
        return redirect(f'/my_account/{username}')

@login_required
def my_account(request): 
    """Takes url request, returns my-account page"""

    if not request.user.is_authenticated:
        return HttpResponse("User not authenticated.")
    username = request.user.username
    
    user_data = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user_data)
    user_form = UserForm(instance=user_data)
    user_profile_form = UserProfileForm(instance=user_profile)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        user_profile_form = UserProfileForm(request.POST, instance=user_profile)

        if user_profile_form.is_valid() and user_form.is_valid():
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()
            profile = user_profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
            #put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            # Now we save the UserProfile model instance.
            
            
            profile.save()

            context_dict= {'user_form': user_form,'user_profile_form': user_profile_form, }
            
            styling_function(request, True, context_dict)

        #return render(request, 'collab_app/my_account.html', context=context_dict)
        return redirect('/collab_app/')
        


    else:
        context_dict = {'user_form': user_form,'user_profile_form': user_profile_form}
        
        styling_function(request, True, context_dict)

        return render(request, 'collab_app/my_account.html', context=context_dict)

def general(request):
    """Takes url request, returns general page"""
    context_dict = {}
    
    bad_category_slugs = [cat.category.slug for cat in ForumCategoryAssociation.objects.all()]
    category_list = Category.objects.order_by('name').exclude(slug__in=bad_category_slugs)

    context_dict["categories"] = category_list

    styling_function(request, True, context_dict)

    return render(request, 'collab_app/general.html', context=context_dict)
    
@login_required
def universities(request):
    """Takes url request, returns universities page"""
    context_dict = {}
    try:
        username = request.user.username
        user_data = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user_data)
        user_university = University.objects.get(user=user_profile)

        universities = University.objects.all()
        universities = University.objects.all().filter(user = user_profile)
        context_dict['universities'] = universities
    except: #No associated universities
        context_dict['universities'] = None

    context_dict['form'] = FindUniversity()

    if request.method == 'POST':
        form = FindUniversity(request.POST)
        if form.is_valid():
            add_uni = University.objects.filter(name__icontains=form.cleaned_data['universities'])
            context_dict['universities'] = add_uni
            context_dict['form'] = form

    styling_function(request, True, context_dict)

    return render(request, 'collab_app/universities.html', context=context_dict)

def show_university(request, university_name_slug):
    """Takes url request, returns a specific university page"""
    context_dict = {}
    
    try:
        university = University.objects.get(slug=university_name_slug)
        context_dict['university'] = university
        categories = ForumCategoryAssociation.objects.filter(forum=university.forum)
        categories = [cat.category for cat in categories]
        context_dict['categories'] = categories

    except Category.DoesNotExist:
        context_dict['university'] = None
        context_dict['categories'] = None


    print("[show_university]:=", context_dict)
    styling_function(request, False, context_dict)
    return render(request, 'collab_app/show_university.html', context=context_dict)

def add_university(request):
    """Takes url request, returns the creation page for new universities"""
    
    context_dict = {}

    if not request.user.is_authenticated:
        return HttpResponse("User not authenticated.")

    form = UniversityForm()
    
    if request.method == 'POST':# A HTTP POST?
        form = UniversityForm(request.POST)
        
        if form.is_valid():
            new_uni = form.save(commit=False)
            new_uni.name = form.cleaned_data['name']
            new_uni.forum = Forum.objects.get_or_create(name=form.cleaned_data['name'])[0]
            new_uni.save()
            return redirect('/collab_app/')
        else:
            print(form.errors)
    styling_function(request, True, context_dict)
    return render(request, 'collab_app/add_university.html', {'form':form})

def show_general_category(request, category_name_slug):
    """Takes url request, returns a specific university page"""

    context_dict = {}
    
    try:
        category = Category.objects.get(slug=category_name_slug) # Get the category with the correct name.
        pages = Page.objects.filter(category=category) # Get all the associated pages for the specified category.
        # Add the pages and category to the context dictionary.
        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        # Assign empties to the context dict.
        context_dict['category'] = None
        context_dict['pages'] = None

    print("[SHOW_GENERAL_CATEGORY] :=", context_dict)
    styling_function(request, False, context_dict)

    return render(request, 'collab_app/show_category.html', context=context_dict)

def show_university_category(request, university_name_slug, category_name_slug):
    """Takes url request, returns a specific university page"""

    context_dict = {}
    
    try:
        university = University.objects.get(slug=university_name_slug)
        categories = ForumCategoryAssociation.objects.filter(forum=university.forum)
        category = [cat.category for cat in categories if cat.category.slug == category_name_slug][0]
        #category = Category.objects.get(slug=category_name_slug) # Get the category with the correct name.
        pages = Page.objects.filter(category=category) # Get all the associated pages for the specified category.
        # Add the pages and category to the context dictionary.
        context_dict['pages'] = pages
        context_dict['category'] = category
        context_dict['university'] = university

    except Category.DoesNotExist:
        # Assign empties to the context dict.
        context_dict['category'] = None
        context_dict['pages'] = None
        context_dict['university'] = None

    styling_function(request, False, context_dict)

    return render(request, 'collab_app/show_category.html', context=context_dict)

def add_general_category(request):
    """Takes url request, returns the creation page for new categories"""

    context_dict = {}

    if not request.user.is_authenticated:
        return HttpResponse("User not authenticated.")

    current_url = resolve(request.path_info).url_name
    
    form = CategoryForm()

    if request.method == 'POST': # A HTTP POST?
        form = CategoryForm(request.POST)
        forum = Forum.objects.get_or_create(name="general", slug="general")
        
        if form.is_valid():
            new_cat = form.save(commit=False)
            new_cat.forum = forum[0]
            new_cat.save()
            return redirect('/collab_app/')

        else:
            print(form.errors)
            
    styling_function(request, True, context_dict)
    return render(request, 'collab_app/add_category.html', {'form': form, 'current_url': current_url})

def add_university_category(request, university_name_slug):
    """Takes url request, returns the creation page for new categories"""

    context_dict = {}

    if not request.user.is_authenticated:
        return HttpResponse("User not authenticated.")

    try:
        university = University.objects.get(slug=university_name_slug)
        form = CategoryForm(request.POST)
        context_dict['form'] = form

    except University.DoesNotExist:
        return redirect('collab_app:index')

    if request.method == 'POST': # A HTTP POST?
        form = CategoryForm(request.POST)
        forum = university.forum
        
        if form.is_valid():
            try:
                 Category.objects.get(name=form.cleaned_data['name'])
                 isNew = False
            except Category.DoesNotExist:
                isNew = True

            if isNew:
                new_cat = form.save(commit=False)
                new_cat.name = form.cleaned_data['name']
                new_cat.forum = forum
                new_cat.save()
                ForumCategoryAssociation.objects.get_or_create(category=new_cat, forum=forum)     
            return redirect(reverse('collab_app:index'))

        else:
            print(form.errors)
    
    styling_function(request, True, context_dict)
    return render(request, 'collab_app/add_category.html', context_dict)

class like_page_view(View):
    @method_decorator(login_required)
    def get(self, request):
        page_id = request.GET['page_id']

        try:
            page = Page.objects.get(id=int(page_id))
        except Page.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        page.likes = page.likes + 1
        page.save()

        return HttpResponse(page.likes)

class like_comment_view(View):
    @method_decorator(login_required)
    def get(self, request):
        comment_id = request.GET['comment_id']

        try:
            comment = Comment.objects.get(id=int(comment_id))
        except Comment.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        comment.likes = comment.likes + 1
        comment.save()

        return HttpResponse(comment.likes)


def show_general_page(request, category_name_slug, page_name_slug):
    """Takes URL request, category slug, page slug, returns general page."""
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        print("CATEGORY:",category)
        page = Page.objects.filter(slug=page_name_slug)[0]
        print("PAGES:",page)
        comments = Comment.objects.filter(post=page)
        print("COMMENT:",comments)

        context_dict['page'] = page
        context_dict['category'] = category
        context_dict['comments'] = comments

    except:
        context_dict['page'] = None
        context_dict['category'] = None
        context_dict['comments'] = None

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentForm(request.POST, initial={'pinned': False, 'post':page})

            if form.is_valid():
                if page:
                    comment = form.save(commit=False)
                    comment.post = page
                    comment.pinned = False
                    comment.save()
            context_dict['form'] = form

    styling_function(request, False, context_dict)
    return render(request, 'collab_app/show_page.html', context_dict)


def show_university_page(request, university_name_slug, category_name_slug, page_name_slug):
    """Takes URL request, university slug, category slug, page slug, returns university page."""

    try:
        context_dict = {}
        university = University.objects.get(slug=university_name_slug)
        print(university)
        category = Category.objects.get(slug=category_name_slug)
        print(category)
        page = Page.objects.get(slug=page_name_slug)
        print(page)

        context_dict["university"] = university
        context_dict["category"] = category
        context_dict["page"] = page

    except:
        context_dict["university"] = None
        context_dict["category"] = None
        context_dict["page"] = None

        # Needs if not user.is_authenticated()
    if request.method == 'POST':
        form = CommentForm(request.POST, initial={'pinned': False, 'post':page})

        if form.is_valid():
            if page:
                comment = form.save(commit=False)
                comment.post = page
                comment.pinned = False
                comment.save()

        context_dict['form'] = form

    styling_function(request, False, context_dict)
    return render(request, 'collab_app/show_page.html', context_dict)

     
def add_general_page(request, category_name_slug):
    """Takes url request, returns the creation page for new pages"""

    if not request.user.is_authenticated:
        return HttpResponse("User not authenticated.")

    try:
        category = Category.objects.get(slug=category_name_slug)
        user_data = User.objects.get(username=request.user.username)
        user_profile = UserProfile.objects.get(user=user_data)

    except Category.DoesNotExist:
        category = None
        return redirect('/collab_app/')
    
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():

            if category:
                page = form.save(commit=False)
                page.category = category
                page.user = user_profile
                page.save()
                return redirect(reverse('collab_app:show_general_category', kwargs={'category_name_slug': category_name_slug}))
            
        else:
            print(form.errors)
    
    context_dict = {'form': form, 'category': category}

    styling_function(request, True, context_dict)
    return render(request, 'collab_app/add_page.html', context=context_dict)

def add_university_page(request, university_name_slug, category_name_slug):
    pass


def add_comment(request, page_name_slug):

    try: #Get page that the comment is for
        page = Page.objects.get(slug=page_name_slug)

    except Page.DoesNotExist:
        page = None

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            if page:
                comment = form.save(commit=False)
                comment.page = page
                comment.save()
                return redirect(reverse('collab_app:show_page', kwargs={'page_name_slug': page_name_slug}))
        else:
            print(form.errors)
    context_dict = {'form': form, 'page':page}
    
    styling_function(request, True, context_dict)
    return render(request, 'collab_app/add_comment.html', context=context_dict)


def search_bar(request):

    context_dict = {}
    if request.method == 'GET':
        search = request.GET.get('search')
        print("[SEARCH QUERY]:", search)

        if search == "":
            return redirect(reverse('collab_app:index'))

        pages = Page.objects.all().filter(title__contains=search)
        print("[PAGES FOUND]:", pages)
        styling_function(request, False, context_dict)
        return render(request, 'collab_app/search_result.html', {'pages':pages})
    
