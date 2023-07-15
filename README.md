# Character Chat

Character-Chat is a project that aims to provide a dynamic platform to interact with large language models in the character of your choice. 
The goal of the project is to help understand the purpose and impact parameters of large language models, such as temperature, top_k, top_k, repeat_penalty etc.
The system uses the Llama Python wrapper to enable efficient serving of large language models, and the Streamlit framework for building a highly interactive user interface.
![Character Chat](character-chat.png)
## Installation

1. **Conda environment**: This project uses a conda environment for managing dependencies. If you do not have Conda installed, follow the instructions [on the conda website](https://docs.conda.io/projects/conda/en/latest/user-guide/install/). 

    Create a new conda environment named `character-chat` using the following command:

    ```
    conda create --name character-chat
    ```

    Activate the environment:

    ```
    conda activate character-chat
    ```

2. **Clone the repository**: Clone the repository by executing the following command in your terminal:

    ```
    git clone 'https://github.com/vigyanik/character-chat'
    ```

    Navigate to the cloned directory:

    ```
    cd character-chat
    ```

3. **Install the dependencies**: Execute the following command to install the required python packages:

    ```
    pip install -r requirements.txt
    ```


4. **Start the server**: In your terminal, execute the following command to start the server on port 8000:

    If you have a GPU, use the following

    ```
    python3 launch_chat.py --model <model_path> --device gpu
    ```

    If you have a Intel or AMD CPU (no GPU), use the following

    ```
    python3 launch_chat.pyt --model <model_path> --device cpu
    ```
    
    If you have a Applce Silicon (M1/M2) Mac, use the following

    ```
    python3 launch_chat.pyt --model <model_path> --device mps
    ```

    Replace `<model_path>` with the huggingface repo ID of the model.

    We recommend one of the following:
    * lmsys/vicuna-7b-v1.3
    * lmsys/vicuna-13b-v1.3     


Navigate to the URL provided in the console to interact with the application. Select a character from the list on the left and then start a conversation in the chat window. Feel free to tweak the parameters and observe their impact on the interaction.

## License

This project is subject to copyright. We are considering adding a permissive license in the future.
