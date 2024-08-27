import time
from rich.console import Console
from rich.table import Table

console = Console()


def list_assistants(client):
    assistants = client.beta.assistants.list()

    create_and_show_assistant_table(assistants)


def create_assistant(client, name, instructions, model, type, store):
    assistant = client.beta.assistants.create(
        name=name,
        instructions=instructions,
        model=model,
        tools=[{"type": type}],
        tool_resources={"file_search": {"vector_store_ids": [store]}}
    )

    create_and_show_assistant_table([assistant])


def retrieve_assistant(client, assistant_id):
    assistant = client.beta.assistants.retrieve(
        assistant_id
    )

    print(assistant)


def update_assistant(client, assistant_id, name, instructions, model, type, store):
    assistant = client.beta.assistants.update(
        assistant_id=assistant_id,
        name=name,
        instructions=instructions,
        model=model,
        tools=[{"type": type}],
        tool_resources={"file_search": {"vector_store_ids": [store]}}
    )

    print(assistant)


def delete_assistant(client, assistant_id):
    assistant = client.beta.assistants.delete(
        assistant_id
    )

    print(assistant)


def create_and_show_assistant_table(rows):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Name", style="cyan")
    table.add_column("Id", style="magenta")
    table.add_column("Created", style="green")
    table.add_column("Description", style="blue")
    table.add_column("Model", style="blue")

    for row in rows:
        table.add_row(
            row.name,
            row.id,
            time.strftime(
                '%H:%M:%S %d.%m.%Y',
                time.gmtime(row.created_at)
            ),
            row.description,
            row.model
        )

    console.print(table)
