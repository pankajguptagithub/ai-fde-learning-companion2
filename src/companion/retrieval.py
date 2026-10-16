import re

from pathlib import Path

KNOWLEDGE_DIR = Path("data/knowledge")

STOP_WORDS = {
    "what","is","in","the","a","an","of","to","and","for","how"
}
def tokenize(text: str) -> set[str]:
    """Convert text into normalized searchable words"""
    words = set(re.findall(r"[a-z0-9]+", text.lower()))
    return words - STOP_WORDS

def load_documents() -> list[dict]:
    """Load all Markdown files from the knowledge directory."""

    documents = []

    for file_path in KNOWLEDGE_DIR.glob("*.md"):
        text = file_path.read_text(encoding="utf-8")

        documents.append(
            {
                "id": file_path.stem,
                "text": text,
                "source": file_path.name,
                }    

         )
    return documents 

def lexical_search(
    query: str,
    documents: list[dict],
    k: int = 3,
) -> list[dict]:

    """Return documents having the highest word overlap with the query."""

    query_tokens = tokenize(query)

    scored_documents = []

    for document in documents:
        document_tokens = tokenize(document["text"])
        score = len(query_tokens & document_tokens)
#        print(
#                document["source"],
#                "matches =",
#                query_tokens & document_tokens
#            )

        if score > 0:
            scored_documents.append(
                (score, document)
            )

    scored_documents.sort(
        key = lambda item: item[0],
        reverse=True
    )

    return [
        document
        for score, document in scored_documents[:k]
    ]


def retrieve(query: str, k: int = 3) -> list[dict]:
    """Main retrieval function used by the application."""

    documents = load_documents()

    return lexical_search(
        query=query,
        documents=documents,
        k=k,
    )
