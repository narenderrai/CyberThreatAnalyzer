PROMPT_TEMPLATES = {
    "timeline_analysis": {
        "template": "What is the typical timeline and progression of {threat_type} attacks?",
        "description": "Analyzes the timeline of specific cyber threats"
    },
    "recent_threats": {
        "template": "What are the most recent cyber threats identified in the past {time_period}?",
        "description": "Identifies recent cyber threats"
    },
    "attack_vector": {
        "template": "What are the primary attack vectors used by {threat_actor}?",
        "description": "Analyzes attack vectors of specific threat actors"
    },
    "ttp_analysis": {
        "template": "What are the main TTPs (Tactics, Techniques, and Procedures) associated with {threat_name}?",
        "description": "Analyzes specific threat TTPs"
    }
}

SAMPLE_QUERIES = [
    "What is the most common timeline in a ransomware attack?",
    "What is the most recent cyber threat identified?",
    "What is the attack vector for Volt Typhoon?",
    "What are the common TTPs used in supply chain attacks?",
]
