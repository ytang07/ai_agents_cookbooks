Title: How to Build An AI Agent

URL Source: http://arize.com/blog/how-to-build-an-ai-agent/

Published Time: 2025-02-18T20:01:34+00:00

Markdown Content:
An agent is a software system that orchestrates multiple processing steps— including calls to large language models—to achieve a desired outcome. Rather than following a linear, predefined path, an agent can traverse a wide solution space, handling decision-making logic, remembering intermediate steps, and determining which actions to take and in which order. This enables agents to complete difficult, broad-ranging tasks that are out of the realm of possibility for traditional software.

In this post we’ll cover everything you need to know to build your own functioning AI agent using [smolagents](https://github.com/huggingface/smolagents), [AutoGen](https://github.com/microsoft/autogen), or [LangGraph](https://github.com/langchain-ai/langgraph).

Do You Need an Agent?
---------------------

It’s not always necessary to implement an agent. It’s always worth pausing to consider, do I really need an agent for this use case? Agents shine when your application requires iterative workflows, adaptive logic, or exploring multiple pathways.

If you’re not sure, ask yourself:

*   Iterative Flows: Does your workflow rely on multi-stage processes where each step informs the next?
*   Adaptive Logic: Do you switch actions based on feedback or prior outcomes?
*   Complex State Management: Do you have a range of possible actions that aren’t limited to a single sequence?

For simpler use cases—like basic queries—an LLM alone may be enough. But agents offer:

*   Memory & Planning: Track previous steps and map out what comes next.
*   Tool Access: Integrate with APIs or the internet for up-to-date info.
*   Longevity & Learning: Improve over time through iterative feedback.

Ultimately, the decision depends on your task’s complexity, available resources, and the added value an agent can bring.

LLM Function Calling: Single-Step vs. Full Agent
------------------------------------------------

A key ingredient in many agent systems is function (tool) calling, where an LLM outputs structured data that maps to specific actions or APIs. This can range from a simple one-step flow—just a single LLM call deciding which function to invoke—to a more advanced, multi-step agent with memory and planning.

### What is Function Calling?

Modern LLMs like GPT-4, Claude, and Llama can produce responses in specific structured formats (e.g., JSON), which an application can parse to decide which ‘tool’ (function, API, service) to execute. This process bridges natural language with programmatic actions.

*   Single-Step Choice: After giving an LLM a list of possible functions, the model selects the appropriate function based on user input.
*   Structured Output: The LLM’s response follows a specific format, making it easier to parse and reducing errors.
*   Scalability: Over time, you can add more functions to handle additional tasks without altering core logic.

### Single LLM Call vs. Full Agent

For more complex tasks, you can expand the LLM’s role to include iterative reasoning and tool usage:

*   Single Call with Function Calling: Best for straightforward tasks where LLM needs to pick the right tool once. Quick to implement.
*   Agent with Memory & Multi-Step Reasoning: Goes beyond the single step, incorporating iterative decision-making and maintaining a stable state across multiple calls. Can orchestrate complex workflows & calling different tools as new information comes in.

Both approaches leverage function calling. But while a basic LLM call solves one-off tasks, a full agent adds layers of logic, memory, and iterative planning – enabling more sophisticated, adaptive solutions.

Building an Agent: Code vs. Framework
-------------------------------------

You can either build your agent from scratch or use a framework like smolagents, LangGraph, or AutoGen. Frameworks handle common challenges—such as state, routing, and skill descriptions—while offering established best practices and examples.

**Why Use a Framework?**

*   Quick Setup: Skip boilerplate and get started faster.
*   Docs & Examples: Larger frameworks often have great resources.
*   Integration: Many tie seamlessly into orchestration libraries like LangChain or LlamaIndex.

**Potential Drawbacks**

*   Reduced Flexibility: Complex agents may outgrow a framework’s abstractions.
*   Opinionated Designs: Adjusting the framework to fit a unique architecture can be difficult.
*   Lock-In Concerns: Switching away can mean a major refactor.

When to Go Custom
-----------------

For highly specialized or large-scale architectures, coding your own agent might be a better fit. It’s easier to fine-tune every layer and avoid limitations imposed by a framework’s design.

Bottom Line: If your agent is simple or you want a quick start, frameworks can help. For complex, evolving systems, a custom approach may grant the flexibility you need—though frameworks like smolagents, langgraph, and autogen are steadily improving and may soon fit more intricate use cases.

The rest of this guide will show you how set up an example agent using the following common frameworks:

*   [smolagents](https://github.com/huggingface/smolagents)
*   [LangGraph](https://github.com/langchain-ai/langgraph)
*   [Autogen](https://github.com/microsoft/autogen)

Build an Agent Using smolagents
-------------------------------

Next up, let’s explore how quickly we can get an agent running using Hugging Face’s smolagents. We’ll walk through the setup, configuration, and a simple example to highlight just how straightforward it can be.

Smolagents is great because:

*   Pre-build Agents: Has a set of prebuilt common agents to use
*   Seamless Integration: Tightly connects with Hugging Face tools & infrastructure for streamlined development
*   Flexible Architecture: Allows for both simple function-calling agents & more intricate workflows

### Step 1: Install the Required Libraries

```
 
pip install smolagent pip install 'smolagents[litellm]'
```

### Step 2: Import all the Essential Building Blocks

Now let’s bring in the classes and tools we’ll be using:

```

from smolagents import (
   CodeAgent,
   ToolCallingAgent,
   ManagedAgent,
   DuckDuckGoSearchTool,
   VisitWebpageTool,
   HfApiModel,
)
from smolagents import LiteLLMModel 
```

Here’s a quick rundown of what each import is about:

*   **LiteLLMModel and HfApiModel:** Two different model classes; really only need one to build an agent (we’ll focus on using HfApiModel)
*   **CodeAgent:** Specialized agent to help with code-related tasks (won’t be the focus of this tutorial, but it’s handy to have it available).  
    ToolCallingAgent: Agent designed to call external tools (ex. web search/code execution)
*   **ManagedAgent:** Manager for your agent, providing structure around tasks, logging, and more.
*   **DuckDuckGoSearchTool & VisitWebpageTool:** Predefined tools in the smolagent library that let the agent search the web and visit webpages. You can also create your own custom tools!

### Step 3: Set Up Our Base Models

We’ll create two model instances—one for a local or custom model, and one for the Hugging Face Hub:

```

model = LiteLLMModel(model_id="meta-llama/Llama-3.2-3B-Instruct")
hfModel = HfApiModel()
```

*   Model\_id is just a placeholder; replace it with a different model.
*   HfApiModel() leverages a Hugging Face model via the Inference API (make sure you have appropriate authentication if needed).

### Step 4: Create Tool Calling Agent

```

agent = ToolCallingAgent(
    tools=[DuckDuckGoSearchTool(), VisitWebpageTool()],
    model=hfModel,
    add_base_tools=True
)
```

**What’s going on here?**

*   tools=\[DuckDuckGoSearchTool(), VisitWebpageTool()\]: We give the agent a search tool and a webpage visitation tool so it can explore the web.
*   model=hfModel: Instructing the agent to use our Hugging Face API model.
*   add\_base\_tools=True: A parameter that adds some basic built-in tools (e.g., for text manipulation).

### Step 5: Run the Agent

Now for the magic moment—let’s see our agent in action. The question we’re asking our agent is:  
“Fetch the share price of Google from 2020 to 2024, and create a line graph from it?”

```

agent.run("fetch the share price of google from 2020 to 2024, and create a line graph from it?")
```

Your agent will now:

1.  Use DuckDuckGoSearchTool to search for historical share prices of Google.
2.  Potentially visit pages with the VisitWebpageTool to find that data.
3.  Attempt to gather information and generate or describe how to create the line graph.

Let’s take it a step further and explore how to manage multiple agents (or keep better tabs on a single agent) by using a ManagedAgent alongside a manager agent. To implement this with our code so far, follow steps 1-3 from above.

### Step 4: Introducing the ManagedAgent (and Manager Agent)

Sometimes you want a little more structure around your agent, especially if you plan on juggling multiple tasks or want to keep logs. That’s where the ManagedAgent comes in. For all of these managed agents, you will need a “boss agent” to coordinate tasks – a manager agent. In the smolagent library, a convenient choice for a manager agent is the CodeAgent.

#### Step 4a: Create your Managed Agents

```


search_agent = ToolCallingAgent(
   tools=[DuckDuckGoSearchTool(), VisitWebpageTool()],
   model=hfModel,
)
managed_agent_search = ManagedAgent(
   agent=search_agent,
   name="search_agent",
   description="This agent can perform web searches."
)
code_worker_agent = CodeAgent(
   tools=[],
   model=hfModel,
)
managed_agent_code = ManagedAgent(
   agent=code_worker_agent,
   name="coding_agent",
   description="This agent can handle code-related tasks."
)
```

#### Step 4b: Create Your Manager Agents

```


manager_agent = CodeAgent(
   tools=[],
   model=hfModel,
   managed_agents=[managed_agent_search, managed_agent_code],
)
```

*   Managed Agent: We transform our search\_agent and code\_worker\_agent into ManagedAgents so we can keep better track of what they do (e.g., logging, chaining tasks, etc.).
*   Manager Agent: This final “boss” agent is a CodeAgent that has both managed\_agent\_search and managed\_agent\_code under its watch.

### Step 5: Run the Agent

```


manager_agent.run("Check the current weather in New York, then explain how to write a basic Python function.")
```

When you call manager\_agent.run(…), it can delegate parts of the request to the appropriate underlying agent(s). That’s it! With a ManagedAgent and a manager agent, you can keep your AI agents organized and ready for more complex workflows.

Congrats! We just finished our first agent!

After you’ve built your agent, track how it’s doing on Phoenix with our [smolagents integration](https://docs.arize.com/phoenix/tracing/integrations-tracing/hfsmolagents).

Build an Agent Using AutoGen
----------------------------

Next up, let’s explore how quickly we can get an agent running using the Autogen Framework. We’ll walk through the setup, configuration, and a simple example to highlight just how straightforward it can be.

### Step 1: Install the Required Libraries

```


pip install pyautogen -q
pip install -q openai autogen
```

### Step 2: Import all the Essential Building Blocks

Now let’s bring in the classes and tools we’ll be using:

```


import openai
from autogen import AssistantAgent, UserProxyAgent
```

Here’s a quick rundown of the imports:

*   **AssistantAgent:** Solves tasks with LLMs.
*   **UserProxyAgent:** Provides feedback to other agents.

### Step 3: Set up your OpenAI API Key & Model

Since AutoGen is backed by an OpenAI Assistant API, you’ll need to set it up prior to creating an agent.

```


openai.api_key =  

config_list = [
   {
       "model": "gpt-4o",
       "api_key": openai.api_key,
   }
]
```

Config\_list: tells agent which model to use and the associated API key. Most useful if you plan to switch between different model chaining.

### Step 4: Create the AssistantAgent

```


writer_agent = AssistantAgent(
   name="writer",
   llm_config={
       "config_list": config_list,
       "temperature": 0.7,
   }
)
editor_agent = AssistantAgent(
   name="editor",
   llm_config={
       "config_list": config_list,
       "temperature": 0.0,
   }
)
```

What’s going on here?

*   These agents are essentially your AI ‘bots,’ each configured using the model information in the config\_list.

### Step 5: Create the UserProxyAgent

```


user_proxy = UserProxyAgent(
   name="user_proxy",
   human_input_mode="NEVER"
)
```

*   This UserProxyAgent acts on behalf of the human user. This is the one that sends questions or tasks to the assistant.
*   The human\_input\_mode = “NEVER” indicated that there will not be interactive user prompts in real time.

### Step 6: Run the Agent

```


story_prompt = ("Please write a short story about a brave explorer in space who encounters mysterious alien life and learns a valuable lesson about love.")
story = user_proxy.initiate_chat(
   writer_agent,
   message=story_prompt,
   max_turns=1)
feedback_prompt = ("Please review the following story and provide constructive feedback along with suggestions for improvement: "+ str(story))

feedback = user_proxy.initiate_chat(
   editor_agent,
   message=feedback_prompt,
   max_turns=1)
```

When you call user\_proxy.initiate\_chat(…), it can delegate parts of the request to the appropriate underlying agent. It’s where the actual ‘chat’ begins.

This example demonstrates a two-step process using two specialized agents—a writer and an editor. First, the user\_proxy agent asks the writer\_agent to compose a short story about a space explorer who learns a lesson on friendship. Next, it passes that story to the editor\_agent for constructive feedback and suggestions. This showcases how multiple agents can collaborate to create and refine content in a single workflow.

That’s it! By following these steps, you’ll have a basic Autogen setup where a UserProxyAgent can send messages to an AssistantAgent configured with the chosen model. You can easily extend this pattern to include multiple agents, tools, or conversation flows as your project grows.

After you’ve built your agent, track how it’s doing on Phoenix with our [AutoGen integration](https://docs.arize.com/phoenix/tracing/integrations-tracing/autogen-support).

Build an Agent Using LangGraph
------------------------------

Next up, let’s explore how quickly we can get an agent running using the LangGraph Framework. We’ll walk through the setup, configuration, and a simple example to highlight just how straightforward it can be.

### Step 1: Install the Required Libraries

```


pip install -q langchain-core langchain-community openai langchain_openai
```

### Step 2: Import all the Essential Building Blocks & Set up OpenAI

Now let’s bring in the classes and tools we’ll be using:

```


import os 
from langgraph.graph import START, END, StateGraph 
from langchain_core.messages import AIMessage, HumanMessage 
from langgraph.graph.message import add_messages 
from langchain_community.chat_models import ChatOpenAI 
from typing_extensions import TypedDict

os.environ["OPENAI_API_KEY"] = ""

```

Here’s a quick rundown of the imports:

*   We bring in classes and functions from langgraph, langchain, and typing to define and manage our workflow.

### Step 3: Define State Type & Create Workflow

```


class State(TypedDict):
   messages: list
workflow = StateGraph(State)
```

*   We create a State object that will be passed from node to node. It holds a list of messages representing the conversation history.
*   A StateGraph is the core of our workflow. We specify State as the type of data that the graph manages.

### Step 4: Helper Function for Extracting Content

```


def extract_content(response) -> str:
   return response.content if hasattr(response, "content") else str(response)
```

**What’s going on here?**

*   When the LLM returns a response, it might have different attributes. This function standardizes it to a string so we can store or process it consistently.

### Step 5: Define Nodes

We’ll have several nodes in our graph—each representing a step in our travel-planning workflow.

#### 5.1 Destination Recommender

```


def destination_node(state: State) -> dict[str, list[AIMessage]]:
   llm = ChatOpenAI(model_name="gpt-4o", temperature=0.6)
   prompt = state["messages"]
[-1].content
   response = llm.invoke(prompt)
   return {"messages": [AIMessage(content=extract_content(response))]}

workflow.add_node("destination", destination_node)
```

*   We use a GPT-4–like model (temperature 0.6) to recommend a travel destination based on the user’s prompt.
*   The output is wrapped in an AIMessage and appended to the conversation state

#### 5.2 Itinerary Builder

```


def itinerary_node(state: State) -> dict[str, list[AIMessage]]:
   llm = ChatOpenAI(model_name="gpt-4o", temperature=0.7)
   destination = state["messages"]
[-1].content
   prompt = (
       "Based on the destination recommendation below, generate a detailed 5-day itinerary for a traveler. "
       "Include daily attractions, local cuisine suggestions, and leisure activities.\n\n"
       "Destination Recommendation:\n" + destination
   )
   response = llm.invoke(prompt)
   return {"messages": [AIMessage(content=extract_content(response))]}

workflow.add_node("itinerary", itinerary_node)
```

*   We use the last message (the recommended destination) to build a prompt for a 5-day itinerary.
*   The LLM’s response is transformed into an AIMessage representing the itinerary details.

#### 5.3 Expense Estimator

```


def expense_node(state: State) -> dict[str, list[AIMessage]]:
   llm = ChatOpenAI(model_name="gpt-4o", temperature=0.0)
   itinerary = state["messages"]
[-1].content
   prompt = (
       "Based on the following 5-day itinerary, provide an approximate expense estimate for the entire trip. "
       "Consider costs such as accommodation, meals, local transportation, and activities.\n\n"
       "Itinerary:\n" + itinerary
   )
   response = llm.invoke(prompt)
   return {"messages": [AIMessage(content=extract_content(response))]}

workflow.add_node("expense", expense_node)
```

*   We take the itinerary and calculate approximate travel expenses.
*   A lower temperature (0.0) aims for more consistent, factual output.

### Step 6: Define Workflow Edges & Compile

```


workflow.add_edge(START, "destination")
workflow.add_edge("destination", "itinerary")
workflow.add_edge("itinerary", "expense")
workflow.add_edge("expense", END)

compiled_app = workflow.compile()
```

**What’s going on here?**

*   We lay out the sequence in which nodes execute.
*   The workflow starts at START, then “destination” → “itinerary” → “expense” → END.

### Step 7: Define Workflow Edges & Compile

```


workflow.add_edge(START, "destination")
workflow.add_edge("destination", "itinerary")
workflow.add_edge("itinerary", "expense")
workflow.add_edge("expense", END)

compiled_app = workflow.compile()
```

*   We lay out the sequence in which nodes execute.
*   The workflow starts at START, then “destination” → “itinerary” → “expense” → END

### Step 8: Invoke Workflow & Retrieve Final Output

```


initial_prompt = (
   "I have a budget of $3000 for a 5-day vacation. I enjoy nature, history, and trying local cuisine. I'm open to international travel in early summer. What destination would you recommend?"
)
result_state = compiled_app.invoke({"messages": [HumanMessage(content=initial_prompt)]})

final_output = result_state["messages"]
[-1].content
print(final_output)
```

That’s it! By following these steps, you’ll have a LangGraph setup where the user’s initial travel criteria flows through a sequence of nodes—destination recommendation, itinerary building, and expense estimation—all orchestrated by a single workflow. This approach is also highly scalable—you can add or remove nodes as your application grows in complexity—and easily personalized by tweaking prompts, changing model parameters, or adding custom decision logic to tailor the user experience.

Once you’ve built your agent, see how it’s doing in Phoenix with our [LangGraph Integration](https://docs.arize.com/phoenix/tracing/integrations-tracing/langgraph).

Conclusion
----------

Building an agent involves balancing simplicity and power—from single-function LLM calls all the way up to complex, multi-node workflows. Whether you’re using a lightweight framework like smolagents, leveraging structured outputs in AutoGen, or orchestrating multiple steps in LangGraph, the key lies in choosing the right abstraction for your problem. Once you’ve set up the necessary routing logic, integrated external tools, and added memory or iterative planning, you’ll have an agent that can tackle real-world tasks with minimal manual intervention. As the space evolves, keep experimenting, stay flexible, and refine your approach to deliver the best possible user experience. Happy building!

[Get started with Phoenix Tracing Integrations](https://docs.arize.com/phoenix/tracing/integrations-tracing)