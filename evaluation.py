import re
def evaluate_requirements_quality(text):
    """
    evaluates the quality of requirements based on specificity, measurability, and testability.
    """
    text_lower = text.lower()
    sentences = re.split(r'[.!?]+', text_lower)
    sentences = [s.strip() for s in sentences if s.strip()]

    # empty text handling
    if not sentences:
        return {
            "specificity_score": 1,
            "measurability_score": 1,
            "testability_score": 1
        }

    specificity_terms = {
        'high_value': [
            'exactly', 'precisely', 'specifically', 'equal to',
            'must be', 'within', 'between', 'no more than', 'no less than'
        ],
        'medium_value': [
            'at least', 'at most', 'maximum', 'minimum', 'less than',
            'greater than', 'up to', 'from', 'to', 'range'
        ],
        'low_value': [
            'during', 'if', 'unless', 'when', 'while', 'only',
            'about', 'approximately', 'around', 'estimated'
        ]
    }

    # count sentences with specificity terms, with weighted values
    specificity_sentence_count = 0
    for sentence in sentences:
        high_matches = sum(
            1 for term in specificity_terms['high_value'] if re.search(r'\b{}\b'.format(re.escape(term)), sentence))
        medium_matches = sum(
            1 for term in specificity_terms['medium_value'] if re.search(r'\b{}\b'.format(re.escape(term)), sentence))
        low_matches = sum(
            1 for term in specificity_terms['low_value'] if re.search(r'\b{}\b'.format(re.escape(term)), sentence))

        # weight: high=1.0, medium=0.6, low=0.3
        specificity_sentence_count += (
                high_matches * 1.0 +
                medium_matches * 0.6 +
                low_matches * 0.3
        )

    measurability_patterns = [
        r'\d+\s*(?:second|minute|hour|day|percent|%)',
        r'\d+\s*(?:kb|mb|gb|tb|byte|bytes)',
        r'\d+\s*(?:kg|g|m|cm|km|meter|meters)',
        r'\d+\s*(?:hz|mhz|ghz)',
        r'(?:response time|latency)\s*(?:of|under|less than)?\s*\d+',
        r'(?:accuracy|precision|error rate)\s*(?:of|at)?\s*\d+(?:\.\d+)?\s*%',
        r'(?:availability|uptime)\s*(?:of|at)?\s*\d+(?:\.\d+)?\s*%',
        r'(?:capacity|throughput|bandwidth)\s*(?:of|at)?\s*\d+'
    ]

    measurable_sentence_count = 0
    for sentence in sentences:
        for pattern in measurability_patterns:
            if re.search(pattern, sentence):
                measurable_sentence_count += 1
                break


    testability_terms = {
        'strong_verbs': [
            'validate', 'verify', 'test', 'measure', 'confirm',
            'demonstrate', 'check', 'assert', 'prove', 'audit'
        ],
        'action_verbs': [
            'display', 'calculate', 'store', 'retrieve', 'send',
            'receive', 'generate', 'create', 'update', 'process',
            'execute', 'run', 'perform', 'log', 'monitor'
        ]
    }

    testable_sentence_count = 0
    for sentence in sentences:
        strong_matches = sum(
            1 for term in testability_terms['strong_verbs'] if re.search(r'\b{}\b'.format(re.escape(term)), sentence))
        action_matches = sum(
            1 for term in testability_terms['action_verbs'] if re.search(r'\b{}\b'.format(re.escape(term)), sentence))

        # weight strong verbs higher
        if strong_matches > 0:
            testable_sentence_count += 1.0
        elif action_matches > 0:
            testable_sentence_count += 0.7

    # calculate percentages of sentences with each quality
    total_sentences = len(sentences)
    specificity_percentage = (specificity_sentence_count / total_sentences) * 100
    measurability_percentage = (measurable_sentence_count / total_sentences) * 100
    testability_percentage = (testable_sentence_count / total_sentences) * 100

    # map percentages to 1-5 scale with a more discriminating approach
    def percentage_to_score(percentage):
        if percentage < 15:
            return 1  # Very poor
        elif percentage < 30:
            return 2  # Poor
        elif percentage < 50:
            return 3  # Average
        elif percentage < 70:
            return 4  # Good
        else:
            return 5  # Excellent

    # apply score mapping
    scores = {
        "specificity_score": percentage_to_score(specificity_percentage),
        "measurability_score": percentage_to_score(measurability_percentage),
        "testability_score": percentage_to_score(testability_percentage)
    }

    return scores

