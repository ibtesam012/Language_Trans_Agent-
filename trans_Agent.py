import os #environment variable ka function ko import kara Ga.!
from dotenv import load_dotenv #env sa secret  keys load karta ha 
import chainlit as cl #chat user interface
from litellm import completion #llm ko promopt bhej kar reponse lana ka lia.
import json #Program ka modules ko read & write ka lia!
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is missing in .env")
@cl.on_chat_start #ya function jab user chat open karta ha tab run hota ha 
async def on_chat_start():
    # Add a system prompt to ensure only translations
    initial_history = [
        {
            "role": "system",
            "content": (
                "You are a translation assistant. Only translate the text given by the user "
                "into the target language they specify. Never mention that you are an AI, "
                "ChatGPT, or talk about yourself."
            )
        }
        ]
    cl.user_session.set("chat_history", initial_history) #chat ki pori history session ma store hoti ha
    await cl.Message(
        content="Welcome to the **Translator Agent By IBTESAM HUSSAIN SHAH**!\n\n"
                "Please tell me **what you want to translate** and **into which language?**"
    ).send()
@cl.on_message #ya function har user message par chalata ha 
async def on_message(message: cl.Message): 
    msg = cl.Message(content="Translating.......!")
    await msg.send() #ya function user ko bata ha ka translation ho rahi ha  
    history = cl.user_session.get("chat_history") or []
    history.append({"role": "user", "content": message.content})#user ka msg history ma add hota ha 
    try:
        response = completion(
            model="gemini/gemini-2.5-flash",
            api_key=gemini_api_key,
            messages=history
        )
        # Extract the assistant reply
        response_content = response.choices[0].message["content"]
        # Update the message in the chat UI
        msg.content = response_content
        await msg.update()
        # Append to history
        history.append({"role": "assistant", "content": response_content})
        cl.user_session.set("chat_history", history)
    except Exception as e: #ager koi error aaye to user ko error dikhaya jata ha
        msg.content = f"Error: {str(e)}"
        await msg.update() 
@cl.on_chat_end
async def on_chat_end():
    history = cl.user_session.get("chat_history") or []
    with open("translation_chat_history.json", "w") as f: #pori chat json file ma save ho jati ha!!
        json.dump(history, f, indent=2)
    print("Chat history saved")
# python -m chainlit run trans_Agent.py 
