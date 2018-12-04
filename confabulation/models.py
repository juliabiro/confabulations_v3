from __future__ import unicode_literals
from datetime import timedelta
from django.db import models
from common.utils import ChoiceEnum
from colorful.fields import RGBColorField


## participants
class ParticipantTypes(ChoiceEnum):
    student = 'student'
    photographer = 'photographer'
    non_photographer = 'non-photgrapher'

class Gender(ChoiceEnum):
    male = 'male'
    female = 'female'
    other = 'other'

class Participant(models.Model):
    def __str__(self):
        return "%s" % self.name

    def get_absolute_url(self):
        return "/participant/%i/" % self.id

    name = models.CharField(max_length=200)
    profile = models.TextField(null=True)
    participation_group = models.CharField(max_length=50, choices=ParticipantTypes.choices())
    gender = models.CharField(max_length=20, choices=Gender.choices())


## recorded databases
class Recording(models.Model):
    def __str__(self):
        return "%s" % self.name

    name = models.CharField(max_length=100)
    date = models.DateField()
    duration = models.DurationField(null=True, blank=True)
    data_collection_circumstances = models.TextField(default="", blank=True)
    sound_recording_url = models.URLField(null=True, blank=True)
    participant = models.ForeignKey('Participant', null=True, on_delete=models.DO_NOTHING)

class Photo(models.Model):
    def __str__(self):
        return "%s" % self.name

    name = models.CharField(max_length=50)
    file_url = models.URLField(null=True, blank=True)

class Transscription(models.Model):
    date = models.DateField()
    text_eng = models.TextField(default="", blank=True)
    text_hu = models.TextField(default="", blank=True)
    recording = models.ForeignKey('Recording', on_delete=models.DO_NOTHING)
    story = models.OneToOneField('Story', null=True, blank=True, on_delete=models.DO_NOTHING)

class Keyword(models.Model):
    def __str__(self):
        return "%s" % self.name
    name = models.CharField(null=True, blank=True, max_length=100)

class Story(models.Model):
    class Meta:
        verbose_name_plural = 'Stories'
        ordering = ['-name']

    def __str__(self):
        return "%s" % self.name

    def get_absolute_url(self):
        return "/story/%i/" % self.id

    name = models.CharField(max_length=100)
    participant = models.ForeignKey('Participant', null=True, on_delete=models.DO_NOTHING)
    photos = models.ManyToManyField('Photo', blank=True)
    order_in_recording = models.IntegerField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True, default=timedelta)
    video_url = models.URLField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails', null=True, blank=True)
    analysis = models.ManyToManyField('AnalysisPoint', blank=True)
    era = models.ManyToManyField('Era', blank=True)
    notes = models.TextField(null=True, blank=True)
    keywords = models.ManyToManyField("Keyword", blank=True)
    #todo connections


## analysis

class AnalysisType(models.Model):
    def __str__(self):
        return "%s" % self.name

    def get_absolute_url(self):
        return "/analysis_type/%i/" % self.id

    name = models.CharField(max_length=50)
    description = models.TextField(default="", blank=True)


class AnalysisPoint(models.Model):
    def __str__(self):
        return "%s" % self.name

    def get_absolute_url(self):
        return "/analysis/%i/" % self.id

    name = models.CharField(max_length=50)
    analysis_type = models.ForeignKey('AnalysisType', on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=2000, null=True, blank=True)
    color_code = RGBColorField()
    order_in_menu = models.IntegerField(null=True)

## connection types
class ConnectionRange(ChoiceEnum):
    interconnection = 'Interconnection'
    intraconnection = 'Intraconnection'

class Connection(models.Model):
    def __str__(self):
        return "%s" % self.name

    def get_absolute_url(self):
        return "/connects/%i/" % self.id

    name =  models.CharField(max_length=50)
    color_code = RGBColorField()
    description = models.CharField(max_length=2000, null=True, blank=True)
    connection_range = models.CharField(max_length=30, choices=ConnectionRange.choices())

class StoryToStoryConnection(models.Model):
    story1 = models.ForeignKey('Story', related_name='story1', on_delete=models.DO_NOTHING)
    story2 = models.ForeignKey('Story', related_name='story2', on_delete=models.DO_NOTHING)
    connection_range = models.CharField(max_length=30, choices=ConnectionRange.choices())

class StoryInTheme(models.Model):
    number = models.IntegerField()
    story = models.ForeignKey('Story', on_delete=models.DO_NOTHING)
    theme = models.ForeignKey('Theme', on_delete=models.DO_NOTHING)

class Theme(models.Model):
    def __str__(self):
        return "%s" % self.name

    def get_absolute_url(self):
        return "/theme/%i/" % self.id

    name = models.CharField(max_length=50)
    description = models.TextField(default="", blank=True)
    stories = models.ManyToManyField('Story', through=StoryInTheme)
    connection_range = models.CharField(max_length=30, choices=ConnectionRange.choices())

class ThemeInChain(models.Model):
    number = models.IntegerField()
    theme = models.ForeignKey('Theme', on_delete=models.DO_NOTHING)
    chain = models.ForeignKey('Chain', on_delete=models.DO_NOTHING)

class Chain(models.Model):
    def __str__(self):
        return"%s" % self.name

    def get_absolute_url(self):
        return "/chain/%i/" % self.id

    name = models.CharField(max_length=50)
    description = models.TextField(default="", blank=True)
    themes = models.ManyToManyField('Theme', through=ThemeInChain)
    connection_range = models.CharField(max_length=30, choices=ConnectionRange.choices())


## Eras

class Era(models.Model):
    def __str__(self):
        return "%s" % self.name
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=2000, null=True, blank=True)
    color_code = RGBColorField()
