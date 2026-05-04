import logging

from jinja2 import Template


def render_birth_notification(
        template_path: str,
        name: str, birthdate: str, additional_info: str) -> str | None:

    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template = Template(f.read())
            return template.render(
                name=name,
                birthdate=birthdate,
                additional_info=additional_info
            )
    except Exception as error:
        logging.error(f"Error while rendering birth_notification template: {error}")
        raise error
