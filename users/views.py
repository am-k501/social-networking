from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login as auth_login
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .models import Friendship
from .serializers import CustomUserSerializer, FriendshipSerializer
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from users.customize_authentication import EmailAuthBackend
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt

class SignupView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer

@csrf_exempt
@api_view(['POST'])

def login_view(request):
    user = EmailAuthBackend().authenticate(email=request.data.get('email'), password=request.data.get('password'), request=request)
    if user is not None:
        auth_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'Message': 'Login successful', 'token': token.key, 'status': '1'}, status=status.HTTP_200_OK)
    return Response({'Message': 'Invalid credentials', 'status': '0'}, status=status.HTTP_400_BAD_REQUEST)

class CustomPagination(PageNumberPagination):
    page_size = 10  # Number of records per page
    page_size_query_param = 'page_size'
    max_page_size = 10
#
@permission_classes([permissions.IsAuthenticated])
class UserSearchView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        keyword = self.request.query_params.get('q', '')
        if keyword:
            return User.objects.filter(Q(email__icontains=keyword) | Q(username__icontains=keyword)).distinct()
        return User.objects.all()
#
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_friend_request(request):
    to_user_id = request.data.get('to_user')
    to_user = User.objects.get(id=to_user_id)
    request_user = request.user
    # Check rate limit
    one_minute_ago = timezone.now() - timedelta(minutes=1)
    recent_requests = Friendship.objects.filter(from_user_id=request_user.id, created_at__gte=one_minute_ago)
    if recent_requests.count() >= 3:
        return Response({'detail': 'Rate limit exceeded'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

    if Friendship.objects.filter(from_user_id=request_user.id, to_user_id=to_user.id).exists():
        return Response({'detail': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)

    Friendship.objects.create(from_user_id=request_user.id, to_user_id=to_user.id, status='pending')
    return Response({'detail': 'Friend request sent'}, status=status.HTTP_201_CREATED)
#
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def respond_to_friend_request(request):
    request_id = request.data.get('request_id')
    action = request.data.get('action')
    try:
        friend_request = Friendship.objects.get(id=request_id, to_user=request.user)
    except Friendship.DoesNotExist:
        return Response({'detail': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)

    if action == 'accept':
        friend_request.status = 'accepted'
        friend_request.save()
        Friendship.objects.create(from_user=request.user, to_user=friend_request.from_user, status='accepted')
        return Response({'detail': 'Friend request accepted'}, status=status.HTTP_200_OK)

    elif action == 'reject':
        friend_request.status = 'rejected'
        friend_request.save()
        return Response({'detail': 'Friend request rejected'}, status=status.HTTP_200_OK)
    return Response({'detail': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
#
@permission_classes([permissions.IsAuthenticated])
class FriendListView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    def get_queryset(self):
        user = self.request.user
        friends = Friendship.objects.filter(Q(from_user=user, status='accepted') | Q(to_user=user, status='accepted')).values_list('from_user', 'to_user')
        friends = set([f for pair in friends for f in pair])
        return User.objects.filter(id__in=friends)

@permission_classes([permissions.IsAuthenticated])
class PendingRequestsView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    def get_queryset(self):
        return User.objects.filter(id__in=Friendship.objects.filter(to_user=self.request.user, status='pending').values_list('from_user', flat=True))
    
    
