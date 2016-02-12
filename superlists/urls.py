from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'lists.views.homePage', name='home'),
    url(r'^lists/the-only-list-in-the-world/$', 'lists.views.viewList', name='view_list'),
    url(r'^lists/new$', 'lists.views.newList', name='new_list'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
]
