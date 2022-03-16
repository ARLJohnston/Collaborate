from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False
    
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(request.POST)
        university_form = University_form(request.POST)
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
            registered = True

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



    return render(request, 'collab_app/sign_up.html',   context = {'user_form': user_form,'university_form' : university_form, 'registered': registered})
    """Takes url request, returns sing-up page"""

    #context_dict = {}
    #return render(request, 'collab_app/sign_up.html', context=context_dict)

def login(request):
    """Takes url request, returns login page"""
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
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
    #context_dict = {}
    #return render(request, 'collab_app/login.html', context=context_dict)

@login_required
def my_account(request):
    if request.method == 'POST':
        user_form= UserProfileForm(request.POST or None)


        
        if user_form.is_valid():
            
            biographyvalue = form.cleaned_data.get("biography")
            picture=form.cleaned_data.get("picture")
            email=form.cleaned_data.get('email')
        
        username = request.POST.get('username')
        context_dict= {'form': form, 'username': username, 
                   'emailvalue':email,'biographyvalue':biographyvalue,'picture':picture}
    else


    """Takes url request, returns my-account page"""
    context_dict = {}
    return render(request, 'collab_app/my_account.html', context=context_dict)

def general(request):
    """Takes url request, returns general page"""
    

def universities(request):

    """Takes url request, returns universities page"""
    pass

def show_university(request,university_name_slug):
    context_dict = {}



    # Attempot to retrieve the category from the category_name_slug.

    try:

        university = University.objects.get(slug=university_name_slug)

        



        # Add the pages and category to the context dictionary.

        context_dict['university'] = university

        



    except Category.DoesNotExist: # If error, then raise a does not exist error.

        # Assign empties to the context dict.

        context_dict['university'] = None

        


    return render(request, 'rango/universities.html', context=context_dict)
    """Takes url request, returns a specific university page"""
    pass

def add_university(request):
    if not request.user.is_authenticated:
        return HttpResponse("User not authenticated.")
    form = UniversityForm()
    # A HTTP POST?
    if request.method == 'POST':
        form = UniversityForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            
            form.save(commit=True)
            # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
            return redirect('/collab_app/')
        else:
            print(form.errors)
    return render(request, 'collab_app/add_university.html', {'form': form})
    """Takes url request, returns the creation page for new universities"""
    pass

def show_category(request,category_name_slug):
    context_dict = {}



    # Attempot to retrieve the category from the category_name_slug.

    try:

        category = Category.objects.get(slug=category_name_slug) # Get the category with the correct name.



        pages = Page.objects.filter(category=category) # Get all the associated pages for the specified category.



        # Add the pages and category to the context dictionary.

        context_dict['pages'] = pages

        context_dict['category'] = category



    except Category.DoesNotExist: # If error, then raise a does not exist error.

        # Assign empties to the context dict.

        context_dict['category'] = None

        context_dict['pages'] = None



    return render(request, 'rango/category.html', context=context_dict)
    """Takes url request, returns a specific university page"""
    

    context_dict = {}
    

def add_category(request,university_name_slug):
    if not request.user.is_authenticated:
        return HttpResponse("User not authenticated.")
    try:
        university = University.objects.get(slug=university_name_slug)
    except University.DoesNotExist:
        university = None
    
    # You cannot  a Category that does not exist...
    if university is None:
        return redirect('/collab_app/')
    
    form = CategoryForm()
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():

            if university:
                category  = form.save(commit=False)
                category.name = category
                page.views = 0
                page.save()
                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
            
        else:
            print(form.errors)
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            
            form.save(commit=True)
            # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
            return redirect('/rango/')
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})
    """Takes url request, returns the creation page for new categories"""
    pass

def show_page(request):


    """Takes url request, returns a specific page"""
    pass

def add_page(request):
    if not request.user.is_authenticated:
        return HttpResponse("User not authenticated.")

    """Takes url request, returns the creation page for new pages"""
    pass