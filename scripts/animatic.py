import cv2
import numpy as np
from moviepy import ImageSequenceClip
from moviepy import concatenate_videoclips, vfx
from moviepy import TextClip, CompositeVideoClip

def get_effect(scene: int):
    effect = ["Zoom_in", "Zoom_out", "Pan"]
    return effect[(scene -1) % 3]

#applies effect for each frame
def ken_burns_effect(frame: np.array, t:int, duration:float, effect: str):
    #this methods needs to run for every frame, all frames under one scene use one effect
    # different frames use different effects
    h, w = frame.shape[: 2]
    progress = t/duration

    if effect == 'Zoom_in':
        scale = (1.3-1.0)*progress + 1.0
        cx = w/2
        cy = h/2    

    elif effect == 'Zoom_out':
        scale = 1.3 - (1.3 - 1.0)*progress 
        cx = w/2
        cy = h/2 

    elif effect == "Pan":
        scale = 1.2
        cy = h/2
        cx = (w*0.56 - w*0.44)*progress + w*0.44

    resized = cv2.resize(frame, (int(w*scale), int(h*scale)))
    rh, rw = resized.shape[: 2]

    x1 = int(cx * scale - w / 2)
    y1 = int(cy * scale - h / 2)

    if x1 < 0:
        x1 = 0
    elif x1 > rw - w:
        x1 = rw - w
    
    if y1 < 0:
        y1 = 0
    elif y1 > rh - h:
        y1 = rh - h

    return resized[y1:y1 + h, x1:x1 + w]  

#collects all the frames from a scene, and outputs 1 video for each scene
def build_scene(img_path: str, scene_num: int, duration: int, fps = 24):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    number_of_frames = int(fps * duration)
    effect = get_effect(scene_num)
    frames = []

    for i in range(number_of_frames):
        t = i/fps
        cropped = ken_burns_effect(img, t, duration, effect)
        frames.append(cropped)
    
    clip = ImageSequenceClip(frames, fps)
    return clip


def estimate_duration(scene_num: int, scene_text: str, wpm = 220, min_duration = 2.0):
    word_count = len(scene_text.split())
    duration = (word_count/wpm) * 60
    if duration < 2.0:
        duration  = min_duration
    return duration

#combining all scene clips
def build_all_clips(scenes: list[dict], frames_dir: str = "outputs/demo/frames", fps: int = 24, progress_callback = None):
    clips = []
    total = len(scenes)

    for idx, scene in enumerate(scenes, start=1):
        if progress_callback:
            progress_callback(idx, total, stage="Building clips")
        
        caption_text =  f"{scene['int_ext']}. {scene['location']} - {scene['time']}"

        img_path = f"{frames_dir}/scene_{scene['scene_number']:03d}.png"
        
        duration = estimate_duration(scene["scene_number"], scene['scene_text'])
        
        clip = build_scene(img_path, scene['scene_number'], duration, fps)
        clip = add_caption(clip, caption_text)
        clips.append(clip)

    return clips

#applies transitions between clips
def build_animatic(clips: list, crossfade_duration: float = 0.5):
    faded_clips = [clips[0]]  # first clip plays with no fade-in, nothing precedes it

    for clip in clips[1:]:
        faded = clip.with_effects([vfx.CrossFadeIn(crossfade_duration)])
        faded_clips.append(faded)

    final = concatenate_videoclips(faded_clips, method="compose", padding=-crossfade_duration)
    return final

def add_caption(clip, text, font_size = 32):
    caption = TextClip(text=text, font_size=font_size, color = "white", bg_color = "black", method = "caption", size = (clip.w, 60))
    caption = caption.with_duration(clip.duration).with_position(("center", "bottom"))
    return CompositeVideoClip([clip, caption])

if __name__ == "__main__":
    from parser import parse_script
    script_text = open("scripts/demo_text.txt").read()
    scenes = parse_script(script_text)
    clips = build_all_clips(scenes)
    final = build_animatic(clips)
    final.write_videofile("outputs/demo/animatic.mp4", fps=24)