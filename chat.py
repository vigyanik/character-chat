import streamlit as st
import requests
import json
import pprint
import sys
import openai

import argparse

# Define the argument parser
parser = argparse.ArgumentParser(description='Provide your host, port and model')

# Define arguments
parser.add_argument('--host', type=str, default='localhost', help='Host to use; default is localhost.')
parser.add_argument('--port', type=int, default=5001, help='Port to use; default is 5001.')
parser.add_argument('--model', type=str, required=True, help='Model to use; must be provided.')

# Parse arguments
args = parser.parse_args()

openai.api_base = f"http://{args.host}:{args.port}/v1"
openai.api_key = "sk-111111111111111111111111111111111111111111111111"
MODEL = f"{args.model}"

with open('characters.json') as f:
  characters = json.load(f)



def prompt(messages, params):
    data = {"messages": messages, "model": MODEL, **params} #"params": params}
    headers = {'Content-type': 'application/json'}
    pprint.pprint(data)
    response = requests.post(URL, data=json.dumps(data), headers=headers)
    pprint.pprint(response.json())
    if response.status_code == 200:
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
st.title('Character Chat')
# Show the list of characters.
st.sidebar.header('Characters')
character_name = st.sidebar.selectbox('Character', character_list, key="character_name", on_change = reset_messages)
st.sidebar.write('You selected:', character_name)

parameters = {
 # "max_new_tokens": {"data_type": "int_range", "default": 2048, "min": 1, "max": 2048, "group": "all"},
  "max_tokens": {"data_type": "int_range", "default": 1024, "min": 1, "max": 1024, "group": "all"},
 # "early_stopping": {"data_type": "option", "default": False, "options": {"False": False, "True": True, "never": "never"}, "group": "all"},
 # "num_beams": {"data_type": "int_range", "default": 1, "min": 1, "max": 5, "group": "all"},
 # "num_beam_groups": {"data_type": "int_range", "default": 1, "min": 1, "max": 5, "group": "all"},
  "temperature": {"data_type": "float_range", "default": 1.0, "min": 0.0, "max": 5.0, "group": "all"},
  "top_k": {"data_type": "int_range", "default": 40, "min": 1, "max": 100, "group": "all"},
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
      full_response = ""
      params = {}
      for param_name, param_value in parameters.items():
        if param_value["data_type"] == "int_range" or param_value["data_type"] == "float_range":
          params[param_name] = widget_value[param_name]
        elif param_value["data_type"] == "option":
          params[param_name] = param_value["options"][widget_value[param_name]]
      pprint.pprint(params)
      for response in openai.ChatCompletion.create(
        model=MODEL,
        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        stream=True):
        full_response += response.choices[0].delta.get("content", "")
        message_placeholder.markdown(full_response + "▌")
  st.session_state.messages.append({"role": "assistant", "content": full_response})

      #full_message = prompt(st.session_state.messages, params)
      #message_placeholder.markdown(full_message["content"])
  #st.session_state.messages.append(full_message)
