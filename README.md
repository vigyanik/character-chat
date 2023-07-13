# Character Chat

Character-Chat is a project that aims to provide a dynamic platform to interact with large language models in the character of your choice. The system uses the Llama C++ Python wrapper to enable efficient serving of large language models, and the Streamlit framework for building a highly interactive user interface.

## Installation

1. **Conda environment**: This project uses a conda environment for managing dependencies. If you do not have Conda installed, follow the instructions [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/). 

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

4. **Install llama-cpp-python**: The `llama-cpp-python` library is a Python wrapper around the Llama C++ library for serving large language models. Install it from PyPI (requires a C compiler):

    ```
    pip install llama-cpp-python
    ```

    The source code and additional installation information can be found [here](https://github.com/abetlen/llama-cpp-python).

## Download the model

We recommend one of the models from [here](https://huggingface.co/TheBloke/Wizard-Vicuna-13B-Uncensored-GGML).

1. Select the model you want to use and download the corresponding `.bin` file by clicking on the 'Download' button.
2. Save the model file in a location of your choice.

## Run the application

1. **Start the server**: In your terminal, execute the following command to start the server on port 8000:

    ```
    python3 -m llama_cpp.server --model <path_to_model_bin_file>
    ```

    Replace `<path_to_model_file>` with the path of the downloaded model bin file.

2. **Start the Streamlit app**: Open another terminal window and navigate to the directory containing `chat.py`. Execute the following command to start the Streamlit app:

    ```
    streamlit run ./chat.py
    ```

Navigate to the URL provided in the console to interact with the application. Select a character from the list on the left and then start a conversation in the chat window. Feel free to tweak the parameters and observe their impact on the interaction.

## License

This project is subject to copyright. We are considering adding a permissive license in the future.
