import os
import argparse
import json
from openai import OpenAI
from dotenv import load_dotenv
from project.create import create_project, modify_project, delete_project, list_projects, add_files_to_project, list_files_in_project, delete_files_in_project, ask_project
from platforms.openai.store import list_stores, create_store, retrieve_store, modify_store, delete_store, list_files, add_files, delete_files, create_file, retrieve_file
from platforms.openai.assistant import list_assistants, create_assistant, retrieve_assistant, modify_assistant, delete_assistant
from platforms.openai.thread import list_threads, create_thread, retrieve_thread, modify_thread, delete_thread
from platforms.openai.message import list_messages, create_message, retrieve_message, modify_message, delete_message
from platforms.openai.run import list_runs, create_run, create_thread_and_run, retrieve_run, modify_run, submit_tool_outputs, cancel_run, create_run_and_poll

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)


def create_parser():
    parser = argparse.ArgumentParser(description="AIConsole")

    subparsers = parser.add_subparsers(dest="command")

    # Project commands
    project_parser = subparsers.add_parser('project', help='Project related commands')
    project_subparsers = project_parser.add_subparsers(dest="project_command")

    # Create project
    project_create_parser = project_subparsers.add_parser('create', help='Create a project')
    project_create_parser.add_argument('--name', help='Name of the project')
    project_create_parser.add_argument('--description', help='Description of the project')
    project_create_parser.add_argument('--platform', help='AI Platform of the project')
    project_create_parser.add_argument('--instructions', help='Instructions of the project')
    project_create_parser.add_argument('--model', help='AI Model of the project')

    # Modify project
    project_modify_parser = project_subparsers.add_parser('modify', help='Modify a project')
    project_modify_parser.add_argument('--project_id', help='ID of the project')
    project_modify_parser.add_argument('--name', help='Name of the project')
    project_modify_parser.add_argument('--description', help='Description of the project')
    project_modify_parser.add_argument('--platform', help='AI Platform of the project')
    project_modify_parser.add_argument('--instructions', help='Instructions of the project')
    project_modify_parser.add_argument('--model', help='AI Model of the project')

    # List projects
    project_list_parser = project_subparsers.add_parser('list', help='List projects')

    # Add files to project
    project_files_parser = project_subparsers.add_parser('files', help='File related commands')
    project_files_subparsers = project_files_parser.add_subparsers(dest="project_files_command")

    # Create store file
    project_files_add_parser = project_files_subparsers.add_parser('add', help='Add a file to a project')
    project_files_add_parser.add_argument('--project_id', type=str, required=True, help='ID of the project')
    project_files_add_parser.add_argument('--files', type=str, nargs='+', help='Add a file(s) to the store')
    project_files_add_parser.add_argument('--directory', type=str, help='Add a directory to the store')
    project_files_add_parser.add_argument('--recursive', action='store_true', help='Recursively add a directory to the store')

    # List files in project
    project_files_list_parser = project_files_subparsers.add_parser('list', help='List files in a project')
    project_files_list_parser.add_argument('--project_id', type=str, required=True, help='ID of the project')

    # Delete files in project
    project_files_delete_parser = project_files_subparsers.add_parser('delete', help='Delete a file in a project')
    project_files_delete_parser.add_argument('--project_id', type=str, required=True, help='ID of the project')
    project_files_delete_parser.add_argument('--file_ids', type=str, nargs='+', help='ID of the file(s) to delete')
    project_files_delete_parser.add_argument('--all', action='store_true', help='Delete all files in the project')
    project_files_delete_parser.add_argument('--permanently', action='store_true', help='Permanently delete the file(s)')

    # Ask project
    project_ask_parser = project_subparsers.add_parser('ask', help='Ask a project')
    project_ask_parser.add_argument('--project_id', help='ID of the project')
    project_ask_parser.add_argument('--question', help='Question of the project')

    # Delete project
    project_delete_parser = project_subparsers.add_parser('delete', help='Delete a project')
    project_delete_parser.add_argument('--project_id', help='ID of the project')

    # Store commands
    store_parser = subparsers.add_parser('store', help='Store related commands')
    store_subparsers = store_parser.add_subparsers(dest="store_command")

    # Create store
    store_create_parser = store_subparsers.add_parser('create', help='Create a store')
    store_create_parser.add_argument('--name', help='Name of the store')
    store_create_parser.add_argument('--expires_after', type=json.loads, help='Number of days after which the store expires')
    store_create_parser.add_argument('--metadata', help='Metadata of the store')
    store_create_parser.add_argument('--file_ids', nargs='+', help='File IDs of the store')
    store_create_parser.add_argument('--chunking_strategy', help='Chunking strategy of the store')

    # List stores
    store_list_parser = store_subparsers.add_parser('list', help='List stores')
    store_list_parser.add_argument('--limit', type=int, help='Maximum number of stores to list')
    store_list_parser.add_argument('--order', type=str, help='Order of the stores')
    store_list_parser.add_argument('--after', type=str, help='ID of the store after which to list')
    store_list_parser.add_argument('--before', type=str, help='ID of the store before which to list')

    # Retrieve store
    store_retrieve_parser = store_subparsers.add_parser('retrieve', help='Retrieve a store')
    store_retrieve_parser.add_argument('--store_id', required=True, help='ID of the store to retrieve')

    # Modify store
    store_update_parser = store_subparsers.add_parser('modify', help='Update a store')
    store_update_parser.add_argument('--store_id', required=True, help='ID of the store to update')
    store_update_parser.add_argument('--name', help='New name of the store')
    store_update_parser.add_argument('--expires_after', type=json.loads, help='Number of days after which the store expires')
    store_update_parser.add_argument('--metadata', help='Metadata of the store')

    # Delete store
    store_delete_parser = store_subparsers.add_parser('delete', help='Delete a store')
    store_delete_parser.add_argument('--store_id', required=True, help='ID of the store to delete')

    # Store File commands
    store_files_parser = store_subparsers.add_parser('files', help='File related commands')
    store_files_subparsers = store_files_parser.add_subparsers(dest="files_command")

    # Create store file
    store_files_create_parser = store_files_subparsers.add_parser('create', help='Create a file')
    store_files_create_parser.add_argument('--store_id', type=str, required=True, help='ID of the store')
    store_files_create_parser.add_argument('--file_id', type=str, required=True, help='ID of the file')
    store_files_create_parser.add_argument('--chunking_strategy', type=json.loads, help='Chunking strategy of the file')

    # List store files
    store_files_list_parser = store_files_subparsers.add_parser('list', help='List files in the store')
    store_files_list_parser.add_argument('--store_id', required=True, help='ID of the store')
    store_files_list_parser.add_argument('--limit', type=int, help='Maximum number of files to list')
    store_files_list_parser.add_argument('--order', type=str, help='Order of the files')
    store_files_list_parser.add_argument('--after', type=str, help='ID of the file after which to list')
    store_files_list_parser.add_argument('--before', type=str, help='ID of the file before which to list')
    store_files_list_parser.add_argument('--filter', type=str, choices=['in_progress', 'completed', 'failed', 'cancelled'], help='Filter of the files')

    # Retrieve store file
    store_files_retrieve_parser = store_files_subparsers.add_parser('retrieve', help='Retrieve a file')
    store_files_retrieve_parser.add_argument('--store_id', required=True, help='ID of the store')
    store_files_retrieve_parser.add_argument('--file_id', required=True, help='ID of the file')

    # Add files to store
    store_files_add_parser = store_files_subparsers.add_parser('add', help='Add files to the store')
    store_files_add_parser.add_argument('--store_id', required=True, help='ID of the store')
    store_files_add_parser.add_argument('--files', nargs='+', help='Add a file(s) to the store')
    store_files_add_parser.add_argument('--directory', help='Add a directory to the store')
    store_files_add_parser.add_argument('--recursive', action='store_true', help='Recursively add a directory to the store')

    # Delete files from store
    store_files_delete_parser = store_files_subparsers.add_parser('delete', help='Delete files from the store.')
    store_files_delete_parser.add_argument('--store_id', required=True, help='ID of the store')
    store_files_delete_parser.add_argument('--all', action='store_true', help='Delete all files from the store.')
    store_files_delete_parser.add_argument('--permanently', action='store_true', help='Delete files also permanently from files.')
    store_files_delete_parser.add_argument('--file_ids', nargs='+', help='Delete a file(s) from the store')

    # Assistant commands
    assistant_parser = subparsers.add_parser('assistant', help='Assistant related commands')
    assistant_subparsers = assistant_parser.add_subparsers(dest="assistant_command")

    # List assistants
    assistant_list_parser = assistant_subparsers.add_parser('list', help='List assistants')
    assistant_list_parser.add_argument('--limit', type=int, help='Maximum number of assistants to list')
    assistant_list_parser.add_argument('--order', type=str, help='Order of the assistants')
    assistant_list_parser.add_argument('--after', type=str, help='ID of the assistant after which to list')
    assistant_list_parser.add_argument('--before', type=str, help='ID of the assistant before which to list')

    # Create assistant
    assistant_create_parser = assistant_subparsers.add_parser('create', help='Create an assistant')
    assistant_create_parser.add_argument('--model', type=str, required=True, help='Model of the assistant')
    assistant_create_parser.add_argument('--name', type=str, help='Name of the assistant')
    assistant_create_parser.add_argument('--description', type=str, help='Description of the assistant')
    assistant_create_parser.add_argument('--instructions', type=str, help='Instructions of the assistant')
    assistant_create_parser.add_argument('--tools', nargs='+', type=json.loads, help='Type of the assistant')
    assistant_create_parser.add_argument('--tool_resources', type=json.loads, help='Tool resources of the assistant')
    assistant_create_parser.add_argument('--metadata', type=json.loads, help='Metadata of the assistant')
    assistant_create_parser.add_argument('--temperature', type=float, help='Temperature of the assistant')
    assistant_create_parser.add_argument('--top_p', type=float, help='Top_p of the assistant')
    assistant_create_parser.add_argument('--response_format', type=json.loads, help='Response_format of the assistant')

    # Retrieve assistant
    assistant_retrieve_parser = assistant_subparsers.add_parser('retrieve', help='Retrieve an assistant')
    assistant_retrieve_parser.add_argument('--assistant_id', required=True, help='ID of the assistant to retrieve')

    # Modify assistant
    assistant_modify_parser = assistant_subparsers.add_parser('modify', help='Update an assistant')
    assistant_modify_parser.add_argument('--assistant_id', required=True, help='ID of the assistant to update')
    assistant_modify_parser.add_argument('--model', type=str, help='Model of the assistant')
    assistant_modify_parser.add_argument('--name', type=str, help='Name of the assistant')
    assistant_modify_parser.add_argument('--description', type=str, help='Description of the assistant')
    assistant_modify_parser.add_argument('--instructions', type=str, help='Instructions of the assistant')
    assistant_modify_parser.add_argument('--tools', nargs='+', type=json.loads, help='Type of the assistant')
    assistant_modify_parser.add_argument('--tool_resources', type=json.loads, help='Tool resources of the assistant')
    assistant_modify_parser.add_argument('--metadata', type=json.loads, help='Metadata of the assistant')
    assistant_modify_parser.add_argument('--temperature', type=float, help='Temperature of the assistant')
    assistant_modify_parser.add_argument('--top_p', type=float, help='Top_p of the assistant')
    assistant_modify_parser.add_argument('--response_format', type=json.loads, help='Response_format of the assistant')

    # Delete assistant
    assistant_delete_parser = assistant_subparsers.add_parser('delete', help='Delete an assistant')
    assistant_delete_parser.add_argument('--assistant_id', required=True, help='ID of the assistant to delete')

    # Thread commands
    thread_parser = subparsers.add_parser('thread', help='Thread related commands')
    thread_subparsers = thread_parser.add_subparsers(dest="thread_command")

    # List threads
    thread_list_parser = thread_subparsers.add_parser('list', help='List threads')

    # Create thread
    thread_create_parser = thread_subparsers.add_parser('create', help='Create a thread')
    thread_create_parser.add_argument('--messages', nargs='+', type=json.loads, help='Messages of the thread')
    thread_create_parser.add_argument('--tool_resources', type=json.loads, help='Tool resources of the thread')
    thread_create_parser.add_argument('--metadata', type=json.loads, help='Metadata of the thread')

    # Retrieve thread
    thread_retrieve_parser = thread_subparsers.add_parser('retrieve', help='Retrieve a thread')
    thread_retrieve_parser.add_argument('--thread_id', required=True, help='ID of the thread to retrieve')

    # Modify thread
    thread_modify_parser = thread_subparsers.add_parser('modify', help='Modify a thread')
    thread_modify_parser.add_argument('--thread_id', required=True, help='ID of the thread to modify')
    thread_modify_parser.add_argument('--tool_resources', type=json.loads, help='Tool resources of the thread')
    thread_modify_parser.add_argument('--metadata', type=json.loads, help='Metadata of the thread')

    # Delete thread
    thread_delete_parser = thread_subparsers.add_parser('delete', help='Delete a thread')
    thread_delete_parser.add_argument('--thread_id', required=True, help='ID of the thread to delete')

    # Message commands
    message_parser = subparsers.add_parser('message', help='Message related commands')
    message_subparsers = message_parser.add_subparsers(dest="message_command")

    # List messages
    message_list_parser = message_subparsers.add_parser('list', help='List messages')
    message_list_parser.add_argument('--thread_id', required=True, help='ID of the thread')
    message_list_parser.add_argument('--limit', type=int, help='Limit of the messages')
    message_list_parser.add_argument('--order', type=str, help='Order of the messages')
    message_list_parser.add_argument('--after', type=str, help='After of the messages')
    message_list_parser.add_argument('--before', type=str, help='Before of the messages')
    message_list_parser.add_argument('--run_id', type=str, help='Run_id of the messages')

    # Create message
    message_create_parser = message_subparsers.add_parser('create', help='Create a message')
    message_create_parser.add_argument('--thread_id', required=True, help='ID of the thread')
    message_create_parser.add_argument('--role', required=True, help='Role of the message')
    message_create_parser.add_argument('--content', required=True, help='Content of the message')
    message_create_parser.add_argument('--attachments', nargs='+', help='Attachments of the message')
    message_create_parser.add_argument('--metadata', type=json.loads, help='Metadata of the message')

    # Retrieve message
    message_retrieve_parser = message_subparsers.add_parser('retrieve', help='Retrieve a message')
    message_retrieve_parser.add_argument('--thread_id', required=True, help='ID of the thread')
    message_retrieve_parser.add_argument('--message_id', required=True, help='ID of the message')

    # Modify message
    message_update_parser = message_subparsers.add_parser('modify', help='Modify a message')
    message_update_parser.add_argument('--thread_id', required=True, help='ID of the thread')
    message_update_parser.add_argument('--message_id', required=True, help='ID of the message')
    message_update_parser.add_argument('--metadata', type=json.loads, help='Metadata of the message')

    # Delete message
    message_delete_parser = message_subparsers.add_parser('delete', help='Delete a message')
    message_delete_parser.add_argument('--thread_id', required=True, help='ID of the thread')
    message_delete_parser.add_argument('--message_id', required=True, help='ID of the message')

    # Run commands
    run_parser = subparsers.add_parser('run', help='Run related commands')
    run_subparsers = run_parser.add_subparsers(dest="run_command")

    # List runs
    run_list_parser = run_subparsers.add_parser('list', help='List runs')
    run_list_parser.add_argument('--thread_id', type=str, required=True, help='ID of the thread')
    run_list_parser.add_argument('--limit', type=int, help='Limit of the runs')
    run_list_parser.add_argument('--order', type=str, help='Order of the runs')
    run_list_parser.add_argument('--after', type=str, help='After of the runs')
    run_list_parser.add_argument('--before', type=str, help='Before of the runs')

    # Create run
    run_create_parser = run_subparsers.add_parser('create', help='Create a run')
    run_create_parser.add_argument('--thread_id', type=str, required=True, help='ID of the thread')
    run_create_parser.add_argument('--assistant_id', type=str, required=True, help='ID of the assistant')
    run_create_parser.add_argument('--model', type=str, help='Model of the run')
    run_create_parser.add_argument('--instructions', type=str, help='Instructions of the run')
    run_create_parser.add_argument('--additional_instructions', type=str, help='Additional instructions of the run')
    run_create_parser.add_argument('--additional_messages', type=str, help='Additional messages of the run')
    run_create_parser.add_argument('--tools', nargs='+', type=json.loads, help='Tools of the run')
    run_create_parser.add_argument('--metadata', type=json.loads, help='Metadata of the run')
    run_create_parser.add_argument('--temperature', type=float, help='Temperature of the run')
    run_create_parser.add_argument('--top_p', type=float, help='Top_p of the run')
    run_create_parser.add_argument('--stream', type=bool, help='Stream of the run')
    run_create_parser.add_argument('--max_prompt_tokens', type=int, help='Max tokens of the run')
    run_create_parser.add_argument('--max_completion_tokens', type=int, help='Max completion tokens of the run')
    run_create_parser.add_argument('--truncation_strategy', type=json.loads, help='Truncation strategy of the run')
    run_create_parser.add_argument('--tool_choice', help='Tool choice of the run')
    run_create_parser.add_argument('--parallel_tool_calls', type=bool, help='Parallel tool calls of the run')
    run_create_parser.add_argument('--response_format', help='Response format of the run')

    # Create thread and run
    run_create_thread_and_run_parser = run_subparsers.add_parser('create_thread_and_run', help='Create thread and run')
    run_create_thread_and_run_parser.add_argument('--assistant_id', type=str, required=True, help='ID of the assistant')
    run_create_thread_and_run_parser.add_argument('--thread', type=json.loads, help='Thread of the run')
    run_create_thread_and_run_parser.add_argument('--model', type=str, help='Model of the run')
    run_create_thread_and_run_parser.add_argument('--instructions', type=str, help='Instructions of the run')
    run_create_thread_and_run_parser.add_argument('--tools', nargs='+', help='Tools of the run')
    run_create_thread_and_run_parser.add_argument('--tool_resources', type=json.loads, help='Tool resources of the run')
    run_create_thread_and_run_parser.add_argument('--metadata', type=json.loads, help='Metadata of the run')
    run_create_thread_and_run_parser.add_argument('--temperature', type=float, help='Temperature of the run')
    run_create_thread_and_run_parser.add_argument('--top_p', type=float, help='Top_p of the run')
    run_create_thread_and_run_parser.add_argument('--stream', type=bool, help='Stream of the run')
    run_create_thread_and_run_parser.add_argument('--max_prompt_tokens', type=int, help='Max prompt tokens of the run')
    run_create_thread_and_run_parser.add_argument('--max_completion_tokens', type=int, help='Max completion tokens of the run')
    run_create_thread_and_run_parser.add_argument('--truncation_strategy', type=json.loads, help='Truncation strategy of the run')
    run_create_thread_and_run_parser.add_argument('--tool_choice', help='Tool choice of the run')
    run_create_thread_and_run_parser.add_argument('--parallel_tool_calls', type=bool, help='Parallel tool calls of the run')
    run_create_thread_and_run_parser.add_argument('--response_format', help='Response format of the run')

    # Retrieve run
    run_retrieve_parser = run_subparsers.add_parser('retrieve', help='Retrieve a run')
    run_retrieve_parser.add_argument('--thread_id', type=str, required=True, help='ID of the thread')
    run_retrieve_parser.add_argument('--run_id', type=str, required=True, help='ID of the run')

    # Modify run
    run_modify_parser = run_subparsers.add_parser('modify', help='Modify a run')
    run_modify_parser.add_argument('--thread_id', type=str, required=True, help='ID of the thread')
    run_modify_parser.add_argument('--run_id', type=str, required=True, help='ID of the run')
    run_modify_parser.add_argument('--metadata', type=json.loads, help='Metadata of the run')

    # Submit tool outputs
    run_submit_tool_outputs_parser = run_subparsers.add_parser('submit_tool_outputs', help='Submit tool outputs')
    run_submit_tool_outputs_parser.add_argument('--thread_id', type=str, required=True, help='ID of the thread')
    run_submit_tool_outputs_parser.add_argument('--run_id', type=str, required=True, help='ID of the run')
    run_submit_tool_outputs_parser.add_argument('--tool_outputs', nargs='+', type=json.loads, help='Tool outputs of the run')
    run_submit_tool_outputs_parser.add_argument('--stream', type=bool, help='Stream of the run')

    # Cancel run
    run_cancel_parser = run_subparsers.add_parser('cancel', help='Cancel a run')
    run_cancel_parser.add_argument('--thread_id', type=str, required=True, help='ID of the thread')
    run_cancel_parser.add_argument('--run_id', type=str, required=True, help='ID of the run')

    return parser


