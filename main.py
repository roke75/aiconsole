import os
import argparse
from openai import OpenAI
from dotenv import load_dotenv
from store import list_stores, create_store, retrieve_store, update_store, delete_store, list_files, add_files, delete_files
from assistant import list_assistants, create_assistant, retrieve_assistant, update_assistant, delete_assistant
from thread import list_threads, create_thread, retrieve_thread, update_thread, delete_thread
from message import list_messages, create_message, create_run


load_dotenv()

OPENAI_APIKEY = os.getenv('OPENAI_APIKEY')
client = OpenAI(api_key=OPENAI_APIKEY)


def create_parser():
    parser = argparse.ArgumentParser(description="Ohjelman komentorivityökalu")

    subparsers = parser.add_subparsers(dest="command")

    # store komennon alakomennot
    store_parser = subparsers.add_parser('store', help='Store related commands')
    store_subparsers = store_parser.add_subparsers(dest="store_command")

    # store create
    store_create_parser = store_subparsers.add_parser('create', help='Create a store')
    store_create_parser.add_argument('--name', required=True, help='Name of the store')

    # store list
    store_list_parser = store_subparsers.add_parser('list', help='List stores')

    # store retrieve
    store_retrieve_parser = store_subparsers.add_parser('retrieve', help='Retrieve a store')
    store_retrieve_parser.add_argument('--id', required=True, help='ID of the store to retrieve')

    # store update
    store_update_parser = store_subparsers.add_parser('update', help='Update a store')
    store_update_parser.add_argument('--id', required=True, help='ID of the store to update')
    store_update_parser.add_argument('--name', help='New name of the store')
    store_update_parser.add_argument('--anchor', help='Anchor timestamp')
    store_update_parser.add_argument('--days', help='Number of days')

    # store delete
    store_delete_parser = store_subparsers.add_parser('delete', help='Delete a store')
    store_delete_parser.add_argument('--id', required=True, help='ID of the store to delete')

    # store files
    store_files_parser = store_subparsers.add_parser('files', help='File related commands')
    store_files_subparsers = store_files_parser.add_subparsers(dest="files_command")
    store_files_list_parser = store_files_subparsers.add_parser('list', help='List files in the store')
    store_files_list_parser.add_argument('--store', required=True, help='ID of the store')
    store_files_add_parser = store_files_subparsers.add_parser('add', help='Add files to the store')
    store_files_add_parser.add_argument('--store', required=True, help='ID of the store')
    store_files_add_parser.add_argument('--files', nargs='+', help='Add a file(s) to the store')
    store_files_add_parser.add_argument('--directory', help='Add a directory to the store')
    store_files_add_parser.add_argument('--recursive', action='store_true', help='Recursively add a directory to the store')
    store_files_delete_parser = store_files_subparsers.add_parser('delete', help='Delete files from the store.')
    store_files_delete_parser.add_argument('--store', required=True, help='ID of the store')
    store_files_delete_parser.add_argument('--all', action='store_true', help='Delete all files from the store.')
    store_files_delete_parser.add_argument('--permanently', action='store_true', help='Delete files also permanently from files.')
    store_files_delete_parser.add_argument('--files', nargs='+', help='Delete a file(s) from the store')

    # assistant komennon alakomennot
    assistant_parser = subparsers.add_parser('assistant', help='Assistant related commands')
    assistant_subparsers = assistant_parser.add_subparsers(dest="assistant_command")

    # assistant list
    assistant_list_parser = assistant_subparsers.add_parser('list', help='List assistants')

    # assistant create
    assistant_create_parser = assistant_subparsers.add_parser('create', help='Create an assistant')
    assistant_create_parser.add_argument('--name', required=True, help='Name of the assistant')
    assistant_create_parser.add_argument('--instructions', help='Instructions of the assistant')
    assistant_create_parser.add_argument('--model', help='Model of the assistant')
    assistant_create_parser.add_argument('--type', help='Type of the assistant')
    assistant_create_parser.add_argument('--store', help='Vector store of the assistant')
    # assistant retrieve
    assistant_retrieve_parser = assistant_subparsers.add_parser('retrieve', help='Retrieve an assistant')
    assistant_retrieve_parser.add_argument('--id', required=True, help='ID of the assistant to retrieve')

    # assistant update
    assistant_update_parser = assistant_subparsers.add_parser('update', help='Update an assistant')
    assistant_update_parser.add_argument('--id', required=True, help='ID of the assistant to update')

    # assistant delete
    assistant_delete_parser = assistant_subparsers.add_parser('delete', help='Delete an assistant')
    assistant_delete_parser.add_argument('--id', required=True, help='ID of the assistant to delete')

    # assistant komennon alakomennot
    thread_parser = subparsers.add_parser('thread', help='Thread related commands')
    thread_subparsers = thread_parser.add_subparsers(dest="thread_command")

    # thread list
    thread_list_parser = thread_subparsers.add_parser('list', help='List threads')

    # thread create
    thread_create_parser = thread_subparsers.add_parser('create', help='Create a thread')

    # thread retrieve
    thread_retrieve_parser = thread_subparsers.add_parser('retrieve', help='Retrieve a thread')
    thread_retrieve_parser.add_argument('--id', required=True, help='ID of the thread to retrieve')

    # thread update
    thread_update_parser = thread_subparsers.add_parser('update', help='Update a thread')
    thread_update_parser.add_argument('--id', required=True, help='ID of the thread to update')

    # thread delete
    thread_delete_parser = thread_subparsers.add_parser('delete', help='Delete a thread')
    thread_delete_parser.add_argument('--id', required=True, help='ID of the thread to delete')

    message_parser = subparsers.add_parser('message', help='Message related commands')
    message_subparsers = message_parser.add_subparsers(dest="message_command")

    # message list
    message_list_parser = message_subparsers.add_parser('list', help='List messages')

    # message create
    message_create_parser = message_subparsers.add_parser('create', help='Create a message')
    message_create_parser.add_argument('--thread', required=True, help='ID of the thread')
    message_create_parser.add_argument('--role', required=True, help='Role of the message')
    message_create_parser.add_argument('--content', required=True, help='Content of the message')

    # message retrieve
    message_retrieve_parser = message_subparsers.add_parser('retrieve', help='Retrieve a message')
    message_retrieve_parser.add_argument('--thread', required=True, help='ID of the thread')
    message_retrieve_parser.add_argument('--id', required=True, help='ID of the message')

    # message update
    message_update_parser = message_subparsers.add_parser('update', help='Update a message')
    message_update_parser.add_argument('--thread', required=True, help='ID of the thread')
    message_update_parser.add_argument('--id', required=True, help='ID of the message')

    # message delete
    message_delete_parser = message_subparsers.add_parser('delete', help='Delete a message')
    message_delete_parser.add_argument('--thread', required=True, help='ID of the thread')
    message_delete_parser.add_argument('--id', required=True, help='ID of the message')

    # run parser
    run_parser = subparsers.add_parser('run', help='Run related commands')
    run_subparsers = run_parser.add_subparsers(dest="run_command")

    # list
    run_list_parser = run_subparsers.add_parser('list', help='List runs')

    # create
    run_create_parser = run_subparsers.add_parser('create', help='Create a run')
    run_create_parser.add_argument('--thread', required=True, help='ID of the thread')
    run_create_parser.add_argument('--assistant', required=True, help='ID of the assistant')
    run_create_parser.add_argument('--instructions', required=True, help='Instructions of the run')


    return parser


