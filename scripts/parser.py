import re

slugline = re.compile(r'^(INT|EXT)\.?\s+(.+?)\s*-\s*(DAY|NIGHT|CONTINUOUS|DUSK|DAWN|MORNING|EVENING)', re.MULTILINE) #gets int/ext and day/night/continuous
charcters = re.compile(r'\b[A-Z]{2,}\b')
non_characters = {'INT', 'EXT', 'DAY', 'NIGHT', 'CONTINUOUS', 'DUSK', 'DAWN', 'MORNING', 'EVENING'}

#returns list of all characters in the script
def extract_characters(script: str):
    matches = charcters.findall(script)
    return list(set(matches) - non_characters)

#parsing the script
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
                'scene_text': scene_text,
                'characters': extract_characters(scene_text)
            }) #returns this for each scene in the script

    return scenes

#returns which scene contains which characters
def build_character_registry(scenes: list):
    known_charcters = set()
    for scene in scenes:
        known_charcters.update(scene['characters'])

    registry = {}
    
    for character in known_charcters:
        pattern = re.compile(rf'\b{character}\b', re.IGNORECASE)
        for scene in scenes:
            if pattern.search(scene['scene_text']):
                registry.setdefault(character, []).append(scene['scene_number'])
    return registry


#develop for each character their image, and pass it as reference image for all other scenes where it has that character


if __name__ == "__main__":
    demo_script = open('scripts/demo_text.txt').read()
    result = parse_script(demo_script)
    for scene in result:
        print(scene)
    print(build_character_registry(result))