from views import console_print, create_and_show_message_table


def list_messages(client, thread_id, limit, order, after, before, run_id):
    messages = client.beta.threads.messages.list(
        thread_id,
        limit=limit,
        order=order,
        after=after,
        before=before,
        run_id=run_id
    )

    create_and_show_message_table(messages)


def create_message(client, thread_id, role, content, attachments=None, metadata=None):
    message = client.beta.threads.messages.create(
        thread_id,
        role=role,
        content=content,
        attachments=attachments,
        metadata=metadata
    )

    create_and_show_message_table([message])


def retrieve_message(client, thread_id, message_id):
    message = client.beta.threads.messages.retrieve(
        thread_id=thread_id,
        message_id=message_id
    )
    print(message.content[0].text.value)
    create_and_show_message_table([message])


def modify_message(client, thread_id, message_id, metadata):
    message = client.beta.threads.messages.update(
        thread_id=thread_id,
        message_id=message_id,
        metadata=metadata
    )

    create_and_show_message_table([message])


def delete_message(client, thread_id, message_id):
    message = client.beta.threads.messages.delete(
        thread_id=thread_id,
        message_id=message_id
    )

    if message.deleted:
        console_print(f"Deleted message with id: {message.id}")
    else:
        console_print(f"Failed to delete message with id: {message.id}")
