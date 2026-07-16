import re

slugline = re.compile(r'^(INT|EXT)\.?\s+(.+?)\s*-\s*(DAY|NIGHT|CONTINUOUS)', re.MULTILINE) #gets int/ext and day/night/continuous

def parse_script(script: str):

    matches = (list(slugline.finditer(script)))
    scenes = []
    last_known_time = 'DAY'  # Default time if CONTINUOUS is the first scene
    for i, match in enumerate(matches):
        int_ext = match.group(1)
        location = match.group(2)
        time = match.group(3)
        if time == 'CONTINUOUS':
            time = last_known_time
        else:
            last_known_time = time
        scene_number = i + 1

        if i + 1 < len(matches):
            start_scene_index = match.end()
            end_scene_index = matches[i + 1].start()
            scene_text = script[start_scene_index:end_scene_index].strip()
        
        else:
            start_scene_index = match.end()
            scene_text = script[start_scene_index:].strip()

        scenes.append({
                'scene_number': scene_number,
                'int_ext': int_ext,
                'location': location,
                'time': time,
                'scene_text': scene_text
            })

    return scenes

'''
if __name__ == "__main__":
    demo_script = open('scripts/demo_text.txt').read()
    result = parse_script(demo_script)
    for scene in result:
        print(scene)
'''