import os
import time
from os import listdir
from os.path import isfile, join
from rich.console import Console
from rich.table import Table


console = Console()


def list_stores(client):
    vector_stores = client.beta.vector_stores.list()

    create_and_show_store_table(vector_stores)


def create_store(client, name):
    vector_store = client.beta.vector_stores.create(
        name=name
    )

    create_and_show_store_table([vector_store])


def retrieve_store(client, store_id):
    vector_store = client.beta.vector_stores.retrieve(
        store_id
    )

    create_and_show_store_table([vector_store])


def update_store(client, store_id, name, anchor, days):
    vector_store = client.beta.vector_stores.update(
        vector_store_id=store_id,
        name=name
    )
    create_and_show_store_table([vector_store])


def delete_store(client, store_id):
    vector_store = client.beta.vector_stores.delete(
        store_id
    )

    if vector_store.deleted:
        console.print(f"Deleted store with id: {vector_store.id}")
    else:
        console.print(f"Failed to delete store with id: {vector_store.id}")


def list_files(client, store_id):
    files = client.beta.vector_stores.files.list(
        store_id
    )

    create_and_show_file_table(files)


def add_files(client, store_id, files=None, directory=None, recursive=False):
    file_paths = []
    if files:
        file_paths = [open(file, "rb") for file in files]

    elif directory:
        file_list = []
        if recursive:
            for root, _, files in os.walk(directory):
                for file in files:
                    filepath = os.path.join(root, file)
                    file_list.append(filepath)
        else:
            file_list = [os.path.join(directory, f) for f in listdir(directory) if isfile(join(directory, f))]

        file_paths = [open(path, "rb") for path in file_list]

    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=store_id, files=file_paths
    )

    if file_batch.status == 'completed':
        console.print(f"Added files to store with id: {store_id}")
    else:
        console.print(f"Failed to add files to store with id: {store_id}")


def delete_files(client, store_id, files, all=False, permanently=False):
    if all:
        all_files = client.beta.vector_stores.files.list(
            vector_store_id=store_id
        )

        for file in all_files:
            response = client.beta.vector_stores.files.delete(
                vector_store_id=store_id,
                file_id=file.id
            )

            if response.deleted:
                console.print(f"Deleted file with id: {file.id}")
            else:
                console.print(f"Failed to delete file with id: {file.id}")
    else:
        for file in files:
            response = client.beta.vector_stores.files.delete(
                vector_store_id=store_id,
                file_id=file
            )

            if response.deleted:
                console.print(f"Deleted file with id: {file}")
            else:
                console.print(f"Failed to delete file with id: {file}")


def create_and_show_store_table(rows):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Name", style="cyan")
    table.add_column("Id", style="magenta")
    table.add_column("Created", style="green")
    table.add_column("Files", style="blue")
    table.add_column("Size", style="blue")
    table.add_column("Status", style="blue")
    table.add_column("Expires after", style="blue")
    table.add_column("Expires at", style="blue")

    for row in rows:
        table.add_row(
            row.name,
            row.id,
            time.strftime(
                '%H:%M:%S %d.%m.%Y',
                time.gmtime(row.created_at)
            ),
            str(row.file_counts.total),
            str(row.usage_bytes),
            row.status,
            time.strftime(
                '%H:%M:%S %d.%m.%Y',
                time.gmtime(row.expires_after)
            ) if row.expires_after else "None",
            time.strftime(
                '%H:%M:%S %d.%m.%Y',
                time.gmtime(row.expires_at)
            ) if row.expires_at else "None"
        )

    console.print(table)


def create_and_show_file_table(rows):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Id", style="cyan")
    table.add_column("Created", style="green")
    table.add_column("Size", style="blue")
    table.add_column("Status", style="blue")

    for row in rows:
        table.add_row(
            row.id,
            time.strftime(
                '%H:%M:%S %d.%m.%Y',
                time.gmtime(row.created_at)
            ),
            str(row.usage_bytes),
            row.status
        )

    console.print(table)