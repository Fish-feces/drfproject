from django.contrib.auth.models import User, Group
from rest_framework import serializers

from app1.models import Snippet


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'groups')
        extra_kwargs = {
            'groups': {'view_name': 'group-detail', 'lookup_field': 'pk'},
        }
        # extra_kwargs = {
        #     'url': {'view_name': 'api:user-detail'},
        #     'groups': {'view_name': 'api:group-detail'},
        # }


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name', 'description')

        # extra_kwargs = {
        #     'url': {'view_name': 'api:group-detail'},
        # }


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
    id = serializers.IntegerField(read_only=True)
    sn = serializers.UUIDField(read_only=True, required=False)
    code = serializers.CharField(allow_blank=False, min_length=6,
                                 # write_only=True,
                                 error_messages={
                                     'min_length': 'code不能小于6个字符',
                                     'blank': '请填写code',
                                 },
                                 # style={'input_type': 'password'}
                                 )
    content = serializers.CharField(required=True, min_length=6,
                                    error_messages={
                                        'min_length': 'content不能小于6个字符',
                                        'blank': '请填写content'
                                    },
                                    label='CONTENT',
                                    help_text='content help_text',)

    def validate(self, attrs):
        del attrs['user']
        return attrs

    def create(self, validated_data):
        """
        根据提供的验证过的数据创建并返回一个新的`Snippet`实例。
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        根据提供的验证过的数据更新和返回一个已经存在的`Snippet`实例。
        """
        instance.code = validated_data.get('code', instance.code)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance

    class Meta:
        model = Snippet
        fields = ('id', 'url', 'sn', 'code', 'content', 'user',)
        # extra_kwargs = {
        #     'url': {'view_name': 'api:snippet-detail'},
        # }