def parse_cmd_args():
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "project":
        if args.project_command == "create":
            create_project(client, args.name, args.description, args.platform, args.instructions, args.model)
        elif args.project_command == "modify":
            modify_project(client, args.project_id, args.name, args.description, args.platform, args.instructions, args.model)
        elif args.project_command == "delete":
            delete_project(args.project_id)
        elif args.project_command == "list":
            list_projects()
        elif args.project_command == "ask":
            ask_project(client, args.project_id, args.question)
        elif args.project_command == "files":
            if args.project_files_command == "add":
                add_files_to_project(client, args.project_id, args.files, args.directory, args.recursive)
            elif args.project_files_command == "list":
                list_files_in_project(client, args.project_id)
            elif args.project_files_command == "delete":
                delete_files_in_project(client, args.project_id, args.file_ids, args.all, args.permanently)
    elif args.command == "store":
        if args.store_command == "create":
            create_store(client, args.name, args.expires_after, args.metadata, args.file_ids, args.chunking_strategy)
        elif args.store_command == "delete":
            delete_store(client, args.store_id)
        elif args.store_command == "list":
            list_stores(client, args.limit, args.order, args.after, args.before)
        elif args.store_command == "retrieve":
            retrieve_store(client, args.store_id)
        elif args.store_command == "modify":
            modify_store(client, args.store_id, args.name, args.expires_after, args.metadata)
        elif args.store_command == "files":
            if args.files_command == "create":
                create_file(client, args.store, args.file_id, args.chunking_strategy)
            elif args.files_command == "list":
                list_files(client, args.store_id)
            elif args.files_command == "add":
                add_files(client, args.store_id, args.files, args.directory, args.recursive)
            elif args.files_command == "retrieve":
                retrieve_file(client, args.store, args.file_id)
            elif args.files_command == "delete":
                delete_files(client, args.store, args.file_ids, args.all, args.permanently)
    elif args.command == "assistant":
        if args.assistant_command == "create":
            create_assistant(client, args.model, args.name, args.description, args.instructions, args.tools, args.tool_resources, args.metadata, args.temperature, args.top_p, args.response_format)
        elif args.assistant_command == "list":
            list_assistants(client, args.limit, args.order, args.after, args.before)
        elif args.assistant_command == "retrieve":
            retrieve_assistant(client, args.assistant_id)
        elif args.assistant_command == "modify":
            modify_assistant(client, args.assistant_id, args.model, args.name, args.description, args.instructions, args.tools, args.tool_resources, args.metadata, args.temperature, args.top_p, args.response_format)
        elif args.assistant_command == "delete":
            delete_assistant(client, args.assistant_id)
    elif args.command == "thread":
        if args.thread_command == "create":
            create_thread(client, args.messages, args.tool_resources, args.metadata)
        elif args.thread_command == "list":
            print("OpenAI doesn't support listing threads yet")
            list_threads(client)
        elif args.thread_command == "retrieve":
            retrieve_thread(client, args.thread_id)
        elif args.thread_command == "modify":
            modify_thread(client, args.thread_id, args.tool_resources, args.metadata)
        elif args.thread_command == "delete":
            delete_thread(client, args.thread_id)
    elif args.command == "message":
        if args.message_command == "create":
            create_message(client, args.thread_id, args.role, args.content, args.attachments, args.metadata)
        elif args.message_command == "list":
            list_messages(client, args.thread_id, args.limit, args.order, args.after, args.before, args.run_id)
        elif args.message_command == "retrieve":
            retrieve_message(client, args.thread_id, args.message_id)
        elif args.message_command == "modify":
            modify_message(client, args.thread_id, args.message_id, args.metadata)
        elif args.message_command == "delete":
            delete_message(client, args.thread_id, args.message_id)
    elif args.command == "run":
        if args.run_command == "list":
            list_runs(client, args.thread_id, args.limit, args.order, args.after, args.before)
        elif args.run_command == "create":
            create_run(client, args.thread_id, args.assistant_id, args.model, args.instructions, args.additional_instructions, args.additional_messages, args.tools, args.metadata, args.temperature, args.top_p, args.stream, args.max_prompt_tokens, args.max_completion_tokens, args.truncation_strategy, args.tool_choice, args.parallel_tool_calls, args.response_format)
        elif args.run_command == "create_thread_and_run":
            create_thread_and_run(client, args.assistant_id, args.thread, args.model, args.instructions, args.tools, args.tool_resources, args.metadata, args.temperature, args.top_p, args.stream, args.max_prompt_tokens, args.max_completion_tokens, args.truncation_strategy, args.tool_choice, args.parallel_tool_calls, args.response_format)
        elif args.run_command == "retrieve":
            retrieve_run(client, args.thread_id, args.run_id)
        elif args.run_command == "modify":
            modify_run(client, args.thread_id, args.run_id, args.metadata)
        elif args.run_command == "submit_tool_outputs":
            submit_tool_outputs(client, args.thread_id, args.run_id, args.tool_outputs, args.stream)
        elif args.run_command == "cancel":
            cancel_run(client, args.thread_id, args.run_id)
