# Zero-shot
def zero_shot_prompt(story):
    return f"""Convert the following user story into specific, measurable, achievable, relevant, and time-bound software requirements:

USER STORY:
{story['text']}

OUTPUT FORMAT:
1. List functional requirements (FR) first
2. List non-functional requirements (NFR) second
3. Each requirement should be specific, measurable, and testable

I want you to only share the functional (FR) and nonfunctional (NFR) requirements as follows and do not share your reasoning with me: 

FR-1: 
FR-2:
NFR-1: 
NFR-2:
and so on..
"""


# Few-shot
def few_shot_prompt(story):
    return f"""
Convert the following user story into specific, measurable, achievable, relevant, and time-bound, functional and non-functional software requirements.

EXAMPLE 1:
User Story: As a user, I want to log in with my email and password.

Requirements:
FR-1: The system shall provide a login form with fields for email and password.
FR-2: The system shall validate that the email field contains a valid email format.
FR-3: The system shall verify credentials against the user database within 2 seconds.
FR-4: The system shall grant access to authorized functionality if credentials are correct.
FR-5: The system shall display an error message if credentials are incorrect.
NFR-1: The login process shall complete within 3 seconds under normal load conditions.
NFR-2: The system shall encrypt password data during transmission.

EXAMPLE 2:
User Story: As an admin, I want to view reports of user activity.

Requirements:
FR-1: The system shall provide a dashboard displaying user activity metrics.
FR-2: The system shall allow filtering of reports by date range and activity type.
FR-3: The system shall enable exporting reports in CSV and PDF formats.
NFR-1: The system shall generate reports within 5 seconds for data spanning up to 30 days.
NFR-2: The dashboard shall refresh automatically every 5 minutes.

Now convert this user story into similar well-structured requirements:
{story['text']}
"""


# Chain-of-Thought
def chain_of_thought_prompt(story):
    return f"""
Convert the following user story into specific, measurable, achievable, relevant, and time-bound software requirements by following these steps:

USER STORY:
{story['text']}

Follow these steps to derive the requirements:

1. Identify the actor (Who is performing the action?)
   - Who is the primary user in this story?
   - What is their role in the system?

2. Identify the action (What do they want to do?)
   - What specific functionality is being requested?
   - What system components would be involved?

3. Identify the goal (Why do they want to do it?)
   - What is the underlying user need?
   - How does this relate to business objectives?

4. Extract assumptions and constraints
   - What implicit needs are not directly stated?
   - What technical or business constraints might apply?

5. Derive detailed functional requirements (FR) from the analysis performed in the previous steps.
   - What specific behaviors must the system exhibit?
   - What are the inputs, processes, and outputs?

6. Derive non-functional requirements (NFR) from the analysis performed in the previous steps.
   - What quality attributes are important (performance, security, usability)?
   - What measurable criteria should apply?

Based on the analysis performed in the steps above, provide a numbered list of clear, specific, and testable functional (FR) and non-functional (NFR) requirements.

Output ONLY the functional (FR) and non-functional (NFR) requirements in the following format and do not share your reasoning with me:

FR-1:
FR-2:
...
NFR-1:
NFR-2:
...
"""


# System Prompt
def system_prompt(story):
    return f"""
You are RequirementsGPT, a specialized AI assistant designed to convert user stories into software requirements. You excel at:
- Extracting implicit needs from vague descriptions
- Ensuring requirements are testable and measurable
- Addressing both functional and quality aspects of the system
- Anticipating edge cases and exception handling needs

USER STORY:
{story['text']}

INSTRUCTIONS:
1. Generate functional requirements (FR)
2. Generate non-functional requirements (NFR)
3. Ensure each requirement is specific, measurable, achievable, relevant, and time-bound (SMART)

I want you to only share the functional (FR) and nonfunctional (NFR) requirements as follows: 

FR-1: 
FR-2:
NFR-1: 
NFR-2:
and so on..
"""

# Self-consistency Prompt - Enhanced with clearer evaluation criteria
def self_consistency_prompt(story):
    return f"""
Generate three different sets of specific, measurable, achievable, relevant, and time-bound software requirements for the following user story, then evaluate them and select the most effective set.

USER STORY:
{story['text']}

APPROACH 1: Focus on technical implementation details
[Generate requirements with emphasis on system behaviors and technical specifications]

APPROACH 2: Focus on user experience and outcomes
[Generate requirements with emphasis on user interactions and success criteria]

APPROACH 3: Focus on business rules and data handling
[Generate requirements with emphasis on business logic and data flow]

EVALUATION CRITERIA:
- Completeness: Covers all aspects of the user story
- Clarity: Unambiguous and specific
- Testability: Can be verified through testing
- Feasibility: Realistic to implement
- Alignment: Supports the core user need

FINAL RECOMMENDATION:
Based on the evaluation, provide the most effective set of requirements with justification for your choice.

I want you to only share the functional (FR) and nonfunctional (NFR) requirements as follows and do not share your reasoning with me: : 

FR-1: 
FR-2:
NFR-1: 
NFR-2:
and so on..
"""



