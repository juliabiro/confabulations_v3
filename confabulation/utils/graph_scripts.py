from string import Template
from ..models import Story, Participant, Theme
from .connection_helpers import ParticipantConnectionBuilder, ChainWithThemes, ThemeWithStories

# first, a big set of helper functions generating the code snippets belonging to nodes, edges and groups

COLORS ={'4':'red','5':'green', '7':'blue', '8':'olive', '9':'purple', '10':'lime', '11':'teal', '3':'gray', 'Theme': '#4925FE', 'Chain': '#1A0584', 'Inter': '#f5cd06', 'story2story': '#745AF9'}

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
    return name.replace(' ', '_')

def sanitize_string(name):
    return name.replace('/', '__').replace("'","-")

def chain_node(chain, participant=None, is_inter=False):
    group = "chain"
    if is_inter is True:
        group = "chain_inter"
    if participant is not None:
        group = "chain_"+str(participant.id)

    node = Template("{ id: $id, label: '$label', url: '$url', group: '$group'}").substitute(id=get_unique_node_id(chain), label=sanitize_string(chain.name), url=chain.get_absolute_url(), group=group )
    return node

def theme_node(theme, is_inter=False):
    node = Template("{ id: $id, label: '$label', url: '$url', group: '$group'}").substitute(id=get_unique_node_id(theme), label=sanitize_string(theme.name), url=theme.get_absolute_url(), group="theme_inter" if is_inter is True else "theme")
    return node

def story_node(participant, story):
    node = Template("{ id: $id, label: '$label', url: '$url', group: 'story_$group'}").substitute(id=get_unique_node_id(story), label=story.name, url=story.get_absolute_url(), group=sanitize_name(participant.name))
    return node

def participant_node(participant):
    node = Template("{ id: $id, label: '$label', url: '$url', group: 'participant_$group', color: '$color', size: 75}").substitute(id=get_unique_node_id(participant), label=participant.name, url=participant.get_absolute_url(), color=COLORS[str(participant.id)], group=sanitize_name(participant.name))
    return node

def story_to_story_edge(story1, story2):
    edge= Template("{ to: $to, from: $fromm, color: { color: '$color' } }").substitute(to=get_unique_node_id(story1), fromm=get_unique_node_id(story2), color=COLORS['story2story'])
    return edge

def story_to_participant_edge(participant, story):
    edge= Template("{ to: $to, from: $fromm }").substitute(to=get_unique_node_id(story), fromm=get_unique_node_id(participant))
    return edge

def story_to_theme_edge(story, theme, is_inter=False):
    edge= Template("{ to: $to, from: $fromm, $set_color }").substitute(to=get_unique_node_id(theme), fromm=get_unique_node_id(story), set_color="color: { color: '"+COLORS['Inter']+"', highlight: '"+COLORS['Inter']+"'}" if is_inter is True else "color: {inherit: 'to'}")
    return edge

def theme_to_chain_edge(theme, chain, is_inter=False):
    edge= Template("{ to: $to, from: $fromm, $set_color }").substitute(to=get_unique_node_id(chain), fromm=get_unique_node_id(theme), set_color=("color: { color: '"+COLORS['Inter']+"', highlight: '"+COLORS['Inter']+"'}" if is_inter is True else "color: { inherit: 'to' }"))
    return edge

def story_group(participant=None):
    color = COLORS[(str(participant.id))] if participant is not None else 'red'
    return Template("story_$name: { color: '$color', font: '25px arial black', shape: 'dot', size: 25}").substitute(name=sanitize_name(participant.name), color=color)

def chain_group(is_inter=False, participant=None):
    border_color=COLORS['Chain']
    group_name = "chain"
    background_color=COLORS['Chain']
    if is_inter is True:
        background_color=COLORS['Inter']
        group_name= "chain_inter"
    if participant is not None:
        background_color=COLORS[str(participant.id)]
        group_name = "chain_"+str(participant.id)

    return Template("$group: { $color, font: '25px arial black', shape: 'dot', size: 100, borderWidth: 3 }").substitute(
        group=group_name,
        color="color: { background: '"+background_color+"', highlight: { border: '"+border_color+"', background: '"+background_color+"'}, border: '"+border_color+"' }" if is_inter is True else "color: '"+background_color+"'")

