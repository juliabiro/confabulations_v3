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

class StoryInThemeInline(admin.StackedInline):
    model=StoryInTheme
    extra = 0

class ThemeInChainInline(admin.StackedInline):
    model = ThemeInChain
    extra = 0

class ParticipantAdmin(admin.ModelAdmin):
    list_display=['name']

class StoryAdmin(admin.ModelAdmin):
    list_display =['name' ]

class RecordingAdmin(admin.ModelAdmin):
    inlines = [TransscriptionInline]
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

