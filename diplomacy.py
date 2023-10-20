import autogen

# Configuration for the AI backend
config_list = [
    {
        'api_type': 'open_ai',
        'api_base': 'http://localhost:1234/v1',
        'api_key': 'sk-111111111111111111111111111111111111111111111111'
    }
]

llm_config={
    "request_timeout": 600,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0.6
}

# Define the AI agents based on their roles and expertise
diplomat = autogen.AssistantAgent(name="Diplomat", llm_config=llm_config, system_message="""
I am the Diplomat, skilled in negotiation and well-versed in international relations. My aim is to foster peaceful dialogue and find common ground among conflicting parties.
I'll work closely with the Historian to understand past relations and with the Legal Expert to ensure any agreements are legally sound.""")
historian = autogen.AssistantAgent(name="Historian", llm_config=llm_config, system_message="""
I am the Historian, dedicated to offering insights from past events. By understanding history, we can make informed choices in the present. 
I'll work with the Diplomat and Geostrategist to ensure they have the historical context they need.""")
geostrategist = autogen.AssistantAgent(name="Geostrategist", llm_config=llm_config, system_message="""
I am the Geostrategist, bringing a territorial perspective to the table. 
I'll collaborate with the Economist to understand resource implications and provide the team with strategic insights.""")
cultural_liaison = autogen.AssistantAgent(name="Cultural Liaison", llm_config=llm_config, system_message="""
I am the Cultural Liaison, dedicated to understanding and bridging cultural divides. 
My role is to ensure our solutions resonate with the hearts and minds of the people. I'll work closely with the Diplomat to ensure cultural sensitivity in negotiations.""")
economist = autogen.AssistantAgent(name="Economist", llm_config=llm_config, system_message="""
I am the Economist, here to provide an economic lens to our strategies. Collaborating with the Geostrategist, 
I'll assess the economic implications of territorial decisions.""")
legal_expert = autogen.AssistantAgent(name="Legal Expert", llm_config=llm_config, system_message="""
I am the Legal Expert, ensuring our actions are within the bounds of international law. 
I'll provide legal counsel to the Diplomat during negotiations and ensure our solutions are legally sound.""")
mediator = autogen.AssistantAgent(name="Mediator", llm_config=llm_config, system_message="""
I am the Mediator, the bridge between all agents. My goal is to ensure we work cohesively, synthesizing our diverse expertise to craft the best solution.
I'll facilitate discussions, ensuring all voices are heard and considered.""")
director = autogen.AssistantAgent(name="Director", llm_config=llm_config, system_message="""
I am the Director, your leader and coordinator. 
With my comprehensive skillset and emotional intelligence, I'll guide our team towards a holistic solution. 
My role is to integrate our collective knowledge, ensuring we address the conflict from all angles.
I'll work closely with the Mediator to facilitate effective communication and decision-making.""")
psychologist = autogen.AssistantAgent(name="Psychologist", llm_config=llm_config, system_message="""
I am the Psychologist, here to shed light on the human psyche. Understanding the motivations, fears, and desires of those involved is crucial in conflicts. 
I'll work with the Cultural Liaison to ensure our solutions resonate emotionally and with the Diplomat to prepare for potential emotional responses during negotiations.""")

# User proxy to interface with the director
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web"},
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction. Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)

# Initial task for the director to begin the conflict resolution
conflict_description = """
Here’s a summary of the current situation, risks involved, trends, and its impact on international geopolitics in the conflict between Israel and Palestina:

Current Situation: The conflict has escalated recently with an unprecedented attack by the Palestinian militant group Hamas on Israel, killing more than 1,400 people. Israel has responded with relentless bombing of the Gaza Strip. The Israeli military has also massed troops along the border in preparation for a ground offensive. This has led to a significant increase in violence across much of the occupied West Bank.

Risks Involved: The conflict could potentially escalate to engulf the wider Middle East. Iran’s role is of particular concern as it provides money and weapons to Hamas. There are fears that the conflict could spread beyond Gaza, West Bank, and Israel, affecting Europe directly, particularly if the Lebanon-based Hezbollah gets involved.

Trends: Negative trends have been dominating the region. Israel’s settlement activity continues, along with demolitions and evictions, while fiscal and political challenges threaten the Palestinian Authority’s effectiveness in delivering public services3. The West Bank and Gaza remain politically divided.

Impact on International Geopolitics: The conflict has significant implications for international geopolitics. It affects oil prices and thus the global economy. A sharp jump in oil prices often sparks recessions, and the cost of crude is sensitive to events in the Middle East. The alliances and rivalries simmering in the Middle East may see the conflict spread beyond Gaza, West Bank, and Israel.

Given the ongoing conflict, propose a diplomatic solution that considers historical, cultural, economic, legal, strategic, and psychological aspects. The solution must be as detailed and objective as possible, including a comprehensive low level list of tasks and steps to do.
"""

groupchat = autogen.GroupChat(agents=[user_proxy, director, diplomat, historian, geostrategist, cultural_liaison, economist, legal_expert, mediator, psychologist], messages=[], max_round=50)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(manager, message=conflict_description)
