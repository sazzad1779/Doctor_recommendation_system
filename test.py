from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
load_dotenv(override=True)
model = init_chat_model(model="gemini-2.0-flash",model_provider="google_genai")
print(model.invoke("what is your name?"))