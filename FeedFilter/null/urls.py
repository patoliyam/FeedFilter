"""null URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from null import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^image_to_annotation', views.i_to_a ,name='i_to_a'),
    url(r'^text_to_annotation', views.t_to_a ,name='t_to_a'),
    url(r'^register$',views.register, name='register'),
    url(r'^login$',views.login_view, name='login_view'),
    url(r'^logout$',views.logout_view, name='logout_view'),
    url(r'^checklogin$',views.checklogin, name='checklogin')
]
