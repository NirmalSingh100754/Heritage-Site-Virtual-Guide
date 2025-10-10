import streamlit as st
from utils.api_client import api_client
from utils.session_state import add_to_chat_history

def handle_image_upload():
    """Handle image upload and analysis"""
    st.header("🖼️ Explore by Image")
    
    uploaded_file = st.file_uploader(
        "Upload an image of a heritage site", 
        type=["jpg", "jpeg", "png"],
        help="Upload a clear image of any historical monument or heritage site"
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if uploaded_file is not None:
            # Display uploaded image
            st.image(uploaded_file, caption="📸 Uploaded Image", use_column_width=True)
            st.session_state.uploaded_image = uploaded_file
            
            if st.button("🔍 Analyze Image", type="primary", use_container_width=True):
                with st.spinner("🔄 AI is analyzing your image..."):
                    result = api_client.analyze_image(
                        uploaded_file.getvalue(), 
                        st.session_state.username
                    )
                    
                    if result:
                        st.session_state.analysis_result = result
                        add_to_chat_history("AI", f"Image Analysis: {result}")
                    else:
                        st.error("❌ Failed to analyze image. Please try again.")
    
    with col2:
        if st.session_state.analysis_result:
            st.markdown("### 📜 Analysis Results")
            st.markdown(f"""
            <div style='
                background: #1c1c1c; 
                border: 1px solid #f0c674; 
                border-radius: 10px; 
                padding: 20px; 
                max-height: 400px; 
                overflow-y: auto;
                color: #e0d5c0;
            '>
                {st.session_state.analysis_result.replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🔄 Analyze New Image", use_container_width=True):
                st.session_state.uploaded_image = None
                st.session_state.analysis_result = None
                st.rerun()