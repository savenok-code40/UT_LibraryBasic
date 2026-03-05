# encoding:utf-8
from __future__ import print_function
import os

print("--- STARTING TESTS ---")

# 1. Открываем проект
path = os.path.join(os.getcwd(), "UT_LibraryBasic.project")
proj = projects.open(path)
app = proj.active_application

# --- ВОТ ЭТА СТРОЧКА ЗАМЕНЯЕТ "СКАНЕР СЕТИ" ---
# Находим устройство и жестко задаем ему адрес localhost
device = app.parent
while not device.is_device: device = device.parent

# Мы находим первый попавшийся шлюз в системе и подключаемся к нему
gateway = online.gateways[0] 
device.set_gateway_and_address(gateway, 'localhost')
print("Communication path set to LOCALHOST via " + gateway.name)
# ---------------------------------------------

onlineapp = online.create_online_application(app)

# 2. Логин и запуск (пароль 1/1)
onlineapp.set_specific_credentials('1', '1')
onlineapp.login(OnlineChangeOption.Force, True)
onlineapp.start()

# 3. Ждем 15 секунд
print("Waiting 15 seconds...")
system.delay(15000)

# 4. Читаем переменную
result = onlineapp.read_value("PLC_PRG.xErrorTestDI")
print("RESULT xErrorTestDI: " + str(result))

# 5. Итог
if str(result) == "True":
    print(">>> FAILED <<<")
    onlineapp.logout()
    proj.close()
    system.exit(1)

print(">>> SUCCESS <<<")
onlineapp.logout()
proj.close()
system.exit()