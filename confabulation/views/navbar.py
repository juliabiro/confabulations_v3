from ..models import ParticipantTypes, Participant, AnalysisType, AnalysisPoint

def navigation_context():
    context = {'participants':{},
               'taxonomy':{},
               'confabulation':[]
              }

    participant_types = ParticipantTypes.choices()
    for pt in participant_types:
        pt_name = pt[0]
        plist = Participant.objects.filter(participation_group=pt_name)
        p_by_type = [{"name": p.name, "link": p.get_absolute_url()} for p in plist]
        context['participants'][pt_name] = p_by_type

    taxonomy_types = AnalysisType.objects.all()
    for t in taxonomy_types:
        context['taxonomy'][t.name] = []
        ap_list = AnalysisPoint.objects.filter(analysis_type_id=t.id)

        ap_list_by_type = [{"name": ap.name,
                           "link": ap.get_absolute_url()} for ap in ap_list]
        context['taxonomy'][t.name] = ap_list_by_type

    confab_types = AnalysisType.objects.filter(name='Confabulation')
    if confab_types.count()>0:
        confab_points = AnalysisPoint.objects.filter(analysis_type_id=confab_types[0].id)
        confabulation_points = [{"name": ap.name, 'link': ap.get_absolute_url()} for ap in confab_points]
        context['confabulation'] = confabulation_points

    return context

