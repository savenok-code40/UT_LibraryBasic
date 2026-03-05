# encoding:utf-8
from __future__ import print_function
import os
import sys

print("--- CODESYS AUTOMATION: START ---")

# 1. Из Примера 23: Закрываем старое
if projects.primary:
    projects.primary.close()

# 2. Открываем проект (путь адаптирован под Jenkins)
project_path = os.path.join(os.getcwd(), "UT_LibraryBasic.project")
print("Opening project: " + project_path)
proj = projects.open(project_path)

# 3. Из Примера 22: Находим Устройство (чтобы задать адрес)
def get_device(obj):
    if obj.is_device: return obj
    for child in obj.get_children(False):
        found = get_device(child)
        if found: return found
    return None

device = get_device(proj)

# 4. Настройка связи (Исправление ошибки GUID)
# Мы ищем шлюз 'Gateway-1' как ОБЪЕКТ, чтобы система его приняла
if device:
    for gw in online.gateways:
        if gw.name == 'Gateway-1': # Имя с твоего скриншота
            print("Connecting to: Gateway-1 -> 0301.300A")
            device.set_gateway_and_address(gw, '0301.300A')
            break

# 5. Из Примера 23: Подготовка приложения
app = proj.active_application
onlineapp = online.create_online_application(app)

# 6. Авторизация (Твои 1 / 1)
onlineapp.set_specific_credentials('1', '1')

# 7. Из Примера 23: Вход в ПЛК
print("Logging in...")
try:
    onlineapp.login(OnlineChangeOption.Try, True)
    
    # 8. Из Примера 23: Запуск (Run)
    if onlineapp.application_state != ApplicationState.run:
        print("Starting PLC...")
        onlineapp.start()

    # Ждем выполнения тестов
    system.delay(10000)

    # 9. Из Примера 23: Чтение значения (Твоя переменная)
    value = onlineapp.read_value("PLC_PRG.xErrorTestDI")
    print("TEST RESULT (xErrorTestDI): " + str(value))

    # Если True - тест провален, выходим с ошибкой для Jenkins
    if str(value) == "True":
        print(">>> FAILED <<<")
        onlineapp.logout()
        proj.close()
        system.exit(1)
    
    print(">>> SUCCESS <<<")

    # 10. Из Примера 23: Выход
    onlineapp.logout()
    proj.close()
    print("--- FINISHED SUCCESSFULLY ---")

except Exception as e:
    print("CRITICAL ERROR: " + str(e))
    system.exit(1)

system.exit()