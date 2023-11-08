action_items = {
    "1. Steven Yuen:": [
        "Research and identify features that cater to Agile work environments.",
        "Investigate the use of a centralized dashboard for managing meetings.",
        "Determine how the solution can differentiate itself from Copilot.",
        "Gather requirements and file from the stakeholders.",
        "Chase up the requirements from the stakeholders."
    ],
    "2. Jason Hong:": [
        "Continue working on current tasks and projects."
    ],
    "3. David Gailey:": [
        "Support the shift towards an Agile focus for the solution.",
        "Assist in identifying unique features and value proposition compared to Copilot."
    ],
    "4. Chris Qu:": [
        "Participate in discussions and provide input on the direction of the solution.",
        "Assist in determining the necessary features for the Telstra-focused solution."
    ],
    "5. All team members:": [
        "Collaborate on integrating Copilot into the solution in the long term."
    ],
    "6. Steven Yuen and Jason Hong:": [
        "Discuss the issue of Copilot access and find a solution."
    ]
}

action_items_cleaned = {key.split(' ', 1)[1]: value for key, value in action_items.items()}

# Print the cleaned dictionary
# print(action_items_cleaned)