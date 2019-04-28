from string import Template
from .connection_helpers import ParticipantConnectionBuilder

COLORS ={'4':'red','5':'green', '7':'blue', '8':'olive', '9':'purple', '10':'lime', '11':'teal', '3':'gray'}

def participant_story_connections(participant):
    builder = ParticipantConnectionBuilder(participant, 'Intraconnection')
    pairs = builder.buildstoryconnections()
    stories = builder.getstoriesinconnections()

    # using tenplate strings https://docs.python.org/3/library/string.html#template-strings
    # because in normal format, the ':' is for identifiers and it is really hard to escape it

    node_list = ','.join(
        [Template("{ id: $id, label: '$label', url: '$url', group: '$group',}").substitute(id=s.id, label=s.name, url=s.get_absolute_url(), group=participant.name.replace(' ','_')) for s in stories]
    )

    # whoops, from is a reserved keyword :)
    edge_list = ','.join([
        Template("{ from: $fromm, to: $to}").substitute(fromm=p.story1.id, to=p.story2.id) for p in pairs]
    )

    group= Template("$name: { color: $color, font: '25px arial black', shape: 'dot',}").substitute(name=participant.name.replace(" ", "_"), color=COLORS[str(participant.id)])

    return node_list, edge_list, group
