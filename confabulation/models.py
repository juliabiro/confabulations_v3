from __future__ import unicode_literals
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
    name = models.CharField(max_length=200)
    profile = models.CharField(max_length=2000)
    participation_group = models.CharField(max_length=50, choices=ParticipantTypes.choices())
    gender = models.CharField(max_length=20, choices=Gender.choices())
    recording = models.OneToOneField('Recording', null=True, blank=True, unique = True)


## recorded databases
class Recording(models.Model):
    name = models.CharField(max_length = 100)
    date = models.DateField()
    duration = models.DurationField(null=True, blank=True)
    data_collection_circumstances = models.CharField(max_length = 2000, null=True, blank=True)
    sound_recording_url = models.URLField(null=True, blank = True)

class Photo(models.Model):
    name = models.CharField(max_length = 50)
    file_path = models.FilePathField(null=True, blank = True)
    file_url = models.URLField(null = True, blank = True)

class Transscription(models.Model):
    date = models.DateField()
    text_eng = models.CharField(max_length=10000, null=True, blank=True)
    text_hu = models.CharField(max_length=10000, null=True, blank=True)

class Story(models.Model):
    name = models.CharField(max_length = 100)
    recording = models.ForeignKey('Recording')
    photos = models.ForeignKey('Photo', null=True, blank=True)
    order_in_recording = models.IntegerField(unique= True, null=True, blank=True) # marks the position of the photo in the recoding
    transscription = models.ForeignKey('Transscription', null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    thumbnail = models.FilePathField(null=True, blank=True)
    analysis_points = models.ForeignKey('AnalysisPoint', null=True, blank=True)
    #todo connections



## analysis

class AnalysisPoint(models.Model):
    name = models.CharField(max_length =100)
    color_code = RGBColorField()

class Confabulation(AnalysisPoint):
    class ConfabulationTypes(ChoiceEnum):
        confabulation = "Confabulation"
        partial_confabulation = "Partial Confabulation"

    type = models.CharField(max_length=50, choices = ConfabulationTypes.choices())

class Interaction(AnalysisPoint):
    class InteractionTypes(ChoiceEnum):
        block = 'blocks'
        analyze = 'analyze'
        respond_to_trigger = 'Respond to trigger question'
        not_respond_to_trigger = 'Not respond to trigger question'

    type = models.CharField(max_length=50, choices = InteractionTypes.choices())

class Emotions(AnalysisPoint):
    class EmotionTypes(ChoiceEnum):
        conflicted = 'Conflicted'
        traumatic = 'Traumatic'
        emotional = 'Emotional'

    types = models.CharField(max_length=50, choices = EmotionTypes.choices())


class Framing(AnalysisPoint):
    class FramingTypes(ChoiceEnum):
        gray_matter = 'Gray Matter'
        identification = 'Identification'
        not_sure_it_is_true = 'Not sure it is true'

    types = models.CharField(max_length=50, choices = FramingTypes.choices())

class Audience(AnalysisPoint):
    class AudienceTypes(ChoiceEnum):
        positive = 'Positive'
        negative = 'Negative'

    types = models.CharField(max_length=50, choices = AudienceTypes.choices())



## connection types
class ConnectionRange(ChoiceEnum):
    interconnection = 'Interconnection'
    intraconnection = 'Intraconnection'

class StoryToStoryConnection(models.Model):
    story1 = models.ForeignKey('Story', related_name='story1')
    story2 = models.ForeignKey('Story', related_name='story2')
    connection_range = models.CharField(max_length=30, choices=ConnectionRange.choices())

class StoryInTheme(models.Model):
    number = models.IntegerField()
    story = models.ForeignKey('Story')
    theme = models.ForeignKey('Theme')

class Theme(models.Model):
    stories = models.ManyToManyField('Story', through=StoryInTheme)
    connection_range = models.CharField(max_length=30, choices=ConnectionRange.choices())

class ThemeInChain(models.Model):
    number = models.IntegerField()
    theme = models.ForeignKey('Theme')
    chain = models.ForeignKey('Chain')

class Chain(models.Model):
    themes = models.ManyToManyField('Theme', through=ThemeInChain)
    connection_range = models.CharField(max_length=30, choices=ConnectionRange.choices())

