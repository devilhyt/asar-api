def decode_story_nodes(input_story: dict) -> dict:
    """get nodes info"""
    ret = dict()
    # search nodes id
    n: dict
    for n in input_story['nodes']:
        ret[n['id']] = n.get('data', {})
        ret[n['id']]['targets'] = set()
    # search targets of node
    for e in input_story['edges']:
        ret[e['source']]['targets'].add(e['target'])

    return ret


def decode_story_paths(tree: dict, current_node: str = 'start', visited: list = None, path: list = None) -> list:
    """search all paths(dfs)"""
    if visited is None:
        visited = []
    if path is None:
        path = []

    visited.append(current_node)
    if (not tree[current_node]['targets']) and current_node == 'end':
        path.append(visited)
    else:
        for n in tree[current_node]['targets']:
            path = decode_story_paths(tree, n, visited.copy(), path.copy())
    return path


def decode_story(story_name: str, input_nodes: dict, input_paths: list) -> list:
    ret = []
    for subpath_cnt, path in enumerate(input_paths):
        steps = []
        for node in path:
            step = None
            if node != 'start' and node != 'end':
                step_type = input_nodes[node]['type']
                if step_type == 'intent' or step_type == 'action':
                    step = {step_type: input_nodes[node]['name']}

                    # entity
                    if input_nodes[node].get('entities'):
                        entities = []
                        e: dict
                        for e in input_nodes[node]['entities']:
                            if k := e.get('entity'):
                                entity = {k: e.get('value')}
                                if r := e.get('role'):
                                    entity['role'] = r
                                if g := e.get('group'):
                                    entity['group'] = g
                                entities.append(entity)
                        if entities:
                            step.update({'entities': entities})
                elif step_type == 'slot_was_set':
                    step = {step_type: []}

                    # slot
                    if input_nodes[node].get('slots'):
                        slots = []
                        s: dict
                        for s in input_nodes[node]['slots']:
                            if k := s.get('slot'):
                                slot = {k: s.get('value')}
                                slots.append(slot)
                        if slots:
                            step = {step_type: slots}
            if step:
                steps.append(step)
        ret.append({'story': f'{story_name}_{subpath_cnt}', 'steps': steps})

    return ret


def compile_stories(vueflow_stories: dict) -> dict:
    stories = []
    for story_name, vueflow in vueflow_stories.items():
        if vueflow:
            story_nodes = decode_story_nodes(vueflow)
            story_paths = decode_story_paths(story_nodes)
            decoded_story = decode_story(story_name, story_nodes, story_paths)
            if decoded_story:
                stories += decoded_story
    return {'stories': stories}
