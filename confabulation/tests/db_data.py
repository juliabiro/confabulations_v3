from confabulation.models import Participant, ParticipantTypes, Gender, Story, Photo, AnalysisPoint, AnalysisType, Keyword, Era, Theme, Chain, StoryToStoryConnection, StoryInTheme, ThemeInChain

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
THEME_INTER_ID = 1
THEME_INTRA_ID = 2
CHAIN_INTER_ID = 1
CHAIN_INTRA_ID = 2

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
                      AnalysisType(name='Going Beyond',
                                   id=3),
                      AnalysisType(name='Connects',
                                   id=4),
    ]

    analysis_points = [AnalysisPoint(name='analysis_point1',
                                     id=ANALYSIS_POINT_ID),
                       AnalysisPoint(name='analysis_point2',
                                     id=2),
                       AnalysisPoint(name="alma_point",
                                     id=3),
                       AnalysisPoint(name="Short Confabulation",
                                     order_in_menu=2,
                                     id=4),
                       AnalysisPoint(name="korte_point",
                                     id=5),
                       AnalysisPoint(name="inner",
                                     id=6),
                       AnalysisPoint(name="Long Confabulation",
                                     order_in_menu=1,
                                     id=7)]

    keywords = [Keyword(name='keyword1', id=1),
                Keyword(name='keyword2', id=2),
                Keyword(name='keyword3', id=3)]

    themes = [Theme(name='Theme 1', connection_range='Interconnection', id=THEME_INTER_ID),
            Theme(name='Theme 2', connection_range='Intraconnection', id=THEME_INTRA_ID),
              Theme(name='Theme 3', connection_range='Intraconnection', id=3)]

    chains = [Chain(name='Chain 1',connection_range='Interconnection', id=CHAIN_INTER_ID),
              Chain(name='Chain 2', connection_range='Intraconnection', id=CHAIN_INTRA_ID)]

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
    analysis_points[5].analysis_type = analysis_types[3]
    analysis_points[6].analysis_type = analysis_types[2]

    for ap in analysis_points:
        ap.save()

    for k in keywords:
        k.save()

    for theme in themes:
        theme.save()

    for chain in chains:
        chain.save()

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

    masik_participant=Participant(name="Masik Participant", id=PARTICIPANT_ID+1)
    masik_participant.save()

    external_story=Story(name='external story', participant=masik_participant, id=16)
    external_story.save()
    # creating the themes
    inter_theme=Theme.objects.get(id=THEME_INTER_ID)
    s1=StoryInTheme(story=valid_story, theme=inter_theme, number=1).save()
    s2=StoryInTheme(story=external_story, theme=inter_theme, number=2).save()

    intra_theme=Theme.objects.get(id=THEME_INTRA_ID)
    StoryInTheme(story=valid_story, theme=intra_theme, number=3).save()
    StoryInTheme(story=harmadik_story, theme=intra_theme, number=4).save()
    intra_theme.save()

    inter_chain=Chain.objects.get(id=CHAIN_INTER_ID)
    ThemeInChain(theme=inter_theme, chain=inter_chain, number=1).save()
    intra_chain=Chain.objects.get(id=CHAIN_INTRA_ID)
    ThemeInChain(theme=intra_theme, chain=intra_chain, number=1).save()
    ThemeInChain(theme=Theme.objects.get(id=3), chain=intra_chain, number=2).save()


def create_connections_data():
    p1 = Participant.objects.create(name="Test Bela",
                              id=PARTICIPANT_ID)
    p2 = Participant.objects.create(name="Test Bela 2",
                                id=PARTICIPANT_ID+1)

    ## data structure
    ## p1: s1, s2, s5
    ## p2: s3, s4, s6

    ## t1 intra s1, s2,
    ## t4 intra s5,
    ## t2 intra s3, s4
    ## t3 inter s2, s3

    ## c1 intra t1, t2
    ## c2 inter t1, t3

    ## s2s: s1, s5

    ## single story: s6

    s1=Story.objects.create(name='story1', id=1, participant=p1)
    s2=Story.objects.create(name='story2', id=2, participant=p1)
    s3=Story.objects.create(name='story3', id=3, participant=p2)
    s4=Story.objects.create(name='story4', id=4, participant=p2)
    s5=Story.objects.create(name='story5', id=5, participant=p1)
    s6=Story.objects.create(name='story6', id=6, participant=p2)

    t1=Theme.objects.create(name='Theme1', id=1, connection_range='Intraconnection')
    t2=Theme.objects.create(name='Theme2', id=2, connection_range='Intraconnection')
    t3=Theme.objects.create(name='Theme3', id=3, connection_range='Interconnection')
    t4=Theme.objects.create(name='Theme4', id=4, connection_range='Intraconnection')

    c1=Chain.objects.create(name='Chain1', id=1, connection_range='Intraconnection')
    c2=Chain.objects.create(name='Chain2', id=2, connection_range='Interconnection')

    StoryInTheme.objects.create(theme=t1, story=s1, number=1)
    StoryInTheme.objects.create(theme=t1, story=s2, number=2)
    StoryInTheme.objects.create(theme=t4, story=s5, number=1)
    StoryInTheme.objects.create(theme=t2, story=s3, number=1)
    StoryInTheme.objects.create(theme=t2, story=s4, number=2)
    StoryInTheme.objects.create(theme=t3, story=s2, number=1)
    StoryInTheme.objects.create(theme=t3, story=s3, number=2)

    ThemeInChain.objects.create(chain=c1, theme=t1, number=1)
    ThemeInChain.objects.create(chain=c1, theme=t2, number=2)
    ThemeInChain.objects.create(chain=c2, theme=t3, number=1)
    ThemeInChain.objects.create(chain=c2, theme=t4, number=2)

    StoryToStoryConnection.objects.create(story1=s1, story2=s5)
