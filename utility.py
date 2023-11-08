import os
import openai
import json  
from thread_utility import ReturnValueThread
from splitter import ticket_splitter,action_splitter,retro_splitter, user_story_splitter

openai.api_key = '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'
openai.Model.list()

def Meeting_Master(filename):

    with open("uploads/"+filename,'r') as file:
        
        data = file.read()

        thread_minutes = ReturnValueThread(target=Compute_Create_Meeting_Minutes, args=(data,))
        thread_action_items = ReturnValueThread(target=Compute_Create_Action_Items, args=(data,))
        thread_next_agenda = ReturnValueThread(target=Compute_Create_Next_Agenda, args=(data,))

        thread_minutes.start()
        thread_action_items.start()
        thread_next_agenda.start()


        # print(data)

        to_return = {
            'minutes':thread_minutes.join(),
            'action_items':thread_action_items.join(),
            'next_agenda':thread_next_agenda.join()
        }

    return to_return


def Compute_Create_Meeting_Minutes(data):

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a project management assistant, skilled in explaining complex programming concepts with creative flair."},
            # {"role": "user", "content": "Can you imagine and create a transcript from a fictional meeting involving four people."}

            {"role": "user", "content": "Below is the transcript from a meeting. Please create minutes for this meeting."},
            {"role": "user", "content": data}
        ]
    )

    # f = open("processed/minutes.txt", "w")
    # f.write(str(completion.choices[0].message))
    # f.close()

    # # the json file where the output must be stored  
    # out_file = open("processed/minutes.json", "w")  
    
    # json.dump(completion.choices[0].message, out_file, indent = 6)  
    
    # out_file.close()

    # print(completion.choices[0].message)

    return completion.choices[0].message

def Compute_Create_Action_Items(data):

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a project management assistant, skilled in explaining complex programming concepts with creative flair."},

            {"role": "user", "content": "Below is the transcript from a meeting. Please create a list of action items for each person. Please format it like in this example: Action Items:\n\n1. Steven Yuen:\n- Research and identify features that cater to Agile work environments.\n- Investigate the use of a centralized dashboard for managing meetings.\n- Determine how the solution can differentiate itself from Copilot.\n- Gather requirements and file from the stakeholders.\n\n2. Jason Hong:\n- Continue working on current tasks and projects.\n\n3. David Gailey:\n- Support the shift towards an Agile focus for the solution.\n- Assist in identifying unique features and value proposition compared to Copilot.\n\n4. Chris Qu:\n- Participate in discussions and provide input on the direction of the solution.\n- Assist in determining the necessary features for the Telstra-focused solution.\n\n5. All team members:\n- Collaborate on integrating Copilot into the solution in the long term.\n\n6. Steven Yuen and Jason Hong:\n- Discuss the issue of Copilot access and find a solution.\n\n7. Steven Yuen:\n- Chase up the requirements from the stakeholders."},
            {"role": "user", "content": data}
        ]
    )

    return action_splitter(completion.choices[0].message["content"])

def Compute_Create_Next_Agenda(data):
    
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a project management assistant, skilled in explaining complex programming concepts with creative flair."},

            {"role": "user", "content": "Below is the transcript from a meeting. Please create an agenda for the next meeting."},
            {"role": "user", "content": data}
        ]
    )

    return completion.choices[0].message


def Agile_Master(filename):

    print("I;m runngin here")

    with open("uploads/"+filename,'r') as file:
        
        data = file.read()

        thread_jira = ReturnValueThread(target=Compute_Suggest_Jira_Tickets, args=(data,))
        thread_story = ReturnValueThread(target=Compute_User_Stories, args=(data,))
        # thread_next_agenda = ReturnValueThread(target=Compute_Create_Next_Agenda, args=(data,))

        thread_jira.start()
        thread_story.start()
        # thread_next_agenda.start()


        # print(data)

        to_return = {
            'jira_tickets':thread_jira.join(),
            'user_story':thread_story.join(),
        }

    return to_return

