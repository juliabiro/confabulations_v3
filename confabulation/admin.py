from django.contrib import admin
from models import *
# Register your models here.

# fields make the dispplay order
# fieldsets allow roganizing in multiple input parts

#list display to contorl what is displayed

# inlines
class PhotoInline(admin.StackedInline):
    model = Photo
    extra = 1 
class TransscriptionInline(admin.StackedInline):
    model=Transscription
    extra = 1
class AnalysisInline(admin.StackedInline):
    model=Analysis
    extra =3

class ThemeInline(admin.StackedInline):
    model = Theme
    extra = 2

class RecordingInline(admin.StackedInline):
    model = Recording

class ParticipantAdmin(admin.ModelAdmin):
    list_display=['name']

class StoryAdmin(admin.ModelAdmin):
    inlines =[AnalysisInline]
    list_display =['name']

class RecordingAdmin(admin.ModelAdmin):
    inlines = [TransscriptionInline]
    list_display =['name', 'date']

class AnalysisPointAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_code']

admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Recording, RecordingAdmin)
admin.site.register(Transscription)
admin.site.register(Photo)
admin.site.register(Story, StoryAdmin)
admin.site.register(Confabulation)
admin.site.register(Interaction, AnalysisPointAdmin)
admin.site.register(Emotion, AnalysisPointAdmin)
admin.site.register(Framing, AnalysisPointAdmin)
admin.site.register(Audience, AnalysisPointAdmin)
admin.site.register(Analysis)
admin.site.register(Theme)
admin.site.register(Chain)

