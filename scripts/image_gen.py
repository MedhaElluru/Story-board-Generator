import os
import dotenv #loads key=value from .env file into env variables
import requests

from runwayml import RunwayML
from parser import parse_script
from prompt_builder import build_prompt

def image_gen(scenes: dict, frames_dir: str = "outputs/demo/frames", progress_callback=None):

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
            prompt = build_prompt(scene)
            task = client.text_to_image.create(model="gen4_image",
                prompt_text=prompt,
                ratio="1360:768"
        ). wait_for_task_output()

            image_url = (task.output[0])
            image = requests.get(image_url, allow_redirects=True)
            with open(f"{frames_dir}/scene_{scene['scene_number']:03d}.png", "wb") as f:
                f.write(image.content)

        except Exception as e:
            print(f"Error generating scene {scene['scene_number']}: {e}")
            failed_scenes.append(scene['scene_number'])

    if failed_scenes:
        print(f"Failed to generate images for scenes: {failed_scenes}")
    else:
        print("All scenes generated successfully!")

    return failed_scenes

if __name__ == "__main__":
    script_text = open("data/demo_script.txt").read()
    scenes = parse_script(script_text)
    image_gen(scenes, frames_dir="outputs/demo/frames")