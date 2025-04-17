import streamlit as st
from utils.qa_system import ask_question
from utils.ticket_system import create_ticket
from utils.company_info import COMPANY_INFO

st.set_page_config(page_title="Dostoevsky Support Bot", page_icon="📚")

st.title("📖 Dostoevsky Support Bot")

st.sidebar.title("About the Project")
st.sidebar.info(COMPANY_INFO)

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Ask a question about Dostoevsky's works:")

if user_input:
    answer, source, confidence = ask_question(user_input)
    st.success(f"**Answer:** {answer}\n\n**Source:** {source}")

    if confidence < 0.5:
        st.warning("I'm not confident in the answer.")

    if st.button("Create Ticket"):
        ticket_id = create_ticket(user_input)
        st.info(f"Ticket created: `{ticket_id}`. Thank you!")

    st.session_state.history.append((user_input, answer))

with st.expander("📩 Create a Support Ticket"):
    name = st.text_input("Your name")
    email = st.text_input("Your email")
    title = st.text_input("Ticket title")
    description = st.text_area("Describe the issue in detail")

    if st.button("Submit Ticket"):
        if name and email and title and description:
            ticket_id = create_ticket(
                question=description,
                username=name,
                user_email=email,
                custom_title=title
            )
            st.success(f"Ticket submitted! ID: `{ticket_id}`")
        else:
            st.error("Please fill in all fields before submitting.")

# Display chat history only once, after all inputs
with st.container():
    if st.session_state.history:
        st.subheader("🗂️ Chat History")
        for i, (question, bot_answer) in enumerate(reversed(st.session_state.history)):
            st.markdown(f"**You:** {question}")
            st.markdown(f"**Bot:** {bot_answer}")
            st.divider()
