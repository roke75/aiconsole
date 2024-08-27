import time
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown

console = Console()


def list_messages(client, thread_id):
    messages = client.beta.threads.messages.list(
        thread_id
    )

    create_and_show_message_table(messages)


def create_message(client, thread_id, role, content):
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role=role,
        content=content
    )

    print(message)


def create_run(client, thread_id, assistant_id, instructions):
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions=instructions
    )

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=thread_id
        )
        response = ''
        for message in messages.data:
            response += message.content[0].text.value

        console.print(Markdown(response))
    else:
        print(run.status)


def retrieve_message(client, thread_id, message_id):
    message = client.beta.threads.messages.retrieve(
        thread_id=thread_id,
        message_id=message_id
    )

    create_and_show_message_table([message])


def update_message(client, thread_id, message_id, role, content):
    message = client.beta.threads.messages.update(
        thread_id=thread_id,
        message_id=message_id,
        role=role,
        content=content
    )

    print(message)


def delete_message(client, thread_id, message_id):
    message = client.beta.threads.messages.delete(
        thread_id=thread_id,
        message_id=message_id
    )

    print(message)


def create_and_show_message_table(rows):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Id", style="cyan")
    table.add_column("Role", style="magenta")
    table.add_column("Content", style="green")

    for row in rows:
        table.add_row(
            str(row.id),
            row.role,
            row.content
        )

    console.print(table)