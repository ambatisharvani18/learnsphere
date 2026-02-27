"""
LearnSphere — Cerebras AI Utility Module
Handles all AI interactions via Cerebras Cloud SDK (OpenAI-compatible).
Roadmap, explanations, code, quizzes, feedback, revision, projects.
"""

import os
import json
import re
from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras

load_dotenv()

_client = None


def get_client():
    """Singleton Cerebras client."""
    global _client
    if _client is None:
        api_key = os.getenv("CEREBRAS_API_KEY")
        if not api_key or api_key == "your_cerebras_api_key_here":
            raise ValueError("Please set your CEREBRAS_API_KEY in the .env file")
        _client = Cerebras(api_key=api_key)
    return _client


def _ask_llm(prompt, model="llama3.1-8b"):
    """Send a prompt to Cerebras and return text."""
    client = get_client()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    return response.choices[0].message.content


# ─────────────────────────── ROADMAP ───────────────────────────

def generate_roadmap(level):
    """Generate an ML learning roadmap based on user level."""
    prompt = f"""You are an expert Machine Learning instructor.
Generate a structured learning roadmap for a **{level}** level student who wants to learn Machine Learning.

Return ONLY a valid JSON array of topic objects. No markdown, no code fences, no extra text.
Each object must have:
- "id": integer starting from 1
- "title": short topic name
- "description": one-line description
- "icon": a single relevant emoji

For Beginner: 10-12 foundational topics (start from basics like "What is ML?", types of ML, linear regression, etc.)
For Intermediate: 10-12 topics (ensemble methods, neural networks, NLP basics, feature engineering, etc.)
For Advanced: 10-12 topics (transformers, GANs, reinforcement learning, MLOps, etc.)

Example format:
[
  {{"id": 1, "title": "What is Machine Learning?", "description": "Understanding the basics of ML and its applications", "icon": "🤖"}},
  {{"id": 2, "title": "Types of ML", "description": "Supervised, unsupervised, and reinforcement learning", "icon": "📊"}}
]
"""
    raw = _ask_llm(prompt)
    raw = re.sub(r"```(?:json)?\s*", "", raw).strip().rstrip("`")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Find the first complete JSON array using bracket depth
        start = raw.find("[")
        if start != -1:
            depth = 0
            for i in range(start, len(raw)):
                if raw[i] == "[":
                    depth += 1
                elif raw[i] == "]":
                    depth -= 1
                    if depth == 0:
                        try:
                            return json.loads(raw[start:i+1])
                        except json.JSONDecodeError:
                            break
        return [{"id": 1, "title": "Machine Learning Basics", "description": "Core ML concepts", "icon": "🤖"}]


# ─────────────────────────── CONTENT ───────────────────────────

def generate_reading_content(topic, level):
    """Generate in-depth reading material (markdown)."""
    prompt = f"""You are an expert ML educator. Create comprehensive, in-depth educational content about **"{topic}"** for a **{level}** level learner.

Structure your response in well-formatted Markdown:
1. **Introduction** — What is it and why does it matter?
2. **Core Concepts** — Detailed explanation with intuitive analogies
3. **Mathematical Foundation** — Key formulas with explanations (use LaTeX notation where helpful)
4. **How It Works (Step-by-Step)** — Clear, numbered walkthrough
5. **Real-World Applications** — 3-4 practical examples
6. **Common Pitfalls & Tips** — Things to watch out for
7. **Key Takeaways** — Bullet-point summary

Make it engaging, use emojis sparingly for visual appeal, and include analogies a {level} student would understand.
"""
    return _ask_llm(prompt)


def generate_code_content(topic, level):
    """Generate hands-on code examples and practice problems."""
    prompt = f"""You are an expert ML coding instructor. Create hands-on Python coding content about **"{topic}"** for a **{level}** level learner.

Provide the following in well-formatted Markdown:

## 📝 Concept Implementation
Write a complete, well-commented Python implementation demonstrating "{topic}".
- Use libraries like NumPy, Pandas, Scikit-learn, or TensorFlow as appropriate.
- Include sample data generation or loading.
- Add detailed comments explaining every step.

## 🧪 Practice Problems
Give **2 coding challenges** related to this topic:
1. **Easy**: A guided problem with hints
2. **Medium/Hard**: A problem that requires deeper thinking

For each problem, provide:
- Problem statement
- Starter code template
- Expected output description
- Hint

## 🔧 Dependencies
List required pip packages.

Make the code production-quality, runnable, and educational.
"""
    return _ask_llm(prompt)


def generate_audio_script(topic, level):
    """Generate a conversational audio lesson script."""
    prompt = f"""You are a friendly, energetic ML tutor recording a podcast-style lesson.
Write a **conversational audio script** (3-5 minutes when read aloud) about **"{topic}"** for a **{level}** level learner.

Rules:
- Write in a natural, spoken style (not formal/academic)
- Use analogies and real-world examples
- Include rhetorical questions to keep the listener engaged
- Start with a catchy hook
- End with a memorable summary
- Do NOT include any formatting, headers, or markdown — just plain spoken text
- Use natural pauses indicated by "..."
- Keep sentences short and punchy for easy listening
"""
    return _ask_llm(prompt)


