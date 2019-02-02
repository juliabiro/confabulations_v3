from ..models import Participant, AnalysisType, AnalysisPoint
from ..utils.connection_helpers import ParticipantConnectionBuilder,UnconnectedStoryFinder

# todo move this out from here
def sidebar_left_context():
    ret = {}
    participants = Participant.objects.all()
    participant_list = [{"name": p.name,
                        "link": p.get_absolute_url()
    } for p in participants]
    ret['participants'] = participant_list

    taxonomy_types = AnalysisType.objects.all().exclude(name='Connects')

    taxonomy = {}
    for t in taxonomy_types:
        taxonomy [t.name] = []
        ap_list = AnalysisPoint.objects.filter(analysis_type_id=t.id).order_by('order_in_menu')

        # populate submenu items
        ap_list_by_type = [{"name": ap.name,
                            "link": ap.get_absolute_url(),
                            "color_code": ap.color_code} for ap in ap_list]
        taxonomy[t.name] = ap_list_by_type

    ret['taxonomy'] = taxonomy

    return ret

def sidebar_right_context(participant_id):
    ret = {}
    intraBuilder = ParticipantConnectionBuilder(participant_id, 'Intraconnection')
    interBuilder = ParticipantConnectionBuilder(participant_id, 'Interconnection')

    intrachains = intraBuilder.buildchains()
    interchains = interBuilder.buildchains()

    chainless_themes = intraBuilder.buildthemes()

    unconnectedStoryFinder = UnconnectedStoryFinder(participant_id)
    single_stories = unconnectedStoryFinder.buildsinglestories()
    ret['interconnections'] = interchains
    ret['intraconnections'] = intrachains
    ret['chainless_themes'] = chainless_themes

    if single_stories:
        ret['single_stories'] = single_stories

    return ret

