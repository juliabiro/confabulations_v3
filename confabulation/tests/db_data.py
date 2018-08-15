from confabulation.models import Participant, ParticipantTypes, Gender, Story, Photo, AnalysisPoint, AnalysisType, Keyword, Era

ERAS = [Era(name="era1", id=1),
        Era(name="era2", id=2)]

PHOTOS = [Photo(name='photo1',
                file_url='/TEST01.jpg',
                id=1),
          Photo(name='photo2',
                file_url='/PHOTO_2',
                id=2),
          Photo(name='photo3',
                file_url='/photo_3',
                id=3)]

ANALYSIS_TYPES = [AnalysisType(name='analysis_type1',
                               id=1),
                  AnalysisType(name='analysis_type2',
                               id=2)]

ANALYSIS_POINTS = [AnalysisPoint(name='analysis_point1',
                                 analysis_type=ANALYSIS_TYPES[0],
                                 id=1),
                   AnalysisPoint(name='analysis_point2',
                                 analysis_type=ANALYSIS_TYPES[1],
                                 id=2)]

PARTICIPANT = Participant(name="Test Bela",
                          profile="test profile",
                          participation_group=ParticipantTypes.photographer,
                          gender=Gender.female,
                          id=1)

KEYWORDS = [Keyword(name='keyword1', id=1),
            Keyword(name='keyword2', id=2),
            Keyword(name='keyword3', id=3)]

STORIES = [Story(name="Test Bela",
                 participant=Participant.objects.get(pk=1),
                 photos=Photo.objects.all(),
                 order_in_recording=2,
                 video_url='/TEST01.mp4',
                 analysis=AnalysisPoint.objects.all(),
                 era=Era.objects.all(),
                 notes="sometext",
                 keywords=Keyword.objects.all(),
                 id=1),
           Story(name="Test Bela",
                 participant=Participant.objects.get(pk=1),
                 photos=Photo.objects.all(),
                 order_in_recording=2,
                 video_url='/invalid_video.mp4',
                 analysis=AnalysisPoint.objects.all(),
                 era=Era.objects.all(),
                 notes="story 2 with invalid video",
                 keywords=Keyword.objects.all(),
                 id=2)]

def populate_db():
    for e in ERAS:
        e.save()
    for p in PHOTOS:
        p.save()
    for at in ANALYSIS_TYPES:
        at.save()
    for ap in ANALYSIS_POINTS:
        ap.save()
        PARTICIPANT.save()
    for k in KEYWORDS:
        k.save()
    for s in STORIES:
        s.save()

