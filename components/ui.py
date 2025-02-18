import streamlit as st

def render_header():
    st.markdown("""
    <style>
    .header {
        padding: 1rem;
        background-color: #262730;
        border-radius: 5px;
        margin-bottom: 2rem;
    }
    </style>
    <div class="header">
        <h1>GPT Cyber Threat Analyzer</h1>
        <p>Analyze and tag cyber threat data using advanced AI</p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    st.sidebar.title("Analysis Options")
    analysis_type = st.sidebar.selectbox(
        "Select Analysis Type",
        ["Custom Query", "Timeline Analysis", "Attack Vector Analysis", "TTP Analysis"]
    )
    
    export_format = st.sidebar.selectbox(
        "Export Format",
        ["CSV", "JSON"]
    )
    
    return analysis_type, export_format.lower()

def render_query_section(templates):
    st.subheader("Query Input")
    
    use_template = st.checkbox("Use Template")
    
    if use_template:
        template_key = st.selectbox(
            "Select Template",
            list(templates.keys())
        )
        template = templates[template_key]["template"]
        params = {}
        if "{threat_type}" in template:
            params["threat_type"] = st.text_input("Threat Type")
        if "{time_period}" in template:
            params["time_period"] = st.text_input("Time Period")
        if "{threat_actor}" in template:
            params["threat_actor"] = st.text_input("Threat Actor")
        if "{threat_name}" in template:
            params["threat_name"] = st.text_input("Threat Name")
            
        query = template.format(**params) if params else template
    else:
        query = st.text_area("Enter your query")
    
    return query

def render_response(response, tags):
    st.subheader("Analysis Results")
    
    with st.expander("Response Details", expanded=True):
        if isinstance(response, dict):
            for key, value in response.items():
                st.markdown(f"**{key}:**")
                st.write(value)
        else:
            st.write(response)
    
    with st.expander("Tags", expanded=True):
        if isinstance(tags, dict):
            for key, value in tags.items():
                st.markdown(f"**{key}:** {value}")
        else:
            st.write(tags)