def Compute_Suggest_Jira_Tickets(data):
    
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a project management assistant, skilled in making Jira tickets."},

            # {"role": "user", "content": "Below is the transcript from a meeting. Please suggest several Jira Tickets based off this transcript. Each ticket should have: ticket title, description, Assignee, acceptance criteria, duration estimate and priority. Please format the response so it looks like this example: Based on the transcript, here are a few Jira tickets that could be created:\n\n1. Ticket Title: Agile Work Environment Integration\n   - Description: Investigate and implement features to align the solution with Telstra's agile work environment, such as support for different types of agile meetings and ceremonies.\n   - Assignee: Steven Yuen\n   - Acceptance Criteria: The solution should provide features that are tailored to agile work practices and support different types of agile meetings. It should integrate seamlessly with Telstra's existing agile tools and workflows.\n   - Duration Estimate: 2 days\n   - Priority: High\n\n2. Ticket Title: Contextual Output Generation\n   - Description: Develop functionality to use the transcripts of past meetings as context to generate more accurate and valuable output for future meetings.\n   - Assignee: Steven Yuen\n   - Acceptance Criteria: The solution should analyze past meeting transcripts and use the context to generate meeting outputs that are tailored to the specific meeting type. The generated output should provide valuable insights and recommendations based on the accumulated knowledge from past meetings.\n   - Duration Estimate: 4 days\n   - Priority: Medium\n\n3. Ticket Title: Centralized Dashboard\n   - Description: Create a centralized dashboard to manage and track all meetings and their associated artifacts, providing a seamless experience for users.\n   - Assignee: Steven Yuen\n   - Acceptance Criteria: The dashboard should allow users to easily schedule, manage, and track meetings. It should provide visibility into meeting details, attendees, agenda, and generated outputs. The dashboard should also support integration with Telstra's existing tools and systems.\n   - Duration Estimate: 2 days\n   - Priority: Medium\n\n4. Ticket Title: Copilot Integration and Customization\n   - Description: Explore the possibility of integrating Telstra's solution with Copilot, tailoring it to meet specific business needs and leveraging the existing platform.\n   - Assignee: Jason Hong\n   - Acceptance Criteria: The integration with Copilot should allow Telstra's solution to complement and enhance the functionalities provided by Copilot. The integration should be seamless and provide added value to Telstra's users. Customization options should be explored to align with Telstra's unique requirements.\n   - Duration Estimate: 4 days\n   - Priority: Medium\n\n5. Ticket Title: Meeting Minutes Tailoring\n   - Description: Modify the meeting minutes feature to align with different meeting types, such as retros, stand-ups, and ceremonies, to provide more relevant and useful outputs.\n   - Assignee: Chris Qu\n   - Acceptance Criteria: The meeting minutes feature should be enhanced to adapt to different meeting types and generate meeting summaries that are tailored to the specific purpose of the meeting. The tailored meeting minutes should provide key highlights, action items, and insights based on the discussions and outcomes of each meeting type.\n   - Duration Estimate: 3 days\n   - Priority: Low\n\nPlease note that these suggested tickets are based on the information provided in the transcript and may need to be adjusted based on further discussions and requirements."},
            {"role": "user", "content": "Below is the transcript from a meeting. Please suggest several Jira Tickets based off this transcript. Each ticket should have: ticket title, description, Assignee, acceptance criteria, duration estimate,  priority and user-story. Please format the response so it looks like this example: Based on the transcript, here are a few Jira tickets that could be created:\n\n1. Ticket Title: Agile Work Environment Integration\n   - Description: Investigate and implement features to align the solution with Telstra's agile work environment, such as support for different types of agile meetings and ceremonies.\n   - Assignee: Steven Yuen\n   - Acceptance Criteria: The solution should provide features that are tailored to agile work practices and support different types of agile meetings. It should integrate seamlessly with Telstra's existing agile tools and workflows.\n   - Duration Estimate: 2 days\n   - Priority: High\n   - User-story:As a project manager, I want a central dashboard to integrate all agile meetings and provide a consistent timeline so that I can easily track and manage all project activities.\n\n2. Ticket Title: Contextual Output Generation\n   - Description: Develop functionality to use the transcripts of past meetings as context to generate more accurate and valuable output for future meetings.\n   - Assignee: Steven Yuen\n   - Acceptance Criteria: The solution should analyze past meeting transcripts and use the context to generate meeting outputs that are tailored to the specific meeting type. The generated output should provide valuable insights and recommendations based on the accumulated knowledge from past meetings.\n   - Duration Estimate: 4 days\n   - Priority: Medium\n   - User-story:As a team member, I want an AI-powered solution that generates meeting minutes tailored for agile ceremonies, such as retros, stand-ups, and planning sessions, so that I can have a clear record of discussions and action items.\n\n3. Ticket Title: Centralized Dashboard\n   - Description: Create a centralized dashboard to manage and track all meetings and their associated artifacts, providing a seamless experience for users.\n   - Assignee: Steven Yuen\n   - Acceptance Criteria: The dashboard should allow users to easily schedule, manage, and track meetings. It should provide visibility into meeting details, attendees, agenda, and generated outputs. The dashboard should also support integration with Telstra's existing tools and systems.\n   - Duration Estimate: 2 days\n   - Priority: Medium\n   - User-story:As a Telstra executive, I want a solution that provides a transcript of agile meetings and generates reports based on the meeting content so that I can gain insights and make informed decisions.\n\n4. Ticket Title: Copilot Integration and Customization\n   - Description: Explore the possibility of integrating Telstra's solution with Copilot, tailoring it to meet specific business needs and leveraging the existing platform.\n   - Assignee: Jason Hong\n   - Acceptance Criteria: The integration with Copilot should allow Telstra's solution to complement and enhance the functionalities provided by Copilot. The integration should be seamless and provide added value to Telstra's users. Customization options should be explored to align with Telstra's unique requirements.\n   - Duration Estimate: 4 days\n   - Priority: Medium\n   - User-story:As a user of an agile work environment, I want a solution that automates repetitive administrative tasks, such as generating tickets and updating progress, so that I can focus more on actual work.\n\n5. Ticket Title: Meeting Minutes Tailoring\n   - Description: Modify the meeting minutes feature to align with different meeting types, such as retros, stand-ups, and ceremonies, to provide more relevant and useful outputs.\n   - Assignee: Chris Qu\n   - Acceptance Criteria: The meeting minutes feature should be enhanced to adapt to different meeting types and generate meeting summaries that are tailored to the specific purpose of the meeting. The tailored meeting minutes should provide key highlights, action items, and insights based on the discussions and outcomes of each meeting type.\n   - Duration Estimate: 3 days\n   - Priority: Low\n   - User-story:As a Telstra employee, I want a cost-effective agile project management tool that offers similar features as Copilot but can be tailored specifically for Telstra's needs, so that we can save costs without compromising functionality.\n\nPlease note that these suggested tickets are based on the information provided in the transcript and may need to be adjusted based on further discussions and requirements."},
            # {"role": "user", "content": "Below is the transcript from a meeting. Please suggest several Jira Tickets based off this transcript. Each ticket should have: ticket title, description, Assignee and priority. Please format the response so it looks like this example: Based on the transcript, here are a few Jira tickets that could be created:\n\n1. Ticket Title: Agile Work Environment Integration\n   - Description: Investigate and implement features to align the solution with Telstra's agile work environment, such as support for different types of agile meetings and ceremonies.\n   - Assignee: Steven Yuen\n   - Priority: High\n\n2. Ticket Title: Contextual Output Generation\n   - Description: Develop functionality to use the transcripts of past meetings as context to generate more accurate and valuable output for future meetings.\n   - Assignee: Steven Yuen\n   - Priority: Medium\n\n3. Ticket Title: Centralized Dashboard\n   - Description: Create a centralized dashboard to manage and track all meetings and their associated artifacts, providing a seamless experience for users.\n   - Assignee: Steven Yuen\n   - Priority: Medium\n\n4. Ticket Title: Copilot Integration and Customization\n   - Description: Explore the possibility of integrating Telstra's solution with Copilot, tailoring it to meet specific business needs and leveraging the existing platform.\n   - Assignee: Jason Hong\n   - Priority: Medium\n\n5. Ticket Title: Meeting Minutes Tailoring\n   - Description: Modify the meeting minutes feature to align with different meeting types, such as retros, stand-ups, and ceremonies, to provide more relevant and useful outputs.\n   - Assignee: Chris Qu\n   - Priority: Low\n\nPlease note that these suggested tickets are based on the information provided in the transcript and may need to be adjusted based on further discussions and requirements."},
            {"role": "user", "content": data}
        ]
    )


    # print(completion.choices[0].message)
    # print(completion.choices[0].message["content"])

    # return ticket_splitter(completion.choices[0].message)

    return ticket_splitter(completion.choices[0].message["content"])

