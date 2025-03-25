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

                # Raw API Response
                st.subheader("📡 Raw API Response")
                with st.expander("View Raw Response", expanded=True):
                    st.json(response)

                # Raw Combined Data (API + Scraped)
                if 'api_response' in response:
                    st.subheader("🔄 Combined Raw Data (API + Scraped)")
                    with st.expander("View Combined Data"):
                        st.json({"api_response": response, "scraped_data": response.get('scraped_data', {})})

                if response["format"] == "json":
                    data = response["data"]
                    st.markdown("## 📊 Threat Analysis Report")
                    st.markdown("---")

                    if "attack_vector" in data:
                        st.markdown("### 🎯 Attack Vector Analysis")
                        cleaned_text = data["attack_vector"].replace('\\boxed{', '').replace('}', '')
                        vectors = cleaned_text.split(". ")
                        for vector in vectors:
                            if vector.strip():
                                st.markdown(f"• {vector.strip()}")
                        st.markdown("")

                    if "timeline" in data:
                        st.markdown("### ⏱️ Attack Timeline")
                        timeline_text = data["timeline"].replace('\\boxed{', '').replace('}', '')
                        steps = [step for step in timeline_text.split(". ") if step.strip()]

                        for i, step in enumerate(steps, 1):
                            step = step.lstrip("123456789. ")
                            st.markdown(f"**{i}.** {step}")
                        st.markdown("")

                    if "impact" in data:
                        st.markdown("### 💥 Potential Impact")
                        cleaned_text = data["impact"].replace('\\boxed{', '').replace('}', '')
                        impacts = [imp.strip() for imp in cleaned_text.split(".") if imp.strip()]

                        for impact in impacts:
                            st.markdown(f"• {impact}")
                        st.markdown("")

                    if "mitigation" in data:
                        st.markdown("### 🛡️ Recommended Mitigations")
                        cleaned_text = data["mitigation"].replace('\\boxed{', '').replace('}', '')
                        mitigations = [mit.strip() for mit in cleaned_text.split(". ") if mit.strip()]

                        for i, mitigation in enumerate(mitigations, 1):
                            if mitigation.lower().startswith("recommended"):
                                mitigation = mitigation.split(":", 1)[1].strip()
                            st.markdown(f"**{i}.** {mitigation}")

                elif response["format"] == "text":
                    try:
                        # Try to parse the content as JSON after cleaning
                        content = response["data"]["content"].replace('\\boxed{', '').replace('}', '')
                        data = eval(content)

                        st.markdown("## 📊 Detailed Analysis Report")

                        if "attack_vector" in data:
                            st.markdown("### 🎯 Attack Vector Analysis")
                            st.text(data["attack_vector"])
                            st.markdown("---")

                        if "timeline" in data:
                            st.markdown("### ⏱️ Attack Timeline")
                            timeline_items = data['timeline'].split(".")
                            for item in timeline_items:
                                if item.strip():
                                    st.markdown(f"- {item.strip()}")
                            st.markdown("---")

                        if "impact" in data:
                            st.markdown("### 💥 Impact Analysis")
                            impact_items = data['impact'].replace('-', '•').split("•")
                            for item in impact_items:
                                if item.strip():
                                    st.markdown(f"- {item.strip()}")
                            st.markdown("---")

                        if "mitigation" in data:
                            st.markdown("### 🛡️ Mitigation Strategies")
                            mitigation_items = data['mitigation'].replace('-', '•').split("•")
                            for item in mitigation_items:
                                if item.strip():
                                    st.markdown(f"- {item.strip()}")
                            st.markdown("---")

                        # Display raw response in expander
                        with st.expander("View Raw JSON Response"):
                            st.json(data)

                    except:
                        # Fallback to plain text display if parsing fails
                        st.markdown("### Analysis Details")
                        clean_content = response["data"]["content"].replace('\\boxed{', '').replace('}', '')
                        st.markdown(clean_content)

            # Generate and display formatted report
            if isinstance(response, dict) and 'api_response' in response:
                # Display the current analysis report
                report = st.session_state.threat_analyzer.generate_threat_report(response)
                st.markdown(report)

                # Display historical analysis in an expander
                with st.expander("📚 View Historical Analysis"):
                    history_df = st.session_state.threat_analyzer.get_historical_analysis()
                    if not history_df.empty:
                        st.dataframe(
                            history_df[['timestamp', 'query']].sort_values('timestamp', ascending=False),
                            use_container_width=True
                        )
                    else:
                        st.info("No historical analysis available yet.")

            if isinstance(tags, dict) and not "error" in tags:
                st.markdown("### Threat Classification")
                for key, value in tags.items():
                    if key != "error":
                        st.markdown(f"**{key}**: {value}")
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