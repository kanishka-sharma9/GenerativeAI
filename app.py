import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

prompt="""You ar a youtube video summarizer.
Use the provided transcript to create an accurate summary of the videoand providing the important summary in points
within 300 words.
the transcript is : """

def gemini_content(transcript_text, prompt=prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(prompt+transcript_text)
    return response.text


def get_ts(url):
    try:
        vdo_id=url.split('=')[1]
        tt=YouTubeTranscriptApi.get_transcript(vdo_id)
        transcript=""
        for i in tt:
            transcript += " " + i['text']

        return transcript

    except Exception as e:
        raise e
    
st.title("YT notes maker")

link=st.text_input('enter vdo link:')

if link:
    id=link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{id}/0.jpg",use_column_width=True)

if st.button("get"):
    tt=get_ts(link)
    if tt:
        summary=gemini_content(tt,prompt)
        st.markdown("# detailed notes:")
        st.write(summary)
