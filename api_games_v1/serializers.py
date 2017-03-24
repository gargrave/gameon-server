from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Game, GameDateRelation, PlatformModel,\
    Tag, TagGameRelation, UserProfile

# Get the UserModel
UserModel = get_user_model()


########################################################
# Tag Serializers
########################################################
class TagSerializer(serializers.ModelSerializer):
    """
    Basic serializer for Tag model.
    """
    class Meta:
        model = Tag
        fields = ('id', 'title')


class TagRelatedField(serializers.RelatedField):
    """
    Custom RelatedField serializer for Tags.
    Simply returns the title of the Tag.
    """

    def to_representation(self, value):
        return {
            'id': value.pk,
            'title': value.title
        }

    def to_internal_value(self, data):
        # simply implementing to get rid of linting warnings
        pass


class TagGameRelationWriteSerializer(serializers.ModelSerializer):
    """
    Basic serializer for TagGameRelation. User this one for writing, as it
    will only be concerned with the IDs of its related fields;
    no special relational binding.
    """
    class Meta:
        model = TagGameRelation
        fields = ('id', '_tag', '_game')


class TagGameRelationReadSerializer(serializers.ModelSerializer):
    """
    Custom serializer for TagGameRelation. Note that this also uses
    the custom TagRelatedField to build a front-end friendly version of
    the necessary data.
    """
    _tag = TagRelatedField(read_only=True)

    class Meta:
        model = TagGameRelation
        fields = ('id', '_tag')


########################################################
# Platform Serializers
########################################################
class PlatformSerializer(serializers.ModelSerializer):
    """
    Basic serializer for Platform model.
    """
    class Meta:
        model = PlatformModel
        fields = ('id', 'title', 'created', 'modified')


class PlatformNestedSerializer(serializers.ModelSerializer):
    """
    Basic serializer for Platform model, when used in the Games read views.
    This simply limits the information that is sent with Games to
    what is necessary. (i.e. no created/modified info, etc.)
    """
    class Meta:
        model = PlatformModel
        fields = ('id', 'title')


########################################################
# Game Serializers
########################################################
class GameReadSerializer(serializers.ModelSerializer):
    """
    Basic serializer for viewing/list Game model.

    This serializer has the following customizations:
    - Dates list is populated as a list of string with the
        associated dates values
    - Platform instance is populated using PlatformNestedSerializer
        because we want to return full Platform data, rather than just the ID.
    """
    dates = serializers.StringRelatedField(many=True, read_only=True)
    platform = PlatformNestedSerializer(read_only=True)

    class Meta:
        model = Game
        fields = ('id', 'title', 'platform', 'dates',
                  'created', 'modified')


class GameWriteSerializer(serializers.ModelSerializer):
    """
    Basic serializer for creating/editing Game model.

    This serializer provides a custom to_representation implementation
        in order to correctly populate the 'platform' and 'dates' fields
        for the return value after a write request.
    """

    class Meta:
        model = Game
        fields = ('id', 'title', 'platform', 'created', 'modified')

    def to_representation(self, obj):
        platform = PlatformModel.objects.get(pk=obj.platform)
        dates = [str(d) for d in GameDateRelation.objects.filter(
            owner=obj.owner,
            game__title=obj.title)]
        return {
            'id': obj.id,
            'title': obj.title,
            'platform': {
                'id': platform.id,
                'title': platform.title,
            },
            'dates': dates,
            'created': obj.created,
            'modified': obj.modified,
        }


########################################################
# User/Auth Serializers
########################################################
class UserProfileSerializer(serializers.ModelSerializer):
    """
    Basic serializer for UserProfile model.
    """
    class Meta:
        model = UserProfile
        fields = ('pk', 'first_name', 'last_name')


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password

    NOTE: This is an override for django-rest-auth's default
        UserDetailsSerializer class, in order to provide more
        details about the user.
    """
    class Meta:
        model = UserModel
        fields = ('pk', 'username', 'email', 'date_joined', 'last_login')
        read_only_fields = ('email',)