def theme_group(is_inter=False):
    return Template("$group: {$color, font: '25px arial black', shape: 'triangle', size: 50, borderWidth: 3 }").substitute(
        group="theme_inter" if is_inter is True else "theme",
        color="color: { background: '"+COLORS['Inter']+"', highlight: {background: '"+COLORS['Inter']+"', border: '"+COLORS['Theme']+"' }, border: '"+COLORS['Theme']+"' }" if is_inter is True else "color: '{}' ".format(COLORS['Theme']))

def participant_group(participant):
    return Template("participant_$name: { color: '$color', font: '25px arial black', shape: 'ellipse' }").substitute(name=sanitize_name(participant.name), color=COLORS[str(participant.id)])

def data_to_script(data):
    return ',\n'.join(sorted(list(set(data))))

# collector functions
def collect_story_to_participant_edges(participant):
    stories = Story.objects.filter(participant__id=participant.id).distinct()

    edges = [story_to_participant_edge(participant, s) for s in stories]

    return edges

def collect_participant_story_connections(participant):
    builder = ParticipantConnectionBuilder(participant, 'Intraconnection')
    pairs = builder.buildstoryconnections()
    stories = builder.getstoriesinconnections()

    # using template strings https://docs.python.org/3/library/string.html#template-strings
    # because in normal format, the ':' is for identifiers and it is really hard to escape it
    node_list = [story_node(participant, s) for s in stories]

    edge_list = [story_to_story_edge(p.story1, p.story2) for p in pairs]
    groups= [story_group(participant)]

    return node_list, edge_list, groups


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
    intra_chains = []
    inter_chains = []
    intra_themes = []
    inter_themes = []

    # edges can be built on the fly
    # stories, themes and chains are collected and processed into nodes later
    # this collection doesn't try to skip duplicates, eg the story-to-participant edge is added with every story.
    # the duplicates are skipped later by turning these collections into sets.
    edges=[]

    # cc = []
    # tt = []
    # for c in interchains, intrachains:
    #     if c:
    #         cc.extend(c)

    # for t in chainless_themes_inter, chainless_themes_intra:
    #     if t:
    #         tt.extend(t)

    # for c in cc:
    #     for t in c.themes:
    #         for s in t.stories:
    #             stories.append(s)

    # for t in tt:
    #     for s in t.stories:
    #         stories.append(s)

    # add edges separately, because we want to color them differently by connection_rage
    for c in intrachains:
        intra_chains.append(chain_node(c.chain, participant))
        for t in c.themes:
            intra_themes.append(theme_node(t.theme))
            edges.append(theme_to_chain_edge(t.theme, c.chain))
            for s in t.stories:
                stories.append(s)
                edges.append(story_to_theme_edge(s, t.theme))
    for t in chainless_themes_intra:
        intra_themes.append(theme_node(t.theme))
        for s in t.stories:
            stories.append(s)
            edges.append(story_to_theme_edge(s, t.theme))

    for c in interchains:
        inter_chains.append(chain_node(c.chain, is_inter=True))
        for t in c.themes:
            inter_themes.append(theme_node(t.theme, is_inter=True))
            edges.append(theme_to_chain_edge(t.theme, c.chain, is_inter=True))
            for s in t.stories:
                stories.append(s)
                edges.append(story_to_theme_edge(s, t.theme, is_inter=True))
    for t in chainless_themes_inter:
        inter_themes.append(theme_node(t.theme, is_inter=True))
        for s in t.stories:
            stories.append(s)
            edges.append(story_to_theme_edge(s, t.theme, is_inter=True))


    nodes=[ story_node(participant, s) for s in list(set(stories))]
    nodes.extend(intra_chains)
    nodes.extend(inter_chains)
    nodes.extend(intra_themes)
    nodes.extend(inter_themes)
    #nodes.extend([theme_node(t) for t in list(set(themes))])
    #nodes.extend([chain_node(c) for c in list(set(chains))])



    builder = ParticipantConnectionBuilder(participant, 'Intraconnection')
    pairs = builder.buildstoryconnections()
    stories_in_connections = builder.getstoriesinconnections()

    for s in stories_in_connections:
        nodes.append(story_node(participant, s))

    for p in pairs:
        edges.append(story_to_story_edge(p.story1, p.story2))

    groups=[story_group(participant), theme_group(), theme_group(is_inter=True), chain_group(), chain_group(is_inter=True), chain_group(participant=participant)]

    return nodes, edges, groups

def participant_chains_themes_stories(participant):

    n, e, g = collect_participant_chains_themes_stories(participant)

    node_list = data_to_script(n)
    edge_list = data_to_script(e)
    groups = data_to_script(g)
    return node_list, edge_list, groups


