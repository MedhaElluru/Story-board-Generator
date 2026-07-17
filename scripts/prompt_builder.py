setting_map = {'INT': 'inside', 'EXT': 'outside'}
STYLE_PREFIX = "black-and-white pencil storyboard sketch, cinematic wide shot" #to maintain consistency
 
#building the prompy by paraphrasing location, time, and prefix along with scene script + character tags
def build_prompt(scene: dict, character_references: dict = None, character_registry: dict = None):

    setting = setting_map.get(scene['int_ext'], 'unknown')
    location_context = f"{setting} a {scene['location'].lower()} during {scene['time'].lower()}"
    prompt = f"{STYLE_PREFIX}, {location_context}, {scene['scene_text']}"

    reference_image = []
    if character_references and character_registry:
        for character, scene_list in character_registry.items():
            if scene['scene_number'] in scene_list and character in character_references:
                prompt = f'{prompt}, @{character}'
                reference_image.append({'uri': character_references[character], 'tag': character})

    return (prompt, reference_image)

'''
if __name__ == "__main__":
    from parser import parse_script
    script = open('scripts/demo_text.txt').read()
    scenes = parse_script(script)
    for scene in scenes:
        print(build_prompt(scene))
'''