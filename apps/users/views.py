from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import User
from .serializers import RegisterSerializer, UserSerializer
from .permissions import IsTeacher, IsOwnerOrTeacher


class RegisterView(generics.CreateAPIView):
    """用户注册 — 公开接口"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )


class UserViewSet(viewsets.ModelViewSet):
    """用户管理 ViewSet"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated(), IsTeacher()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """教师只能看到自己名下的学生"""
        qs = super().get_queryset()
        if self.request.user.user_type == 'teacher':
            return qs.filter(teacher=self.request.user) | User.objects.filter(id=self.request.user.id)
        return qs

    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        """查看或修改当前登录用户信息"""
        if request.method == 'GET':
            return Response(UserSerializer(request.user).data)
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
