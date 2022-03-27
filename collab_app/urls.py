from django.urls import path
from collab_app import views

app_name = 'collab_app'
urlpatterns = [
      path('', views.index, name='index'),
      path('index/', views.index, name='index'),
      path('about/', views.about, name='about'),
      path('contact_us/', views.contact_us, name='contact_us'),
      path('search_bar/', views.search_bar, name="search_bar"),

      path('sign_up/', views.sign_up, name='sign_up'),
      path('login/', views.login_view, name='login'),
      path('my_account/', views.my_account, name='my_account'),
      path('my_account/<slug:account_name_slug>/', views.my_account),
      path('add_comment/<slug:page_name_slug>/', views.add_comment, name='add_comment'),

      # General pages
      path('general/', views.general, name='general'),
      
      path('general/<slug:category_name_slug>/', views.show_general_category,
            name='show_general_category'),
      path('general/add_general_category', views.add_general_category, name='add_general_category'),
      
      path('general/<slug:category_name_slug>/add_general_page', views.add_page, name='add_general_page'),

      path('general/<slug:category_name_slug>/<slug:page_name_slug>/',
            views.show_general_page, name='show_general_page'),

      path('general/<slug:category_name_slug>/add_page', views.add_general_page, name='add_page'),

      # University pages
      path('universities/', views.universities, name='universities'),

      path('universities/add_university/', views.add_university,
            name='add_university'),
      path('universities/<slug:university_name_slug>/',
            views.show_university, name='show_university'),
      
      path('universities/<slug:university_name_slug>/add_university_category',
          views.add_university_category, name='add_university_category'),

      path('universities/<slug:university_name_slug>/<slug:category_name_slug>/',
            views.show_university_category, name='show_university_category'),
            
      path('universities/<slug:university_name_slug>/<slug:category_name_slug>/add_university_page', views.add_page, name='add_university_page'),

      path('universities/<slug:university_name_slug>/<slug:category_name_slug>/<slug:page_name_slug>/',
            views.show_university_page, name='show_university_page'),

      # Like AJAX request
      path('like_page/', views.like_page_view.as_view(), name='like_page'),
]