def Compute_User_Stories(data):

    print("I'm runnung here 2")
    
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a project management assistant, skilled in making agile user stories."},

            {"role": "user", "content": "Below is the transcript from a meeting. Please suggest several user stories in the format: as a [], I want [] so that []. Use the format that is in this example: As a Telstra employee, I want a user-friendly agile project management tool so that I can efficiently manage and track all agile ceremonies and tasks.\n\nAs a project manager, I want a central dashboard to integrate all agile meetings and provide a consistent timeline so that I can easily track and manage all project activities.\n\nAs a team member, I want an AI-powered solution that generates meeting minutes tailored for agile ceremonies, such as retros, stand-ups, and planning sessions, so that I can have a clear record of discussions and action items.\n\nAs a Telstra executive, I want a solution that provides a transcript of agile meetings and generates reports based on the meeting content so that I can gain insights and make informed decisions.\n\nAs a user of an agile work environment, I want a solution that automates repetitive administrative tasks, such as generating tickets and updating progress, so that I can focus more on actual work.\n\nAs a Telstra employee, I want a cost-effective agile project management tool that offers similar features as Copilot but can be tailored specifically for Telstra's needs, so that we can save costs without compromising functionality."},
            {"role": "user", "content": data}
        ]
    )


    # print(completion.choices[0].message)
    # print(completion.choices[0].message["content"])
    # print("ticket splitter")


    return user_story_splitter(completion.choices[0].message["content"])
    # return (completion.choices[0])


