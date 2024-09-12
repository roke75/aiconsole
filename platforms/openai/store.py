import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
from views.views import create_and_show_store_table, create_and_show_file_table, console_print

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

    return vector_store


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
    supported_file_types = (
        "c", "cpp", "css", "csv", "docx", "gif", "html", "java", "jpeg",
        "jpg", "js", "json", "md", "pdf", "php", "pkl", "png", "pptx",
        "py", "rb", "tar", "tex", "ts", "txt", "webp", "xlsx", "xml", "zip"
    )

    def is_valid_file(file):
        return file.split('.')[-1] in supported_file_types

    if directory:
        for root, dirs, all_files in os.walk(directory):
            # Exclude directories starting with '.' or '_'
            dirs[:] = [d for d in dirs if not (d.startswith('.') or d.startswith('_') or d.startswith('venv'))]
            for file_name in all_files:
                # Exclude files starting with '.' or '_'
                if not (file_name.startswith('.') or file_name.startswith('_')):
                    file_path = os.path.join(root, file_name)
                    if is_valid_file(file_name):
                        file_paths.append(Path(file_path))
            if not recursive:
                break

    if files:
        for file in files:
            if not (os.path.basename(file).startswith('.') or os.path.basename(file).startswith('_')):
                try:
                    file_paths.append(Path(file))
                except IOError as e:
                    console_print(f"Error opening file: {e}")

    try:
        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=store_id, files=file_paths
        )
        console_print(f"Successfully uploaded files: {file_paths}")
    except Exception as e:
        console_print(f"Failed to upload files: {e}")


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
