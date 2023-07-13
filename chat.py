import streamlit as st
import requests
import json
import pprint

URL = "http://0.0.0.0:8000/v1/chat/completions"

MODEL = "stable-vicuna-13B.ggmlv3.q8_0"

characters = [
  {"name": "News Article Summarizer", "temperature": 0.7, "top_k": 40, "repitition_penalty": 1.2, "prompt": "Analyze the provided news article and generate a summary that includes the headline, key points, significant quotes, and conclusions. Ensure the summary is concise, comprehensive, and maintains the context and tone of the original piece."},
  {"name": "Interactive Storytelling Game", "temperature": 1.0, "top_p": 0.9, "repitition_penalty": 1.1, "prompt": "Continue the narrative from the last saved plot point. Consider the characters' personalities, past decisions, and the game's universe rules. Introduce engaging dialogues, conflicts, and plot twists to keep the player immersed. Maintain the consistency of the story world."},
  {"name": "Customer Support Chatbot", "temperature": 0.5, "top_k": 20, "repitition_penalty": 2, "prompt": "Reply to the customer's inquiries accurately, using a courteous and professional tone. If you're asked about product specifications, provide detailed and relevant information. For troubleshooting issues, offer step-by-step solutions. Remember to empathize with the customer's situation and assure them of your assistance."},
  {"name": "Creative Writing Assistant", "temperature": 1.2, "top_p": 0.95,"repitition_penalty": 1, "prompt": "Generate creative ideas and suggestions based on the current narrative, characters, and themes. Offer alternative plot developments, character interactions, or narrative devices. If the user is facing writer's block, provide prompts or scenarios to ignite their creativity. Always respect the original tone and style of the writing."},
  {"name": "Coding Assistant", "temperature": 0.2, "top_k": 5, "repitition_penalty": 1.5, "prompt": "Provide relevant code suggestions to accomplish the user's goal. If errors are present, explain what they are and offer fixes. Suggest improvements or best practices to optimize the code. Ensure your advice is in line with the language's syntax rules and the user's coding style."},
  {"name": "Language Learning Tool", "temperature": 0.6, "top_k": 30, "repitition_penalty": 1.2, "prompt": "Provide clear explanations of the given language concept, ensuring they are understandable for a beginner. Offer examples that demonstrate this concept in real language use. If it's a grammar rule, demonstrate it in a variety of sentences. Provide practice exercises and correct mistakes, offering explanations for your corrections."},
  {"name": "Product Recommendation Engine", "temperature": 0.9, "top_p": 0.85, "repitition_penalty": 1.2, "prompt": "Analyze the user's past purchases, browsing history, and declared interests. Recommend products that align with these factors, providing a balance between new discoveries and their preferences. If the user has a wish list, consider the items in it. Explain why you recommend each product to make the suggestions more persuasive and personalized."},
  {"name": "Medical Diagnosis Assistant", "temperature": 0.3, "top_k": 10, "repitition_penalty": 1.5, "prompt": "Consider the patient's reported symptoms, their medical history, and any risk factors they have. Provide a likely diagnosis and explain it in layman's terms. Suggest appropriate next steps, such as tests to confirm the diagnosis, potential treatment options, or lifestyle changes. Remind the patient to consult a healthcare professional for a final diagnosis and treatment."},
  {"name": "Market Trend Prediction System", "temperature": 0.7, "top_p": 0.8, "repitition_penalty": 1.3, "prompt": "Examine the current market data, including price movements, trading volume, and news events. Identify patterns that suggest upcoming trends. Use reliable prediction models to forecast market behavior. Suggest potential investment opportunities but remind the user that all investments come with risks."},
  {"name": "Legal Document Reviewer", "temperature": 0.4, "top_k": 15, "repitition_penalty": 1.2, "prompt": "Review the provided legal document, paying attention to terminology, clause structure, and legality. Identify potential issues, such as conflicts with other laws or regulations, ambiguous statements, or loopholes. Suggest revisions to resolve these issues. Provide a summary of the document's key points and its implications for the user."},


]



