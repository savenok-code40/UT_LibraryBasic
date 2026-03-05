# encoding:utf-8
from __future__ import print_function
import os
import sys

print("--- CODESYS CI/CD: VERIFIED START ---")

# 1. Открытие проекта
project_name = "UT_LibraryBasic.project"
path = os.path.join(os.getcwd(), project_name)

if os.path.exists(path):
    print("Opening: " + path)
    proj = projects.open(path)
    
    # 2. Поиск приложения (через основной проект)
    app = proj.active_application
    print("Application: " + app.get_name(False))

    # 3. Настройка связи (через устройство)
    # Ищем родительский узел устройства
    device = app
    while device and not device.is_device:
        device = device.parent
    
    if device:
        print("Setting Gateway for: " + device.get_name(False))
        # Метод set_gateway_and_address точно есть у объектов Device
        device.set_gateway_and_address('Gateway', 'localhost')
    
    # 4. Создание онлайн-соединения
    onlineapp = online.create_online_application(app)

    # 5. Логин (Force - для автоматической компиляции и загрузки)
    print("Logging in to PLC...")
    try:
        # В SP19 это самый надежный способ "протолкнуть" код
        onlineapp.login(OnlineChangeOption.Force, True)
        
        # 6. Запуск и ожидание
        print("PLC Start...")
        onlineapp.start()
        system.delay(10000) # 10 секунд на тесты

        # 7. Чтение результата
        result = onlineapp.read_value("PLC_PRG.xErrorTestDI")
        print("RESULT xErrorTestDI = " + str(result))

        if str(result) == "True":
            print(">>> TESTS FAILED <<<")
            onlineapp.logout()
            proj.close()
            system.exit(1)
        else:
            print(">>> TESTS PASSED <<<")

        onlineapp.logout()
    except Exception as e:
        print("EXECUTION ERROR: " + str(e))
        system.exit(1)

    proj.close()
    print("--- CI/CD FINISHED ---")
else:
    print("ERROR: File not found!")
    system.exit(1)

system.exit()