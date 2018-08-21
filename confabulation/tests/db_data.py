from confabulation.models import Participant, ParticipantTypes, Gender, Story, Photo, AnalysisPoint, AnalysisType, Keyword, Era

VALID_STORY_ID = 1
INVALID_STORY_ID = 2
PARTICIPANT_ID = 1
VALID_VIDEO_NAME = 'TEST01.mp4'
INVALID_VIDEO_NAME = 'JULI.mp4'
VALID_PHOTO_NAME = 'TEST01.jpg'
MISSING_PHOTO_NAME = 'TEST100.jpg'
INVALID_PHOTO_NAME = 'PHOTO_2'
MALFORMED_PHOTO_NAME = 'photo_3'
ANALYSIS_POINT_ID = 1
ANALYSIS_TYPE_ID = 1

def populate_db():
    eras = [Era(name="era1", id=1),
            Era(name="era2", id=2)]

    photos = [Photo(name=VALID_PHOTO_NAME,
                    file_url='/'+VALID_PHOTO_NAME,
                    id=1),
              Photo(name=INVALID_PHOTO_NAME,
                    file_url='/'+INVALID_PHOTO_NAME,
                    id=2),
              Photo(name=MISSING_PHOTO_NAME,
                    file_url='/'+MISSING_PHOTO_NAME,
                    id=3),
              Photo(name=MALFORMED_PHOTO_NAME,
                    file_url='/'+MALFORMED_PHOTO_NAME,
                    id=4)]

    analysis_types = [AnalysisType(name='analysis_type1',
                                   id=ANALYSIS_TYPE_ID),
                      AnalysisType(name='analysis_type2',
                                   id=2),
                      AnalysisType(name='Confabulation',
                                   id=3)]

    analysis_points = [AnalysisPoint(name='analysis_point1',
                                     id=ANALYSIS_POINT_ID),
                       AnalysisPoint(name='analysis_point2',
                                     id=2),
                       AnalysisPoint(name="alma_point",
                                     id=3),
                       AnalysisPoint(name="Short Confabulation",
                                     id=4),
                       AnalysisPoint(name="korte_point",
                                     id=5)]

    keywords = [Keyword(name='keyword1', id=1),
                Keyword(name='keyword2', id=2),
                Keyword(name='keyword3', id=3)]

    for e in eras:
        e.save()
    for p in photos:
        p.save()
    for at in analysis_types:
        at.save()

    analysis_points[0].analysis_type = analysis_types[0]
    analysis_points[1].analysis_type = analysis_types[1]
    analysis_points[2].analysis_type = analysis_types[0]
    analysis_points[3].analysis_type = analysis_types[2]
    analysis_points[4].analysis_type = analysis_types[0]

    for ap in analysis_points:
        ap.save()

    for k in keywords:
        k.save()

    participant = Participant(name="Test Bela",
                              id=PARTICIPANT_ID)
    participant.profile = "test profile"
    participant.participation_group = ParticipantTypes.photographer
    participant.gender = Gender.female
    participant.save()


    # creating the stories
    valid_story = Story.objects.create(name='elso story', id=VALID_STORY_ID)
    valid_story.participant = participant
    valid_story.photos.add(photos[0])
    valid_story.order_in_recording = 2
    valid_story.video_url = '/'+VALID_VIDEO_NAME
    valid_story.analysis.add(analysis_points[0])
    valid_story.era.add(eras[0])
    valid_story.era.add(eras[1])
    valid_story.notes = "sometext"
    valid_story.keywords.add(Keyword.objects.get(pk=1))
    valid_story.save()

    invalid_story = Story.objects.create(name='masodik story', id=INVALID_STORY_ID)
    invalid_story.participant = participant
    invalid_story.photos.add(photos[1])
    invalid_story.photos.add(photos[2])
    invalid_story.photos.add(photos[3])
    invalid_story.order_in_recording = 2
    invalid_story.video_url = INVALID_VIDEO_NAME
    invalid_story.era.add(eras[0])
    invalid_story.notes = "invalid notes"
    invalid_story.keywords.add(keywords[1])
    invalid_story.keywords.add(keywords[2])
    invalid_story.save()

    harmadik_story = Story.objects.create(name='harmadik story', id=15)
    harmadik_story.participant = participant
    harmadik_story.save()