def generate_visual_content(topic, level):
    """Generate text-based visual explanations: ASCII diagrams, flowcharts, concept maps."""
    prompt = f"""You are an expert ML educator who specializes in VISUAL explanations.
Create rich visual-textual content about **"{topic}"** for a **{level}** level learner.

Include ALL of the following in well-formatted Markdown:

## 🎨 Concept Map
Create a text-based concept map showing how key ideas in "{topic}" connect to each other.
Use arrows (→, ←, ↔) and boxes to show relationships.

## 📊 ASCII Diagram
Draw a detailed ASCII art diagram showing the architecture/flow/process of "{topic}".
Make it clear and well-labeled. Example style:
```
┌──────────┐    ┌──────────┐    ┌──────────┐
│  Input   │───▶│ Process  │───▶│  Output  │
└──────────┘    └──────────┘    └──────────┘
```

## 🔄 Step-by-Step Visual Walkthrough
Show each step of the algorithm/concept with visual representations.
Use numbered steps with diagrams for data transformations.

## 📈 Comparison Table
Create a markdown table comparing key aspects, variants, or related concepts.

## 🧩 Mental Model
Provide a real-world analogy with a visual metaphor that makes the concept click.

Make everything highly visual and easy to scan. Use plenty of formatting, tables, and diagrams.
"""
    return _ask_llm(prompt)


# ─────────────────────────── QUIZ ───────────────────────────

def generate_quiz(topic, level):
    """Generate 3 varied quiz questions: scenario, code analysis, and MCQ."""
    prompt = f"""You are an ML assessment expert. Create exactly 3 quiz questions about **"{topic}"** for a **{level}** level learner.

Return ONLY a valid JSON array with exactly 3 objects. No markdown, no code fences.

Question types (one of each):
1. **"scenario"** — A real-life scenario question where the student must apply their knowledge
2. **"code_analysis"** — Show a Python code snippet and ask what it does, what's wrong, or what the output is
3. **"mcq"** — A multiple-choice question with 4 options

Each object must have:
- "type": one of "scenario", "code_analysis", "mcq"
- "question": the full question text (for code_analysis, include the code snippet in the question)
- "options": array of 4 strings (for mcq and code_analysis), null for scenario
- "correct_answer": the correct answer text
- "explanation": brief explanation of why this is correct

Example:
[
  {{
    "type": "scenario",
    "question": "A company wants to predict customer churn based on usage data. Which ML approach would you recommend and why?",
    "options": null,
    "correct_answer": "Binary classification using logistic regression or random forest, as churn prediction is a two-class problem with structured features.",
    "explanation": "Customer churn is a binary outcome (stays/leaves), making it a classification problem."
  }},
  {{
    "type": "code_analysis",
    "question": "What does this code do?\\nfrom sklearn.linear_model import LinearRegression\\nmodel = LinearRegression()\\nmodel.fit(X_train, y_train)\\nprint(model.coef_)",
    "options": ["Prints the intercept", "Prints the feature coefficients", "Prints accuracy", "Prints predictions"],
    "correct_answer": "Prints the feature coefficients",
    "explanation": "model.coef_ returns the learned coefficients/weights for each feature in linear regression."
  }},
  {{
    "type": "mcq",
    "question": "Which metric is most appropriate for an imbalanced classification dataset?",
    "options": ["Accuracy", "F1-Score", "MSE", "R-squared"],
    "correct_answer": "F1-Score",
    "explanation": "F1-Score balances precision and recall, making it suitable for imbalanced datasets where accuracy can be misleading."
  }}
]
"""
    raw = _ask_llm(prompt)
    raw = re.sub(r"```(?:json)?\s*", "", raw).strip().rstrip("`")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r'\[.*\]', raw, re.DOTALL)
        if match:
            return json.loads(match.group())
        return []


# ─────────────────────────── FEEDBACK ───────────────────────────

