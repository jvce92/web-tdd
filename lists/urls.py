from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^(\d+)/$', 'lists.views.viewList', name='view_list'),
    url(r'^new$', 'lists.views.newList', name='new_list'),
    url(r'^(\d+)/addItem$', 'lists.views.addItem', name='add_item'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
]