def Retro_Master(filename):

    with open("uploads/"+filename,'r') as file:
        
        data = file.read()

        thread_retro = ReturnValueThread(target=Compute_Retro_Suggestions, args=(data,))

        thread_retro.start()

        # print(data)

        to_return = {
            'retro_actions':thread_retro.join(),
        }

    return to_return

def Compute_Retro_Suggestions(data):
    
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a project management assistant, skilled in making agile retro ceremony action points."},

            {"role": "user", "content": "Below is the transcript from an agile retro meeting. Please suggest several action points based off this retro.Please use this format: Based on the transcript from the retrospective meeting, here are several action points that can be derived:\n\n1. Differentiate our product with an Agile focus: Tailor our solution towards an Agile work environment, since this is something that the current copilot solution lacks. This can include features that reduce time-consuming administrative tasks and cater specifically to Agile ceremonies such as retrospectives and stand-ups.\n\n2. Make the most out of the context window: Ensure that our solution can accumulate knowledge from past meetings and use it to provide valuable insights. This can involve improving the meeting generator to take into account the purpose of the meeting (retro, stand-up, ceremony) and adjust the output accordingly.\n\n3. Create a centralized dashboard: Differentiate our product by developing a central dashboard that allows users to manage and track all their meetings and associated tasks. This will add value by providing a centralized and streamlined experience, which is currently lacking in the copilot solution.\n\n4. Integrate with copilot in the long term: While access to copilot is currently limited, we can consider integrating our solution with copilot in the future. This will require collaboration and co-development with Microsoft, leveraging our strategic partnership, and allowing for a more seamless experience for users.\n\n5. Investigate Telstra-specific needs: Research and analyze Telstra's Agile work environment and identify any specific requirements and pain points that can be addressed by our solution. This will enable us to create a product that is tailored to Telstra's needs and provides a unique value proposition.\n\n6. Gather requirements: Chase up the requirements from the product stakeholders, such as the business and executive teams, to ensure that their needs are considered in the development of the solution.\n\nThese action points address the goal of differentiating our product from copilot and ensuring that it aligns with Telstra's Agile work environment, while also considering the integration possibilities with copilot in the long term."},
            {"role": "user", "content": data}
        ]
    )

    return retro_splitter(completion.choices[0].message["content"])

def Compute_Meta(data):

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a project management assistant, skilled in extracting information from meeting transcripts."},

            {"role": "user", "content": "Below is the transcript from an online meeting. Can you tell me the meeting date, the list of attendees, and meeting duration? You can calculate the duration by looking at the transcript time codes. Can you put the output like in this example: Meeting Date: 6/11/2023/nAttendees: Yuen, Steven; Hong, Jason; Gailey, David; Qu, Chris,/nDuration: 16:38"},
            {"role": "user", "content": data}
        ]
    )
    
    return split_meta_info(completion.choices[0].message["content"])

