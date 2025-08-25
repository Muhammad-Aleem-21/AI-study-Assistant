"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static
# from django.contrib.auth import views as auth_views

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
#     path('', include('study.urls')),   # now homepage = study app
# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# from django.contrib import admin
# from django.urls import path, include
# from django.contrib.auth import views as auth_views
# from django.views.generic import RedirectView

# urlpatterns = [
#     path('admin/', admin.site.urls),

#     # LOGIN: redirect already-authenticated users away from the login page
#     path(
#         'login/',
#         auth_views.LoginView.as_view(
#             template_name='auth/login.html',
#             redirect_authenticated_user=True
#         ),
#         name='login'
#     ),
#     path('logout/', auth_views.LogoutView.as_view(), name='logout'),

#     # Home (/) -> redirect to the login page
#     path('', RedirectView.as_view(pattern_name='login', permanent=False)),

#     # Your app routes (remain the same)
#     path('study/', include('study.urls')),   # note_list will live at /study/
# ]

# urlpatterns = [
#     path('admin/', admin.site.urls),

#     path(
#         'login/',
#         auth_views.LoginView.as_view(
#             template_name='auth/login.html',
#             redirect_authenticated_user=True
#         ),
#         name='login'
#     ),

#     # Redirect to login after logout
#     path(
#         'logout/',
#         auth_views.LogoutView.as_view(next_page='login'),
#         name='logout'
#     ),

#     path('', RedirectView.as_view(pattern_name='login', permanent=False)),

#     path('study/', include('study.urls')),
# ]

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='auth/login.html',
            redirect_authenticated_user=True
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),  # no template needed
        #auth_views.LogoutView.as_view(next_page='login'), 
        name='logout'
    ),

    # Landing page is login
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),

    path('study/', include('study.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
