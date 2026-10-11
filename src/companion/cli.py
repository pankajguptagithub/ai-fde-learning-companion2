from companion.model import ask_model

if __name__ == "__main__":
    topic = input("Topic: ").strip()
    print(ask_model(f"Teach me {topic}."))
