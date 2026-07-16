setting_map = {'INT': 'inside', 'EXT': 'outside'}
STYLE_PREFIX = "black-and-white pencil storyboard sketch, cinematic wide shot" #to maintain consistency
 
def build_prompt(scene: dict):
    #first_beat = scene['scene_text'].split('.')[0]  # Get the first line of the scene text
    setting = setting_map.get(scene['int_ext'], 'unknown')
    location_context = f"{setting} a {scene['location'].lower()} during {scene['time'].lower()}"
    prompt = f"{STYLE_PREFIX}, {location_context}, {scene['scene_text']}"
    return prompt

'''
if __name__ == "__main__":
    from parser import parse_script
    script = open('scripts/demo_text.txt').read()
    scenes = parse_script(script)
    for scene in scenes:
        print(build_prompt(scene))
'''