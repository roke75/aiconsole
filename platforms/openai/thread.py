from views.views import console_print, create_and_show_thread_table


def list_threads(client):
    threads = client.beta.threads.list()

    create_and_show_thread_table(threads)


def create_thread(client, messages=None, tool_resources=None, metadata=None):
    thread = client.beta.threads.create(
        messages=messages,
        tool_resources=tool_resources,
        metadata=metadata
    )

    console_print(f"Created thread with id: {thread.id}")

    return thread


def retrieve_thread(client, thread_id):
    thread = client.beta.threads.retrieve(
        thread_id
    )

    create_and_show_thread_table([thread])


def modify_thread(client, thread_id, tool_resources, metadata):
    thread = client.beta.threads.update(
        thread_id,
        tool_resources=tool_resources,
        metadata=metadata
    )

    create_and_show_thread_table([thread])


def delete_thread(client, thread_id):
    thread = client.beta.threads.delete(
        thread_id
    )

    if thread.deleted:
        console_print(f"Deleted thread with id: {thread.id}")
    else:
        console_print(f"Failed to delete thread with id: {thread.id}")
