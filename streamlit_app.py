"""
Streamlit Interface for Context-Aware Spell Checker
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any
import time

from spell_checker import ContextAwareSpellChecker, SpellCheckResult

# Page configuration
st.set_page_config(
    page_title="Context-Aware Spell Checker",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    
    .correction-item {
        background: #e3f2fd;
        padding: 0.5rem;
        border-radius: 6px;
        margin: 0.25rem;
        display: inline-block;
    }
    
    .stTextArea > div > div > textarea {
        font-size: 16px;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_spell_checker():
    """Load and cache the spell checker"""
    with st.spinner("Loading spell checker..."):
        return ContextAwareSpellChecker()

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🧠 Context-Aware Spell Checker</h1>
        <p>Advanced spell checking powered by BERT and context analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load spell checker
    spell_checker = load_spell_checker()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Model selection
        model_options = [
            "bert-base-uncased",
            "bert-base-cased", 
            "distilbert-base-uncased",
            "roberta-base"
        ]
        
        selected_model = st.selectbox(
            "Select Model",
            model_options,
            index=0
        )
        
        st.markdown("---")
        
        # Display system info
        st.subheader("📊 System Info")
        st.info(f"**Current Model:** {spell_checker.model_name}")
        st.info(f"**Device:** {spell_checker.device}")
        
        # Database stats
        st.subheader("🗄️ Database Stats")
        misspellings = spell_checker.db.get_misspellings()
        homophones = spell_checker.db.get_homophones()
        
        st.metric("Misspellings", len(misspellings))
        st.metric("Homophone Groups", len(homophones))
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Text Input")
        
        # Text input
        text_input = st.text_area(
            "Enter text to check:",
            height=200,
            placeholder="Type or paste your text here...",
            help="The spell checker will analyze your text for spelling errors, homophones, and context issues."
        )
        
        # Buttons
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        
        with col_btn1:
            check_button = st.button("🔍 Check Spelling", type="primary", use_container_width=True)
        
        with col_btn2:
            clear_button = st.button("🗑️ Clear", use_container_width=True)
        
        with col_btn3:
            example_button = st.button("📋 Load Example", use_container_width=True)
        
        if clear_button:
            st.rerun()
        
        if example_button:
            example_text = "She went to the sea to meat her friend. Their going to the store to buy there groceries. I recieve the package yesterday and it was definately worth it."
            st.session_state.example_text = example_text
            st.rerun()
        
        if 'example_text' in st.session_state:
            text_input = st.session_state.example_text
    
    with col2:
        st.subheader("📈 Quick Stats")
        
        if text_input:
            # Basic text stats
            word_count = len(text_input.split())
            char_count = len(text_input)
            sentence_count = text_input.count('.') + text_input.count('!') + text_input.count('?')
            
            st.metric("Words", word_count)
            st.metric("Characters", char_count)
            st.metric("Sentences", sentence_count)
    
    # Process text if button clicked
    if check_button and text_input:
        with st.spinner("Analyzing text..."):
            # Perform spell check
            result = spell_checker.correct_text(text_input)
            stats = spell_checker.get_text_statistics(text_input)
            
            # Store results in session state
            st.session_state.spell_check_result = result
            st.session_state.text_stats = stats
    
    # Display results
    if 'spell_check_result' in st.session_state:
        result = st.session_state.spell_check_result
        stats = st.session_state.text_stats
        
        st.markdown("---")
        st.subheader("📊 Results")
        
        # Create tabs for different result views
        tab1, tab2, tab3, tab4 = st.tabs(["📝 Text Analysis", "🔧 Corrections", "📈 Statistics", "🎯 Confidence"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Original Text:**")
                st.text_area("", result.original_text, height=100, disabled=True)
            
            with col2:
                st.markdown("**Corrected Text:**")
                st.text_area("", result.corrected_text, height=100, disabled=True)
        
        with tab2:
            if result.corrections_made:
                st.markdown("**Corrections Made:**")
                
                corrections_df = pd.DataFrame(result.corrections_made)
                
                # Display corrections in a nice format
                for i, correction in enumerate(result.corrections_made):
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        st.markdown(f"**{correction['original']}**")
                    
                    with col2:
                        st.markdown(f"**→ {correction['corrected']}**")
                    
                    with col3:
                        st.markdown(f"*({correction['type']})*")
                
                # Show suggestions if available
                if result.suggestions:
                    st.markdown("**Detailed Suggestions:**")
                    for suggestion in result.suggestions:
                        with st.expander(f"Word: {suggestion.get('word', 'Unknown')}"):
                            st.json(suggestion)
            else:
                st.success("✅ No corrections needed! Your text looks good.")
        
        with tab3:
            # Text statistics
            st.markdown("**Text Statistics:**")
            
            # Create metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Word Count", stats['word_count'])
            
            with col2:
                st.metric("Character Count", stats['character_count'])
            
            with col3:
                st.metric("Sentence Count", stats['sentence_count'])
            
            with col4:
                st.metric("Readability Score", f"{stats['flesch_reading_ease']:.1f}")
            
            # Readability visualization
            st.markdown("**Readability Analysis:**")
            
            readability_data = {
                'Metric': ['Flesch Reading Ease', 'Flesch-Kincaid Grade', 'Automated Readability Index'],
                'Score': [stats['flesch_reading_ease'], stats['flesch_kincaid_grade'], stats['readability_score']]
            }
            
            fig = px.bar(
                readability_data, 
                x='Metric', 
                y='Score',
                title="Readability Metrics",
                color='Score',
                color_continuous_scale='viridis'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            # Confidence analysis
            st.markdown("**Confidence Analysis:**")
            
            confidence_score = result.confidence_score
            
            # Confidence gauge
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = confidence_score * 100,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Overall Confidence"},
                delta = {'reference': 80},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Confidence breakdown
            if result.corrections_made:
                st.markdown("**Confidence by Correction Type:**")
                
                correction_types = {}
                for correction in result.corrections_made:
                    corr_type = correction['type']
                    if corr_type not in correction_types:
                        correction_types[corr_type] = 0
                    correction_types[corr_type] += 1
                
                fig = px.pie(
                    values=list(correction_types.values()),
                    names=list(correction_types.keys()),
                    title="Correction Types Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
