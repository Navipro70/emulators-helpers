import json
import os
import random

"""
Пременные конфигурации
"""
LDPLAYER_PATH = (
    "D:\\LDPlayer\\LDPlayer9\\vms\\config"  # Замените папку на вашу по аналогии
)
emulators = range(
    0, 100
)  # Указываем с какого по какой эмулятор хотим сделать настройку

new_resolution_width = range(460, 740)  # Ширина эмулятора
new_resolution_height = range(560, 1240)  # Высота эмлутора
new_resolution_dpi = range(250, 350)

def update_config(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            config_data = json.load(file)
    except Exception as _:
        print(
            f"Нету конфига {file_path}, попробуйте создать эмулятор или изменить поле emulators"
        )
        return

    config_data["advancedSettings.resolution"] = {}
    config_data["advancedSettings.resolution"]["width"] = random.choice(new_resolution_width)
    config_data["advancedSettings.resolution"]["height"] = random.choice(new_resolution_height)
    config_data["advancedSettings.resolutionDpi"] = random.choice(new_resolution_dpi)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(config_data, file, indent=4)

    print(f"Файл {file_path} записан с новой конфигурацией экранов.")


def process_all_configs(directory):
    for emulator_id in emulators:
        filename = f"leidian{emulator_id}.config"
        file_path = os.path.join(directory, filename)
        update_config(file_path)


if __name__ == "__main__":
    process_all_configs(LDPLAYER_PATH)