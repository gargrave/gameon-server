from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Game, Tag, TagGameRelation, UserProfile

# Get the UserModel
UserModel = get_user_model()


########################################################
# Tag Serializers
########################################################
class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'title')


class TagRelatedField(serializers.RelatedField):
    """
    Custom RelatedField serializer for Tags. Simply returns the title of the Tag.
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
# Game Serializers
########################################################
class GameSerializer(serializers.ModelSerializer):
    # use the custom serializer to build a tag list
    tags = TagGameRelationReadSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = ('id', 'title', 'tags',
                  'created', 'modified')


########################################################
# User/Auth Serializers
########################################################
class UserProfileSerializer(serializers.ModelSerializer):

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
