import streamlit as st
import os

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
    st.subheader("Threat Analysis Report")

    with st.container():
        if isinstance(response, dict):
            if "error" in response:
                st.error(f"Error: {response['error']}")
                if 'setup_instructions' in response:
                    st.warning("Setup Instructions:")
                    st.info(response['setup_instructions'])
            elif "status" in response and response["status"] == "success":
                st.success("Analysis Complete")

                if response["format"] == "json":
                    data = response["data"]
                    # Display as formatted report sections
                    if "attack_vector" in data:
                        st.markdown("### Attack Vector Analysis")
                        st.markdown(data["attack_vector"])

                    if "timeline" in data:
                        st.markdown("### Attack Timeline")
                        st.markdown(data["timeline"])

                    if "impact" in data:
                        st.markdown("### Potential Impact")
                        st.markdown(data["impact"])

                    if "mitigation" in data:
                        st.markdown("### Recommended Mitigations")
                        st.markdown(data["mitigation"])

                elif response["format"] == "text":
                    st.markdown("### Analysis Details")
                    st.markdown(response["data"]["content"])

                    if "sections" in response["data"]:
                        for section in response["data"]["sections"]:
                            st.markdown(f"- {section}")

        if isinstance(tags, dict) and not "error" in tags:
            st.markdown("### Threat Classification")
            if "TTP" in tags:
                st.markdown(f"**TTPs:** {tags['TTP']}")
            if "attack_vector" in tags:
                st.markdown(f"**Attack Vector:** {tags['attack_vector']}")
            if "threat_actor" in tags:
                st.markdown(f"**Threat Actor:** {tags['threat_actor']}")
            if "target_sector" in tags:
                st.markdown(f"**Target Sector:** {tags['target_sector']}")
            if "Severity Level" in tags:
                st.markdown(f"**Severity Level:** {tags['Severity Level']}")