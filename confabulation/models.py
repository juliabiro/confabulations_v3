from __future__ import unicode_literals
from django.db import models
from common.utils import ChoiceEnum



class ParticipantTypes(ChoiceEnum):
    student = 'student'
    photographer = 'photographer'
    non_photographer = 'non-photgrapher'

class AnalysisPoint(ChoiceEnum):
    confabulation = 'confabulation'
    connection = 'connection'
    interaction = 'interaction'
    emotion = 'emotion'
    framing = 'framing'

class Interactions(ChoiceEnum):
    block = 'block'
    analyze = 'analyzer'
    non_block_trigger = 'non-block trigger'
    respond_to_trigger = 'respond to trigger'
    audience = 'audience'

class Emotions(ChoiceEnum):
    trauma = 'traume'
    conflicted = 'conflicted'
    surprised = 'surprsied'

class Framing(ChoiceEnum):
    gray_matter = 'gray matter'
    identify_only = 'identify only'
    insecure_deflection = 'insecure deflection'
    connection = 'connection'
    theme  =  'theme'
    themeconnection = 'themeconnection'
    theme_ubject = 'theme subject'

class Connections(ChoiceEnum):
    story_to_story = 'story to story connection'
    theme = 'theme over multiple stories'
    theme_to_theme = 'theme to theme connection'
    theme_motif = 'common motif over multiple themes'

class Gender(ChoiceEnum):
    male = 'male'
    female = 'female'
    other = 'other'
# Create your models here.

class Participant(models.Model):
    name = models.CharField(max_length=200)
    profile = models.CharField(max_length=2000)
    participation_group = models.CharField(max_length=50, choices=ParticipantTypes.choices())
    gender = models.CharField(max_length=20, choices=Gender.choices())
    recording = models.OneToOneField('Recording', null=True, blank=True, unique = True)


class Recording(models.Model):
    name = models.CharField(max_length = 100)
    date = models.DateField()
    stories = models.ForeignKey('Story', null=True, blank = True)
    data_collection_circumstances = models.CharField(max_length = 2000)
    sound_recording = models.FilePathField(null=True, blank=True)
    photos = models.ForeignKey("Photo", null=True, blank=True)

class Photo(models.Model):
    name = models.CharField(max_length = 50)
    file = models.FilePathField()
    duration = models.DurationField()
    order_in_recording = models.IntegerField(unique= True, null=True, blank=True) # marks the position of the photo in the recoding

class Story(models.Model):
    name = models.CharField(max_length = 100)
    photos = models.ForeignKey('Photo', null=True, blank=True)
    transscribe_eng = models.CharField(max_length=10000, null=True, blank=True)
    transscribe_hu = models.CharField(max_length=10000, null=True, blank=True)
    video_url = models.FilePathField(null=True, blank=True)
    thumbnail = models.FilePathField(null=True, blank=True)
    analysis_points = models.CharField(max_length=50, choices = AnalysisPoint.choices())
    emotions = models.CharField(max_length=50, choices = Emotions.choices(), null=True, blank=True)
    interactions = models.CharField(max_length=50, choices = Interactions.choices(), null=True, blank=True)
    framing = models.CharField(max_length=50, choices = Framing.choices(), null=True, blank=True)
    connections = models.CharField(max_length=50, choices = Connections.choices(), null=True, blank=True)


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

