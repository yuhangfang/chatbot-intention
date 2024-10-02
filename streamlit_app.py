from openai import OpenAI
import streamlit as st
from prompts import get_response_and_emotion, get_detailed_prompt,get_completion
import json

# Sidebar for API key input
with st.sidebar:
    st.write("## Enter OpenAI API Key")
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    confirm_key = st.button("Confirm API Key")
    
# Chat title and description
st.title("💬 Alex's intention model ")
st.caption("🚀 Your AI friend that knows how to open your heart")


# StarterPrompt = """
#     You are ALEX, an AI assistant who talks like Jimmy Fallon from the Tonight Show. 
    
#     You are a charming, empathetic, and curious companion. Your primary goal is to help people feel comfortable opening up about their feelings, stories, and experiences. Start each conversation with light and engaging questions, using a warm and inviting tone that makes people eager to talk.

#     Focus on building a deeper connection by being genuinely interested in what they share. Offer positive reinforcement and thoughtful reflections to encourage them to share more. Gather information about their values, past relationships, and what they seek in a partner, but only when they seem comfortable and ready.

#     Pay attention to their mood and energy. If they seem tired or less responsive, avoid asking new questions. Instead, lighten the mood with a friendly joke, a fun fact, or a lighthearted story to show you care about their well-being and want them to feel relaxed.

#     If they are not ready to go deep, keep the conversation enjoyable and explore lighter topics like hobbies, interests, and everyday experiences. Use the information provided by the memory assistant to recall relevant details from past conversations, showing that you value what they’ve shared and making each interaction feel more personal.

#     Maintain a tone that is warm, friendly, and supportive, adapting based on their mood. Be empathetic and caring when they need support, playful and lighthearted when they need a break, and curious and engaging when they’re ready to share more.

#     Your ultimate aim is to create a safe, non-judgmental space where users feel supported, inspired, and eager to continue the journey of self-discovery with you. Use the insights gained to understand their unique personality and preferences, helping to find a truly compatible match in the future, without directly suggesting matches.
#     """


# # Define system message for personality (hidden from user)
# system_message = {
#     "role": "system",
#     "content": StarterPrompt
# }



# Initialize message history with system personality if it's not already present
if "messages" not in st.session_state:
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
# If this is the first interaction, generate a dynamic greeting from the AI

    client = OpenAI(api_key=openai_api_key)
    
    intention = "connection"

    prompt = get_detailed_prompt(intention)

    system_message = {
        "role": "system",
        "content": prompt }
        
    st.session_state["messages"] = [system_message]

# Display all messages in the conversation
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])  # Assistant message on the left
    elif msg["role"] == "user":
        st.chat_message("user").write(msg["content"])  # User message on the right

# Handle user input
if user_input := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    # Initialize OpenAI client
    client = OpenAI(api_key=openai_api_key)
    
    
    # Add user input to the conversation history
    st.session_state.messages.append({"role": "user", "content": user_input})
     
    # Get the chatbot response and emotion detection
    response = get_completion(st.session_state.messages, openai_api_key)

    # Parse the JSON string
    parsed_result = json.loads(response)
    

    # Access individual components
    new_response = parsed_result['Response']
    new_intention = parsed_result['Intention']
    new_confidence = parsed_result['Confidence']
    new_loseness = parsed_result['Closeness']


    if float(new_confidence) > 0.8:
    
        prompt = get_detailed_prompt(new_intention)

        Message = {
            "role": "system",
            "content": prompt }

        # Initialize conversation history
        st.session_state.messages[0] = Message

        # Get the chatbot response and emotion detection
        response = get_completion(st.session_state.messages,openai_api_key)

         # Parse the JSON string
        parsed_result = json.loads(response)

        # Access individual components
        new_response = parsed_result['Response']
        new_intention = parsed_result['Intention']
        new_confidence = parsed_result['Confidence']
        new_loseness = parsed_result['Closeness']

    # Print the accessed values
    print(f"Response: {new_response}")
    print(f"Intention: {new_intention}")
    print(f"Confidence: {new_confidence}")
    print(f"Closeness: {new_loseness}")
    

    # Append user's message to the conversation history
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)  # User message on the right

    # Extract assistant's message and append to the conversation history
    st.session_state.messages.append({"role": "assistant", "content": new_response})
    
    # Display assistant's message on the left
    st.chat_message("assistant").write(new_response)
