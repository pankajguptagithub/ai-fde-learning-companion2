import streamlit as st
import requests 

st.title("AI FDE Learning Companion")

user_id = st.text_input("User ID")
topic = st.text_input("Topic")

if "lesson_data" not in st.session_state:
    st.session_state.lesson_data = None

if st.button("Start Learning"):
    response = requests.post(
        "http://127.0.0.1:8000/learn",
        json = {
            "user_id": user_id,
            "topic": topic,
            "mode": "quiz",
            #"learner_answers": ["Retrieval and Generation"],
            "learner_answers": [],
            "max_attempts": 3,
        },
    )

    st.write(response.status_code)
    st.write(response.json())

    st.session_state.lesson_dta = response.json()

if st.session_state.lesson_data:

    data = st.session_state.lesson_data

    st.subheader("Lesson")
    st.write(data.get("lesson",""))

    st.subheader("Question")
    st.write(data.get("question",""))

    answer = st.text_area("Your Answer")


    if st.button("Submit Answer"):
        response = requests.post(
            "http://127.0.0.1:8000/learn",
            json = {
                "user_id": user_id,
                "topic": topic,
                "mode": "quiz",
                "learner_answers": [answer],
                "max_attempts": 3,
            },
        )

        result = response.json

        st.subheader("Score")
        st.write(data.get("evaluation",{}).get("score"))

        st.subheader("Feedback")
        st.write(data.get("evaluation",{}).get("feedback"))

        st.subheader("Next Action")
        st.write(result.get("next_action"))
