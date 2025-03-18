import streamlit as st
import os # Added for environment variable handling

def render_header():
    st.title("Cyber Threat Analysis Platform")
    st.markdown("""
    This platform helps security analysts understand, categorize, and respond to cyber threats.
    Use the query input section to ask about specific threats or browse the sample queries.
    """)

def render_sidebar():
    st.sidebar.title("Settings")

    analysis_type = st.sidebar.selectbox(
        "Analysis Type",
        ["Timeline", "Attack Vectors", "TTPs", "Recent Threats"]
    )

    export_format = st.sidebar.selectbox(
        "Export Format",
        ["csv", "json"]
    )

    # No model selection shown to end users
    # API configuration happens server-side

    return analysis_type, export_format

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
            # Check if it's an error response
            if "error" in response:
                st.error(f"Error: {response['error']}")
                if 'raw_response' in response and response['raw_response']:
                    st.text_area("Raw Response", response['raw_response'], height=300)
                
                # Display setup instructions if available
                if 'setup_instructions' in response:
                    st.warning("Setup Instructions:")
                    st.info(response['setup_instructions'])
            elif "status" in response and response["status"] == "success":
                st.success("API Response received successfully")
                
                if response["format"] == "json":
                    st.json(response["data"])
                elif response["format"] == "text":
                    st.markdown("### Analysis Content")
                    st.write(response["data"]["content"])
                    
                    if "sections" in response["data"]:
                        st.markdown("### Sections")
                        for section in response["data"]["sections"]:
                            st.text(section)
                    
                    # Add a button to open Secrets tool
                    if 'error' in response and ("API key" in response['error'].lower() or "OPENROUTER_API_KEY" in response['error']):
                        st.markdown("""
                        ### How to set your API key:
                        1. Click on the **Tools** button in the left sidebar
                        2. Select **Secrets**
                        3. Add a new secret with key `OPENROUTER_API_KEY` and your API key as the value
                        4. Restart your application
                        """)
            else:
                # Normal dictionary response
                for key, value in response.items():
                    st.markdown(f"**{key}:**")
                    st.write(value)
        else:
            # Handle string or other type responses
            st.text_area("Response", str(response), height=300)

    with st.expander("Tags", expanded=True):
        if isinstance(tags, dict):
            # Check if it's an error response in tags
            if "error" in tags:
                st.error(f"Error: {tags['error']}")
                if 'raw_response' in tags and tags['raw_response']:
                    st.text_area("Raw Tags Response", tags['raw_response'], height=300)
                
                # Display setup instructions if available
                if 'setup_instructions' in tags:
                    st.warning("Setup Instructions:")
                    st.info(tags['setup_instructions'])
            else:
                # Normal dictionary tags
                for key, value in tags.items():
                    st.markdown(f"**{key}:** {value}")
        else:
            # Handle string or other type tags
            st.text_area("Tags", str(tags), height=300)