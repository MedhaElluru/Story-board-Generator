import streamlit as st
import uuid
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from pipeline import run_pipeline
from credit_tracker import get_credit_balance

st.set_page_config(page_title="Storyboard Generator", layout="wide")
st.title("Automated Storyboard Generator")


def show_live_tab():
    #st.info("Coming soon — upload your own script here.")
    st.header('Try you own script')

    try:
        balance = get_credit_balance()
        st.caption(f"Runway credits remaining: {balance}")
    except Exception:
        st.caption("Runway credits remaining: unavailable")

    user_script = st.text_area("Paste your own script", height = 300)

    if st.button("Generate storyboard"):
        if not user_script.strip():
            st.warning("Paste a script first")
        
        else:
            
            progress_bar = st.progress(0)
            status_text = st.empty()

            def update_progress(current, total, stage = "Generating"):
                status_text.text(f"{stage}: {current} of {total}...")
                progress_bar.progress(current / total)

            session_id = str(uuid.uuid4())
            output_dir = f"outputs/live/{session_id}"
            animatic_path = run_pipeline(user_script, output_dir, scene_cap=6, progress_callback=update_progress)

            progress_bar.empty()
            status_text.empty()
            st.success('Done!')

            frames_dir = f"{output_dir}/frames"
            scene_count = len(os.listdir(frames_dir))

            with st.expander("View Frames"):
                
                st.subheader("Storyboard Frames")
                cols = st.columns(3)
                frame_files = sorted(os.listdir(frames_dir))
                for idx, filename in enumerate(frame_files):
                    with cols[idx % 3]:
                        st.image(f"{frames_dir}/{filename}", caption=filename)

    

            st.subheader("Animatic")
            st.video(animatic_path, width = 1000)



def show_demo_tab():
    st.header("Demo: Coffee Shop Scene")

    script_text = open("scripts/demo_text.txt").read()
    with st.expander("View script"):
        st.text(script_text)

    with st.expander("View Frames"):
        st.subheader("Storyboard Frames")
        cols = st.columns(3)
        for i in range(1, 7):
            with cols[(i - 1) % 3]:
                st.image(f"outputs/demo/frames/scene_{i:03d}.png", caption=f"Scene {i}")

    st.subheader("Animatic")
    st.video("outputs/demo/animatic.mp4", width = 1000)


tab1, tab2 = st.tabs(['Demo', 'Live'])

with tab1:
    show_demo_tab()
 
with tab2:
    show_live_tab()