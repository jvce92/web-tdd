from django.conf.urls import include, url
from django.contrib import admin
from lists import views

urlpatterns = [
    # Examples:
    url(r'^(\d+)/$', views.viewList, name='view_list'),
    url(r'^new$', views.newList, name='new_list'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
]
