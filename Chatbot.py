from openai import AzureOpenAI
import streamlit as st

st.title("💬 CSC Internal Assistant")
st.caption("🚀 Proof of Concept (In testing)")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

endpoint = st.secrets["AZURE_OPENAI_ENDPOINT"]
deployment = st.secrets["CHAT_COMPLETIONS_DEPLOYMENT_NAME"]
search_endpoint = st.secrets["SEARCH_ENDPOINT"]
search_index = st.secrets["SEARCH_INDEX"]
openai_api_key = st.secrets["AZURE_OPENAI_API_KEY"]
      
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=openai_api_key,
    api_version="2024-02-01",
)

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    #response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)

    response = client.chat.completions.create(
        model=deployment,
        messages=st.session_state.messages,
        extra_body={
            "data_sources": [
                {
                    "type": "azure_search",
                    "parameters": {
                        "endpoint": search_endpoint,
                        "index_name": search_index,
                        "authentication": {
                            "type": "system_assigned_managed_identity"
                        }
                    }
                }
            ]
        }
    )
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
