# AIConsole

AIConsole is a command-line interface tool designed for managing various components of OpenAI, such as vector stores and assistants. With AIConsole, users can create, update, list, and delete vector stores; manage assistants; handle conversation threads and messages; and execute runs for result capture and display.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
  - [Vector Store Management](#vector-store-management)
  - [Assistant Management](#assistant-management)
  - [Thread and Message Management](#thread-management)
  - [Message Management](#message-management)
  - [Run Management](#run-management)
- [Contribution](#contribution)
- [License](#license)

## Installation

To install AIConsole, clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/roke75/AIConsole.git
cd AIConsole
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Create .env file with the following contents:
```bash
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
```

## Usage

### Vector Store Management

- **List Vector Stores:**
  ```bash
  python main.py store list
  ```

- **Create Vector Store:**
  ```bash
  python main.py store create --name <store_name>
  ```

- **Retrieve Vector Store:**
  ```bash
  python main.py store retrieve --store_id <store_id>
  ```

- **modify Vector Store:**
  ```bash
  python main.py store modify --store_id <store_id> --name <store_name> --expires_after <expires_after> --metadata <metadata>
  ```

- **Delete Vector Store:**
  ```bash
  python main.py store delete --store_id <store_id>
  ```

- **Create File to Vector Store:**
  ```bash
  python main.py store files create --store_id <store_id> --file_id <file_id> --chunking_strategy <chunking_strategy>
  ```

- **Retrieve File from Vector Store:**
  ```bash
  python main.py store files retrieve --store_id <store_id> --file_id <file_id>
  ```

- **List Files in Vector Store:**
  ```bash
  python main.py store files list --store_id <store_id>
  ```

- **Upload File(s) to Vector Store:**
  ```bash
  python main.py store files add --store_id <store_id> --files <file_path_1> <file_path_2> ... <file_path_n>
  ```

  **Upload Directory to Vector Store:**
  ```bash
  python main.py store files add --store_id <store_id> --directory <directory_path> --recursive
  ```

  **Delete File(s) from Vector Store:**
  ```bash
  python main.py store files delete --store_id <store_id> (--all) (--permanently) --file_ids <file_id_1> <file_id_2> ... <file_id_n>
  ```

### Assistant Management

- **Create Assistant:**
  ```bash
  python main.py assistant create --name <assistant_name> --instructions <instructions> --model <model> --type <type> --store <store_id>
  ```

- **Retrieve Assistant:**
  ```bash
  python main.py assistant retrieve --id <assistant_id>
  ```

- **List Assistants:**
  ```bash
  python main.py assistant list
  ```

- **Update Assistant:**
  ```bash
  python main.py assistant update --id <assistant_id> --name <new_assistant_name> --instructions <new_instructions> --model <new_model> --type <new_type>
  ```

- **Delete Assistant:**
  ```bash
  python main.py assistant delete --id <assistant_id>
  ```

### Thread Management

- **Create Thread:**
  ```bash
  python main.py thread create
  ```

- **Retrieve Thread:**
  ```bash
  python main.py thread retrieve --id <thread_id>
  ```

- **List Threads:**
  ```bash
  python main.py thread list
  ```

- **Update Thread:**
  ```bash
  python main.py thread update --id <thread_id> --name <new_name>
  ```

- **Delete Thread:**
  ```bash
  python main.py thread delete --id <thread_id>
  ```

### Message Management
- **Create Message**
  ```bash
  python main.py message create --thread <thread_id> --role <role> --content <content>
  ```

- **Retrieve Message:**
  ```bash
  python main.py message retrieve --id <message_id>
  ```

- **List Messages**
  ```bash
  python main.py message list
  ```

- **Update Message:**
  ```bash
  python main.py message update --thread <thread_id> --id <message_id>
  ```

- **Delete Message:**
  ```bash
  python main.py message delete --thread <thread_id> --id <message_id>
  ```

### Run Management

- **Execute Run:**
  ```bash
  python main.py run --thread <thread_id> --assistant <assistant_id> --instructions <instructions>
  ```

- **List Runs:**
  ```bash
  python main.py run list
  ```

## Contribution

Contributions are welcome! Please fork the repository and submit a pull request for review.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
