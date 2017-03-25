from __future__ import unicode_literals
from django.db import models
from common.utils import ChoiceEnum



class ParticipantTypes(ChoiceEnum):
    student = 0
    photographer = 1
    non_photographer = 2

class AnalysisPoint(ChoiceEnum):
    confabulation = 0
    connection = 1
    interaction = 2
    emotion = 3
    framing = 4

class Interactions(ChoiceEnum):
    block = 0
    analyze = 1
    non_block_trigger = 2
    respond_to_trigger = 3
    audience = 4

class Emotions(ChoiceEnum):
    trauma = 0
    conflicted = 1
    surprised = 3

class Framing(ChoiceEnum):
    gray_matter = 0
    identify_only = 1
    unsecure_deflection = 2
    connection = 1
    theme  =  2
    themeconnection = 3
    themeSubject = 4

class Connections(ChoiceEnum):
    story_to_story = 0
    theme = 1
    theme_to_theme = 2
    theme_subject = 3

# Create your models here.

class Participant(models.Model):
    name = models.CharField(max_length=200, primary_key = True)
    profile = models.CharField(max_length=2000)
    participation_group = models.CharField(max_length=1, choices=ParticipantTypes.choices())
    gender = models.IntegerField(default=0)
    recording = models.OneToOneField('Recording', unique = True)


class Recording(models.Model):
    date = models.DateField()
    stories = models.ForeignKey('Story')
    data_collection_circumstances = models.CharField(max_length = 2000)
    sound_recording = models.FilePathField()
    photos = models.ForeignKey("Photo")

class Photo(models.Model):
    name = models.CharField(max_length = 50)
    file = models.FilePathField()
    duration = models.DurationField()
    order_in_recording = models.IntegerField(unique= True) # marks the position of the photo in the recoding

class Story(models.Model):
    photo = models.ForeignKey('Photo')
    transscribe_eng = models.CharField(max_length=10000)
    transscribe_hu = models.CharField(max_length=10000)
    video_url = models.FilePathField()
    thumbnail = models.FilePathField()
    analysis_points = models.CharField(max_length=1, choices = AnalysisPoint.choices())
    emotions = models.CharField(max_length=1, choices = Emotions.choices())
    interactions = models.CharField(max_length=1, choices = Interactions.choices())
    framing = models.CharField(max_length=1, choices = Framing.choices())
    connections = models.CharField(max_length=1, choices = Connections.choices())


class StoryConnection(models.Model):
    story = models.ManyToManyField('Story')

class Theme(models.Model):
    name = models.CharField(max_length = 50)
    photos = models.ForeignKey('Story')

class ThemeConnection(models.Model):
    story = models.ManyToManyField('Theme')

class Subject(models.Model):
    name = models.CharField(max_length = 50)
    themes = models.ManyToManyField('Theme')

