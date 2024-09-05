from views import create_and_show_assistant_table, console_print


def list_assistants(client, limit=None, order=None, after=None, before=None):
    assistants = client.beta.assistants.list(
        limit=limit,
        order=order,
        after=after,
        before=before
    )

    create_and_show_assistant_table(assistants)


def create_assistant(client, model, name, description, instructions, tools, tool_resources, metadata, temperature, top_p, response_format):
    assistant = client.beta.assistants.create(
        model=model,
        name=name,
        description=description,
        instructions=instructions,
        tools=tools,
        tool_resources=tool_resources,
        metadata=metadata,
        temperature=temperature,
        top_p=top_p,
        response_format=response_format
    )

    create_and_show_assistant_table([assistant])


def retrieve_assistant(client, assistant_id):
    assistant = client.beta.assistants.retrieve(
        assistant_id
    )

    create_and_show_assistant_table([assistant])


def modify_assistant(client, assistant_id, model, name, description, instructions, tools, tool_resources, metadata, temperature, top_p, response_format):
    assistant = client.beta.assistants.update(
        assistant_id,
        model=model,
        name=name,
        description=description,
        instructions=instructions,
        tools=tools,
        tool_resources=tool_resources,
        metadata=metadata,
        temperature=temperature,
        top_p=top_p,
        response_format=response_format
    )

    create_and_show_assistant_table([assistant])


def delete_assistant(client, assistant_id):
    assistant = client.beta.assistants.delete(
        assistant_id
    )

    if assistant.deleted:
        console_print(f"Deleted assistant with id: {assistant.id}")
    else:
        console_print(f"Failed to delete assistant with id: {assistant.id}")
