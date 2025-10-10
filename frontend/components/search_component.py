import streamlit as st
from utils.api_client import api_client
from utils.session_state import add_to_chat_history

def handle_search():
    """Handle heritage site search"""
    st.header("🔍 Search Heritage")
    
    # Test connection first
    if not api_client.test_connection():
        st.error("🚫 Cannot connect to backend API. Please make sure the backend server is running.")
        return
    
    search_query = st.text_input(
        "Ask about any heritage site:",
        placeholder="e.g., Taj Mahal, Great Wall of China, Pyramids of Giza...",
        key="search_input"
    )
    
    if st.button("🚀 Search", use_container_width=True) and search_query:
        with st.spinner("🔍 Searching for heritage information..."):
            result = api_client.analyze_text(search_query, st.session_state.username)
            
            if result:
                st.markdown("### 📖 Search Results")
                st.markdown(f"""
                <div style='
                    background: #1c1c1c; 
                    border: 1px solid #f0c674; 
                    border-radius: 10px; 
                    padding: 20px; 
                    color: #e0d5c0;
                    white-space: pre-line;
                '>
                    {result}
                </div>
                """, unsafe_allow_html=True)
                
                add_to_chat_history("User", f"Search: {search_query}")
                add_to_chat_history("AI", f"Search Results: {result}")
                st.success("✅ Search completed successfully!")
            else:
                st.error("❌ Failed to get search results. The backend might be having issues.")
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("---")
        st.subheader("💬 Recent Conversations")
        
        for chat in reversed(st.session_state.chat_history[-5:]):  # Show last 5
            role_icon = "🤖" if chat["role"] == "AI" else "👤"
            bg_color = "#2d5016" if chat["role"] == "AI" else "#1c1c1c"
            
            st.markdown(f"""
            <div style='
                background: {bg_color}; 
                border: 1px solid #f0c674; 
                border-radius: 10px; 
                padding: 15px; 
                margin: 10px 0;
                color: #e0d5c0;
                white-space: pre-line;
            '>
                <strong>{role_icon} {chat['role']}:</strong><br>
                {chat['message']}
            </div>
            """, unsafe_allow_html=True)