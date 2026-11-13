# Documentation Building Agents
## Introduction
### The Goal
I am on a quest to build an agent that can categorize mail in an Outlook mailbox based on the mail's content. 

### The Strategy
In order to learn how to do this I used Microsoft Copilot to generate a tutorial for me that started with the very basics of agent building. Whenever I finished the exercises and understood the information Copilot provided me, I requested Copilot to continue the tutorial and continued working on the new exercises and information. 

In my initial prompt I directed Copilot to give me a tutorial in Python. A Google search suggested that this is the best language to use due to its simplicity, extensive libraries, and strong community support.

**Currently I am still in this iterative tutorial process. Once I feel I have a good enough grasp on how to build agents, I plan to apply what I've learned to creating an agent that actually satisfies the goal requirement.**

## Progression
### Lesson 1: building a primitive AI
*See: oldFiles/1_primitive_agent.py*

To start off, Copilot suggested I build a "primitive AI". This AI did not consist of any AI models yet, but showed the general structure an agent should be built with. Copilot taught me about the observe -> think -> act process that llm's go through:
1. **Observe**: Gather information about the world and itself
2. **Think**: The agent considers its situation and decides on the best way to act based on a "decision policy"
3. **Act**: The agent acts out the decided choice, which changes the world through consequences.

### Lesson 2: using a model to think
*See: oldFiles/2_agent.py*

In this lesson I upgraded the primitive agent by replacing the rule-based think method with a model that takes a prompt and responds with the best way to act. Copilot advised me to use **Ollama** for importing and using models in my code because they allow the use of Local Models, meaning there is no risk of sensitive data leaking online. Basically you download a model to your local device and specify you want to use that in your code. For the tutorials I was advised to use the "qwen3.5:4b" model. Qwen3.5 was suggested as a good model for practicing building agents, and :4b means I want the model to use 4 billion parameters. Copilot claimed this would be good enough for any practice purposes. I did end up having to use my personal desktop to run the model as the Qquest laptop had no proper GPU installed to run the model, leading to very long waiting times to get responses.

This lesson taught me how to download models from Ollama, build prompts to contact the model with, and how to use the response from the model to decide on how to act.

### Lesson 3: providing tools to the model
*See: oldFiles/3_tool_agent.py*

In this lesson I learned about how to provide a model with tools to expand their capabilities to acquire information. A tool is a function the agent can execute to acquire information it does not implicitly have access to. Tools can be used to collect any data that is relevant and available either through an API or through self-provided data. 

This lesson is where things became more interesting regarding how to properly use prompts to get a response in a desired format for further processing. It took me a little while to get to a point where I could get the model to extract exactly the best tool for the job and the required parameter value for the tool function from the question provided by the user. It was also challenging to get the response in a proper JSON format so that I could properly extract the tool and parameter value from the response string. 

This lesson made me realise that I'd need more knowledge about how to properly construct a prompt before I could effectively use models to provide me with specifically the information I need. To brush up on this knowledge I decided to go through several trainings from the AWS Artificial Intelligence Practitioner Learning Plan (https://skillbuilder.aws/learning-plan/G8ENMJ5QBE/aws-artificial-intelligence-practitioner-learning-plan/SU2A1EJM1A?trk=d37ff52f-b536-4e4f-8094-37e05a0006ee&sc_channel=el). This was surprisingly useful, as it made me more comfortable in writing prompts through knowing what I could add to a prompt without confusing the model.

### Lesson 9: Alternative Approach
I redesigned model 8 by using a different Copilot account and asking it questions on how I should improve my model. While the resulting model is significantly worse due to it not being an agentic loop, there are some properties that I should consider implementing in further models:
- The schema attribute for every tool in the tool registry
- Separating the task of selecting a tool and the task of generating arguments for the selected tool into two prompts that are used sequentially rather than expecting the model to perform two tasks in a single prompt.

### Lesson 10: Refactors and Upgrades
I'd like to try to see if I can increase the quality of model 8 by implementing the previously mentioned good qualities of model 9.
The readability of the code has definitely improved, and separating the prompts reduced the errors produced in selecting the tool.
It does look like so far the generation of arguments is still performing poorly.

