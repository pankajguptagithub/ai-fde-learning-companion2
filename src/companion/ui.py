import streamlit as st
import requests 

API_URL = "http://127.0.0.1:8000/learn"

st.set_page_config(
    page_title="AI FDE learning companion",
)

st.title("AI FDE Learning Companion")

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
                        API_URL,
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
                        API_URL,
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
    st.write("**Score:**",evaluation.get("score","Not available"))
    st.write("**Feedback:**",evaluation.get("feedback","Not available"))
    st.write("**Next Action**",result.get("next_action","Not available"))
