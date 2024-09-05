from views import console_print, console_print_markdown, create_and_show_run_table


def create_run(client, thread_id, assistant_id, model, instructions, additional_instructions, additional_messages, tools, metadata, temperature, top_p, stream, max_prompt_tokens, max_completion_tokens, truncation_strategy, tool_choice, parallel_tool_calls=True, response_format=None):
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        model=model,
        instructions=instructions,
        additional_instructions=additional_instructions,
        additional_messages=additional_messages,
        tools=tools,
        metadata=metadata,
        temperature=temperature,
        top_p=top_p,
        stream=stream,
        max_prompt_tokens=max_prompt_tokens,
        max_completion_tokens=max_completion_tokens,
        truncation_strategy=truncation_strategy,
        tool_choice=tool_choice,
        parallel_tool_calls=parallel_tool_calls if parallel_tool_calls is not None else True,
        response_format=response_format
    )

    create_and_show_run_table([run])


def create_thread_and_run(client, assistant_id, thread, model, instructions, tools, tool_resources, metadata, temperature, top_p, stream, max_prompt_tokens, max_completion_tokens, truncation_strategy, tool_choice, parallel_tool_calls=True, response_format=None):
    print(parallel_tool_calls)
    thread = client.beta.threads.create_and_run(
        assistant_id=assistant_id,
        thread=thread,
        model=model,
        instructions=instructions,
        tools=tools,
        tool_resources=tool_resources,
        metadata=metadata,
        temperature=temperature,
        top_p=top_p,
        stream=stream,
        max_prompt_tokens=max_prompt_tokens,
        max_completion_tokens=max_completion_tokens,
        truncation_strategy=truncation_strategy,
        tool_choice=tool_choice,
        parallel_tool_calls=parallel_tool_calls if parallel_tool_calls is not None else True,
        response_format=response_format
    )

    create_and_show_run_table([thread])


def list_runs(client, thread_id, limit=None, order=None, after=None, before=None):
    runs = client.beta.threads.runs.list(
        thread_id,
        limit=limit,
        order=order,
        after=after,
        before=before
    )

    create_and_show_run_table(runs)


def retrieve_run(client, thread_id, run_id):
    run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id
    )

    create_and_show_run_table([run])


def modify_run(client, thread_id, run_id, metadata):
    run = client.beta.threads.runs.update(
        thread_id=thread_id,
        run_id=run_id,
        metadata=metadata
    )

    create_and_show_run_table([run])


def submit_tool_outputs(client, thread_id, run_id, tool_outputs, stream):
    run = client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread_id,
        run_id=run_id,
        tool_outputs=tool_outputs,
        stream=stream
    )

    console_print(run)


def cancel_run(client, thread_id, run_id):
    run = client.beta.threads.runs.cancel(
        thread_id=thread_id,
        run_id=run_id
    )

    console_print(run)


def create_run_and_poll(client, thread_id, assistant_id, instructions):
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

        console_print_markdown(response)
    else:
        console_print(run.status)
