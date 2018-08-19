from ..models import Participant

# todo move this out from here
def sidebar_context():
    participants = Participant.objects.all()
    participant_list = [{"name": p.name,
                         "link": p.get_absolute_url()
    } for p in participants]

    return {"participants": participant_list}
