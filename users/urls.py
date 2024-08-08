from django.urls import path
from .views import SignupView, login_view , UserSearchView , send_friend_request , respond_to_friend_request , FriendListView , PendingRequestsView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', login_view, name='login'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('send-request/', send_friend_request, name='send-friend-request'),
    path('respond-request/', respond_to_friend_request, name='respond-friend-request'),
    path('friends/', FriendListView.as_view(), name='list-friends'),
    path('pending-requests/', PendingRequestsView.as_view(), name='pending-requests'),
]
