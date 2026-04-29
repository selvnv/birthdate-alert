import os
from math import ceil
from tabulate import tabulate

def get_env_value(var_name):
    env_value = os.getenv(var_name)
    return env_value


def clean_env_value(env_value: str):
    if not isinstance(env_value, str):
        print(f"\033[1m\033[91m[WARN] clean_env_value() >>>> \033[0m env_value must be a string, but {type(env_value)} got",)
        return env_value

    env_value = env_value.strip()

    # Очистка значения от кавычек
    quotes = ["\"", "'"]
    if len(env_value) > 2:
        if env_value[0] in quotes and env_value[0] == env_value[-1]:
            env_value = env_value[1:-1]

    return env_value


def print_table_paged(row_data,
                         headers: list,
                         page_size: int = 8):
    total_rows = len(row_data)
    total_pages = ceil(total_rows / page_size)

    current_page = 0

    while current_page < total_pages:
        start_row = current_page * page_size
        end_row = min(start_row + page_size, total_rows)

        selection = row_data[start_row:end_row]

        print(tabulate(
            selection,
            headers=headers,
            tablefmt="rounded_grid"
        ))

        user_choice = input(
            f"\nPage {current_page + 1} of {total_pages}." +
            f"Rows {end_row} of {total_rows}. \n" +
            f"Press \033[1m\033[92menter\033[0m to continue (\033[1m\033[92mq\033[0m to skip\\exit): "
        )

        if user_choice == "q":
            break

        current_page += 1