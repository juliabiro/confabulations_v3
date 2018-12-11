from ..models import Participant, AnalysisType, AnalysisPoint

# todo move this out from here
def sidebar_context(sidebar_participants, sidebar_taxonomy):
    ret = {}
    if sidebar_participants:
        participants = Participant.objects.all()
        participant_list = [{"name": p.name,
                            "link": p.get_absolute_url()
        } for p in participants]
        ret['participants'] = participant_list

    if sidebar_taxonomy:
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
