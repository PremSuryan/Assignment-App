from django.urls import path, include
from rest_framework import routers
from .views import VideoViewSet
from . import views
from .views import stream_video, search_videos, login_view, register_view, logout_view, upload_video, delete_video

# router = routers.DefaultRouter()
# router.register(r'videos', VideoViewSet)

urlpatterns = [
    # path('api/', include(router.urls)),

    path('register_view', register_view, name='register_view'),
    path('', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('videoviewlist', VideoViewSet.list, name='videoviewlist'),
    path('video/<int:video_id>/', stream_video, name='stream_video'),
    path('search', search_videos, name='search_videos'),
    path('upload/', upload_video, name='upload_video'),
    path('delete_video/<int:video_id>/', delete_video, name='delete_video'),
    # Other URLs for authentication, searching, etc.
]
