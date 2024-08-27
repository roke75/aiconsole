# AIConsole

AIConsole is a command-line interface tool designed for managing various components of OpenAI, such as vector stores and assistants. With AIConsole, users can create, update, list, and delete vector stores; manage assistants; handle conversation threads and messages; and execute runs for result capture and display.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
  - [Vector Store Management](#vector-store-management)
  - [Assistant Management](#assistant-management)
  - [Thread and Message Management](#thread-and-message-management)
  - [Run Management](#run-management)
- [Contribution](#contribution)
- [License](#license)

## Installation

To install AIConsole, clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/roke75/AIConsole.git
cd AIConsole
pip install -r requirements.txt
```

## Usage

### Vector Store Management

- **List Vector Stores:**
  ```bash
  python aiconsole.py list_vector_stores
  ```

- **Create Vector Store:**
  ```bash
  python aiconsole.py create_vector_store --name <store_name> --type <store_type> --settings <settings_json>
  ```

- **Update Vector Store:**
  ```bash
  python aiconsole.py update_vector_store --id <store_id> --settings <settings_json>
  ```

- **Delete Vector Store:**
  ```bash
  python aiconsole.py delete_vector_store --id <store_id>
  ```

### Assistant Management

- **Create Assistant:**
  ```bash
  python aiconsole.py create_assistant --name <assistant_name> --model <model_type> --instructions <instructions_json>
  ```

- **List Assistants:**
  ```bash
  python aiconsole.py list_assistants
  ```

- **Update Assistant:**
  ```bash
  python aiconsole.py update_assistant --id <assistant_id> --settings <settings_json>
  ```

- **Delete Assistant:**
  ```bash
  python aiconsole.py delete_assistant --id <assistant_id>
  ```

### Thread and Message Management

- **Create Thread:**
  ```bash
  python aiconsole.py create_thread --name <thread_name>
  ```

- **List Threads:**
  ```bash
  python aiconsole.py list_threads
  ```

- **Create Message in Thread:**
  ```bash
  python aiconsole.py create_message --thread_id <thread_id> --content <message_content>
  ```

- **List Messages in Thread:**
  ```bash
  python aiconsole.py list_messages --thread_id <thread_id>
  ```

- **Update Message:**
  ```bash
  python aiconsole.py update_message --id <message_id> --content <new_content>
  ```

- **Delete Message:**
  ```bash
  python aiconsole.py delete_message --id <message_id>
  ```

### Run Management

- **Execute Run:**
  ```bash
  python aiconsole.py execute_run --assistant_id <assistant_id> --thread_id <thread_id>
  ```

- **List Runs:**
  ```bash
  python aiconsole.py list_runs
  ```

- **Get Run Result:**
  ```bash
  python aiconsole.py get_run_result --run_id <run_id>
  ```

## Contribution

Contributions are welcome! Please fork the repository and submit a pull request for review.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
