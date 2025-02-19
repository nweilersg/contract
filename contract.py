import streamlit as st
from openai import OpenAI
from io import BytesIO
import base64
import pdfplumber

st.set_page_config(page_title='Construction Contract Risk Assessment and Renegotiation', page_icon='ðŸ‘ï¸')

st.markdown('# Construction Contract Risk Assessment and Renegotiation')
api_key = st.text_input('OpenAI API Key', '', type='password')

# Get user inputs
text_input = st.text_input('Query', '')
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
        f"""
        Considering the law in ${text_input} and general best practice for managing construction contract risk find the highest risk clauses and create a table summarising these risks.
        In the table you must include the columns as risk type, risk description, risk severity (1-10), article number, page number. Write this table back to me.*
        Below the table write a renegotiation letter outlining my concerns with the terms and with suggestions over fairer terms which we'd like to discuss further. Ignore any terms which would be non negotiable like compliance with local laws.*
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

