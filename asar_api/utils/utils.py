from typing import List
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO

class MyYAML(YAML):
    def dump(self, data, stream=None, **kw):
        inefficient = False
        if stream is None:
            inefficient = True
            stream = StringIO()
        YAML.dump(self, data, stream, **kw)
        if inefficient:
            return stream.getvalue()

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


def decode_story(story_name: str, input_nodes: dict, input_paths: list, rule_mode: bool = False) -> list:
    ret = []
    for subpath_cnt, path in enumerate(input_paths):
        steps = []
        for node in path:
            step = None
            if node != 'start' and node != 'end':
                step_type = input_nodes[node]['type']
                if step_type == 'intent':
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
                elif step_type == 'action':
                    step = {step_type: input_nodes[node]['name']}
                elif step_type == 'response':
                    step = {'action': f'utter_{input_nodes[node]["name"]}'}
                elif step_type == 'slot_was_set':
                    ss: list
                    if ss := input_nodes[node].get('slots'):
                        slots = []
                        s: dict
                        for s in ss:
                            if k := s.get('slot'):
                                if 'value' in s:
                                    v = s.get('value')
                                    slots.append({k: v})
                                else:
                                    slots.append(k)
                        if slots:
                            step = {step_type: slots}
                elif step_type == 'form':
                    step = {'action': f'{input_nodes[node]["name"]}_form'}
                elif step_type == 'active_loop':
                    if n := input_nodes[node].get('name'):
                        step = {'active_loop': f'{n}_form'}
                    else:
                        step = {'active_loop': None}
            if step:
                steps.append(step)
                
        if rule_mode:
            rule = {'rule': f'{story_name}_{subpath_cnt}'}
            rule.update(
                {'conversation_start': input_nodes['start'].get('conversation_start', False)})
            rule.update(
                {'wait_for_user_input': input_nodes['start'].get('wait_for_user_input', True)})

            condition = []
            if conditions := input_nodes['start'].get('condition'):
                c:dict
                for c in conditions:
                    c_type = c['type']
                    if c_type == 'slot_was_set':
                        slots = []
                        if k := c.get('slot'):
                            if 'value' in c:
                                v = c.get('value')
                                slots.append({k: v})
                            else:
                                slots.append(k)
                        if slots:
                            condition.append({c_type: slots})
                    elif c_type == 'active_loop':
                        if v := c.get('value'):
                            condition.append({c_type: f'{v}_form'})
                        else:
                            condition.append({c_type: None})
            rule.update({'condition': condition})
            rule.update({'steps': steps})
            ret.append(rule)
        else:
            ret.append(
                {'story': f'{story_name}_{subpath_cnt}', 'steps': steps})

    return ret


def compile_stories(vueflow_stories: dict, rule_mode: bool = False) -> dict:
    stories = []
    for story_name, vueflow in vueflow_stories.items():
        if vueflow:
            story_nodes = decode_story_nodes(vueflow)
            story_paths = decode_story_paths(story_nodes)
            decoded_story = decode_story(
                story_name, story_nodes, story_paths, rule_mode)
            if decoded_story:
                stories += decoded_story
    if rule_mode:
        return {'rules': stories}
    else:
        return {'stories': stories}
