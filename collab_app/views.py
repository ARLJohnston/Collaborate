from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User

from collab_app.forms import UserForm, UserProfileForm, UniversityForm, PageForm, CategoryForm
from collab_app.models import UserProfile, University, Category, Page

def index(request):
    """Takes url request, returns Http response."""
    context_dict = {}
    return render(request, 'collab_app/index.html', context=context_dict)

def about(request):
    """Takes url request, returns about page"""
    context_dict = {}
    return render(request, 'collab_app/about.html', context=context_dict)

def contact_us(request):
    """Takes url request, returns contact-us page"""
    context_dict = {}
    return render(request, 'collab_app/contact_us.html', context=context_dict)

def sign_up(request):
    """Takes url request, returns sing-up page"""

    is_registered = False
    
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(request.POST)
        university_form = UniversityForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # If the two forms are valid...
        if user_form.is_valid()  and university_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
            university = university_form.save(commit=False)
            university.user = user
            
            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
            #put it in the UserProfile model.
            if 'picture' in request.FILES:
                user.picture = request.FILES['picture']
            
            # Now we save the UserProfile model instance.
            user.save()
            university.save()
            profile.save()

            # Update our variable to indicate that the template
            # registration was successful.
            is_registered = True

        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)

    else:

        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()
        university_form = UniversityForm()

    context_dict = {'user_form': user_form,'university_form' : university_form, 'registered': is_registered}

    return render(request, 'collab_app/sign_up.html', context=context_dict)

def login(request):
    """Takes url request, returns login page"""
    # If the request is a HTTP POST, try to pull out the relevant information.
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
        return render(request, 'collab_app/login.html')

@login_required
def my_account(request): 
    """Takes url request, returns my-account page"""

    if not request.user.is_authenticated:
        return HttpResponse("User not authenticated.")
    
    username = request.user.username
    user_profile = UserProfile.objects.get(email=username)
    user_data = User.objects.get(username=username)
    user_form = UserForm(instance=user_data)
    user_profile_form = UserProfileForm(instance=user_profile)

    if request.method == 'POST':
        user_profile_form = UserProfileForm(request.POST)
        user_form = UserForm(request.POST)
        user_form.save()
        user_profile_form.save()

        if user_profile_form.is_valid() and user_form.is_valid():
            
            biographyvalue = user_profile_form.cleaned_data.get("biography")
            picture = user_profile_form.cleaned_data.get("picture")
            email = user_profile_form.cleaned_data.get('email')
        
            username = user_form.cleaned_data.get('username')
            context_dict= {'user_form': user_form,'user_profile_form': user_profile_form, 'username': username, 
                        'emailvalue':email,'biographyvalue':biographyvalue,'picture':picture}

        return render(request, 'collab_app/my_account.html', context=context_dict)

    else:
        context_dict = {'user_form': user_form,'user_profile_form': user_profile_form}

        return render(request, 'collab_app/my_account.html', context=context_dict)

def general(request):
    """Takes url request, returns general page"""
    context_dict = {}

    return render('collab_app/general.html', context=context_dict)
    

def universities(request):
    """Takes url request, returns universities page"""
    context_dict = {}

    return render('collab_app/universities.html', context=context_dict)

def show_university(request,university_name_slug):
    """Takes url request, returns a specific university page"""

    context_dict = {}

    try:
        # Attempt to retrieve the category from the category_name_slug.
        university = University.objects.get(slug=university_name_slug)

        # Add the pages and category to the context dictionary.
        context_dict['university'] = university

    except Category.DoesNotExist:
        # Assign empties to the context dict.
        context_dict['university'] = None

    return render(request, 'collab_app/universities.html', context=context_dict)

def add_university(request):
    """Takes url request, returns the creation page for new universities"""

    if not request.user.is_authenticated:
        return HttpResponse("User not authenticated.")
    form = UniversityForm()
    
    if request.method == 'POST':# A HTTP POST?
        form = UniversityForm(request.POST)
        
        if form.is_valid():# Have we been provided with a valid form?
            # Save the new category to the database.
            form.save(commit=True)
            # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
            return redirect('/collab_app/')
        else:
            print(form.errors)
    return render(request, 'collab_app/add_university.html', {'form': form})

def show_category(request,category_name_slug):
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

    return render(request, 'collab_app/category.html', context=context_dict)

def add_category(request,university_name_slug):
    """Takes url request, returns the creation page for new categories"""

    if not request.user.is_authenticated:
        return HttpResponse("User not authenticated.")

    try:
        university = University.objects.get(slug=university_name_slug)

    except University.DoesNotExist:
        university = None
    
    if university is None:# You cannot  a Category that does not exist...
        return redirect('/collab_app/')
    
    form = CategoryForm()
    
    """
    DUPLICATE: is this meant to be here?

     if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():

            if university:
                category  = form.save(commit=False)
                category.name = category
                page.views = 0 <---- page is not defined, is this meant to be here?
                page.save()
                return redirect(reverse('collab_app:show_category', kwargs={'category_name_slug': category_name_slug}))

        else:
            print(form.errors) """

    if request.method == 'POST': # A HTTP POST?
        form = CategoryForm(request.POST)
        
        if form.is_valid(): # Have we been provided with a valid form?
            form.save(commit=True) # Save the new category to the database.
            # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
            return redirect('/collab_app/')

        else:
            print(form.errors)

    return render(request, 'collab_app/add_category.html', {'form': form})

def show_page(request):
	pass
     
def add_page(request,category_name_slug):
    """Takes url request, returns the creation page for new pages"""

    if not request.user.is_authenticated:
        return HttpResponse("User not authenticated.")

    try:
        category = Category.objects.get(slug=category_name_slug)

    except Category.DoesNotExist:
        category = None
    
    
    if category is None: # You cannot add a page to a Category that does not exist...
        return redirect('/collab_app/')
    
    form = PageForm()
    
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():

            if category:
                page = form.save(commit=False)
                page.category = category
                page.save()
                return redirect(reverse('collab_app:show_category', kwargs={'category_name_slug': category_name_slug}))
            
        else:
            print(form.errors)
    
    context_dict = {'form': form, 'category': category}

    return render(request, 'collab_app/add_page.html', context=context_dict)

    
    
