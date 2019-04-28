from string import Template
from .connection_helpers import ParticipantConnectionBuilder

COLORS ={'4':'red','5':'green', '7':'blue', '8':'olive', '9':'purple', '10':'lime', '11':'teal', '3':'gray'}

OBJECT_TYPE_PREFIXES={
    'Story': '10',
    'Particant': '20',
    'Theme': '30',
    'Chain': '40',
    'AnalysisPoint':'50',
    'AnalysisType': '60',
}

# The problem this function solves is that the id of the objects in the database cannot be used as ids for the nodes, because the ids are not unique across all objects (there is a Story with id=3 and there is a Participant with id=3 etc.). Therefore if we want to create graphs from different objects, we need to create ids in a different way.
# Solution: prepend object id-s with prefixes unique to types (after expanding them to be uniform in length)
def get_unique_node_id(node):
    typ = type(node).__name__
    postfix = str(node.id).zfill(4)
    return OBJECT_TYPE_PREFIXES[typ]+postfix


def participant_story_connections(participant):
    builder = ParticipantConnectionBuilder(participant, 'Intraconnection')
    pairs = builder.buildstoryconnections()
    stories = builder.getstoriesinconnections()

    # using template strings https://docs.python.org/3/library/string.html#template-strings
    # because in normal format, the ':' is for identifiers and it is really hard to escape it

    node_list = ','.join(
        [Template("{ id: $id, label: '$label', url: '$url', group: '$group',}").substitute(id=get_unique_node_id(s), label=s.name, url=s.get_absolute_url(), group=participant.name.replace(' ','_')) for s in stories]
    )

    # whoops, from is a reserved keyword :)
    edge_list = ','.join([
        Template("{ from: $fromm, to: $to}").substitute(fromm=get_unique_node_id (p.story1), to=get_unique_node_id(p.story2)) for p in pairs]
    )

    group= Template("$name: { color: '$color', font: '25px arial black', shape: 'dot',}").substitute(name=participant.name.replace(" ", "_"), color=COLORS[str(participant.id)])

    return node_list, edge_list, group
