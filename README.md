# AIConsole

AIConsole is a command-line interface tool designed for managing various components of OpenAI, such as vector stores and assistants. With AIConsole, users can create, update, list, and delete vector stores; manage assistants; handle conversation threads and messages; and execute runs for result capture and display.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
  - [Local project](#project)
  - [Store](#store)
  - [Assistant](#assistant)
  - [Thread](#thread)
  - [Message](#message)
  - [Run](#run)
- [Contributing](#contributing)
- [License](#license)


## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/roke75/AIConsole.git
    ```

2. Change to the project directory:

    ```bash
    cd AIConsole
    ```

3. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

4. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Set up environment variables:

    Create a `.env` file in the root directory and add the required environment variables:

    ```env
    OPENAI_API_KEY=your_openai_api_key_here
    ```

## Usage

Use "--help" or "-h" after command to get help for each command.
See https://platform.openai.com/docs/api-reference/introduction for more details.

```bash
python main.py --help
```
```bash
python main.py store --help
```
```bash
python main.py store list --help
```
```bash
python main.py store list --limit 10 --order asc
```

### Example commands

#### Local projects

- **Create Project:**

    ```bash
    python main.py project create --name "Example Project" --instructions "You are helpfull senior Python developer." --model "gpt-4o"
    ```

- **List Projects:**

    ```bash
    python main.py project list
    ```

- **Add file(s) to project:**

    ```bash
    python main.py project files add --project_id "project_id"  --files platforms/openai/*.py
    ```

- **Delete file(s) from project:**

    ```bash
    python main.py project files delete --project_id "project_id"  --all --permanently
    ```

- **Ask Question:**

    ```bash
    python main.py project ask --project_id "project_id" --question "Is there any bugs in the code?"
    ```

#### Store

- **Create Store:**

    ```bash
    python main.py store create --name "Example Store"
    ```
    See more: https://platform.openai.com/docs/api-reference/vector-stores/create

- **List Stores:**

    ```bash
    python main.py store list
    ```
    See more: https://platform.openai.com/docs/api-reference/vector-stores/list

- **Retrieve Store:**

    ```bash
    python main.py store retrieve --store_id "store_id"
    ```
    See more: https://platform.openai.com/docs/api-reference/vector-stores/retrieve

- **Modify Store:**

    ```bash
    python main.py store modify --store_id "store_id" --name "new_store_name"
    ```
    See more: https://platform.openai.com/docs/api-reference/vector-stores/modify

- **Delete Store:**

    ```bash
    python main.py store delete --store_id "store_id"
    ```
    See more: https://platform.openai.com/docs/api-reference/vector-stores/delete

- **Create File to Store:**

    ```bash
    python main.py store files create --store_id "store_id" --file_id "file_id"
    ```
    See more: https://platform.openai.com/docs/api-reference/vector-stores-files/createFile

- **List Files in Store:**

    ```bash
    python main.py store files list --store_id "store_id"
    ```
    See more: https://platform.openai.com/docs/api-reference/vector-stores-files/listFiles

- **Retrieve File from Store:**

    ```bash
    python main.py store files retrieve --store_id "store_id" --file_id "file_id"
    ```
    See more: https://platform.openai.com/docs/api-reference/vector-stores-files/getFile

- **Delete File from Store:**

    ```bash
    python main.py store files delete --store_id "store_id" --file_id "file_id"
    ```
    See more: https://platform.openai.com/docs/api-reference/vector-stores-files/deleteFile

- **Upload File(s) to Store:**

    ```bash
    python main.py store files add --store_id "store_id" --files "file_path_1" "file_path_2" "file_path_3"
    ```
- **Upload Directory to Store:**

    ```bash
    python main.py store files add --store_id "store_id" --directory "directory_path" --recursive
    ```

#### Assistant

- **Create Assistant:**

    ```bash
    python main.py assistant create --model "gpt-4o" --name "Example Assistant" --description "An example assistant" --instructions "instructions text"
    ```
    See more: https://platform.openai.com/docs/api-reference/assistants/createAssistant

- **List Assistants:**

    ```bash
    python main.py assistant list
    ```
    See more: https://platform.openai.com/docs/api-reference/assistants/listAssistants

- **Retrieve Assistant:**

    ```bash
    python main.py assistant retrieve --assistant_id "assistant_id"
    ```
    See more: https://platform.openai.com/docs/api-reference/assistants/getAssistant

- **Modify Assistant:**

    ```bash
    python main.py assistant modify --assistant_id "assistant_id" --name "New assistant name" --description "New description"
    ```
    See more: https://platform.openai.com/docs/api-reference/assistants/modifyAssistant

- **Delete Assistant:**

    ```bash
    python main.py assistant delete --assistant_id "assistant_id"
    ```
    See more: https://platform.openai.com/docs/api-reference/assistants/deleteAssistant

#### Thread

- **Create Thread:**

    ```bash
    python main.py thread create
    ```
    See more: https://platform.openai.com/docs/api-reference/threads/createThread

- **Retrieve Thread:**

    ```bash
    python main.py thread retrieve --thread_id "thread_id"
    ```
    See more: https://platform.openai.com/docs/api-reference/threads/getThread

- **Modify Thread:**

    ```bash
    python main.py thread modify --thread_id "thread_id" --tool_resources '{"resource": "new_resource"}'
    ```
    See more: https://platform.openai.com/docs/api-reference/threads/modifyThread

- **Delete Thread:**

    ```bash
    python main.py thread delete --thread_id "thread_id"
    ```
    See more: https://platform.openai.com/docs/api-reference/threads/deleteThread

#### Message

- **Create Message:**

    ```bash
    python main.py message create --thread_id "thread_id" --role user --content "This is a message content."
    ```
    See more: https://platform.openai.com/docs/api-reference/messages/createMessage

- **List Messages:**

    ```bash
    python main.py message list --thread_id "thread_id"
    ```
    See more: https://platform.openai.com/docs/api-reference/messages/listMessages
- **Retrieve Message:**

    ```bash
    python main.py message retrieve --thread_id "thread_id" --message_id "message_id"
    ```
    See more: https://platform.openai.com/docs/api-reference/messages/getMessage

- **Modify Message:**

    ```bash
    python main.py message modify --thread_id "thread_id" --message_id "message_id" --metadata '{"key": "value"}'
    ```
    See more: https://platform.openai.com/docs/api-reference/messages/modifyMessage

- **Delete Message:**

    ```bash
    python main.py message delete --thread_id "thread_id" --message_id "message_id"
    ```
    See more: https://platform.openai.com/docs/api-reference/messages/deleteMessage

#### Run

- **Create Run:**

    ```bash
    python main.py run create --thread_id "thread_id" --assistant_id "assistant_id"
    ```
    See more: https://platform.openai.com/docs/api-reference/runs/createRun

- **Create Thread and Run:**

    ```bash
    python main.py run create_thread_and_run --assistant_id "assistant_id" --thread '{"messages": [{"role": "user", "content": "Explain the meaning of life"}]}'
    ```
    See more: https://platform.openai.com/docs/api-reference/runs/createThreadAndRun

- **List Runs:**

    ```bash
    python main.py run list --thread_id "thread_id"
    ```
    See more: https://platform.openai.com/docs/api-reference/runs/listRuns

- **Retrieve Run:**

    ```bash
    python main.py run retrieve --thread_id "thread_id" --run_id "run_id"
    ```
    See more: https://platform.openai.com/docs/api-reference/runs/getRun

- **Modify Run:**

    ```bash
    python main.py run modify --thread_id "thread_id" --run_id "run_id" --metadata '{"key": "value"}'
    ```
    See more: https://platform.openai.com/docs/api-reference/runs/modifyRun

- **Submit Tool Outputs:**

    ```bash
    python main.py run submit_tool_outputs --thread_id "thread_id" --run_id "run_id" --tool_outputs '{"output": "data"}'
    ```
    See more: https://platform.openai.com/docs/api-reference/runs/submitToolOutputs

- **Cancel Run:**

    ```bash
    python main.py run cancel --thread_id "thread_id" --run_id "run_id"
    ```
    See more: https://platform.openai.com/docs/api-reference/runs/cancelRun

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.