from pathlib import Path
from pydantic import BaseModel, Extra
from ..config import STORIES_FILE_NAME
from .file_basis import FileBasis


class Story(FileBasis):
    def __init__(self, prj_path: Path) -> None:
        super().__init__(prj_path=prj_path,
                         file_name=STORIES_FILE_NAME,
                         object_schema=StoryObjectSchema)
    def compile(self) -> dict:
        def decode_story_nodes(input_story : dict):
            """get nodes info"""
            ret = dict()
            # search nodes id
            for n in input_story['nodes']:
                ret[n['id']] = n.get('data', {})
                ret[n['id']]['targets'] = set()
            # search targets of node
            for e in input_story['edges']:
                ret[e['source']]['targets'].add(e['target'])
                
            return ret
        
        def decode_story_paths(tree: dict, current_node: str = 'start', visited: list = None, path: list = None):
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
        
        def decode_story(story_name, input_nodes, input_paths):
            ret = []
            for cnt, path in enumerate(input_paths):
                steps = []
                for node in path:
                    step = None
                    if node != 'start' and node != 'end':
                        step_type = input_nodes[node]['type']
                        if step_type == 'intent' or step_type == 'action':
                            step = {step_type: input_nodes[node]['name']}

                            # entity
                            if 'entities' in input_nodes[node]:
                                entities = []
                                e:dict
                                for e in input_nodes[node]['entities']:
                                    entity = {e['key']: e['value']}
                                    if r := e.get('role'):
                                        entity['role'] = r
                                    if g := e.get('group'):
                                        entity['group'] = g
                                    entities.append(entity)
                                step['entities'] = entities
                        elif step_type == 'slot_was_set':
                            step = {step_type: []}

                            # slot
                            if 'slots' in input_nodes[node]:
                                slots = []
                                for s in input_nodes[node]['slots']:
                                    slot = {s['key']: s['value']}
                                    slots.append(slot)
                                step['slots'] = slot
                    if step:
                        steps.append(step)
                ret.append({'story': f'{story_name}_{cnt}', 'steps': steps})
                
            return ret
        
        def compile_stories(vueflow_stories):
            stories = []
            for story_name, vueflow in vueflow_stories.items():
                if vueflow:
                    story_nodes = decode_story_nodes(vueflow)
                    story_paths = decode_story_paths(story_nodes)
                    print(story_paths)
                    decoded_story = decode_story(story_name, story_nodes, story_paths)
                    if decoded_story:
                        stories += decoded_story
            return {'stories': stories}

        content = self.content
        stories =compile_stories(content)
        return stories


class StoryObjectSchema(BaseModel, extra=Extra.allow):
    pass
