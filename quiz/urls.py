from django.urls import path

from api.views import TagListView

urlpatterns = [
    path('tags/', TagListView.as_view(), name='tag_list'),
]
