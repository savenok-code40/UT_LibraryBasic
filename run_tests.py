# encoding:utf-8
from __future__ import print_function
import os
import sys

print("--- STEP: CONNECTION TEST ONLY ---")

# 1. Открытие проекта
path = os.path.join(os.getcwd(), "UT_LibraryBasic.project")
proj = projects.open(path)
app = proj.active_application

# 2. Настройка адреса (данные с твоего скриншота)
device = app
while device and not device.is_device:
    device = device.parent

if device:
    print("Target: PC-SAVENOK [0301.300A]")
    # Мы пробуем задать адрес напрямую, как это делает CODESYS
    device.set_communication_address('0301.300A')
else:
    print("ERROR: Device node not found!")
    system.exit(1)

# 3. Попытка авторизованного логина
onlineapp = online.create_online_application(app)
onlineapp.set_specific_credentials('1', '1')

print("Sending Login (1/1)...")
try:
    # OnlineChangeOption.Try — самый быстрый способ проверить связь
    onlineapp.login(OnlineChangeOption.Try, True)
    print(">>> CONNECTED TO PLC SUCCESSFUL! <<<")
    
    # Сразу выходим, если получилось
    onlineapp.logout()
    print("Logout completed.")
except Exception as e:
    print("CONNECTION FAILED: " + str(e))
    system.exit(1)

proj.close()
print("--- END OF CONNECTION TEST ---")
system.exit()