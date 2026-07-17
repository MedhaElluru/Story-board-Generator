import os
import dotenv #loads key=value from .env file into env variables
import requests

from runwayml import RunwayML
from parser import parse_script
from prompt_builder import build_prompt, STYLE_PREFIX


def get_reference_images(registry: dict):

    dotenv.load_dotenv()
    reference_images_url = {}
    client = RunwayML(api_key = os.getenv("RUNWAYML_API_SECRET"))

    for character in registry:  
        prompt = f"{STYLE_PREFIX}, portrait of a person, neutral pose, plain background"
        try:
            task = client.text_to_image.create(model="gen4_image",
                prompt_text=prompt,
                ratio="1360:768"
        ). wait_for_task_output()
            reference_images_url[character] = task.output[0]
            print(f"Reference generated for {character}")
            
        except:
            print(f'Failed to generate reference image for {character}')

    return reference_images_url


def image_gen(scenes: dict, frames_dir: str = "outputs/demo/frames", progress_callback=None, character_references: dict = None, character_registry: dict = None):
    
    dotenv.load_dotenv()
    client = RunwayML(api_key=os.getenv("RUNWAYML_API_SECRET"))
    
    os.makedirs(frames_dir, exist_ok=True) 

    failed_scenes = []
    total = len(scenes)
    
    for idx, scene in enumerate(scenes, start=1):
        print(f"Generating scene {scene['scene_number']}...")
        if progress_callback:
            progress_callback(idx, total)
        try:
            prompt, reference_images = build_prompt(scene, character_references, character_registry)
            
            reference_images = reference_images[:3]
            print(f"Scene {scene['scene_number']} reference_images: {reference_images}")

            kwargs = {
                "model": "gen4_image",
                "prompt_text": prompt,
                "ratio": "1360:768",
            }
            if reference_images:
                kwargs["reference_images"] = reference_images
            try:

                task = client.text_to_image.create(**kwargs).wait_for_task_output()
            except Exception:
               
                print(f"Scene {scene['scene_number']} failed once, retrying...")
                task = client.text_to_image.create(**kwargs).wait_for_task_output()
            '''
            task = client.text_to_image.create(model="gen4_image",
                prompt_text=prompt,
                ratio="1360:768",
                reference_images=reference_images if reference_images else None

        ). wait_for_task_output()
        '''

            image_url = (task.output[0])
            image = requests.get(image_url, allow_redirects=True)
            with open(f"{frames_dir}/scene_{scene['scene_number']:03d}.png", "wb") as f:
                f.write(image.content)

        except Exception as e:
            print(f"Error generating scene {scene['scene_number']}: {e}")
            print(f"Error generating scene {scene['scene_number']}: {e}")
            print(f"Full exception details: {repr(e)}")
            failed_scenes.append(scene['scene_number'])

    if failed_scenes:
        print(f"Failed to generate images for scenes: {failed_scenes}")
    else:
        print("All scenes generated successfully!")

    return failed_scenes


if __name__ == "__main__":
    from parser import parse_script, build_character_registry

    script_text = open("scripts/demo_text.txt").read()
    scenes = parse_script(script_text)
    registry = build_character_registry(scenes)
    references = get_reference_images(registry)
    print(references)