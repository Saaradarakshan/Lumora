# app.py
"""
Lumora - Career & Learning Navigation System
Personalized Learning Roadmaps, Skill Gap Analytics & Mentorship
"""

import sys
import os
import requests
import streamlit as st
import plotly.graph_objects as go

# Local engines for reliable matching
from course_database import COURSES
from PathPilot import INTERNSHIPS
import recommendation_engine as rec_engine
import skill_gap_analyzer as gap_analyzer
import gemini_advisor

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api")

st.set_page_config(
    page_title="Lumora - Career & Learning Navigator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Google Fonts & Custom CSS ───────────────────────────────────────────────────
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">', unsafe_allow_html=True)

st.markdown("""
    <style>
    :root {
        --bg-deep:      #070b14;
        --bg-card:      #0f172a;
        --border:       rgba(56, 189, 248, 0.15);
        --cyan:         #38bdf8;
        --purple:       #a855f7;
        --pink:         #ec4899;
        --text-main:    #f8fafc;
        --text-muted:   #94a3b8;
        --success:      #10b981;
    }

    html, body, [class*="stApp"] {
        background-color: var(--bg-deep) !important;
        font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
        color: var(--text-main) !important;
    }

    [data-testid="stSidebar"] {
        background: #0b1120 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    [data-testid="stSidebar"] * { color: var(--text-main) !important; }

    .main-header {
        font-size: 3.3rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
        line-height: 1.15;
        margin-bottom: 6px;
    }
    .sub-header {
        font-size: 1.1rem;
        text-align: center;
        color: var(--text-muted);
        margin-top: 0;
        margin-bottom: 30px;
        font-weight: 400;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: transparent;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(15, 23, 42, 0.6) !important;
        color: var(--text-muted) !important;
        border-radius: 10px !important;
        font-weight: 600;
        padding: 10px 22px;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.15) 0%, rgba(168, 85, 247, 0.15) 100%) !important;
        color: #38bdf8 !important;
        border: 1px solid rgba(56, 189, 248, 0.4) !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.15);
    }

    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea,
    [data-testid="stSelectbox"] > div {
        background: #0f172a !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        color: var(--text-main) !important;
        border-radius: 12px !important;
    }
    [data-testid="stTextInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.25) !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #0284c7 0%, #7c3aed 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 28px !important;
        font-size: 1rem !important;
        letter-spacing: 0.3px;
        transition: all 0.25s ease !important;
        box-shadow: 0 4px 20px rgba(2, 132, 199, 0.35);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 28px rgba(124, 58, 237, 0.45) !important;
    }

    .rec-card, .course-card {
        padding: 22px 26px;
        border-radius: 16px;
        background: #0f172a;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin: 16px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
        transition: all 0.25s ease;
    }
    .rec-card:hover, .course-card:hover {
        transform: translateY(-3px);
        border-color: rgba(56, 189, 248, 0.4);
        box-shadow: 0 12px 40px rgba(56, 189, 248, 0.12);
        background: #131d35;
    }
    .card-title {
        font-size: 1.22rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .card-meta {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-bottom: 12px;
    }
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 700;
        margin-right: 6px;
    }
    .badge-cyan { background: rgba(56, 189, 248, 0.12); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }
    .badge-purple { background: rgba(168, 85, 247, 0.12); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.3); }
    .badge-green { background: rgba(16, 185, 129, 0.12); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-pink { background: rgba(236, 72, 153, 0.12); color: #f472b6; border: 1px solid rgba(236, 72, 153, 0.3); }

    .skill-pill {
        display: inline-block;
        padding: 3px 10px;
        margin: 2px 4px 2px 0;
        border-radius: 12px;
        font-size: 0.78rem;
        font-weight: 600;
        background: rgba(56, 189, 248, 0.08);
        border: 1px solid rgba(56, 189, 248, 0.25);
        color: #38bdf8;
    }
    .skill-pill-missing {
        display: inline-block;
        padding: 3px 10px;
        margin: 2px 4px 2px 0;
        border-radius: 12px;
        font-size: 0.78rem;
        font-weight: 600;
        background: rgba(244, 63, 94, 0.08);
        border: 1px solid rgba(244, 63, 94, 0.25);
        color: #fb7185;
    }
    </style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown('<h1 class="main-header">Lumora Career Navigator</h1>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Your Personalized Learning Roadmap, Skill Gap Analyzer & Career Mentor</div>', unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🧭 Student Career Hub")
    st.markdown("Discover the fastest path to your target role with personalized course recommendations, skill gap breakdowns, and curated internships.")
    st.markdown("---")
    st.markdown("#### 💡 Pro Tips for Success")
    st.markdown("""
    - **Add Specific Skills**: Include tools, frameworks, and programming languages you know.
    - **Review Missing Skills**: Check the Analytics tab to prioritize what to learn next.
    - **Build Projects**: Apply your new skills to create standout portfolio projects.
    """)
    st.markdown("---")
    st.caption("Lumora Navigator • Empowering Your Career Journey")

# ── Recommendation Fetchers ──────────────────────────────────────────────────
def fetch_course_recommendations(payload):
    try:
        res = requests.post(f"{BACKEND_URL}/recommend-courses", json=payload, timeout=3)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    
    # Built-in engine fallback
    user_skills_set = {s.strip().lower() for s in payload["user_skills"] if s.strip()}
    recs = rec_engine.recommend_courses(user_skills_set, payload["experience_level"], payload["domain_pref"])
    return [
        {
            "id": idx + 1,
            "name": r["course"].name,
            "platform": r["course"].platform,
            "difficulty": r["course"].difficulty,
            "domain": r["course"].domain,
            "duration": r["course"].duration,
            "match_percentage": r["percentage"],
            "matched_skills": list(r["matched_skills"])
        }
        for idx, r in enumerate(recs)
    ]

def fetch_internship_recommendations(payload):
    try:
        res = requests.post(f"{BACKEND_URL}/recommend-internships", json=payload, timeout=3)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    
    # Built-in engine fallback
    user_skills_set = {s.strip().lower() for s in payload["user_skills"] if s.strip()}
    from PathPilot import score_internship
    results = []
    for idx, intern in enumerate(INTERNSHIPS):
        score, pct, matched = score_internship(intern, user_skills_set, payload["experience_level"], payload["domain_pref"], "any")
        if score > 0:
            results.append({
                "id": idx + 1,
                "title": intern.title,
                "company": intern.company,
                "level": intern.level,
                "domain": intern.domain,
                "mode": intern.mode,
                "match_percentage": pct,
                "matched_skills": list(matched)
            })
    results.sort(key=lambda x: x["match_percentage"], reverse=True)
    return results

def fetch_career_advice(payload):
    try:
        res = requests.post(f"{BACKEND_URL}/generate-career-advice", json=payload, timeout=30)
        if res.status_code == 200:
            return res.json().get("advice")
    except Exception:
        pass
    
    # Built-in advisor fallback
    skills_set = {s.strip().lower() for s in payload["user_skills"] if s.strip()}
    return gemini_advisor.generate_career_advice(
        skills_set, payload["goal"], payload["experience_level"], payload["top_recommendation"]
    )

# ── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Your Profile", 
    "📊 Skill Gap & Analytics", 
    "📚 Courses", 
    "💼 Internships", 
    "🧭 Career Strategy & Roadmap"
])

# ────────────────── TAB 1: Profile ──────────────────
with tab1:
    st.markdown("### 🎯 Define Your Career Goal & Current Skills")
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        goal = st.text_input("Target Role / Goal", value=st.session_state.get("goal", "Data Scientist"), placeholder="e.g., Data Scientist, Full Stack Developer")
        col_a, col_b = st.columns(2)
        with col_a:
            experience = st.selectbox("Current Experience Level", ["beginner", "intermediate", "advanced"], index=0)
        with col_b:
            domain = st.selectbox("Industry Domain", ["any", "ml", "ai", "data", "web", "cloud", "cybersecurity", "iot"], index=1)
            
        st.markdown("#### ⚡ Popular Skill Chips")
        chips = ["Python", "SQL", "Machine Learning", "Pandas", "React", "JavaScript", "Docker", "AWS", "FastAPI", "Linux"]
        selected_chips = st.pills("Click to quickly add skills to your profile:", chips, selection_mode="multi") if hasattr(st, "pills") else []
        
    with col2:
        current_text = st.session_state.get("skills_text", "Python, SQL, HTML, CSS")
        if selected_chips:
            existing = [s.strip() for s in current_text.split(",") if s.strip()]
            combined = list(dict.fromkeys(existing + list(selected_chips)))
            current_text = ", ".join(combined)
            
        skills_input = st.text_area("Skills You Already Have (Comma Separated)", value=current_text, height=140, placeholder="Python, SQL, Pandas, Git, Docker")
        
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Analyze Profile & Build My Roadmap", use_container_width=True):
        if not goal or not skills_input:
            st.warning("Please specify your target goal and at least one skill.")
        else:
            with st.spinner("Analyzing your skill profile and finding the best matching paths..."):
                user_skills_list = [s.strip().lower() for s in skills_input.split(",") if s.strip()]
                payload = {
                    "user_skills": user_skills_list,
                    "goal": goal,
                    "experience_level": experience,
                    "domain_pref": domain
                }
                
                courses = fetch_course_recommendations(payload)
                internships = fetch_internship_recommendations(payload)
                
                st.session_state.payload = payload
                st.session_state.courses = courses
                st.session_state.internships = internships
                st.session_state.goal = goal
                st.session_state.skills_text = skills_input
                
                st.success("✨ Analysis complete! Check the Skill Gap, Courses, and Career Strategy tabs.")

# ────────────────── TAB 2: Skill Gap & Analytics ──────────────────
with tab2:
    if "payload" in st.session_state and "courses" in st.session_state:
        user_skills = set(st.session_state.payload["user_skills"])
        
        all_required = set()
        for c in COURSES:
            if st.session_state.payload["domain_pref"] == "any" or c.domain == st.session_state.payload["domain_pref"]:
                all_required.update([s.lower() for s in c.skills])
                
        gap_results = gap_analyzer.analyze_skill_gap(user_skills, list(all_required))
        
        st.markdown("### 📊 Skill Competency & Gap Breakdown")
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Goal Readiness Score", f"{gap_results['match_percentage']}%")
        m2.metric("Skills Mastered", f"{gap_results['total_matched']}")
        m3.metric("Skills to Build", f"{gap_results['total_missing']}")
        m4.metric("Total Domain Skills", f"{gap_results['total_required']}")
        
        st.markdown("---")
        col_chart1, col_chart2 = st.columns([1, 1], gap="large")
        
        with col_chart1:
            st.markdown("#### 🎯 Domain Skill Coverage")
            fig = go.Figure(data=[go.Pie(
                labels=["Mastered Skills", "Skills to Acquire"],
                values=[gap_results['total_matched'], gap_results['total_missing']],
                hole=.6,
                marker=dict(colors=["#38bdf8", "#ec4899"])
            )])
            fig.update_layout(
                showlegend=True,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f8fafc"),
                margin=dict(t=20, b=20, l=20, r=20),
                height=280
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col_chart2:
            st.markdown("#### 💡 Priority Order to Learn Next")
            priority_skills = gap_analyzer.suggest_learning_priority(gap_results["missing_skills"])
            if priority_skills:
                for idx, skill in enumerate(priority_skills[:8], 1):
                    st.markdown(f"**{idx}.** <span class='skill-pill-missing'>{skill.upper()}</span>", unsafe_allow_html=True)
            else:
                st.success("🎉 You possess all required core skills for this domain!")
                
        st.markdown("#### 📖 Recommended Learning Resources")
        resources = gap_analyzer.get_learning_resources(gap_results["missing_skills"][:6])
        res_cols = st.columns(min(len(resources), 3) or 1)
        for i, (skill, links) in enumerate(resources.items()):
            with res_cols[i % len(res_cols)]:
                st.markdown(f"**{skill.title()}**")
                for link in links:
                    st.markdown(f"- {link}")
    else:
        st.info("👈 Enter your profile details in Tab 1 and click **Analyze Profile** to view your skill analytics.")

# ────────────────── TAB 3: Courses ──────────────────
with tab3:
    if "courses" in st.session_state and st.session_state.courses:
        st.markdown(f"### 📚 Recommended Courses for **{st.session_state.goal}**")
        
        filter_col1, filter_col2 = st.columns([1, 2])
        with filter_col1:
            min_match = st.slider("Minimum Match Percentage", 0, 100, 20)
            
        filtered_courses = [c for c in st.session_state.courses if c["match_percentage"] >= min_match]
        
        for course in filtered_courses:
            matched_tags = "".join([f"<span class='skill-pill'>✓ {s}</span>" for s in course["matched_skills"]])
            
            st.markdown(f"""
            <div class="rec-card">
                <div class="card-title">
                    <span>{course['name']}</span>
                    <span class="badge badge-cyan">{course['match_percentage']}% Match</span>
                </div>
                <div class="card-meta">
                    <span class="badge badge-purple">{course['platform']}</span>
                    <span class="badge badge-green">{course['difficulty'].title()}</span>
                    <span class="badge badge-pink">⏱ {course['duration']}</span>
                </div>
                <p style="margin-top: 10px; font-size: 0.9rem; color: #94a3b8;">
                    <strong>Matched Skills:</strong> {matched_tags if matched_tags else '<span style=\"color:#64748b;\">Foundational Track</span>'}
                </p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Update your profile in Tab 1 to see course recommendations.")

# ────────────────── TAB 4: Internships ──────────────────
with tab4:
    if "internships" in st.session_state and st.session_state.internships:
        st.markdown(f"### 💼 Top Matching Internship Opportunities")
        for intern in st.session_state.internships:
            matched_tags = "".join([f"<span class='skill-pill'>✓ {s}</span>" for s in intern["matched_skills"]])
            st.markdown(f"""
            <div class="rec-card">
                <div class="card-title">
                    <span>{intern['title']} @ {intern['company']}</span>
                    <span class="badge badge-pink">{intern['match_percentage']}% Match</span>
                </div>
                <div class="card-meta">
                    <span class="badge badge-cyan">🌐 {intern['mode'].title()}</span>
                    <span class="badge badge-purple">📈 {intern['level'].title()}</span>
                    <span class="badge badge-green">📁 {intern['domain'].upper()}</span>
                </div>
                <p style="margin-top: 10px; font-size: 0.9rem; color: #94a3b8;">
                    <strong>Matching Strengths:</strong> {matched_tags if matched_tags else '<span style=\"color:#64748b;\">General match</span>'}
                </p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Update your profile in Tab 1 to see internship matches.")

# ────────────────── TAB 5: Career Strategy & Roadmap ──────────────────
with tab5:
    if "payload" in st.session_state and "courses" in st.session_state:
        st.markdown("### 🧭 Personalized Career Strategy & Roadmap")
        st.caption("Generate a tailored step-by-step action plan with milestone targets, project ideas, and interview strategies.")
        
        if st.button("✨ Generate My Action Plan & Strategy", use_container_width=True):
            with st.spinner("Crafting your personalized career roadmap & guidance..."):
                top_course = st.session_state.courses[0]['name'] if st.session_state.courses else "Foundational Course"
                payload = {
                    "user_skills": st.session_state.payload["user_skills"],
                    "goal": st.session_state.payload["goal"],
                    "experience_level": st.session_state.payload["experience_level"],
                    "top_recommendation": top_course
                }
                
                advice_text = fetch_career_advice(payload)
                st.session_state.advice = advice_text
                
        if "advice" in st.session_state:
            st.markdown("---")
            st.markdown(st.session_state.advice)
            st.download_button(
                "📥 Download Career Plan (.txt)",
                data=st.session_state.advice,
                file_name=f"Lumora_Career_Plan_{st.session_state.goal.replace(' ', '_')}.txt",
                mime="text/plain"
            )
    else:
        st.info("Please analyze your profile in Tab 1 first to generate your custom career plan.")