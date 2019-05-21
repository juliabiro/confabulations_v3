from ..models import ParticipantTypes, Participant, AnalysisType, AnalysisPoint, Connection

SPECIAL_ANALYSIS_TYPES=['Going Beyond']

def navigation_context():
    context = {'participants':{},
               'taxonomy':{},
               'confabulation':[],
               'connects': [],
               'graphs':[],
              }

    participants = Participant.objects.distinct().order_by('name')
    context['participants'] = [{'name':p.name, 'url':p.get_absolute_url()} for p in participants]


    taxonomy_types = AnalysisType.objects.all().exclude(name='Connects')

    for t in taxonomy_types:
        context['taxonomy'][t.name] = []
        ap_list = AnalysisPoint.objects.filter(analysis_type_id=t.id).order_by('order_in_menu')

        # populate submenu items
        ap_list_by_type = [{"name": ap.name,
                           "link": ap.get_absolute_url()} for ap in ap_list]
        context['taxonomy'][t.name] = ap_list_by_type

    connection_types = Connection.objects.distinct()
    for ct in connection_types:
        context['connects'].append({'name': ct.name,
                                    'link': ct.get_absolute_url()})

    for special in SPECIAL_ANALYSIS_TYPES:

        special_types = AnalysisType.objects.filter(name=special)
        if special_types.count()>0:
            special_points = AnalysisPoint.objects.filter(analysis_type_id=special_types[0].id).order_by('order_in_menu')
            special_points_links = [{"name": ap.name, 'link': ap.get_absolute_url()} for ap in special_points]
            context_name = special.lower()

            # an even more special menu item
            if special =="Going Beyond":
                context_name = 'confabulation'
                special_points_links =special_points_links[:2]

            context[context_name] = special_points_links

    context['graphs'] = [{'name':p.name, 'url': '/graph/'+str(p.id)+'/'} for p in participants]

    context['graphs'].append({'name': 'all connections', 'url': '/graph/'})
    return context

