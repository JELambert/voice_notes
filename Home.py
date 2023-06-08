import streamlit as st
from langchain.llms import OpenAI
import whisper
import os
from tempfile import NamedTemporaryFile

os.environ['KMP_DUPLICATE_LIB_OK']='True'

st.title('🎤🗒️ VoiceMarkdown!')

openai_api_key = st.sidebar.text_input('OpenAI API Key')

model = whisper.load_model("base.en")

def run_whisper(input_file, output_path):
    result = model.transcribe(input_file)
    with open(output_path, 'w') as f:
        f.write(result['text'])
        f.close()
    return result['text']

def generate_response(input_text):
  llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
  st.markdown(llm(input_text))

audio_file = st.file_uploader('Upload your audio file:', type='m4a')
if audio_file:
    with st.spinner("Transcribing..."):
        with NamedTemporaryFile(suffix="m4a") as temp:
            temp.write(audio_file.getvalue())
            temp.seek(0)
            model = whisper.load_model("base")
            result = model.transcribe(temp.name)
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