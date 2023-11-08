import re

def ticket_splitter(input_string):

    # input_string = "Based on the transcript, here are a few Jira tickets that could be created:\n\n1. Ticket Title: Agile Work Environment Integration\n   - Description: Investigate and implement features to align the solution with Telstra's agile work environment, such as support for different types of agile meetings and ceremonies.\n   - Assignee: Steven Yuen\n   - Priority: High\n\n2. Ticket Title: Contextual Output Generation\n   - Description: Develop functionality to use the transcripts of past meetings as context to generate more accurate and valuable output for future meetings.\n   - Assignee: Steven Yuen\n   - Priority: Medium\n\n3. Ticket Title: Centralized Dashboard\n   - Description: Create a centralized dashboard to manage and track all meetings and their associated artifacts, providing a seamless experience for users.\n   - Assignee: Steven Yuen\n   - Priority: Medium\n\n4. Ticket Title: Copilot Integration and Customization\n   - Description: Explore the possibility of integrating Telstra's solution with Copilot, tailoring it to meet specific business needs and leveraging the existing platform.\n   - Assignee: Jason Hong\n   - Priority: Medium\n\n5. Ticket Title: Meeting Minutes Tailoring\n   - Description: Modify the meeting minutes feature to align with different meeting types, such as retros, stand-ups, and ceremonies, to provide more relevant and useful outputs.\n   - Assignee: Chris Qu\n   - Priority: Low\n\nPlease note that these suggested tickets are based on the information provided in the transcript and may need to be adjusted based on further discussions and requirements."

    # Split the input string into sections based on '\n\n'
    sections = input_string.split('\n\n')

    to_return = []

    # Print each section in the list
    for i in range(1,len(sections)-1):


        # Split the input string into lines
        lines = sections[i].split('\n')

        # Initialize an empty dictionary to store the key-value pairs
        ticket_info = {}

        for line in lines:
            # Split each line into key and value using ':'
            key, value = line.strip().split(': ')
            # Remove leading and trailing spaces from the key and value
            key = key.strip()
            value = value.strip()
            # Add the key-value pair to the dictionary
            ticket_info[key] = value

        to_return.append(ticket_info)

    # Define key mapping for renaming
    key_mapping = {
        "Ticket Title": "title",
        "Description": "description",
        "Assignee": "assignee",
        "Acceptance Criteria": "acceptanceCriteria",
        "Duration Estimate": "estimate",
        "Priority": "priority",
        "User-story": "userStory"
    }

    # Rename keys in each dictionary in the list
    result = [rename_keys(data, key_mapping) for data in to_return]

    return result

# Function to rename keys in a dictionary
def rename_keys(dictionary, key_mapping):
    new_dict = {}
    for key, value in dictionary.items():
        for old_key, new_name in key_mapping.items():
            if key.endswith(old_key):
                new_key = new_name
                new_dict[new_key] = value
    return new_dict


def action_splitter(input_string):

    # print(input_string)

    
    # Split the input string into sections based on '\n\n'
    sections = input_string.split('\n\n')

    # Initialize an empty dictionary to store the action items
    action_items = {}

    for section in sections:
        # Split each section into lines
        lines = section.split('\n')
        
        # The first line contains the team member's name and action item number
        team_member = lines[0]
        
        # Initialize a list to store the action items for the team member
        action_item_list = []
        
        for line in lines[1:]:
            if line.startswith('- '):
                # Extract and add each action item to the list
                action_item_list.append(line.lstrip('- '))
        
        # Add the team member and their action items to the dictionary
        action_items[team_member] = action_item_list

    # Print the resulting dictionary
    # print(action_items)

    return action_items

def retro_splitter(input_string):

    # print(input_string)

    # Split the input string into sections based on '\n\n'
    sections = input_string.split('\n\n')

    # Initialize an empty dictionary to store the action items
    action_items = {}

    for section in sections:
        # Split each section into lines
        lines = section.split('\n')
        
        # The first line contains the action item number and description
        action_item_and_description = lines[0].split('. ', 1)
        
        # Check if there is an action item number and description
        if len(action_item_and_description) == 2:
            action_item, action_description = action_item_and_description
            # Add the action item and description to the dictionary
            action_items[action_item] = action_description

    return action_items

def user_story_splitter(input_string):
    # Split the input string into requirements based on '\n\n'
    requirements = input_string.split('\n\n')

    # Initialize an empty dictionary to store the requirements
    requirements_dict = {}

    # Initialize a counter for requirement numbers
    requirement_number = 1

    for requirement_text in requirements:
        # Add the requirement to the dictionary with a generated number as the key
        requirements_dict[f"{requirement_number}. Requirement"] = requirement_text
        requirement_number += 1

    return requirements_dict

