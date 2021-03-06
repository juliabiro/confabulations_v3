from ..models import Participant, AnalysisType, AnalysisPoint
from ..utils.connection_helpers import ParticipantConnectionBuilder, UnconnectedStoryFinder
from ..utils.media_helpers import get_graph_url

# todo move this out from here
def sidebar_left_context():
    ret = {}
    participants = Participant.objects.all()
    participant_list = [{"name": p.name,
                        "link": p.get_absolute_url()
    } for p in participants]
    ret['participants'] = participant_list

    taxonomy_types = AnalysisType.objects.all().exclude(name='Connects')

    taxonomy =[]
    for t in taxonomy_types:
        ap_list = AnalysisPoint.objects.filter(analysis_type_id=t.id).order_by('order_in_menu')

        # populate submenu items
        ap_list_by_type = [{"name": ap.name,
                            "link": ap.get_absolute_url(),
                            "color_code": ap.color_code} for ap in ap_list]
        taxonomy.append({'name':t.name, 'url':t.get_absolute_url(), 'ap_list': ap_list_by_type})

    ret['taxonomy'] = taxonomy

    return ret

def sidebar_right_context(participant_id):
    ret = {}
    intraBuilder = ParticipantConnectionBuilder(participant_id, 'Intraconnection')
    interBuilder = ParticipantConnectionBuilder(participant_id, 'Interconnection')

    intrachains = intraBuilder.buildchains()
    interchains = interBuilder.buildchains()

    chainless_themes_intra = intraBuilder.buildchainlessthemes()
    chainless_themes_inter = interBuilder.buildchainlessthemes()

    unconnectedStoryFinder = UnconnectedStoryFinder(participant_id)
    single_stories = unconnectedStoryFinder.buildsinglestories()
    ret['interconnections'] = interchains
    ret['intraconnections'] = intrachains
    ret['chainless_themes_inter'] = chainless_themes_inter
    ret['chainless_themes_intra'] = chainless_themes_intra


    ret['graph_url'] = get_graph_url(participant_id)
    ret['graph_link'] = '/graph/{}/'.format(participant_id)

    if single_stories:
        ret['single_stories'] = single_stories

    return ret

