id: context-001 title; Context Engineering tags; [context,prompt,memory,retrieval]

Context Engineering

Context Engineering is the process of deciding what information should be supplied to a language model for a particular task 

The model may receive context from several sources

1. User profile 
2. Current converstaion 
3. Previous learning history 
4. Retrieved documents 
5. Tool results
6. Current task instructions

Prompt Engineering vs Context Engineering

prompt enginerring fouses primarily on how instructions are written
Context engineering focuses on selecting organiizing and supplying the information needed by the model 

Context selection 
More context is not always better. 
Useful context should be:

- Relevant to the current task
- Recent enough to be applicable 
- From an appropriate source 
- Small enough to avoid unnecessary noise
Example if a learner asks: "Explain Reranking."

The system may know: 

- The learner already understands embeddings 
- The learner already understands vector search
- The learner previosuly struggled with reranking 

The model can therefore explain reranking starting from concepts the learner already understands instead of giving a generic explanation