I improved the performance and readability of the code in several ways:
- I added the option to provide temperature values and json_schemas to the Brain method that contacts the model through the chat() function. I also added a 'think' parameter, which causes the method to print the complete thought process of the model related to the response in question.
- I took the example schema's out of the prompt and the tool registry, and instead used pydantic BaseModels that I directly used as a parameter in the chat() function. 
- The above change also allowed for easy json-validation to ensure the responses are correctly formatted when accessed further down the code.
- I created a 'prompts' directory in which I created three files: constants.py, which contains the system prompts, generators.py, which contains functions to dynamically generate user prompts, and schemas.py, which contains the pydantic BaseModels used to provide and validate the json schemas.
- I also created a schemas.py file in the 'tools' directory, which contains a pydantic BaseModel for every tool in the tool registry. This is required to dynamically provide the model with the correct json schema in the generate_arguments step. 
- I created an executor to separate the execution code from the step decision code. This greatly improved the readability of my code. 
- I added observations to the user prompt to generate arguments so that the model can use previous observations to determine which file it needs to use as argument to tools. This resolved the issue where the model kept making up filenames to pass as arguments.
- I added typings to all relevant parameters and variables using basic types and imported types from the Typing package. This should improve the readability of the code.

### Lesson 11: Critics
In this iteration of the agent I modified the select_action() method from the executor so that it fulfils the function of a critic. This means that instead of simply returning 'yes' or 'no' as an assessment of whether there is enough information to generate a final answer, the model now also provides a reasoning for their choice and points out what information is missing. The reasoning and missing information are stored in the agent's memory so that it can be accessed during tool selection.

I also removed the non-rag tools because they were confusing the model and essentially provided no benefit to the functioning of the agent.

For a while asking the agent a question about information that cannot be found in the knowledge base created an infinite loop where the critic kept insisting to look for more information in the knowledge base. I managed to fix this by changing the list of responses the critic may choose from. Instead of "yes" or "no", referring to whether there is enough information, the critic now respons with "enough", "more", or "exhausted". This gives the critic the explicit option to decide additional searches are unlikely to produce new information. Additionally, the critic's decision making also improved by specifying in the system prompt that "more" means more information should be collected specifically from the knowledge base. 

What's interesting is that logging the reasoning from the critic also shows that it looks at how tools were used previously in the session and decides to respond with "exhausted" based on what's already been tried.

### Lesson 12: Upgrading the planner
The goal of this model was to upgrade the planner so that instead of going through the same motions every iteration, it dynamically creates and updates a plan based on the information it has gathered so far.

First I updated some terminology in the files: the pydantic model classes now have Model in their names for clarity, and the json_schema attribute of the tools in the tool registry is renamed to response_model to better reflect that the associated value is a pydantic model class. To reflect this change in the file names, I also renamed the schema.py files to models.py.

The planner has been upgraded in the following ways:
- The planner start by creating a plan that contains steps that the agent should go through before answering the question.
- Every agent iteration, the planner decides what the next action should be. This can return one of three options: (1) 'tool', meaning more information should be collected in order to finish the current step of the plan; (2) complete_step, meaning enough information is available to consider the current step of the plan completed and thus to move on to the next step in the plan; (3) 'done', meaning there are no steps remaining in the plan and thus a final answer can be generated with all collected information.
- The plan and the current step are also stored in the memory so that it can easily be accessed and provided in prompts.

What's important about this upgrade is that now the agent does not follow a predetermined flow of actions anymore. 

I also added some other improvements to the code:
- Added a 'logs' directory in which the agent creates an 'observations.txt' file upon returning a value or crashing due to an error. This .txt file contains all observations stored in the memory. The purpose of this file is purely for debugging.
- Improved the formatting of the observations to increase the readability of the observations.txt file.
- I refactored the user prompt generators by creating one function for all user prompts instead of one function for each prompt. Exception to this is the generate_arguments user prompt generator because this user prompt has a different structure to the other ones.

### Lesson 13: Accessing external sources for information
Before implementing any external sources I upgraded the data processing of my agent. I implemented the following things:
- Added a folder data_processing that contains all files related to preparing data.
- Instead of embedding entire documents, the agent now separates documents into chunks and embeds the chunks instead.
- The semantic_search tool now returns a formatted string containing organized metadata of the top 5 most similar chunks from the knowledge files.

I also removed the read_document and search_documents tools, considering these functionalities are already built into semantic_search. I renamed the last remaining tool from semantic_search to retrieve_knowledge to better signify that this tool is the main tool for collecting knowledge from the knowledge files.

On top of that I also created a centralized place in the agents folder where all models will be stored. This 'models' folder will make it easier to find all models quickly and saves me the headache of finding models files all around the project to see where the model class is that I need.
