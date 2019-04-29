from string import Template
from ..models import Story, Participant, Theme
from .connection_helpers import ParticipantConnectionBuilder, ChainWithThemes, ThemeWithStories

# first, a big set of helper functions generating the code snippets belonging to nodes, edges and groups

COLORS ={'4':'red','5':'green', '7':'blue', '8':'olive', '9':'purple', '10':'lime', '11':'teal', '3':'gray'}

OBJECT_TYPE_PREFIXES={
    'Story': '10',
    'Participant': '20',
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

def sanitize_name(name):
    return name.replace('/', '__').replace("'","-")

def chain_node(participant, chain):
    node = Template("{id: $id, label:'$label', url: '$url', group: 'chain', color: '$color',size: 50, mass: 0.1}").substitute(id=get_unique_node_id(chain), label=sanitize_name(chain.name), url=chain.get_absolute_url(), color=COLORS[str(participant.id)])
    return node

def theme_node(participant, theme):
    node = Template("{id: $id, label:'$label', url: '$url', group: 'theme', color: '$color',size: 25, mass:0.2}").substitute(id=get_unique_node_id(theme), label=sanitize_name(theme.name), url=theme.get_absolute_url(), color=COLORS[str(participant.id)])
    return node

def story_node(participant, story):
    node = Template("{ id: $id, label: '$label', url: '$url', group: 'story_$group',size:12, mass:0.5}").substitute(id=get_unique_node_id(story), label=story.name, url=story.get_absolute_url(), group=participant.name.replace(' ','_'))
    return node

def participant_node(participant):
    node = Template("{id: $id, label:'$label', url: '$url', group: 'participant_$group', color: '$color', size: 75, mass: 0.01}").substitute(id=get_unique_node_id(participant), label=participant.name, url=participant.get_absolute_url(), color=COLORS[str(participant.id)], group=participant.name.replace(' ','_'))
    return node

def story_to_story_edge(story1, story2):
    edge= Template("{to: $to, from:$fromm}").substitute(to=get_unique_node_id(story1), fromm=get_unique_node_id(story2))
    return edge

def story_to_participant_edge(participant, story):
    edge= Template("{to: $to, from:$fromm}").substitute(to=get_unique_node_id(story), fromm=get_unique_node_id(participant))
    return edge

def story_to_theme_edge(theme, story):
    edge= Template("{to: $to, from:$fromm}").substitute(to=get_unique_node_id(story), fromm=get_unique_node_id(theme))
    return edge

def theme_to_chain_edge(theme, chain):
    edge= Template("{to: $to, from:$fromm}").substitute(to=get_unique_node_id(chain), fromm=get_unique_node_id(theme))
    return edge

def story_group(participant=None):
    color = COLORS[(str(participant.id))] if participant is not None else 'red'
    return Template("story_$name: { color: '$color',font: '25px arial black', shape: 'dot',}").substitute(name=participant.name.replace(" ", "_"), color=color)

def theme_group(participant=None):
    color = COLORS[(str(participant.id))] if participant is not None else 'aqua'
    return Template("theme: { color: '$color',font: '25px arial black', shape: 'triangle',}").substitute( color=color)

def chain_group(participant=None):
    color = COLORS[(str(participant.id))] if participant is not None else 'maroon'
    return Template("chain: { color: '$color',font: '25px arial black', shape: 'hexagon',}").substitute(color=color)

def participant_group(participant):
    return Template("participant_$name: {color: '$color', font: '25px arial black', shape: 'ellipse',}").substitute(name=participant.name.replace(' ','_'), color=COLORS[str(participant.id)])

def data_to_script(data):
    return ',\n'.join(list(set(data)))

# collector functions
def story_to_participant_edges(participant):
    stories = Story.objects.filter(participant__id=participant.id).distinct()

    edges = data_to_script([
        story_to_participant_edge(participant, s) for s in stories
    ])

    return edges

def collect_participant_story_connections(participant):
    builder = ParticipantConnectionBuilder(participant, 'Intraconnection')
    pairs = builder.buildstoryconnections()
    stories = builder.getstoriesinconnections()

    # using template strings https://docs.python.org/3/library/string.html#template-strings
    # because in normal format, the ':' is for identifiers and it is really hard to escape it
    node_list = [story_node(participant, s) for s in stories]

    edge_list = [story_to_story_edge(p.story1, p.story2) for p in pairs]
    group= story_group(participant)

    return node_list, edge_list, group


def participant_story_connections(participant):
    n, e, g = collect_participant_story_connections(participant)

    node_list = data_to_script(n)
    edge_list = data_to_script(e)
    group = data_to_script(g)
    return node_list, edge_list, group


# bug function getting all parts necessary
def collect_participant_chains_themes_stories(participant):
    participant_id = participant.id
    intraBuilder = ParticipantConnectionBuilder(participant_id, 'Intraconnection')
    interBuilder = ParticipantConnectionBuilder(participant_id, 'Interconnection')
    intrachains = intraBuilder.buildchains()
    interchains = interBuilder.buildchains()

    chainless_themes_intra = intraBuilder.buildchainlessthemes()
    chainless_themes_inter = interBuilder.buildchainlessthemes()

    stories = []
    chains = []
    themes = []

    # edges can be built on the fly
    # stories, themes and chains are collected and processed into nodes later
    # this collection doesn't try to skip duplicates, eg the story-to-participant edge is added with every story.
    # the duplicates are skipped later by turning these collections into sets.
    edges=[]

    cc = []
    tt = []
    for c in interchains, intrachains:
        if c:
            cc.extend(c)

    for t in chainless_themes_inter, chainless_themes_intra:
        if t:
            tt.extend(t)

    for c in cc:
        chains.append(c.chain)
        for t in c.themes:
            themes.append(t.theme)
            edges.append(theme_to_chain_edge(t.theme,c.chain))
            for s in t.stories:
                stories.append(s)
                edges.append(story_to_theme_edge(s,t.theme))

    for t in tt:
        themes.append(t.theme)
        for s in t.stories:
            stories.append(s)
            edges.append(story_to_theme_edge(s,t.theme))

    nodes=[ story_node(participant, s) for s in list(set(stories))]
    nodes.extend([theme_node(participant, t) for t in list(set(themes))])
    nodes.extend([chain_node(participant, c) for c in list(set(chains))])



    builder = ParticipantConnectionBuilder(participant, 'Intraconnection')
    pairs = builder.buildstoryconnections()
    stories_in_connections = builder.getstoriesinconnections()

    for s in stories_in_connections:
        nodes.append(story_node(participant, s))

    for p in pairs:
        edges.append(story_to_story_edge(p.story1, p.story2))

    groups=[story_group(participant), theme_group(), chain_group()]

    return nodes, edges, groups

def participant_chains_themes_stories(participant):

    n, e, g = collect_participant_chains_themes_stories(participant)

    node_list = data_to_script(n)
    edge_list = data_to_script(e)
    groups = data_to_script(g)
    return node_list, edge_list, groups


