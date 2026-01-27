from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from .models import Role, Permission, UserRole, RolePermission


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class RegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'password', 'password2']
        extra_kwargs = {
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "密码不匹配"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        # 确保即使没有提供 email 字段，也能成功创建用户
        user = User.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(TokenObtainPairSerializer):
    """用户登录序列化器"""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token


class PermissionSerializer(serializers.ModelSerializer):
    """权限序列化器"""
    class Meta:
        model = Permission
        fields = ['id', 'codename', 'name', 'type', 'content_type', 'object_id', 'description', 'created_at', 'updated_at']


class RoleSerializer(serializers.ModelSerializer):
    """角色序列化器"""
    permissions = serializers.SerializerMethodField()

    def get_permissions(self, obj):
        """获取角色的权限"""
        # 通过rolepermission_set获取所有关联的权限
        permissions = obj.rolepermission_set.values_list('permission', flat=True)
        return PermissionSerializer(Permission.objects.filter(id__in=permissions), many=True).data

    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'permissions']


class UserRoleSerializer(serializers.ModelSerializer):
    """用户角色关联序列化器"""
    user = UserSerializer(read_only=True)
    role = RoleSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    role_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserRole
        fields = ['id', 'user', 'role', 'user_id', 'role_id', 'created_at']

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        role_id = validated_data.pop('role_id')
        return UserRole.objects.create(user_id=user_id, role_id=role_id, **validated_data)


class RolePermissionSerializer(serializers.ModelSerializer):
    """角色权限关联序列化器"""
    role = RoleSerializer(read_only=True)
    permission = PermissionSerializer(read_only=True)
    role_id = serializers.IntegerField(write_only=True)
    permission_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = RolePermission
        fields = ['id', 'role', 'permission', 'role_id', 'permission_id', 'created_at']

    def create(self, validated_data):
        role_id = validated_data.pop('role_id')
        permission_id = validated_data.pop('permission_id')
        return RolePermission.objects.create(role_id=role_id, permission_id=permission_id, **validated_data)


class UserWithRolesSerializer(serializers.ModelSerializer):
    """带有角色信息的用户序列化器"""
    roles = RoleSerializer(many=True, read_only=True, source='userrole_set')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'roles']