def evaluate_answers(topic, level, quiz_data, user_answers):
    """Evaluate user answers and provide feedback with strong/weak areas."""
    qa_text = ""
    for i, (q, ua) in enumerate(zip(quiz_data, user_answers), 1):
        qa_text += f"""
Question {i} ({q['type']}): {q['question']}
Correct Answer: {q['correct_answer']}
User's Answer: {ua}
"""

    prompt = f"""You are an ML educator evaluating a **{level}** student's quiz on **"{topic}"**.

Here are the questions and answers:
{qa_text}

Provide a detailed evaluation in valid JSON (no markdown, no code fences):
{{
  "score": <number 0-3>,
  "total": 3,
  "percentage": <number 0-100>,
  "per_question": [
    {{
      "question_num": 1,
      "is_correct": true or false,
      "feedback": "specific feedback for this answer"
    }},
    {{
      "question_num": 2,
      "is_correct": true or false,
      "feedback": "specific feedback for this answer"
    }},
    {{
      "question_num": 3,
      "is_correct": true or false,
      "feedback": "specific feedback for this answer"
    }}
  ],
  "strong_areas": ["list of concepts the student understands well"],
  "weak_areas": ["list of concepts the student needs to improve"],
  "overall_feedback": "encouraging, constructive overall feedback paragraph"
}}

Be fair but encouraging. Give partial credit for partially correct answers.
"""
    raw = _ask_llm(prompt)
    raw = re.sub(r"```(?:json)?\s*", "", raw).strip().rstrip("`")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            return json.loads(match.group())
        return {"score": 0, "total": 3, "percentage": 0, "per_question": [], "strong_areas": [], "weak_areas": ["Unable to evaluate"], "overall_feedback": "Please try again."}


# ─────────────────────────── REVISION ───────────────────────────

def generate_revision(topic, level, weak_areas):
    """Generate targeted revision material for weak areas."""
    weak_str = ", ".join(weak_areas) if weak_areas else "general concepts"
    prompt = f"""You are an expert ML tutor providing targeted revision for a **{level}** student.

The student just studied **"{topic}"** and struggled with: **{weak_str}**

Create focused revision material in Markdown:

## 🔄 Quick Revision: {topic}

### Areas to Strengthen
For each weak area, provide:
1. **Simple Explanation** — Explain it like they're hearing it for the first time
2. **Memory Aid** — A mnemonic, analogy, or trick to remember it
3. **Quick Example** — A concrete, simple example
4. **Practice Tip** — One specific thing they can do to practice

### 📋 Cheat Sheet
Create a concise reference table or bullet list of the most important formulas/concepts.

### 🎯 Action Items
3 specific next steps the student should take to strengthen their understanding.

Keep it concise, encouraging, and actionable.
"""
    return _ask_llm(prompt)


# ─────────────────────────── PROJECTS ───────────────────────────

def generate_project_suggestions(topics_covered, level):
    """Generate capstone project suggestions based on topics covered."""
    topics_str = ", ".join(topics_covered)
    prompt = f"""You are an ML mentor suggesting capstone projects for a **{level}** student.

They have studied these topics: **{topics_str}**

Suggest **3 project ideas** in Markdown format:

For each project provide:
### 🚀 Project [N]: [Project Name]
- **Difficulty**: Easy / Medium / Hard
- **Description**: 2-3 sentences about what the project does
- **Skills Applied**: Which of their studied topics this uses
- **Dataset Suggestion**: Where to find data (Kaggle, UCI, etc.)
- **Key Steps**: Numbered implementation roadmap (5-7 steps)
- **Bonus Challenge**: An extension to make it more impressive

Make projects practical, portfolio-worthy, and progressively challenging.
"""
    return _ask_llm(prompt)


# ─────────────────────────── DOUBT CLEARING ───────────────────────────

def answer_doubt(question, context_topic=None, level=None):
    """Answer a student's doubt about ML."""
    context = ""
    if context_topic:
        context = f"The student is currently learning about **{context_topic}**. "
    if level:
        context += f"They are a **{level}** level learner. "

    prompt = f"""{context}You are a friendly, expert ML tutor helping a student clear their doubt.

Student's question: {question}

Provide a clear, concise answer in Markdown:
- Use simple language appropriate to their level
- Include a quick example or analogy if helpful
- Keep it focused and to the point (not too long)
- If the question is about code, include a short code snippet
"""
    return _ask_llm(prompt)


# ─────────────────────────── FLASHCARDS ───────────────────────────

def generate_flashcards(topic, level):
    """Generate interactive flashcards for quick review."""
    prompt = f"""Create exactly 5 flashcards about **"{topic}"** for a **{level}** level learner.

Return ONLY a valid JSON array. No markdown, no code fences, no extra text.

Each flashcard must have:
- "front": a concise question or term (1 line)
- "back": a clear, concise answer or definition (2-3 lines max)
- "emoji": a relevant emoji

Example:
[
  {{"front": "What is overfitting?", "back": "When a model learns noise in training data and performs poorly on new data.", "emoji": "📈"}},
  {{"front": "Define learning rate", "back": "A hyperparameter controlling weight updates during training.", "emoji": "⚡"}}
]
"""
    raw = _ask_llm(prompt)
    raw = re.sub(r"```(?:json)?\s*", "", raw).strip().rstrip("`")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find("[")
        if start != -1:
            depth = 0
            for i in range(start, len(raw)):
                if raw[i] == "[":
                    depth += 1
                elif raw[i] == "]":
                    depth -= 1
                    if depth == 0:
                        try:
                            return json.loads(raw[start:i+1])
                        except json.JSONDecodeError:
                            break
        return [{"front": f"What is {topic}?", "back": "Review this topic!", "emoji": "📘"}]
