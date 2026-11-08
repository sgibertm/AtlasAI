# =============================================================================
# CHAT INTERFACE: Streamlit-based UI for interactive user data collection.
# 1. Manages chat history and navigation between questions.
# 2. Integrates Natural Language Parsing (NLP) to validate user responses.
# 3. Transitions to the recommendation phase once all inputs are collected.
# =============================================================================

import streamlit as st
from nav.utils import create_parser, safe_parse, questions

def chat():
    st.title("Travel Advisor AI")
    st.write("Tell me about your dream vacation. If I don't understand, I'll ask again. I'll use Fuzzy Logic to match your style!")

    # History of the chat
    for message in st.session_state.chat:
        if message["role"] == "user":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        else:
            with st.chat_message(message["role"], avatar = "img/logo.png"):
                st.markdown(message["content"])


    # If we still have questions
    if st.session_state.step < len(questions):

        q = questions[st.session_state.step]

        with st.chat_message("assistant", avatar = "img/logo.png"):
            st.write(f"**{q['question']}**")
            st.caption(q['example'])

        user_input = st.chat_input("Type your answer here...", )

        if user_input:
            parser = create_parser()
            parses = safe_parse(user_input, parser)

            #Update chat history
            st.session_state.chat.append({"role": "assistant", "content": q["question"]})

            st.session_state.chat.append({"role": "user", "content": user_input.lower()})

            if parses:

                extracted = []

                for tree in parses:
                    extracted.extend(q["extract_func"](tree))

                if extracted:
                    # Save only if it matches the current question
                    st.session_state.responses[q["key"]] = " ".join(extracted).lower() #same as user_input.lower()
                    st.session_state.step += 1
                    st.rerun()
                else:
                    st.session_state.chat.append({"role": "assistant", "content": f"That doesn't answer the question. {q['example']}"})
                    st.rerun()
            else:
                st.session_state.chat.append({"role": "assistant", "content": f"I didn't understand you. {q['example']}"})
                st.rerun()

    else:

        st.success("Analysis complete! Go to the 'Recommendations' tab to see your results.")
        if st.button("View My Destinations", use_container_width=True):
            st.session_state.page = "recommendation"
            st.rerun()
