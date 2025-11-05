import streamlit as st
from utils.api_client import api_client
from utils.session_state import add_to_chat_history
import time

def handle_image_upload():
    """Handle image upload and analysis with enhanced UX"""
    st.header("🖼️ Explore by Image")
    
    st.info("""
    📸 **How to get the best results:**
    - Upload clear, well-lit images of heritage sites
    - Include the entire monument in the frame
    - Avoid blurry or dark images
    - Supported formats: JPG, JPEG, PNG
    """)
    
    uploaded_file = st.file_uploader(
        "Choose an image of a heritage site", 
        type=["jpg", "jpeg", "png"],
        help="Maximum file size: 10MB"
    )
    
    if uploaded_file is not None:
        # Display image preview with enhanced styling
        st.markdown("### 📷 Image Preview")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.image(uploaded_file, caption="Your Uploaded Image", use_column_width=True)
            
            # File info
            file_size = len(uploaded_file.getvalue()) / 1024  # KB
            st.caption(f"📁 File: {uploaded_file.name} | 📏 Size: {file_size:.1f} KB")
        
        with col2:
            st.markdown("### 🎯 Ready to Analyze?")
            st.write("Click the button below to discover the history behind this image!")
            
            if st.button("🔍 Analyze Heritage", type="primary", use_container_width=True):
                # Enhanced progress tracking for image analysis
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                steps = [
                    "📤 Uploading image...",
                    "🔄 Processing with AI...", 
                    "🔍 Analyzing architectural features...",
                    "📚 Gathering historical context...",
                    "✨ Finalizing analysis..."
                ]
                
                for i, step in enumerate(steps):
                    progress = (i + 1) * 20
                    progress_bar.progress(progress)
                    status_text.text(step)
                    time.sleep(0.5)  # Simulate processing time
                
                # Perform actual analysis
                result = api_client.analyze_image(
                    uploaded_file.getvalue(), 
                    st.session_state.username
                )
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                if result:
                    st.session_state.analysis_result = result
                    add_to_chat_history("AI", f"Image Analysis: {result}")
                    st.balloons()
                    st.success("🎉 Image analysis completed successfully!")
                else:
                    st.error("❌ Failed to analyze image. Please try again with a different image.")
        
        # Display analysis results with enhanced styling
        if st.session_state.analysis_result:
            st.markdown("---")
            st.markdown("### 📜 Heritage Analysis Results")
            
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
                max-height: 500px;
                overflow-y: auto;
                box-shadow: 0 8px 25px rgba(240, 198, 116, 0.2);
            '>
                {st.session_state.analysis_result}
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🔄 Analyze New Image", use_container_width=True):
                    st.session_state.uploaded_image = None
                    st.session_state.analysis_result = None
                    st.rerun()
            with col2:
                if st.button("💾 Save Results", use_container_width=True):
                    st.info("💡 Save feature coming soon!")
            with col3:
                if st.button("📤 Share", use_container_width=True):
                    st.info("💡 Share feature coming soon!")