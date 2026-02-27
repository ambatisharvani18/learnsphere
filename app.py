import streamlit as st
import os
import io
from dotenv import load_dotenv
from google import genai
from gtts import gTTS

# 1. Setup & Environment
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("🚨 API Key not found! Please check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)
MODEL_ID = "gemini-2.5-flash" # Most stable for free tier

# 2. Page Navigation System
if "page" not in st.session_state:
    st.session_state.page = "welcome"
if "user_data" not in st.session_state:
    st.session_state.user_data = {"level": "", "topic": "", "style": ""}

# --- PAGE 1: WELCOME & LEVEL ---
if st.session_state.page == "welcome":
    st.title("🌟 Welcome to AI-Academy")
    st.write("Your personalized journey into Machine Learning starts here.")
    
    level = st.selectbox("What is your current ML level?", ["Beginner", "Intermediate", "Advanced"])
    if st.button("Start Journey"):
        st.session_state.user_data['level'] = level
        st.session_state.page = "roadmap"
        st.rerun()

# --- PAGE 2: ROADMAP ---
elif st.session_state.page == "roadmap":
    st.title(f"🗺️ Your {st.session_state.user_data['level']} Roadmap")
    
    with st.spinner("Generating roadmap..."):
        prompt = f"Create a 5-step ML roadmap for a {st.session_state.user_data['level']} student. Return ONLY the list."
        roadmap = client.models.generate_content(model=MODEL_ID, contents=prompt).text
    
    st.markdown(roadmap)
    topic = st.text_input("Enter a topic you want to master:")
    if st.button("Learn Topic"):
        st.session_state.user_data['topic'] = topic
        st.session_state.page = "style"
        st.rerun()

# --- PAGE 3: LEARNING STYLE & LESSON ---
# --- PAGE 3: LEARNING STYLE & LESSON ---
elif st.session_state.page == "style":
    st.title(f"📚 Mastering {st.session_state.user_data['topic']}")
    style = st.radio("How do you learn best?", ["Reading", "Auditory", "Kinesthetic (Code)", "Visual"])
    
    if st.button("Generate Lesson"):
        prompt = f"Explain {st.session_state.user_data['topic']} in-depth for a {st.session_state.user_data['level']} learner."
        with st.spinner("Preparing your lesson..."):
            if style == "Reading":
                st.write(client.models.generate_content(model=MODEL_ID, contents=prompt).text)
            elif style == "Kinesthetic (Code)":
                st.code(client.models.generate_content(model=MODEL_ID, contents=prompt + " Provide Python code.").text)
            elif style == "Auditory":
                text = client.models.generate_content(model=MODEL_ID, contents=prompt).text
                tts = gTTS(text=text[:1000], lang='en')
                audio_fp = io.BytesIO()
                tts.write_to_fp(audio_fp)
                st.audio(audio_fp.getvalue(), format="audio/mp3")
                st.write(text)
            elif style == "Visual":
                st.video(f"https://www.youtube.com/results?search_query={st.session_state.user_data['topic']}")
                st.write(client.models.generate_content(model=MODEL_ID, contents=prompt + " Use descriptive imagery.").text)
            
            # Save a flag so the "Next" button appears
            st.session_state.lesson_completed = True

    # This button is now OUTSIDE the if st.button block so it stays visible
    if st.session_state.get("lesson_completed"):
        if st.button("Proceed to Knowledge Check ➡️"):
            st.session_state.page = "test"
            st.rerun()

# --- PAGE 4: ADAPTIVE TEST & FEEDBACK ---
# --- PAGE 4: 3-QUESTION ADAPTIVE TEST ---
elif st.session_state.page == "test":
    st.title("📝 Mastery Check (3 Questions)")

    # 1. Initialize Test Variables
    if "q_count" not in st.session_state:
        st.session_state.q_count = 1
        st.session_state.history = []
        st.session_state.current_q = ""

    # 2. Check if we have completed 3 questions
    if st.session_state.q_count <= 3:
        st.subheader(f"Question {st.session_state.q_count} of 3")
        
        # Generate a new question if we don't have one
        if not st.session_state.current_q:
            with st.spinner("Generating next challenge..."):
                q_type = "MCQ with 4 options" if st.session_state.q_count < 3 else "Coding logic problem"
                q_prompt = f"Ask a {q_type} for a {st.session_state.user_data['level']} on {st.session_state.user_data['topic']}."
                st.session_state.current_q = client.models.generate_content(model=MODEL_ID, contents=q_prompt).text
        
        st.info(st.session_state.current_q)
        user_ans = st.text_area("Your Answer:", key=f"ans_{st.session_state.q_count}")

        if st.button("Submit Answer"):
            # Save the interaction to history
            st.session_state.history.append({"q": st.session_state.current_q, "a": user_ans})
            st.session_state.q_count += 1
            st.session_state.current_q = "" # Reset for next question
            st.rerun()

    # 3. Final Feedback & Recommendations
    else:
        st.success("🎉 Quiz Completed!")
        with st.spinner("Analyzing your overall performance..."):
            history_text = "\n".join([f"Q: {h['q']}\nA: {h['a']}" for h in st.session_state.history])
            
            final_prompt = f"""
            The user just finished an ML quiz on {st.session_state.user_data['topic']}.
            History: {history_text}
            
            Please provide:
            1. **Overall Feedback**: How did they do?
            2. **Revision Parts**: List 2-3 specific sub-topics they should re-read.
            3. **Mini Projects/Coding Tasks**: Suggest 2 small hands-on tasks to increase knowledge.
            """
            
            analysis = client.models.generate_content(model=MODEL_ID, contents=final_prompt).text
            st.markdown(analysis)

        if st.button("Start New Topic"):
            # Reset all test data
            for key in ["q_count", "history", "current_q", "lesson_completed"]:
                if key in st.session_state: del st.session_state[key]
            st.session_state.page = "roadmap"
            st.rerun()