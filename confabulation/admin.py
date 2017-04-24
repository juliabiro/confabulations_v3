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

class AnalysisPointInline(admin.StackedInline):
    model=AnalysisPoint
    extra = 0

class ThemeInline(admin.StackedInline):
    model = Theme
    extra = 2

class RecordingInline(admin.StackedInline):
    model = Recording
    extra = 0

class StoryConnectionInline1(admin.StackedInline):
    model = StoryToStoryConnection
    fk_name ='story1'
    extra = 0

class StoryConnectionInline2(admin.StackedInline):
    model = StoryToStoryConnection
    fk_name ='story2'
    extra = 0

class StoryInThemeInline(admin.StackedInline):
    model=StoryInTheme
    extra = 0

class ThemeInChainInline(admin.StackedInline):
    model = ThemeInChain
    extra = 0

class ParticipantAdmin(admin.ModelAdmin):
    inlines = [RecordingInline]
    list_display=['name']

class StoryAdmin(admin.ModelAdmin):
    inlines = [TransscriptionInline, StoryConnectionInline1, StoryConnectionInline2]
    list_display =['participant','name' ]

class RecordingAdmin(admin.ModelAdmin):
    list_display =['name', 'date']

class AnalysisTypeAdmin(admin.ModelAdmin):
    inlines = [AnalysisPointInline]
    list_display = ['name']

class AnalysisPointAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_code']

class ThemeAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines=[StoryInThemeInline]

class ChainAdmin(admin.ModelAdmin):
    list_display=['name']
    inlines=[ThemeInChainInline]



admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Recording, RecordingAdmin)
admin.site.register(Transscription)
admin.site.register(Photo)
admin.site.register(AnalysisPoint, AnalysisPointAdmin)
admin.site.register(AnalysisType, AnalysisTypeAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Chain, ChainAdmin)
