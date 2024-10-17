from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    # TokenVerifyView,
)

from profiles.views import FollowProfileView, RegisterView, ProfileSearchView,UnFollowProfileView, FollowedListView

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'), #tokenin süresi itti mi kontrolü için, bu projede gerek yok
    path('search/', ProfileSearchView.as_view(), name='search_profile'),
    path('follow/<str:username>/', FollowProfileView.as_view(), name='follow_profile'),
    path('unfollow/<str:username>/', UnFollowProfileView.as_view(), name='unfollow_profile'),
    path('followed-list/', FollowedListView.as_view(), name='followed_list'),
]