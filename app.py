import random
import time

import streamlit as st

from randq.selector import rand_draw


st.set_page_config(page_title="Random Question", page_icon="?")
st.title("Random Question")
st.caption("Build a roster and a question bank, then draw a pair.")


if "names" not in st.session_state:
    st.session_state.names = []
if "questions" not in st.session_state:
    st.session_state.questions = []
if "used_pairs" not in st.session_state:
    st.session_state.used_pairs = set()
if "result" not in st.session_state:
    st.session_state.result = None
if "rng" not in st.session_state:
    st.session_state.rng = random.Random()

party_mode = st.toggle("Party mode", key="party_mode")

if party_mode:
    st.markdown(
        """
        <style>
        :root {
            --party-pink: #ff2d8d;
            --party-yellow: #ffe45e;
            --party-cyan: #36e0ff;
            --party-purple: #7928ff;
            --party-ink: #24113f;
        }
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #fff06a 0%, #ff9bd6 36%, #80f7ff 72%, #c8a6ff 100%);
            background-attachment: fixed;
        }
        [data-testid="stHeader"] {
            background: transparent;
        }
        .block-container {
            background: rgba(255, 255, 255, 0.72);
            border: 4px solid var(--party-pink);
            border-radius: 18px;
            box-shadow: 10px 10px 0 var(--party-purple), 0 0 35px rgba(255, 45, 141, 0.42);
        }
        h1, h2, h3, p, label, [data-testid="stMarkdownContainer"] {
            color: var(--party-ink) !important;
        }
        h1 {
            text-shadow: 3px 3px 0 var(--party-yellow);
        }
        [data-testid="stTextInput"] input {
            background: #fffdf0;
            border: 3px solid var(--party-cyan);
            color: var(--party-ink);
            box-shadow: 4px 4px 0 var(--party-yellow);
        }
        [data-testid="stButton"] button {
            background: var(--party-pink);
            border: 3px solid var(--party-purple);
            color: white;
            font-weight: 800;
            box-shadow: 4px 4px 0 var(--party-yellow);
        }
        [data-testid="stButton"] button:hover {
            background: var(--party-purple);
            border-color: var(--party-pink);
            color: white;
        }
        [data-testid="stAlert"] {
            background: rgba(255, 228, 94, 0.82);
            border: 3px solid var(--party-pink);
            color: var(--party-ink);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def add_item(input_key, target_key):
    value = st.session_state[input_key].strip()
    if value:
        st.session_state[target_key].append(value)


def draw_pair(allow_repeats):
    names = st.session_state.names
    questions = st.session_state.questions
    rng = st.session_state.rng

    if allow_repeats:
        return rand_draw(names, questions, rng)

    possible_pairs = len(names) * len(questions)
    for _ in range(possible_pairs):
        pair = rand_draw(names, questions, rng)
        if pair not in st.session_state.used_pairs:
            return pair
    return None


st.subheader("Roster")
name_input, name_add = st.columns([4, 1])
with name_input:
    st.text_input("Name", key="name_input")
with name_add:
    st.write("")
    st.button("Add", key="add_name", on_click=add_item, args=("name_input", "names"))
st.write(st.session_state.names or "No names added yet.")

st.subheader("Questions")
question_input, question_add = st.columns([4, 1])
with question_input:
    st.text_input("Question", key="question_input")
with question_add:
    st.write("")
    st.button(
        "Add",
        key="add_question",
        on_click=add_item,
        args=("question_input", "questions"),
    )
st.write(st.session_state.questions or "No questions added yet.")

no_repeats = st.checkbox("No repeats", value=False)
draw_clicked = st.button("Draw", type="primary", disabled=not st.session_state.names or not st.session_state.questions)

if draw_clicked:
    pair = draw_pair(no_repeats)
    if pair is None:
        st.session_state.result = None
        st.error("All possible name and question pairs have been drawn.")
    else:
        flash = st.empty()
        flash_count = 10
        for _ in range(flash_count):
            flash_pair = draw_pair(False)
            if flash_pair is not None:
                flash.info(f"{flash_pair[0]}, please answer: {flash_pair[1]}")
            time.sleep(0.3)
        flash.empty()
        st.session_state.result = pair
        st.session_state.used_pairs.add(pair)

if st.session_state.result is not None:
    chosen_name, chosen_question = st.session_state.result
    st.success(f"{chosen_name}, please answer: {chosen_question}")
