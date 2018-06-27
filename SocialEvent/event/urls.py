from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from event import views

urlpatterns = [
    url(r'^test/(?P<id>[0-9]+)/$', views.CommentView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

