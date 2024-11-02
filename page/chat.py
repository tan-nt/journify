import streamlit as st
from openai import OpenAI
import logging
import streamlit as st  # 1.34.0
import extra_streamlit_components as stx
from streamlit_float import *
import tiktoken
import json
import time
from datetime import datetime
import streamlit as st
import streamlit as st
from openai import OpenAI
import logging
import streamlit as st 
import extra_streamlit_components as stx
from streamlit_float import *
import tiktoken
import json
import time
from datetime import datetime
import streamlit as st

logger = logging.getLogger()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
logging.basicConfig(encoding="UTF-8", level=logging.INFO)

def display_chat():
    st.session_state.page = "chat"
    # Display content based on the current page
    float_init()
    cookie_manager = stx.CookieManager(key="cookie_manager")
    def log_feedback(icon):
        # We display a nice toast
        st.toast("Thanks for your feedback!", icon="👌")
        # We retrieve the last question and answer
        last_messages = json.dumps(st.session_state["messages"][-2:])
        # We record the timestamp
        activity = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": "
        # And include the messages
        activity += "positive" if icon == "👍" else "negative"
        activity += ": " + last_messages
        # And log everything
        logger.info(activity)
    @st.dialog("🎨 Upload a picture")
    def upload_document():
        st.warning(
            "This is a demo dialog window. You need to process the file afterwards.",
            icon="💡",
        )
        picture = st.file_uploader(
            "Choose a file", type=["jpg", "png", "bmp"], label_visibility="hidden"
        )
        if picture:
            st.session_state["uploaded_pic"] = True
            st.rerun()
    def get_conversation_title():
        full_text = "".join([item["content"] for item in st.session_state["messages"]])
        response = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {
                    "role": "user",
                    "content": "Summarize the following conversation in 3 words:"
                    + full_text,
                },
            ],
            stop=None,
        )
        conversation_title = response.choices[0].message.content
        return conversation_title
    if "uploaded_pic" in st.session_state and st.session_state["uploaded_pic"]:
        st.toast("Picture uploaded!", icon="📥")
        del st.session_state["uploaded_pic"]
    # Model Choice - Name to be adapted to your deployment
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"
    # Adapted from https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    user_avatar = "👩‍💻"
    assistant_avatar = "🤖"
    # We rebuild the previous conversation stored in st.session_state["messages"] with the corresponding emojis
    for message in st.session_state["messages"]:
        with st.chat_message(
            message["role"],
            avatar=assistant_avatar if message["role"] == "assistant" else user_avatar,
        ):
            st.markdown(message["content"])
    # A chat input will add the corresponding prompt to the st.session_state["messages"]
    if prompt := st.chat_input("How can I help you?"):
        st.session_state["messages"].append({"role": "user", "content": prompt})
        # and display it in the chat history
        with st.chat_message("user", avatar=user_avatar):
            st.markdown(prompt)
    # If the prompt is initialized or if the user is asking for a rerun, we
    # launch the chat completion by the LLM
    if prompt or ("rerun" in st.session_state and st.session_state["rerun"]):
        with st.chat_message("assistant", avatar=assistant_avatar):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state["messages"]
                ],
                stream=True,
                max_tokens=300,  # Limited to 300 tokens for demo purposes
            )
            response = st.write_stream(stream)
        st.session_state["messages"].append({"role": "assistant", "content": response})
        # In case this is a rerun, we set the "rerun" state back to False
        if "rerun" in st.session_state and st.session_state["rerun"]:
            st.session_state["rerun"] = False
    st.write("")
    # If there is at least one message in the chat, we display the options
    if len(st.session_state["messages"]) > 0:
        if "conversation_id" not in st.session_state:
            st.session_state["conversation_id"] = "history_" + datetime.now().strftime("%Y%m%d%H%M%S")
        action_buttons_container = st.container()
        action_buttons_container.float(
            "bottom: 7.2rem;background-color: var(--default-backgroundColor); padding-top: 1rem;"
        )
        # We set the space between the icons thanks to a share of 100
        cols_dimensions = [7, 14.9, 14.5, 9.1, 9, 8.6, 8.7]
        cols_dimensions.append(100 - sum(cols_dimensions))
        col0, col1, col2, col3, col4, col5, col6, col7 = action_buttons_container.columns(
            cols_dimensions
        )
        with col1:
            # Converts the list of messages into a JSON Bytes format
            json_messages = json.dumps(st.session_state["messages"]).encode("utf-8")
            # And the corresponding Download button
            st.download_button(
                label="📥 Save!",
                data=json_messages,
                file_name="chat_conversation.json",
                mime="application/json",
            )
        with col2:
            # We set the message back to 0 and rerun the app
            # (this part could probably be improved with the cache option)
            if st.button("Clear 🧹"):
                st.session_state["messages"] = []
                del st.session_state["conversation_id"]
                if "uploaded_pic" in st.session_state:
                    del st.session_state["uploaded_pic"]
                st.rerun()
        with col3:
            if st.button("🎨"):
                upload_document()
        with col4:
            icon = "🔁"
            if st.button(icon):
                st.session_state["rerun"] = True
                st.rerun()
        with col5:
            icon = "👍"
            # The button will trigger the logging function
            if st.button(icon):
                log_feedback(icon)
        with col6:
            icon = "👎"
            # The button will trigger the logging function
            if st.button(icon):
                log_feedback(icon)
        with col7:
            # We initiate a tokenizer
            enc = tiktoken.get_encoding("cl100k_base")
            # We encode the messages
            tokenized_full_text = enc.encode(
                " ".join([item["content"] for item in st.session_state["messages"]])
            )
            # And display the corresponding number of tokens
            label = f"💬 {len(tokenized_full_text)} tokens"
            st.link_button(label, "https://platform.openai.com/tokenizer")
    else:
        # At the first run of a session, we temporarly display a message
        if "disclaimer" not in st.session_state:
            with st.empty():
                for seconds in range(3):
                    st.warning(
                        "‎ You can click on 👍 or 👎 to provide feedback regarding the quality of responses.",
                        icon="💡",
                    )
                    time.sleep(1)
                st.write("")
                st.session_state["disclaimer"] = True
    if "conversation_id" in st.session_state:
        conversation_title = get_conversation_title()
        cookie_manager.set(st.session_state["conversation_id"], val={conversation_title: st.session_state["messages"]})
