def ticket_splitter(input_string):

    # input_string = "Based on the transcript, here are a few Jira tickets that could be created:\n\n1. Ticket Title: Agile Work Environment Integration\n   - Description: Investigate and implement features to align the solution with Telstra's agile work environment, such as support for different types of agile meetings and ceremonies.\n   - Assignee: Steven Yuen\n   - Priority: High\n\n2. Ticket Title: Contextual Output Generation\n   - Description: Develop functionality to use the transcripts of past meetings as context to generate more accurate and valuable output for future meetings.\n   - Assignee: Steven Yuen\n   - Priority: Medium\n\n3. Ticket Title: Centralized Dashboard\n   - Description: Create a centralized dashboard to manage and track all meetings and their associated artifacts, providing a seamless experience for users.\n   - Assignee: Steven Yuen\n   - Priority: Medium\n\n4. Ticket Title: Copilot Integration and Customization\n   - Description: Explore the possibility of integrating Telstra's solution with Copilot, tailoring it to meet specific business needs and leveraging the existing platform.\n   - Assignee: Jason Hong\n   - Priority: Medium\n\n5. Ticket Title: Meeting Minutes Tailoring\n   - Description: Modify the meeting minutes feature to align with different meeting types, such as retros, stand-ups, and ceremonies, to provide more relevant and useful outputs.\n   - Assignee: Chris Qu\n   - Priority: Low\n\nPlease note that these suggested tickets are based on the information provided in the transcript and may need to be adjusted based on further discussions and requirements."

    # Split the input string into sections based on '\n\n'
    sections = input_string.split('\n\n')

    to_return = []

    # Print each section in the list
    for i in range(1,len(sections)-1):
        # print(sections[i])


        # Split the input string into lines
        lines = sections[i].split('\n')

        # Initialize an empty dictionary to store the key-value pairs
        ticket_info = {}

        for line in lines:

            # print(line)
            try:
                # Split each line into key and value using ':'
                key, value = line.strip().split(': ')
                # Remove leading and trailing spaces from the key and value
                key = key.strip()
                value = value.strip()
                # Add the key-value pair to the dictionary
                ticket_info[key] = value

            except():
                pass

        to_return.append(ticket_info)

    return to_return


def main():
    print(ticket_splitter("JIRA Tickets:\n\nTicket 1:\nTitle: Improve Agile Work Environment Integration\nDescription: This ticket involves enhancing our solution to be better aligned with Telstra's Agile work environment. We need to identify and address the gaps in Copilot's integration with Agile processes. By focusing on agility, we can differentiate our product and provide more value to Telstra. This ticket will involve researching Agile methodologies and adapting our solution to cater to Telstra's specific needs.\nAssignee: Yuen, Steven\nPriority: High\n\nTicket 2:\nTitle: Enhance Context Window in Meeting Transcripts\nDescription: Currently, Copilot does not utilize the full context window of meeting transcripts to generate outputs. This ticket involves optimizing our solution to accumulate and leverage knowledge from past meetings. By using the entire context window, we can provide more accurate and relevant outputs to Telstra. This ticket will require modifying our algorithm and analyzing the feasibility of incorporating past meeting data.\nAssignee: Yuen, Steven\nPriority: Medium\n\nTicket 3:\nTitle: Develop Centralized Dashboard for Meeting Management\nDescription: To further differentiate our product from Copilot, we will create a centralized dashboard for managing all meetings. This ticket involves designing and implementing a user-friendly dashboard that allows Telstra users to seamlessly navigate and track their meetings. The dashboard should integrate with our solution and provide a clear overview of meeting details, actions, and outcomes. This feature will enhance the user experience and improve efficiency in meeting management.\nAssignee: Yuen, Steven\nPriority: High\n\nTicket 4:\nTitle: Tailor Meeting Minutes to Agile Ceremonies\nDescription: To cater to Telstra's Agile work environment, we need to modify our meeting minutes generation feature to align with different Agile ceremonies such as retrospectives and stand-ups. This ticket involves understanding the requirements and expectations of each Agile ceremony and adapting our solution to generate meeting minutes that provide meaningful insights and support effective decision-making. This feature will enhance the value of our solution for Telstra teams.\nAssignee: Yuen, Steven\nPriority: Medium\n\nTicket 5:\nTitle: Investigate Access to Copilot and Integration Possibilities\nDescription: Currently, access to Copilot is limited, and we need to understand the possibilities of integrating our solution with the existing Copilot platform. This ticket involves researching Copilot's capabilities, evaluating the feasibility of our integration, and understanding the partnership agreement with Microsoft. The findings from this investigation will inform our long-term strategy and determine the optimal approach for collaboration and integration with Copilot.\nAssignee: Gailey, David\nPriority: High"))

if __name__ == '__main__':
    main()