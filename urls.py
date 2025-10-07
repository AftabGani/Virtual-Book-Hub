from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('books/', views.book_list, name='book_list'),  # Protected by login_required
    path('register/', views.register, name='register'),  # No login required (registration page)
    path('request-book/', views.request_book, name='request_book'),  # Protected by login_required
    path('add-book/', views.add_book, name='add_book'),  # Protected by login_required and staff/superuser
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Default login view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Default logout view
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