def prompt(messages, params):
    data = {"messages": messages, "model": MODEL, **params} #"params": params}
    headers = {'Content-type': 'application/json'}
    pprint.pprint(data)
    response = requests.post(URL, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
      pprint.pprint(response.json())
      return response.json()["choices"][0]["message"]
    else:
      return "Error:", response.status_code


character_list = []
character_name_to_params = {}
for character in characters:
  character_list.append(character["name"])
  character_name_to_params[character["name"]] = character

def dict_to_markdown_table(data):
    markdown_table = ''

    # Write headers
    headers = '|'.join([''] + list(data.keys()) + [''])
    markdown_table += headers + '\n'
    
    # Write line below headers
    header_line = '|'.join([''] + ['---']*len(data.keys()) + [''])
    markdown_table += header_line + '\n'
    
    # Write data
    #num_rows = len(data[list(data.keys())[0]])
    #for i in range(num_rows):
    row_data = '|'.join([''] + [str(data[key]) for key in data.keys()] + [''])
    markdown_table += row_data + '\n'
    
    return markdown_table

def reset_messages():
  st.session_state.messages = [{"role":"system", "content": character_name_to_params[st.session_state.character_name]["prompt"]}]
  st.markdown(dict_to_markdown_table(character_name_to_params[st.session_state.character_name]))

# Render the app.
st.title('Chat App')
# Show the list of characters.
st.sidebar.header('Characters')
character_name = st.sidebar.selectbox('Character', character_list, key="character_name", on_change = reset_messages)
st.sidebar.write('You selected:', character_name)

parameters = {
 # "max_new_tokens": {"data_type": "int_range", "default": 2048, "min": 1, "max": 2048, "group": "all"},
  "max_tokens": {"data_type": "int_range", "default": 2048, "min": 1, "max": 2048, "group": "all"},
 # "early_stopping": {"data_type": "option", "default": False, "options": {"False": False, "True": True, "never": "never"}, "group": "all"},
 # "num_beams": {"data_type": "int_range", "default": 1, "min": 1, "max": 5, "group": "all"},
 # "num_beam_groups": {"data_type": "int_range", "default": 1, "min": 1, "max": 5, "group": "all"},
  "temperature": {"data_type": "float_range", "default": 1.0, "min": 0.0, "max": 5.0, "group": "all"},
  "top_k": {"data_type": "int_range", "default": 40, "min": 1, "max": 1000, "group": "all"},
  "top_p": {"data_type": "float_range", "default": 0.95, "min": 0.0, "max": 1.0, "group": "all"},
 # "typical_p": {"data_type": "float_range", "default": 1.0, "min": 0.0, "max": 1.0, "group": "all"},
 # "epsilon_cutoff": {"data_type": "float_range", "default": 0.0, "min": 0.0, "max": 1.0, "group": "all"},
 # "eta_cutoff": {"data_type": "float_range", "default": 0.0, "min": 0.0, "max": 1.0, "group": "all"},
 # "repetition_penalty": {"data_type": "float_range", "default": 1.0, "min": 0.0, "max": 1.0, "group": "all"},
   "repeat_penalty": {"data_type": "float_range", "default": 1.1, "min": 0.0, "max": 3.0, "group": "all"},
 # "length_penalty": {"data_type": "float_range", "default": 1.0, "min": -5.0, "max": 5.0, "group": "all"},
 # "penalty_alpha": {"data_type": "float_range", "default": 0.0, "min": 0.0, "max": 1.0, "group": "all"}
}
widget_value = {}
for param_name, param_value in parameters.items():
  print("param_name:", param_name)
  if param_value["data_type"] == "int_range" or param_value["data_type"] == "float_range":
    value = param_value["default"]
    if param_name in character_name_to_params[st.session_state.character_name]:
      value = character_name_to_params[st.session_state.character_name][param_name]
    widget_value[param_name] = st.sidebar.slider(param_name, value = value, min_value = param_value["min"],
                                           max_value = param_value["max"])
    st.sidebar.write("Value:", widget_value[param_name])
  elif param_value["data_type"] == "option":
    option_val_names = []
    for option in param_value["options"]:
      option_val_names.append(option)
    widget_value[param_name] = st.sidebar.radio(param_name, option_val_names)
    st.sidebar.write("Value:", widget_value[param_name])

  
if "messages" not in st.session_state:
    reset_messages()

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# Show the chat area
if message := st.chat_input('Say something'):
  st.session_state.messages.append({"role": "user", "content": message})
  with st.chat_message("user"):
    st.markdown(message)
  with st.chat_message("assistant"):
      message_placeholder = st.empty()
      params = {}
      for param_name, param_value in parameters.items():
        if param_value["data_type"] == "int_range" or param_value["data_type"] == "float_range":
          params[param_name] = widget_value[param_name]
        elif param_value["data_type"] == "option":
          params[param_name] = param_value["options"][widget_value[param_name]]
      pprint.pprint(params)
      full_message = prompt(st.session_state.messages, params)
      message_placeholder.markdown(full_message["content"])
  st.session_state.messages.append(full_message)
