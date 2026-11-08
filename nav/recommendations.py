# =============================================================================
# RESULTS DISPLAY: Visualizes fuzzy logic outputs within the Streamlit UI.
# 1. Maps linguistic chat responses into numeric inputs for the inference engine.
# 2. Displays the top-ranked destination as a primary highlighted recommendation.
# 3. Renders a comparative match confidence for the Top 3 results.
# =============================================================================

import streamlit as st
import json
from nav.utils import results, questions
from fuzzy.inference_engine import recommend_destination

def recommendations():
    st.title("Your Personalized Vacation Recommendations")
    

    if st.session_state.step < len(questions):
        st.error(f"Please complete the chat first! You have answered {st.session_state.step} out of {len(questions)} questions.")
        if st.button("Go back to Chat", use_container_width=True):
            st.session_state.page = "chat"
            st.rerun()
        return
    

    numeric_inputs = results(st.session_state.responses)

    numeric_inputs = {
        "time": numeric_inputs.get("time"),
        "budget": numeric_inputs.get("budget"),
        "weather": numeric_inputs.get("weather"),
        "duration": numeric_inputs.get("duration"),
        "distance": numeric_inputs.get("distance"),
        "type": numeric_inputs.get("vacation_type")
    }


    with st.spinner("Analyzing your preferences with Fuzzy Logic..."):
        best, top_scores = recommend_destination(numeric_inputs)

    if not best:
        st.error("We couldn't find a perfect match. Try resetting and changing your preferences!")
        return

    with open("fuzzy/countries.json") as f:
        countries = json.load(f)


        
    
    st.markdown(f"""
        <div style="background-color: #D3e4ff; padding: 25px; border-radius: 15px; border-left: 10px solid #1d4ed8; height: 100%;">
            <h2 style="margin: 0; color: #1e3a8a;">Top Pick: {best}</h2>
            <p style="color: #1e3a8a; font-size: 1.1rem; margin-top: 10px;">
                Based on your preferences, <b>{best}</b> is the ideal destination for your next trip!
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Llista de recomanacions detallada
    st.subheader("Analysis of Top 3 Destinations")
    
    for i, (dest, score) in enumerate(top_scores.items()):

        display_score = score * 100 
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown(f"### #{i+1} {dest}")
        
        with col2:
            st.markdown(f"**Match Confidence: {display_score:.1f}%**")
            st.progress(score)
    
    
    st.divider()
    
    data_best = countries[best]
    
    st.header("Quick Facts")
    
    # Utilitzem columnes niades per organitzar les mètriques en graella
    m1, m2 = st.columns(2)
    
    with m1:
        st.metric(label="Continent", value=data_best['continent'])
        st.metric(label="Weather", value=data_best['weather'].capitalize())
        st.metric(label="Duration", value=data_best['duration'].capitalize())

    with m2:
        st.metric(label="Budget", value=data_best['budget'].capitalize())
        st.metric(label="Distance", value=data_best['distance'].capitalize())
        # Per a llistes, seleccionem el primer element o les ajuntem
        st.metric(label="Main Style", value=data_best['type'][0].capitalize())

    

    st.divider()
    
    # Botó per veure paràmetres tècnics (OPCIONAL)
    with st.expander("See technical fuzzy inputs"):
        st.write(numeric_inputs)