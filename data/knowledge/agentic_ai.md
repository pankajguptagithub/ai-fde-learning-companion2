id: agentic-001 title: Agentic AI tags: [ agent, tools, reasoning, workflow] 

Agentic AI 

Agentic AI systems use language models together with tools, states and workflow logic to perform multi step task. 
A typical agentic workflow is:

1. Receive a goal or task
2. Determine the next action 
3. Select an appropriate tool when required
4. Execute the tool 
5. Observer the result 
6. Whether another action is required 
7. Continue until a stopping condition is reached 

Tools

Tools allow an agent to interact with capabilities outside the language model
Examples include: 

- Retrieving a learner profile 
- Searching a knowledge base
- Saving a learning attempt
- Calling an external API

State 

State contains information required across different steps of the workflow.
Examples: 

- Current topic
- Number of attempts 
- Previous answer
- Evaluation score
- Retrieved evidence

Agent Loop
An agent may operate through a loop:

Goal -> decides -> Act -> Observe -> Decide again -> Stop

The loop must have clear stopping conditions to prevent uncontrolled execution.

Agent verses model
Al naguage model primarily generates outputs from inputs.
An agent uses a model inside a larger system that can maintain state, select tools, executes action, observer results, and continue working towards a defined goal










