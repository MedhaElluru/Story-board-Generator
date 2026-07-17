# parse script --> image_gen --> build all clips --> build animatic

import os
from parser import parse_script, build_character_registry
from image_gen import image_gen, get_reference_images
from animatic import build_all_clips, build_animatic

def run_pipeline(script_text: str, output_dir: str, scene_cap: int = None, progress_callback = None):
    scenes = parse_script(script_text)
    if scene_cap:
        scenes = scenes[: scene_cap]

    character_registry = build_character_registry(scenes)
    character_references = get_reference_images(character_registry)


    frames_dir = f"{output_dir}/frames"
    os.makedirs(frames_dir, exist_ok=True)
    failed_scenes = image_gen(scenes, frames_dir, progress_callback=progress_callback, character_references=character_references, character_registry=character_registry)


    if failed_scenes:
        scenes = [s for s in scenes if s['scene_number'] not in failed_scenes] #not wasting credits for failed scenes

    if not scenes:
        raise RuntimeError("All scenes failed to generate — no frames available for animatic.")
    
    clips = build_all_clips(scenes, frames_dir, progress_callback=progress_callback)
    final = build_animatic(clips)

    animatic_path = f"{output_dir}/animatic.mp4"
    final.write_videofile(animatic_path, fps=24)
    return animatic_path

if __name__ == "__main__":
    script_text = open("scripts/demo_text.txt").read()
    result_path = run_pipeline(script_text, output_dir="outputs/demo")
    print(f"Animatic saved to: {result_path}")