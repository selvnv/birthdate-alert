import os

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