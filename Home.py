import streamlit as st
import os
from tempfile import NamedTemporaryFile
from langchain.llms import OpenAI
import openai

os.environ['KMP_DUPLICATE_LIB_OK']='True'

st.title('🎤🗒️ VoiceMarkdown!')

openai_api_key = st.sidebar.text_input('OpenAI API Key')
openai.api_key = openai_api_key

def generate_response(input_text):
  llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
  st.markdown(llm(input_text))

audio_file = st.file_uploader('Upload your audio file:', type='m4a')
if audio_file:
    with st.spinner("Transcribing..."):
        result = openai.Audio.transcribe("whisper-1", audio_file)
        st.write(result["text"])


st.markdown('\n')
st.markdown('----------')


with st.form('my_form'):
  instructions = st.text_area('Put any prompt instructions here.', ' ')
  submitted = st.form_submit_button('Submit')
  if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
  if submitted and openai_api_key.startswith('sk-'):
    text = instructions + "\n\n What Follows is the transcript ---\n\n" + result["text"]
    with st.spinner('Contacting the LLM Agents....'):
        generate_response(text)