# Role Prompt
def role_prompt(story):
    return f"""
You are a Senior Requirements Engineer with 15 years of experience in software development. Your expertise is in translating business needs into technical specifications that bridge business goals and development work.

APPROACH THIS TASK AS A PROFESSIONAL WOULD:
- Consider system architecture implications
- Think about integration points with other systems
- Address security and compliance needs
- Consider maintenance and supportability

USER STORY:
{story['text']}

Produce a set of professional-grade specific, measurable, achievable, relevant, and time-bound requirements that would be ready for development team implementation. Include:
1. Numbered functional requirements (with FR prefix)
2. Numbered non-functional requirements (with NFR prefix)
3. Potential risks or dependencies

I want you to only share the functional (FR) and nonfunctional (NFR) requirements as follows and do not share your reasoning with me: 

FR-1: 
FR-2:
NFR-1: 
NFR-2:
and so on..
"""

# Contexual Prompt
def contextual_prompt(story):

    return f"""
BUSINESS CONTEXT:
{story['context']}

USER STORY:
{story['text']}

TASK:
Using the business context provided, convert the user story into specific, measurable, achievable, relevant, and time-bound software requirements that address:
1. Core functionality needed
2. Integration with existing systems
3. Performance considerations under peak load
4. Monitoring and error handling requirements
5. User experience factors

I want you to only share the specific, measurable, achievable, relevant, and time-bound functiona functional (FR) and nonfunctional (NFR) requirements as follows and do not share your reasoning with me: 

FR-1: 
FR-2:
NFR-1: 
NFR-2:
and so on..
"""


# Tree of Thoughts Prompt
def tree_of_thoughts_prompt(story):
    return f"""
Let's approach this user story by exploring multiple thought branches to ensure comprehensive requirements.

USER STORY:
{story['text']}

TREE OF THOUGHTS:

Branch 1: Core Functionality
- What is the primary action or functionality being requested?
- What triggers this functionality?
- What systems or components are involved?
- What are the expected outcomes or results?
- Branch 1 Requirements: [requirements focused on core functionality]

Branch 2: User Experience Considerations
- How will users interact with this feature?
- What information should be presented to users?
- What design/interface elements are needed?
- How does this impact the overall user experience?
- Branch 2 Requirements: [requirements focused on user experience]

Branch 3: Data Management
- What data needs to be captured or processed?
- Where and how is data stored?
- How is data security and privacy maintained?
- What data transformations or calculations are required?
- Branch 3 Requirements: [requirements focused on data handling]

Branch 4: Error Handling and Edge Cases
- What can go wrong with this functionality?
- How should errors be managed and communicated?
- What alternative paths or fallbacks exist?
- How are exceptions logged and monitored?
- Branch 4 Requirements: [requirements focused on error handling]

CONSOLIDATED REQUIREMENTS:
[Combine the most important requirements from each branch into a cohesive set]

I want you to only share the specific, measurable, achievable, relevant, and time-bound functional (FR) and nonfunctional (NFR) requirements as follows and do not share your reasoning with me: : 

FR-1: 
FR-2:
NFR-1: 
NFR-2:
and so on..
"""


# React Prompt - Enhanced with clearer reasoning-action loop
def react_prompt(story):
    return f"""
Let's solve this requirement engineering task using a Reasoning-Action loop.

USER STORY:
{story['text']}

REASONING STEP 1:
Let's identify the core functionality requested in this user story. What is the primary action or outcome the user expects?

ACTION STEP 1:
FR-1: [Primary functional requirement based on the core need]
FR-2: [Secondary functional requirement that supports the core need]

REASONING STEP 2:
Now let's consider the triggers, conditions, and context for this functionality. What needs to happen before, during, and after the main function?

ACTION STEP 2:
FR-3: [Requirement related to preconditions or triggers]
FR-4: [Requirement related to process steps or data handling]

REASONING STEP 3:
We need to consider reliability, error conditions, and alternative paths. What happens when things don't work as expected?

ACTION STEP 3:
FR-5: [Requirement addressing error handling or alternative flows]
FR-6: [Requirement addressing backup functionality or notifications]
NFR-1: [Non-functional requirement related to performance or timing]

REASONING STEP 4:
Let's consider user experience, accessibility, and other quality attributes important for this feature.

ACTION STEP 4:
NFR-2: [Non-functional requirement related to user interface or experience]
NFR-3: [Non-functional requirement related to quality attributes like accessibility or security]

FINAL REQUIREMENTS:
[Comprehensive list of all requirements developed through the reasoning-action process]

I want you to only share the specific, measurable, achievable, relevant, and time-bound functional (FR) and nonfunctional (NFR) requirements as follows and do not share your reasoning with me: : 

FR-1: 
FR-2:
NFR-1: 
NFR-2:
and so on..
"""

