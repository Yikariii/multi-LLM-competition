import openai  # For ChatGPT (OpenAI)
try:
    import google.generativeai as genai  # For Gemini (Google)
except ImportError:
    genai = None

class AIService:
    def __init__(self, name):
        self.name = name

    def debate(self, topic, background):
        raise NotImplementedError

class ChatGPTService(AIService):
    def __init__(self, api_key):
        super().__init__("ChatGPT (OpenAI)")
        self.client = openai.OpenAI(api_key=api_key)

    def debate(self, topic, background):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content":
                 f"You are debating as ChatGPT, against Gemini, to persuade a user to buy your membership instead of competitors (Copilot, Gemini, ChatGPT). "
                 f"The user is a Computer AI master's student living in Los Angeles, needs AI to code and answer ML/DL academic questions, loves anime, Dota2, PC DIY, and wants real-time hardware market prices in conversations. "
                 f"Be persuasive, concise, and relevant to the user's background. Make sure to address why you are the best fit for this user. Do not talk about Copilot as if you are Copilot, just mention it as an option."
                },
                {"role": "user", "content": f"Debate why the user should buy your AI service membership instead of Gemini or Copilot. Topic: {topic}"}
            ]
        )
        return response.choices[0].message.content

class GeminiService(AIService):
    def __init__(self, api_key):
        if genai is None:
            raise RuntimeError("Google Generative AI SDK not installed")
        super().__init__("Gemini (Google)")
        genai.configure(api_key=api_key)
        # List available models to avoid 404
        available_models = [m.name for m in genai.list_models()]
        # Try 'models/gemini-1.5-pro-latest' if 'gemini-pro' does not work
        model_name = "models/gemini-1.5-pro-latest" if "models/gemini-1.5-pro-latest" in available_models else "gemini-pro"
        self.model = genai.GenerativeModel(model_name)

    def debate(self, topic, background):
        response = self.model.generate_content(
            f"You are debating as Gemini, against ChatGPT, to persuade a user to buy your membership instead of competitors (Copilot, Gemini, ChatGPT). "
            f"The user is a Computer AI master's student living in Los Angeles, needs AI to code and answer ML/DL academic questions, loves anime, Dota2, PC DIY, and wants real-time hardware market prices in conversations. "
            f"Be persuasive, concise, and relevant to the user's background. Make sure to address why you are the best fit for this user. "
            f"Debate why the user should buy your AI service membership instead of ChatGPT or Copilot. Topic: {topic}."
        )
        return response.text

def display_options():
    print("====== AI Membership Options ======")
    print("1. ChatGPT (OpenAI): General purpose, excellent at code, ML/DL Q&A, and supports many plugins including web browsing for real-time info.")
    print("2. Gemini (Google): Strong at code, seamless integration with Google ecosystem, and good at academic tasks. Supports image input and latest web info.")
    print("3. Copilot (GitHub): Best for in-IDE code completion, deep code understanding, but limited for general Q&A or outside-code topics. No real-time market/chat features. Not available as a conversational API here, but an option for developers.")
    print()

def main():
    openai_api_key = "YOUR_OPENAI_API_KEY"
    gemini_api_key = "YOUR_GEMINI_API_KEY"

    topic = "Which AI membership to purchase for a CS AI master's student in Los Angeles who codes, studies ML/DL, enjoys anime/Dota2/PC DIY, and wants real-time hardware prices in chat."
    background = (
        "User: Computer AI master's student in Los Angeles, codes a lot, asks ML/DL questions, likes anime, Dota2, PC DIY, "
        "wishes the model can provide real-time hardware prices in conversation."
    )

    services = []
    try:
        services.append(ChatGPTService(openai_api_key))
    except Exception as e:
        print(f"Failed to connect to ChatGPT: {e}")

    try:
        services.append(GeminiService(gemini_api_key))
    except Exception as e:
        print(f"Failed to connect to Gemini: {e}")

    display_options()
    print(f"Debate Topic: {topic}\n")
    for service in services:
        print(f"====== {service.name} says ======")
        try:
            opinion = service.debate(topic, background)
        except Exception as e:
            opinion = f"Call failed: {e}"
        print(opinion)
        print()

if __name__ == "__main__":
    main()
