# app.py

# To run: streamlit run app.py OR python -m streamlit run app.py

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from recommendation_engine import recommend_courses, generate_learning_path, normalize_list
from skill_gap_analyzer import analyze_skill_gap, get_learning_resources
import json
import os

# Page config
st.set_page_config(
    page_title="PathPilot AI - Learning Path Generator",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #FF6B6B;
        text-align: center;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        text-align: center;
        color: #4ECDC4;
    }
    .card {
        padding: 20px;
        border-radius: 10px;
        background: #f8f9fa;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .skill-tag {
        display: inline-block;
        padding: 5px 15px;
        margin: 5px;
        border-radius: 20px;
        background: #4ECDC4;
        color: white;
        font-size: 0.9rem;
    }
    .missing-tag {
        background: #FF6B6B;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">🚀 PathPilot AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Your Personalized Learning Navigator</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/150x150?text=PathPilot", width=150)
    st.markdown("## 🎯 About")
    st.markdown("""
    PathPilot uses AI to create personalized learning paths 
    based on your skills, goals, and experience level.
    
    **Features:**
    - ✅ Smart Skill Analysis
    - ✅ Personalized Course Recommendations
    - ✅ Structured Learning Roadmap
    - ✅ Progress Tracking
    - ✅ AI Career Guidance
    """)
    
    st.markdown("---")
    st.markdown("Built with ❤️ for HCL Hackathon")

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["🎯 Your Profile", "📚 Learning Path", "📊 Progress", "🤖 AI Advisor"])

with tab1:
    st.markdown("### Tell us about yourself")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Your Name", placeholder="Enter your name")
        goal = st.text_input("What do you want to learn?", placeholder="e.g., Data Science, Web Development")
        
        experience = st.selectbox(
            "Experience Level",
            ["beginner", "intermediate", "advanced"]
        )
    
    with col2:
        skills_input = st.text_area(
            "Your Skills (comma separated)",
            placeholder="e.g., Python, SQL, HTML, CSS",
            help="List all the skills you already know"
        )
        
        hours_per_day = st.slider(
            "Hours available per day",
            min_value=1,
            max_value=8,
            value=2
        )
    
    if st.button("🚀 Generate My Learning Path", type="primary"):
        if not goal or not skills_input:
            st.error("Please enter your goal and skills!")
        else:
            with st.spinner("Analyzing your profile and generating path..."):
                # Parse skills
                user_skills = set(normalize_list(skills_input.split(",")))
                
                # Store in session
                st.session_state.user_skills = user_skills
                st.session_state.goal = goal
                st.session_state.experience = experience
                st.session_state.hours_per_day = hours_per_day
                
                # Generate path
                learning_path = generate_learning_path(user_skills, goal, experience)
                st.session_state.learning_path = learning_path
                
                # Also store for AI advisor
                st.session_state.recommendations = learning_path.get('roadmap', [])
                
                st.success("✅ Learning path generated successfully!")
                st.balloons()
                
                # Show quick stats
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📚 Courses", learning_path['total_courses'])
                with col2:
                    st.metric("⏱️ Duration", f"{len(learning_path['roadmap'])} months")
                with col3:
                    missing = len(learning_path['skill_gap']['missing_skills'])
                    st.metric("🔍 Skills to Learn", missing)

with tab2:
    if 'learning_path' not in st.session_state:
        st.info("👈 Go to 'Your Profile' and generate your learning path first!")
    else:
        path = st.session_state.learning_path
        
        st.markdown(f"## Your Learning Path for {path['goal']}")
        st.markdown(f"*Based on your skills: {', '.join(path['current_skills'])}*")
        
        # Skill gap visualization
        if path['skill_gap']['missing_skills']:
            st.markdown("### 🔍 Skills You Need to Learn")
            missing_skills = path['skill_gap']['missing_skills']
            col1, col2, col3 = st.columns(3)
            for i, skill in enumerate(missing_skills[:6]):
                with col1 if i < 2 else col2 if i < 4 else col3:
                    st.markdown(f'<span class="skill-tag missing-tag">{skill.upper()}</span>', unsafe_allow_html=True)
        else:
            st.success("🎉 You have all the skills needed!")
        
        # Roadmap
        st.markdown("### 📅 Your Learning Roadmap")
        
        for month_data in path['roadmap']:
            with st.expander(f"📆 {month_data['title']}", expanded=True):
                for i, rec in enumerate(month_data['courses'], 1):
                    course = rec['course']
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{i}. {course.name}**")
                        st.markdown(f"*{course.platform}* | ⭐ {course.difficulty} | ⏱️ {course.duration}")
                        if course.prerequisites:
                            st.caption(f"Prerequisites: {', '.join(course.prerequisites)}")
                    with col2:
                        st.markdown(f"**Match:** {rec['percentage']}%")
                        if rec['matched_skills']:
                            st.caption(f"Skills: {', '.join(list(rec['matched_skills'])[:3])}")
                    st.divider()

with tab3:
    if 'learning_path' not in st.session_state:
        st.info("👈 Generate a learning path first to see your progress!")
    else:
        st.markdown("### 📊 Your Progress Dashboard")
        
        # Simulated progress (in real app, this would come from database)
        import random
        total_courses = st.session_state.learning_path['total_courses']
        completed = random.randint(0, total_courses // 2)  # Simulated
        progress_pct = int((completed / total_courses) * 100) if total_courses > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📚 Total Courses", total_courses)
        with col2:
            st.metric("✅ Completed", completed)
        with col3:
            st.metric("📈 Progress", f"{progress_pct}%")
        
        # Progress bar
        st.progress(progress_pct / 100)
        
        # Skill radar chart
        st.markdown("### 🎯 Skill Radar")
        
        skills = st.session_state.learning_path['current_skills'][:6]
        if skills:
            # Simulate skill levels (0-100)
            current_levels = [random.randint(20, 70) for _ in skills]
            target_levels = [80] * len(skills)
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=current_levels,
                theta=skills,
                fill='toself',
                name='Your Skills',
                line_color='#4ECDC4'
            ))
            fig.add_trace(go.Scatterpolar(
                r=target_levels,
                theta=skills,
                fill='toself',
                name='Target',
                line_color='#FF6B6B'
            ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                showlegend=True,
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

with tab4:
    if 'learning_path' not in st.session_state:
        st.info("👈 Generate a learning path first to get AI advice!")
    else:
        st.markdown("### 🤖 AI Career Advisor")
        st.markdown("*Powered by Google Gemini*")
        
        if st.button("Get AI Career Guidance"):
            with st.spinner("Generating personalized career report..."):
                # Import Gemini integration
                from gemini_advisor import generate_career_advice
                
                # Get user data
                user_skills = st.session_state.user_skills
                goal = st.session_state.goal
                experience = st.session_state.experience
                
                # Get top course
                top_course = None
                if st.session_state.learning_path['roadmap']:
                    first_month = st.session_state.learning_path['roadmap'][0]
                    if first_month['courses']:
                        top_course = first_month['courses'][0]['course']
                
                # Generate advice
                advice = generate_career_advice(
                    user_skills=user_skills,
                    goal=goal,
                    level=experience,
                    top_course=top_course
                )
                
                st.markdown("### 📄 AI Career Report")
                st.markdown(advice)
                
                # Download option
                st.download_button(
                    label="📥 Download Report",
                    data=advice,
                    file_name="career_report.txt",
                    mime="text/plain"
                )