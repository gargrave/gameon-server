from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    """
    Base model for basic fields that most Models will use.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class UserProfile(BaseModel):
    """
    Basic profile to attach to user accounts. Used for storing
    information and preferences for a user that are not a part of
    the user/auth model.
    """
    owner = models.ForeignKey(User)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)


class Game(BaseModel):
    """
    Model for a single Game instance.
    """
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Tag(BaseModel):
    """
    A basic tag model to allow a user to tag Games.

    Note that the Tag model itself does not contain any references to
    its associated Game(s). This is done in the TagGameRelation model.
    """
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('owner', 'title')


class TagGameRelation(BaseModel):
    """
    A relation tying a Tag to a Game.
    """
    owner = models.ForeignKey(User)
    _tag = models.ForeignKey(Tag)
    _game = models.ForeignKey(Game, related_name="tags")

    def __str__(self):
        return 'Game: {} | Tag: {}'.format(
            str(self._game), str(self._tag))
