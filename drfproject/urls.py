"""drfproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token

from app1 import views
from drfproject import settings

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)  # user-list, basename = user
router.register(r'groups', views.GroupViewSet)
router.register(r'snippet', views.SnippetViewSet)

schema_view = get_schema_view(title='Pastebin API')

# 使用自动URL路由连接我们的API。
# 另外，我们还包括支持浏览器浏览API的登录URL。
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    # url(r'^', include((router.urls, 'api'), namespace='api')),  # app_name
    url('^schema/$', schema_view),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^snippets/$', views.SnippetList.as_view()),
    url(r'^snippets/(?P<id>[0-9]+)/$', views.SnippetDetail.as_view()),
    url(r'docs/', include_docs_urls(title="Test Docs")),
    url(r'^login/', obtain_jwt_token),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(url(r'^debug/', include(debug_toolbar.urls)))
