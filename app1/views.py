from django.contrib.auth.models import User, Group
from app1.serializers import UserSerializer, GroupSerializer, SnippetSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import mixins, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions
from django.contrib.auth import authenticate, login
from rest_framework import generics

from app1.models import Snippet


class UserViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的API路径。
    """
    queryset = User.objects.order_by('-date_joined')
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            raise exceptions.ValidationError('已经登陆')
        username = self.request.data.get('username')
        password = self.request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
        else:
            raise exceptions.ValidationError('用户名或密码错误,或账号被禁用')
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)


class GroupViewSet(viewsets.ModelViewSet):
    """
    允许组查看或编辑的API路径。
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (permissions.IsAdminUser, )
    authentication_classes = (SessionAuthentication, )
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    # authentication_classes = (JSONWebTokenAuthentication,)
    filter_fields = '__all__'
    search_fields = ('code', 'content', 'language', 'sn', 'title',)
    ordering_fields = '__all__'
    ordering = ('created',)


class SnippetList(APIView):
    """
    列出所有的snippets或者创建一个新的snippet。
    """
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):
    """
    检索，更新或删除一个snippet示例。
    """
    def get_object(self, id):
        try:
            return Snippet.objects.get(id=id)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        snippet = self.get_object(id)
        serializer = SnippetSerializer(snippet, context={'request': request})
        return Response(serializer.data)

    def put(self, request, id, format=None):
        snippet = self.get_object(id)
        serializer = SnippetSerializer(snippet, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        snippet = self.get_object(id)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
