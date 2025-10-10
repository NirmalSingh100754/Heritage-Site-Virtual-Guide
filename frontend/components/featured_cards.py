import streamlit as st

def display_featured_cards(recommendations):
    """Display featured heritage sites in cards"""
    if not recommendations:
        st.info("🌟 No recommendations available at the moment.")
        return
    
    cols = st.columns(3)
    for idx, site in enumerate(recommendations):
        with cols[idx % 3]:
            with st.container():
                st.markdown(f"""
                <div class='card'>
                    <h3>{site.get('name', 'Unknown Site')}</h3>
                    <p><strong>📍 {site.get('location', 'Unknown Location')}</strong></p>
                    <p>{site.get('description', 'No description available.')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Explore", key=f"explore_{idx}"):
                    st.session_state.current_search = site['name']
                    st.rerun()