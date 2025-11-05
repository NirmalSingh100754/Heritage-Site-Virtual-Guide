import streamlit as st
import time
from utils.api_client import api_client
from utils.session_state import add_to_chat_history

def handle_search():
    """Handle heritage site search with enhanced UX"""
    st.header("🔍 Search Heritage")
    
    # Connection status
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input(
            "Ask about any heritage site:",
            placeholder="e.g., Taj Mahal, Great Wall of China, Pyramids of Giza...",
            key="search_input"
        )
    
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        if api_client.test_connection():
            st.success("✅ Connected")
        else:
            st.error("🚫 Disconnected")
    
    if st.button("🚀 Search Heritage", use_container_width=True, type="primary") and search_query:
        # Create a progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(100):
            # Update progress bar
            progress_bar.progress(i + 1)
            
            # Update status text
            if i < 25:
                status_text.text("🔄 Connecting to AI service...")
            elif i < 50:
                status_text.text("🔍 Searching historical database...")
            elif i < 75:
                status_text.text("📚 Gathering heritage information...")
            else:
                status_text.text("✨ Finalizing results...")
            
            time.sleep(0.02)  # Simulate progress
        
        # Perform actual search
        result = api_client.analyze_text(search_query, st.session_state.username)
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        if result:
            st.balloons()  # Celebration effect
            st.markdown("### 📖 Heritage Information")
            
            # Enhanced result display with better formatting
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #1c1c1c, #2d2d2d);
                border: 2px solid #f0c674;
                border-radius: 15px;
                padding: 25px;
                color: #e0d5c0;
                white-space: pre-line;
                line-height: 1.6;
                font-size: 16px;
                box-shadow: 0 8px 25px rgba(240, 198, 116, 0.2);
            '>
                {result}
            </div>
            """, unsafe_allow_html=True)
            
            add_to_chat_history("User", f"Search: {search_query}")
            add_to_chat_history("AI", f"Search Results: {result}")
            
            # Success message with emoji
            st.success("🎉 Heritage information retrieved successfully!")
            
        else:
            st.error("""
            ❌ Failed to get search results. This could be due to:
            - Network connectivity issues
            - AI service temporarily unavailable
            - Invalid search query
            
            Please try again in a moment.
            """)
    
    # Enhanced chat history display
    if st.session_state.chat_history:
        st.markdown("---")
        st.subheader("📜 Recent Explorations")
        
        for chat in reversed(st.session_state.chat_history[-5:]):
            role_icon = "🏛️" if chat["role"] == "AI" else "👤"
            bg_color = "linear-gradient(135deg, #2d5016, #3a6620)" if chat["role"] == "AI" else "linear-gradient(135deg, #1c1c1c, #2d2d2d)"
            border_color = "#4CAF50" if chat["role"] == "AI" else "#f0c674"
            
            st.markdown(f"""
            <div style='
                background: {bg_color};
                border: 2px solid {border_color};
                border-radius: 12px;
                padding: 18px;
                margin: 12px 0;
                color: #e0d5c0;
                white-space: pre-line;
                line-height: 1.5;
            '>
                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 20px; margin-right: 10px;">{role_icon}</span>
                    <strong style="color: #f0c674;">{chat['role']}</strong>
                </div>
                {chat['message']}
            </div>
            """, unsafe_allow_html=True)