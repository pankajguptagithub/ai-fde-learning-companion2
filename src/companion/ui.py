import streamlit as st
import requests 

LEARN_API_URL = "http://127.0.0.1:8000/learn"
CHAT_API_URL = "htpp://127.0.0.1:8000/chat"

st.set_page_config(
    page_title="AI FDE learning companion",
    page_icon="🎓",
)

st.title("AI FDE Learning Companion")

chat_tab, learning_tab = st.tabs(
    ["AI Chat - Phase 1","Learning Companion"]
)

#===========================================
#   TAB 1 - PHASE 1: DIRECT MODEL CALL
#===========================================

with chat_tab:
    
    st.subheader("Ask the AI Model")

    question = st.text_area(
        "Your Question",
        key="chat_question",
    )

    if st.button("Ask AI"):

        if not question.strip():
            st.warning("Please ask your query")

        else:
            try:
                with st.spinner("Calling AI model..."):

                    response = requests.post(
                        CHAT_API_URL,
                        json = {
                            "question": question.strip()
                        },
                        timeout = 60,
                    )

                    response.raise_for_status()

                    data = response.json()

                    st.subheader("AI Response")
                    st.write(data.get("answer","No response received"))

            except requests.exceptions.RequestException as exc:
                st.error(f"Unable to call AI API:{exc}")

#===========================================
#   TAB2 - LEARNING COMPANION
#===========================================

with learning_tab:


    if "lesson_data" not in st.session_state:
        st.session_state.lesson_data = None

    if "result_data" not in st.session_state:
        st.session_state.result_data = None

    user_id = st.text_input("User ID")
    topic = st.text_input("Topic")


    if st.button("Start Learning"):
        if not user_id.strip() or not topic.strip():
            st.warning("Please enter both User ID and Topic")
        else:
            try:
                with st.spinner("Loading lesson..."):
                    response = requests.post(
                            LEARN_API_URL,
                            json = {
                                "user_id": user_id.strip(),
                                "topic": topic.strip(),
                                "mode": "quiz",
                                #"learner_answers": ["Retrieval and Generation"],
                                "learner_answers": [],
                                "max_attempts": 3,
                            },
                            timeout = 30,
                    )

                    response.raise_for_status()

                    st.session_state.lesson_data = response.json()
                    st.session_state.result_data = None
            
            except requests.exceptions.RequestException as exc:
                st.error(f"Unable to connect to the learning API: {exc}")


    if st.session_state.lesson_data:
        lesson_data = st.session_state.lesson_data

        errors = lesson_data.get("errors", [])

        if errors:
            st.error("\n".join(errors))
        else:
            st.subheader("Lesson")
            st.write(lesson_data.get("lesson", "Lesson not available"))

        st.subheader("Question")
        st.write(lesson_data.get("question", "Question not available"))

        answer = st.text_area("Your Answer")

        if st.button("Submit Answer"):
            if not answer.strip():
                st.warning("Please enter your answer")
            else:
                try:
                    with st.spinner("Evaluating answer..."):
                        response = requests.post(
                            LEARN_API_URL,
                            json = {
                                "user_id": user_id.strip(),
                                "topic": topic.strip(),
                                "mode": "quiz",
                                "learner_answers": [answer.strip()],
                                "max_attempts":3,
                            },
                            timeout=30,
                        )

                        response.raise_for_status()
                        st.session_state.result_data = response.json()
                except request.exceptions.RequestException as exc:
                    st.error(f"Unable to connect to the learning API : {exc}")


    if st.session_state.result_data:
        result = st.session_state.result_data
        evaluation = result.get("evaluation",{})

        st.subheader("Result")
        st.write(
                "**Score:**",
                evaluation.get(
                    "score","Not available"
                )
        )
        st.write(
                "**Feedback:**",
                evaluation.get(
                    "feedback",
                    "Not available"
                    ),
                )
        st.write(
                "**Next Action**",
                result.get(
                    "next_action",
                    "Not available"
                ),
        )
