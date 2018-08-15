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
                                   id=1),
                      AnalysisType(name='analysis_type2',
                                   id=2)]

    analysis_points = [AnalysisPoint(name='analysis_point1',
                                     analysis_type=analysis_types[0],
                                     id=1),
                       AnalysisPoint(name='analysis_point2',
                                     analysis_type=analysis_types[1],
                                     id=2)]

    keywords = [Keyword(name='keyword1', id=1),
                Keyword(name='keyword2', id=2),
                Keyword(name='keyword3', id=3)]

    for e in eras:
        e.save()
    for p in photos:
        p.save()
    for at in analysis_types:
        at.save()


    for counter, value in enumerate(analysis_points):
        value.analysis_type = analysis_types[counter]
        value.save()


    for k in keywords:
        k.save()
    participant = Participant(name="Test Bela",
                              id=PARTICIPANT_ID)
    participant.profile = "test profile"
    participant.participation_group = ParticipantTypes.photographer
    participant.gender = Gender.female
    participant.save()


    # creating the stories
    valid_story = Story.objects.create(name='Test Bela', id=VALID_STORY_ID)
    valid_story.participant = participant
    valid_story.photos.add(photos[0])
    valid_story.order_in_recording = 2
    valid_story.video_url = '/'+VALID_VIDEO_NAME
    valid_story.analysis.add(analysis_points[0])
    valid_story.era.add(eras[0])
    valid_story.era.add(eras[1])
    valid_story.notes = "sometext"
    valid_story.keywords.add(keywords[0])
    valid_story.save()

    invalid_story = Story.objects.create(name='invalid lajos', id=INVALID_STORY_ID)
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
