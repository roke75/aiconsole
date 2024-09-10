import os
import json
import random
import string
import time
from views.views import create_and_show_project_table, console_print
from platforms.openai.store import create_store, add_files, list_files, delete_files
from platforms.openai.assistant import create_assistant, modify_assistant
from platforms.openai.thread import create_thread
from platforms.openai.message import create_message
from platforms.openai.run import create_run_and_poll


def load_settings():
    SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'settings.json')
    settings = json.load(open(SETTINGS_FILE, 'r', encoding='utf-8'))

    return settings


def write_settings(settings):
    SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'settings.json')

    json.dump(settings, open(SETTINGS_FILE, 'w', encoding='utf-8'), indent=4)


def create_project(client, name, description, platform, instructions, model):
    settings = load_settings()
    alphabet = string.ascii_letters + string.digits + '-_'
    rndstr = 'pr-' + ''.join(random.choices(alphabet, k=8))

    project = {
        'name': name,
        'description': description,
        'platform': platform,
        'created_at': int(time.time()),
        'modified_at': int(time.time()),
        'store_id': None,
        'assistant_id': None,
        'thread_id': None,
        'instructions': instructions,
        'model': model,
        'files': [],
    }

    settings['projects'][rndstr] = project

    # create store
    store = create_store(client, rndstr)

    settings['projects'][rndstr]['store_id'] = store.id

    # create assistant

    assistant = create_assistant(client, model, rndstr, None, instructions, [{"type":"file_search"}], {"file_search": {"vector_store_ids": [store.id]}}, None, None, None, None)

    settings['projects'][rndstr]['assistant_id'] = assistant.id

    # create thread
    thread = create_thread(client, None, None, None)

    settings['projects'][rndstr]['thread_id'] = thread.id

    console_print("Created project with id: " + rndstr)

    write_settings(settings)


def modify_project(client, project_id, name=None, description=None, platform=None, instructions=None, model=None):
    settings = load_settings()
    if name:
        settings["projects"][project_id]["name"] = name

    if description:
        settings["projects"][project_id]["description"] = description

    if platform:
        settings["projects"][project_id]["platform"] = platform

    if instructions:
        settings["projects"][project_id]["instructions"] = instructions

        client.beta.assistants.update(
            settings["projects"][project_id]["assistant_id"],
            instructions=instructions
        )

    if model:
        settings["projects"][project_id]["model"] = model

        client.beta.assistants.update(
            settings["projects"][project_id]["assistant_id"],
            model=model
        )

    settings["projects"][project_id]["modified_at"] = int(time.time())

    write_settings(settings)


def list_projects():
    settings = load_settings()

    create_and_show_project_table(settings["projects"])


def delete_project(project_id):
    settings = load_settings()
    del settings["projects"][project_id]

    write_settings(settings)


def add_files_to_project(client, project_id, files=None, directory=None, recursive=False):
    settings = load_settings()
    store_id = settings["projects"][project_id]["store_id"]

    add_files(client, store_id, files, directory, recursive)


def list_files_in_project(client, project_id):
    settings = load_settings()
    store_id = settings["projects"][project_id]["store_id"]

    list_files(client, store_id)


def delete_files_in_project(client, project_id, file_ids=None, all=False, permanently=False):
    settings = load_settings()
    store_id = settings["projects"][project_id]["store_id"]

    delete_files(client, store_id, file_ids, all, permanently)


def ask_project(client, project_id, question):
    settings = load_settings()

    thread = settings["projects"][project_id]["thread_id"]
    assistant = settings["projects"][project_id]["assistant_id"]

    message = create_message(client, thread, "user", question)

    create_run_and_poll(client, thread, assistant, None)
