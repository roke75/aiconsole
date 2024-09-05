import os
from os import listdir
from os.path import isfile, join
from views import create_and_show_store_table, create_and_show_file_table, console_print

def list_stores(client, limit=None, order=None, after=None, before=None):
    vector_stores = client.beta.vector_stores.list(
        limit=limit,
        order=order,
        after=after,
        before=before
    )

    create_and_show_store_table(vector_stores)


def create_store(client, name, expires_after=None, metadata=None, file_ids=None, chunking_strategy=None):
    vector_store = client.beta.vector_stores.create(
        name=name,
        expires_after=expires_after,
        metadata=metadata,
        file_ids=file_ids,
        chunking_strategy=chunking_strategy
    )

    create_and_show_store_table([vector_store])


def retrieve_store(client, store_id):
    vector_store = client.beta.vector_stores.retrieve(
        store_id
    )

    create_and_show_store_table([vector_store])


def modify_store(client, store_id, name=None, expires_after=None, metadata=None):
    vector_store = client.beta.vector_stores.update(
        vector_store_id=store_id,
        name=name,
        expires_after=expires_after,
        metadata=metadata
    )
    create_and_show_store_table([vector_store])


def delete_store(client, store_id):
    vector_store = client.beta.vector_stores.delete(
        store_id
    )

    if vector_store.deleted:
        console_print(f"Deleted store with id: {vector_store.id}")
    else:
        console_print(f"Failed to delete store with id: {vector_store.id}")


def create_file(client, store_id, file_id, chunking_strategy=None):
    file = client.beta.vector_stores.files.create(
        vector_store_id=store_id,
        file_id=file_id,
        chunking_strategy=chunking_strategy
    )

    if file.id:
        console_print(f"Created file with id: {file.id}")
    else:
        console_print(f"Failed to create file with id: {file.id}")


def list_files(client, store_id, limit=None, order=None, after=None, before=None, filter=None):
    files = client.beta.vector_stores.files.list(
        vector_store_id=store_id,
        limit=limit,
        order=order,
        after=after,
        before=before,
        filter=filter
    )

    create_and_show_file_table(files)


def retrieve_file(client, store_id, file_id):
    file = client.beta.vector_stores.files.retrieve(
        vector_store_id=store_id,
        file_id=file_id
    )

    create_and_show_file_table([file])


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
        console_print(f"Added files to store with id: {store_id}")
    else:
        console_print(f"Failed to add files to store with id: {store_id}")


def delete_files(client, store_id, file_ids, delete_all=False, delete_permanently=False):
    if delete_all:
        all_files = client.beta.vector_stores.files.list(
            vector_store_id=store_id
        )

        for file in all_files:
            response = client.beta.vector_stores.files.delete(
                vector_store_id=store_id,
                file_id=file.id
            )

            if response.deleted:
                console_print(f"Deleted file from store with id: {file.id}")
            else:
                console_print(f"Failed to delete file from store with id: {file.id}")

            if delete_permanently:
                response = client.files.delete(file.id)

                if response.deleted:
                    console_print(f"Deleted file permanently with id: {file.id}")
                else:
                    console_print(f"Failed to delete file permanently with id: {file.id}")

    else:
        for file in file_ids:
            response = client.beta.vector_stores.files.delete(
                vector_store_id=store_id,
                file_id=file
            )

            if response.deleted:
                console_print(f"Deleted file with id: {file}")
            else:
                console_print(f"Failed to delete file with id: {file}")

            if delete_permanently:
                response = client.files.delete(file)

                if response.deleted:
                    console_print(f"Deleted file permanently with id: {file}")
                else:
                    console_print(f"Failed to delete file permanently with id: {file}")
