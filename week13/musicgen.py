import streamlit as st
import requests

# Run the api first https://github.com/venetanji/audiocraft-server/
audiocraft_api = "http://localhost:8000/generate_music"

def musicgen():
    st.title("MusicGen api usage example:")

    og_descriptions = st.text_input("Comma separated music keywords", placeholder="happy, energetic, fast")
    descriptions = og_descriptions.strip().split(",") if og_descriptions else []
    seconds = st.slider("Generation length in seconds", 1, 10, 2)
    model  = st.selectbox("Model", [
        "facebook/musicgen-small",
        "facebook/musicgen-medium",
        "facebook/musicgen-large",
        "facebook/musicgen-melody"])

    if st.button("Generate Music"):
        st.write("Generating music...")
        options ={
            "descriptions": descriptions,
            "duration": seconds,
            "model_name": model
        }
        print(options)
        # make a post request to our audiocraft-api
        response = requests.post(audiocraft_api, params=options)
        st.write(response)
        if response.status_code == 200:
            audio_data = response.content
            st.audio(audio_data, format='audio/wav')
            st.download_button(label="Download Music", data=audio_data, file_name="generated_music.wav", mime="audio/wav")
        else:
            st.write("Failed to generate music")

        # Call the musicgen API here
        st.write(f"Generated music for prompt: {og_descriptions}")
        st.write(f"Model: {model}")
        st.write(f"Generation length: {seconds} seconds")
        st.write("Music generated successfully!")


musicgen_page = st.Page(musicgen, title="MusicGen")
pages = [musicgen_page]
pg = st.navigation(pages)
pg.run()