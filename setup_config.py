import json
import os
import random

"""
Пременные конфигурации
"""
LDPLAYER_PATH = "D:\\LDPlayer\\LDPlayer9\\vms\\config"  # Замените папку на вашу по аналогии
emulators = range(0, 100)  # Указываем с какого по какой эмулятор хотим сделать настройку

"""
Настройки
"""
new_root = True
new_adb_debug = 1  # Включение adb debug, 0 - выключить, 1 - включить, нужно дла будущей втоматизации
new_resolution_width = 900  # Ширина эмулятора
new_resolution_height = 1600  # Высота эмлутора
new_resolution_dpi = 320  # dpi эмулятора
new_close_option = 1 # 1 - пропускать окно с предупреждением закрытия эмулятора, 0 - показывать окно
new_cpu_count = 1  # Кол-во ядер для эмулятора
new_memory_size = 2048  # ОЗУ выделяемое для эмулятора


# Здесь указываем локацию по latitude (от и до), генерируется рандомно
min_latitude, max_latitude = (
    40.512,
    60.241,
)  

# Здесь указываем локацию по longtirude (от и до), генерируется рандомно
min_longitude, max_longitude = (
    25.141,
    40.123,
)  

# Здесь по аналогии можете добавить телефоны которые ставите на эмуляторы
phones = [
    {"phoneModel": "MX912", "phoneManufacturer": "nubia"},
    {"phoneModel": "REDMI9SKNOTE9", "phoneManufacturer": "Xiaomi"},
    #{"phoneModel": "ВАША МОДЕЛЬ", "phoneManufacturer": "ВАШ ПРОИЗВОДИТЕЛЬ"},
]


def update_config(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            config_data = json.load(file)
    except Exception as _:
        print(
            f"Нету конфига {file_path}, попробуйте создать эмулятор или изменить поле emulators"
        )
        return

    new_imei = generate_imei()
    config_data["propertySettings.phoneIMEI"] = new_imei

    new_imsi = generate_imsi()
    config_data["propertySettings.phoneIMSI"] = new_imsi

    new_sim_serial = generate_sim_serial()
    config_data["propertySettings.phoneSimSerial"] = new_sim_serial

    new_android_id = generate_android_id()
    config_data["propertySettings.phoneAndroidId"] = new_android_id

    new_mac_address = generate_mac_address()
    config_data["propertySettings.macAddress"] = new_mac_address

    location = generate_coordinates()
    config_data["statusSettings.location"] = location

    random_phone = get_random_phone()
    config_data["propertySettings.phoneModel"] = f"{random_phone['phoneModel']}"
    config_data["propertySettings.phoneManufacturer"] = (
        f"{random_phone['phoneManufacturer']}"
    )

    config_data["basicSettings.rootMode"] = True
    config_data["basicSettings.adbDebug"] = new_adb_debug

    config_data["advancedSettings.resolution"] = {}
    config_data["advancedSettings.resolution"]["width"] = new_resolution_width
    config_data["advancedSettings.resolution"]["height"] = new_resolution_height

    config_data["advancedSettings.resolutionDpi"] = new_resolution_dpi

    config_data["statusSettings.closeOption"] = new_close_option

    config_data["advancedSettings.cpuCount"] = new_cpu_count

    config_data["advancedSettings.memorySize"] = new_memory_size

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(config_data, file, indent=4)

    print(f"Файл {file_path} записан с новой конфигурацией.")


"""
Функции генерации данных
"""


def get_random_phone():
    """Возвращает случайный телефон из указанного списка списка."""
    if not phones:
        raise ValueError("Список телефонов не должен быть пустым")

    return random.choice(phones)


def generate_imei():
    def luhn_checksum(imei):
        def digits_of(n):
            return [int(d) for d in str(n)]

        digits = digits_of(imei)
        odd_sum = sum(digits[-1::-2])
        even_sum = sum(sum(digits_of(2 * d)) for d in digits[-2::-2])
        return (odd_sum + even_sum) % 10

    imei_base = [random.randint(0, 9) for _ in range(14)]
    imei_str = "".join(map(str, imei_base))
    checksum = luhn_checksum(imei_str + "0")
    check_digit = 0 if checksum == 0 else 10 - checksum
    return imei_str + str(check_digit)


def generate_imsi():
    mcc = "".join(random.choices("0123456789", k=3))
    mnc_length = random.choice([2, 3])
    mnc = "".join(random.choices("0123456789", k=mnc_length))
    msin_length = 15 - len(mcc) - len(mnc)
    msin = "".join(random.choices("0123456789", k=msin_length))
    return mcc + mnc + msin


def generate_sim_serial():
    def luhn_checksum(num):
        def digits_of(n):
            return [int(d) for d in str(n)]

        digits = digits_of(num)
        odd_sum = sum(digits[-1::-2])
        even_sum = sum(sum(digits_of(2 * d)) for d in digits[-2::-2])
        return (odd_sum + even_sum) % 10

    iccid_base = "".join(random.choices("0123456789", k=18))
    checksum = luhn_checksum(iccid_base + "0")
    check_digit = 0 if checksum == 0 else 10 - checksum
    return iccid_base + str(check_digit)


def generate_android_id():
    return "".join(random.choices("0123456789ABCDEF", k=16))


def generate_coordinates():
    latitude = round(random.uniform(min_latitude, max_latitude), 4)
    longitude = round(random.uniform(min_longitude, max_longitude), 4)
    return {"lng": longitude, "lat": latitude}


def generate_mac_address():
    """Генерирует случайный MAC-адрес без двоеточий."""
    mac_address = "".join(["{:02x}".format(random.randint(0, 255)) for _ in range(6)])
    return mac_address.upper()


def process_all_configs(directory):
    for emulator_id in emulators:
        filename = f"leidian{emulator_id}.config"
        file_path = os.path.join(directory, filename)
        update_config(file_path)


if __name__ == "__main__":
    process_all_configs(LDPLAYER_PATH)