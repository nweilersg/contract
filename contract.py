import streamlit as st
from openai import OpenAI
from io import BytesIO
import base64
import pdfplumber

st.set_page_config(page_title='Construction Contract Document', page_icon='ðŸ‘ï¸')

st.markdown('# Construction Contract Document Administration')
api_key = st.text_input('OpenAI API Key', '', type='password')

# Get user inputs
#text_input = st.text_input('Query', '')
text_input = st.text_area('Query', height=20)
img_input = st.file_uploader('Source Contract Document (pdf)', type="pdf", accept_multiple_files=True)

# Send API request
if st.button('Send'):
    if not api_key:
        st.warning('API Key required')
        st.stop()
    if not (text_input or img_input):
        st.warning('What is your query!')
        st.stop()
    msg = {'role': 'user', 'content': []}
    if text_input:
       msg['content'].append({'type': 'text', 'text': 
        f"""${text_input}
        """                       
        })
    for img in img_input:
        file_type = img.name.split('.')[-1].lower()
        if file_type in ['pdf']:
            text = ''
            with pdfplumber.open(BytesIO(img.read())) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    print(len(text))
                    if text:
                        msg['content'].append(
                            {
                                'type': 'text',
                                'text': text
                            }
                        )
        else:
            st.warning('Only PDF document supported')
            st.stop()
    
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model='gpt-4o',
        temperature=0.0,
        max_tokens=2000,
        messages=[msg],
        stream=True
    )


    st.write_stream(response)

