from ..models import ParticipantTypes, Participant, AnalysisType, AnalysisPoint

SPECIAL_ANALYSIS_TYPES=['Going Beyond', 'Connects']

def navigation_context():
    context = {'participants':{},
               'taxonomy':{},
               'confabulation':[],
               'connects': []
              }

    participant_types = ParticipantTypes.choices()
    for pt in participant_types:
        pt_name = pt[0]
        plist = Participant.objects.filter(participation_group=pt_name)
        p_by_type = [{"name": p.name, "link": p.get_absolute_url()} for p in plist]
        context['participants'][pt_name] = p_by_type

    taxonomy_types = AnalysisType.objects.all().exclude(name='Connects')

    for t in taxonomy_types:
        context['taxonomy'][t.name] = []
        ap_list = AnalysisPoint.objects.filter(analysis_type_id=t.id).order_by('order_in_menu')

        # populate submenu items
        ap_list_by_type = [{"name": ap.name,
                           "link": ap.get_absolute_url()} for ap in ap_list]
        context['taxonomy'][t.name] = ap_list_by_type

    for special in SPECIAL_ANALYSIS_TYPES:

        special_types = AnalysisType.objects.filter(name=special)
        if special_types.count()>0:
            special_points = AnalysisPoint.objects.filter(analysis_type_id=special_types[0].id).order_by('order_in_menu')
            special_points_links = [{"name": ap.name, 'link': ap.get_absolute_url()} for ap in special_points]
            context_name = special.lower()
            if special =="Going Beyond":
                context_name = 'confabulation'
            context[context_name] = special_points_links

    return context

