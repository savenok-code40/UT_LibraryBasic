# encoding:utf-8
from __future__ import print_function
import os

print("--- CODESYS AUTOMATIC CONNECTION ---")

# 1. Открываем проект
path = os.path.join(os.getcwd(), "UT_LibraryBasic.project")
proj = projects.open(path)
app = proj.active_application

# 2. ПОИСК ШЛЮЗА (Вместо "сканировать сеть")
print("Searching for Gateway...")
my_gateway = None
for gw in online.gateways:
    if gw.name == 'Gateway': # Проверьте имя в Communication Settings (обычно 'Gateway')
        my_gateway = gw
        break

if my_gateway:
    # Находим устройство в дереве (ПЛК)
    device = app
    while device and not device.is_device:
        device = device.parent
    
    if device:
        print("Connecting to localhost via " + my_gateway.name)
        # Передаем ОБЪЕКТ шлюза, чтобы CODESYS сам взял его GUID
        device.set_gateway_and_address(my_gateway, 'localhost')
    else:
        print("ERROR: Device node not found!")
        system.exit(1)
else:
    print("ERROR: Gateway not found in system!")
    system.exit(1)

# 3. ПОПЫТКА ЛОГИНА (с твоим паролем 1/1)
onlineapp = online.create_online_application(app)
onlineapp.set_specific_credentials('1', '1')

print("Logging in...")
try:
    onlineapp.login(OnlineChangeOption.Force, True)
    print("LOGIN SUCCESSFUL!")
    
    # 4. ЗАПУСК И ПРОВЕРКА (упрощенно)
    onlineapp.start()
    system.delay(10000)
    
    result = onlineapp.read_value("PLC_PRG.xErrorTestDI")
    print("TEST RESULT: " + str(result))
    
    if str(result) == "True":
        system.exit(1)

except Exception as e:
    print("CONNECTION FAILED: " + str(e))
    system.exit(1)

onlineapp.logout()
proj.close()
system.exit()