def meeting_minute_string_to_dict(meeting_minutes_text):

    # print("Within this function")

    # Initialize the dictionary
    meeting_minutes_dict = {
        'minutes': {
            'date': '',
            'time': '',
            'location': '',
            'attendees': [],
            'agenda': [],
            'summary': [],
            'actionItems': [],
            'adjourned': '',
        }
    }

    # Use regular expressions to extract information from the input text
    date_match = re.search(r'Meeting Date: (.+)', meeting_minutes_text)
    if date_match:
        meeting_minutes_dict['minutes']['date'] = date_match.group(1)

    time_match = re.search(r'Meeting Start Time: (.+)', meeting_minutes_text)
    if time_match:
        meeting_minutes_dict['minutes']['time'] = time_match.group(1)

    location_match = re.search(r'Meeting Location: (.+)', meeting_minutes_text)
    if location_match:
        meeting_minutes_dict['minutes']['location'] = location_match.group(1)

    # Extract attendees
    attendees_match = re.search(r'Attendees:(.+?)\n\nAgenda:', meeting_minutes_text, re.DOTALL)
    if attendees_match:
        attendees = [name.strip() for name in attendees_match.group(1).strip().split(', ')]
        meeting_minutes_dict['minutes']['attendees'] = attendees

    # Extract agenda
    agenda_match = re.search(r'Agenda:(.+?)\n\nMinutes:', meeting_minutes_text, re.DOTALL)
    if agenda_match:
        agenda = [item.strip() for item in agenda_match.group(1).strip().split('\n')]
        meeting_minutes_dict['minutes']['agenda'] = agenda

    # Extract meeting minutes
    minutes_match = re.search(r'Minutes:(.+?)\n\nNext Steps:', meeting_minutes_text, re.DOTALL)
    if minutes_match:
        minutes = [item.strip() for item in minutes_match.group(1).strip().split('\n')]
        meeting_minutes_dict['minutes']['summary'] = minutes

    # Extract action items
    action_items_match = re.search(r'Action Items:(.+?)\n\nMeeting Conclusion:', meeting_minutes_text, re.DOTALL)
    if action_items_match:
        action_items = [item.strip() for item in action_items_match.group(1).strip().split('\n')]
        meeting_minutes_dict['minutes']['actionItems'] = action_items

    # Extract meeting adjourned time
    adjourned_match = re.search(r'Meeting End Time: (.+)', meeting_minutes_text)
    if adjourned_match:
        meeting_minutes_dict['minutes']['adjourned'] = adjourned_match.group(1)


    # print("Finished this function")

    return meeting_minutes_dict

def agend_to_dict(input_string):
    # Split the input string by lines
    lines = input_string.split('\n')

    # Initialize the dictionary
    agenda_dict = {
        'agenda': {
            'date': '',
            'startTime': '',
            'endTime': '',
            'location': '',
            'items': []
        }
    }

    # Initialize the current section
    current_section = None

    # Iterate through the lines
    for line in lines:
        line = line.strip()
        if line:
            # Check if the line is a section (e.g., "1. Welcome and Introductions")
            if line[0].isdigit() and line[1] == '.':
                current_section = {
                    'item': line[line.find(' ') + 1:],
                    'detail': []
                }
                agenda_dict['agenda']['items'].append(current_section)
            # Check if the line contains a key-value pair (e.g., "Date: [Insert Date]")
            elif ':' in line:
                key, value = map(str.strip, line.split(':', 1))
                agenda_dict['agenda'][key.lower()] = value
            elif current_section is not None:
                # Assume it's an agenda item detail and add it to the 'detail' list
                current_section['detail'].append(line)
    return agenda_dict


def main():
    action_splitter("Action Items:\n\n1. Steven Yuen:\n- Research and identify features that cater to Agile work environments.\n- Investigate the use of a centralized dashboard for managing meetings.\n- Determine how the solution can differentiate itself from Copilot.\n- Gather requirements and file from the stakeholders.\n\n2. Jason Hong:\n- Continue working on current tasks and projects.\n\n3. David Gailey:\n- Support the shift towards an Agile focus for the solution.\n- Assist in identifying unique features and value proposition compared to Copilot.\n\n4. Chris Qu:\n- Participate in discussions and provide input on the direction of the solution.\n- Assist in determining the necessary features for the Telstra-focused solution.\n\n5. All team members:\n- Collaborate on integrating Copilot into the solution in the long term.\n\n6. Steven Yuen and Jason Hong:\n- Discuss the issue of Copilot access and find a solution.\n\n7. Steven Yuen:\n- Chase up the requirements from the stakeholders.")

if __name__ == '__main__':
    main()