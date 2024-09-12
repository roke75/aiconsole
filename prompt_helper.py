from prompt_toolkit import PromptSession
from project.create import ask_project


def create_prompt(client, project_id):
    session = PromptSession()

    while True:
        try:
            text = session.prompt('> ')
        except EOFError:
            break
        except KeyboardInterrupt:
            break
        else:
            ask_project(client, project_id, text)
