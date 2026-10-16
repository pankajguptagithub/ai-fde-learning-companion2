id: rag-001 title: Retrieval AUgmented Generation tags; [rag, retrieval, generation]

Retrieval Augmented Generation

Retrieval Augmented Generation (RAG) combines information retrieval with language model generation 

A typical RAG flow is: 

1. A user submits a query
2. Relevant information is retrieved from an extgernal knowledge source 
3. The retrieved information is added to the model's context
4. The language model generated an answer using that context 

RAG helps an application answer questiosn usign information that was not necessarrily contained in the model's original training data

Retrieval

Retrieval identifies information relevant to the user's query

Generation 

Generates uses the retrieved information as context while producting the final answer.

Rerantking

reransking is an optional stage afteri nitial retrieval. 

The initial retriever may return several candidate documents or chunks. A reranker applies another relevance assessment to these candeidates and reorders them so that the most relevant information can be prioritized for the model. 
