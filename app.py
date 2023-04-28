import streamlit as st
import pyttsx3
import base64

def get_binary_file_downloader_html(bin_file, file_label='File'):
    """
    Generates a link allowing the data in a given file to be downloaded in a Streamlit app.
    
    Adapted from https://stackoverflow.com/a/38755348/5992655
    
    :param bin_file: The binary file data.
    :param file_label: The label for the file link.
    :return: HTML code for a link to download the binary file.
    """
    bin_str = base64.b64encode(bin_file).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}">Download {file_label}</a>'
    return href


def text_to_speech(text):
    # Initialize the engine
    engine = pyttsx3.init()

    # Set the speed and volume
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)

    # Say the text and save to file
    engine.save_to_file(text, 'output.wav')
    engine.runAndWait()

    # Open the audio file and read its contents
    with open('output.wav', 'rb') as f:
        audio_data = f.read()

    return audio_data

def clear_inputs():
    global text_input
    global text_file
    text_input = ''
    text_file = None

# Set the app title
st.title("Text-to-Speech App")

# Add a radio button to choose between text input and file upload
option = st.radio('Select input type:', ('Text', 'File Upload'))

# If text input is chosen, display a text input widget
if option == 'Text':
    text_input = st.text_input("Enter text to convert to speech:")

# If file upload is chosen, display a file uploader
else:
    text_file = st.file_uploader("Upload a text file:")
    if text_file is not None:
        text_input = text_file.getvalue().decode()
        st.success('Text file uploaded successfully!')

# Add a button to trigger the text-to-speech function
if st.button("Convert to speech"):
    if text_input:
        audio_data = text_to_speech(text_input)
        st.success("Conversion successful!")

        # Add a link to download the audio file
        st.audio(audio_data, format='audio/wav', start_time=0)
        st.markdown(get_binary_file_downloader_html(audio_data, 'output.wav'), unsafe_allow_html=True)
    else:
        st.warning('Please provide input before converting to speech.')

# Add a button to clear the text input field and uploaded file
if st.button('Clear Input'):
    clear_inputs()
    st.success('Input cleared successfully!')
