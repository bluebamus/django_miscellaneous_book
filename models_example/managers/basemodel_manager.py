# https://www.simononsoftware.com/how-to-make-django-base-model/#the-huge-mess

from django.db import models
from django.db.models import Q
from datetime import datetime


class ChannelManager(models.Manager):
    def channel_for_indexing(self):
        return self.filter(Q(last_index__isnull=True) | Q(reindex__exact=True)).first()


class PlaylistManager(models.Manager):
    def playlist_for_indexing(self):
        return self.filter(Q(last_index__isnull=True) | Q(reindex__exact=True)).first()


class VideoManager(models.Manager):
    def video_for_indexing(self):
        return self.filter(Q(last_index__isnull=True) | Q(reindex__exact=True)).first()


class BaseModel(models.Model):

    etag = models.CharField(max_length=300, blank=True, null=True)
    reindex = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    last_error = models.CharField(max_length=300, blank=True, null=True)
    last_indexing = models.DateTimeField(blank=True, null=True)
    last_error_indexing = models.DateTimeField(blank=True, null=True)
    last_successful_indexing = models.DateTimeField(blank=True, null=True)
    youtube_url = models.CharField(max_length=1234, blank=True, null=True)

    def indexing_error(self, e):
        self.last_error_indexing = datetime.now()
        self.last_indexing = datetime.now()
        self.last_error = e

    def indexing_ok(self):
        self.last_indexing = datetime.now()
        self.last_successful_indexing = datetime.now()
        self.last_error = None

    class Meta:
        abstract = True


class Channel(BaseModel):
    channel_id = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    objects = ChannelManager()

    def __str__(self):
        return self.title if self.title else self.channel_id


class Playlist(BaseModel):
    channel = models.ForeignKey(Channel, blank=True, null=True)
    playlist_id = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    objects = PlaylistManager()

    def __str__(self):
        return self.title if self.title else self.playlist_id


class Video(BaseModel):
    playlist = models.ForeignKey(Playlist, null=True, blank=True, related_name="videos")
    channel = models.ForeignKey(Channel, null=True, blank=True, related_name="videos")
    video_id = models.CharField(max_length=200, unique=False)
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    length = models.TimeField(blank=True, null=True)

    objects = VideoManager()

    def __str__(self):
        return self.title if self.title else self.video_id
