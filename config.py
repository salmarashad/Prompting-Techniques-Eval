from prompt_techniques import *

# define model configurations for testing
model_configs = {
    "precise": {
        "model_name": "gemini-2.0-flash-001",
        "temperature": 0.2,
        "top_p": 0.95,
        "top_k": 40
    },
    "default": {
        "model_name": "gemini-2.0-flash-001",
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40
    },
    "creative": {
        "model_name": "gemini-2.0-flash-001",
        "temperature": 1.0,
        "top_p": 0.95,
        "top_k": 40
    }
}

prompt_strategies = {
    "Zero-shot": zero_shot_prompt,
    "Few-shot": few_shot_prompt,
    "Chain-of-Thought": chain_of_thought_prompt,
    "Self-Consistency": self_consistency_prompt,
    "System Prompt": system_prompt,
    "Role Prompt": role_prompt,
    "Contextual": contextual_prompt,
    "Tree of Thoughts": tree_of_thoughts_prompt,
    "ReAct": react_prompt
}