def Master_AI(filename,ID,meta_name,meta_type):

    with open("meetings/"+str(ID)+'/'+filename,'r') as file:
    
        data = file.read()


    # Meta
    thread_meta = ReturnValueThread(target=Compute_Meta, args=(data,))

    # Meeting
    thread_minutes = ReturnValueThread(target=Compute_Create_Meeting_Minutes, args=(data,))
    thread_action_items = ReturnValueThread(target=Compute_Create_Action_Items, args=(data,))
    thread_next_agenda = ReturnValueThread(target=Compute_Create_Next_Agenda, args=(data,))

    # Agile
    thread_jira = ReturnValueThread(target=Compute_Suggest_Jira_Tickets, args=(data,))
    # thread_story = ReturnValueThread(target=Compute_User_Stories, args=(data,))

    # Retro
    thread_retro = ReturnValueThread(target=Compute_Retro_Suggestions, args=(data,))

    thread_meta.start()

    thread_minutes.start()
    thread_action_items.start()
    thread_next_agenda.start()

    thread_jira.start()
    # thread_story.start()

    thread_retro.start()

    meta_dict = thread_meta.join()

    # print(meta_dict)



    # meta_file = open("meetings/"+str(ID)+'/meta.json', "w") 

    meta_dict_to_append = {'ID':ID,'title':meta_name,'type':meta_type,'date':meta_dict['Meeting Date'],'duration':meta_dict['Duration'],'attendees':meta_dict['Attendees']}

    make_file_metadata('meetings/' +str(ID),meta_dict_to_append)


    to_return = {
        'Meta':{
            'ID':ID,
            'title':meta_name,
            'type':meta_type,
            'date':meta_dict['Meeting Date'],
            'duration':meta_dict['Duration'],
            'attendees':meta_dict['Attendees']
        },
        'Meeting': {
            'minutes': thread_minutes.join(),
            'action_items': thread_action_items.join(),
            'next_agenda': thread_next_agenda.join()
        },
        'Jira': {
            'jira_tickets': thread_jira.join(),
            # 'user_story': thread_story.join()
        },
        'Retro': {
            'retro_actions': thread_retro.join()
        }
    }



    out_file = open("meetings/"+str(ID)+'/master_output.json', "w") 

    json.dump(to_return, out_file, indent = 6)  

    out_file.close()

    return meta_dict_to_append


# -----------------------------------------
def split_meta_info(meeting_info):
    info_dict = {}
    lines = meeting_info.strip().split('\n')
    
    for line in lines:
        key, value = line.split(': ')
        if key == "Meeting Date":
            info_dict["Meeting Date"] = value
        elif key == "Attendees":
            attendees = value.split('; ')
            info_dict["Attendees"] = attendees
        elif key == "Duration":
            info_dict["Duration"] = value
    
    return info_dict
# -----------------------------------------

def make_file_metadata(file_path,meta_dict):

    full_path = file_path + '/meta.json'

    with open(full_path, 'w') as outfile:
        json.dump(meta_dict, outfile)

    meta_master_maker()

    return

# 

def meta_master_maker():

    # Define the root folder where you want to start scanning
    root_folder = os.getcwd()+'/meetings'

    # Define the output file where you want to aggregate the data
    output_file = 'master_list.json'

    # Collect JSON files
    json_files = collect_json_files(root_folder)

    # Aggregate JSON files into the master JSON file
    aggregate_json_files(json_files, output_file)
    return

# Function to recursively scan subfolders and collect JSON files
def collect_json_files(root_folder):
    json_files = []
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith('.json') and not file.startswith('master'):
                json_files.append(os.path.join(root, file))
    return json_files

# Function to aggregate JSON files into a master JSON file
def aggregate_json_files(json_files, output_file):
    master_data = []

    for json_file in json_files:
        with open(json_file, 'r') as file:
            data = json.load(file)
            master_data.append(data)

    with open(output_file, 'w') as outfile:
        json.dump(master_data, outfile, indent=4)
