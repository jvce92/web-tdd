from django.conf.urls import include, url
from django.contrib import admin
from lists import views as listsViews

urlpatterns = [
    # Examples:
    url(r'^$', listsViews.homePage, name='home'),
    url(r'^lists/', include('lists.urls')),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
]