def parse_cmd_args():
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "store":
        if args.store_command == "create":
            create_store(client, args.name)
        elif args.store_command == "delete":
            delete_store(client, args.id)
        elif args.store_command == "list":
            list_stores(client)
        elif args.store_command == "retrieve":
            retrieve_store(client, args.id)
        elif args.store_command == "update":
            update_store(client, args.id, args.name, args.anchor, args.days)
        elif args.store_command == "files":
            if args.files_command == "list":
                list_files(client, args.store)
            elif args.files_command == "add":
                add_files(client, args.store, args.files, args.directory, args.recursive)
            elif args.files_command == "retrieve":
                print("Retrieve file")
            elif args.files_command == "delete":
                delete_files(client, args.store, args.files, args.all, args.permanently)
    elif args.command == "assistant":
        if args.assistant_command == "create":
            create_assistant(client, args.name, args.instructions, args.model, args.type, args.store)
        elif args.assistant_command == "list":
            list_assistants(client)
        elif args.assistant_command == "retrieve":
            print(f"Retrieving assistant with id: {args.id}")
        elif args.assistant_command == "update":
            print(f"Updating assistant with id: {args.id}")
        elif args.assistant_command == "delete":
            print(f"Deleting assistant with id: {args.id}")
    elif args.command == "thread":
        if args.thread_command == "create":
            create_thread(client)
        elif args.thread_command == "list":
            print("OpenAI doesn't support listing threads yet")
        elif args.thread_command == "retrieve":
            print(f"Retrieving thread with id: {args.id}")
        elif args.thread_command == "update":
            print(f"Updating thread with id: {args.id}")
        elif args.thread_command == "delete":
            print(f"Deleting thread with id: {args.id}")
    elif args.command == "message":
        if args.message_command == "create":
            create_message(client, args.thread, args.role, args.content)
        elif args.message_command == "list":
            print("List messages")
        elif args.message_command == "retrieve":
            print(f"Retrieving message with id: {args.id}")
        elif args.message_command == "update":
            print(f"Updating message with id: {args.id}")
        elif args.message_command == "delete":
            print(f"Deleting message with id: {args.id}")
    elif args.command == "run":
        if args.run_command == "list":
            print("List runs")
        elif args.run_command == "create":
            create_run(client, args.thread, args.assistant, args.instructions)


def main():
    parse_cmd_args()


if __name__ == "__main__":
    main()
