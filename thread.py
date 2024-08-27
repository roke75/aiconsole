import time
from rich.console import Console
from rich.table import Table

console = Console()


def list_threads(client):
    threads = client.beta.threads.list()

    create_and_show_thread_table(threads)


def create_thread(client):
    thread = client.beta.threads.create()

    console.print(f"Created thread with id: {thread.id}")


def retrieve_thread(client, thread_id):
    thread = client.beta.threads.retrieve(
        thread_id
    )

    create_and_show_thread_table([thread])



def update_thread(client, thread_id, name):
    thread = client.beta.threads.update(
        thread_id=thread_id,
        name=name
    )

    create_and_show_thread_table([thread])


def delete_thread(client, thread_id):
    thread = client.beta.threads.delete(
        thread_id
    )

    if thread.deleted:
        console.print(f"Deleted thread with id: {thread.id}")
    else:
        console.print(f"Failed to delete thread with id: {thread.id}")


def create_and_show_thread_table(rows):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Name", style="cyan")
    table.add_column("Id", style="magenta")
    table.add_column("Created", style="green")
    table.add_column("Description", style="blue")

    for row in rows:
        table.add_row(row.name, row.id, row.created_at, row.description)

    console.print(table)