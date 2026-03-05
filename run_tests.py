# encoding:utf-8
from __future__ import print_function
import os
import sys

print("--- CODESYS CI/CD: STARTING FINAL TEST ---")

# 1. Закрываем лишние проекты, если они висят в памяти
if projects.primary:
    projects.primary.close()

# 2. Формируем путь к твоему проекту в Jenkins
project_name = "UT_LibraryBasic.project"
path = os.path.join(os.getcwd(), project_name)

if os.path.exists(path):
    # Открываем проект
    proj = projects.open(path)
    
    # ИСПОЛЬЗУЕМ ЭТАЛОННЫЙ МЕТОД ИЗ ТВОЕГО ПРИМЕРА
    app = proj.active_application
    print("Active Application: " + app.get_name(False))
    
    onlineapp = online.create_online_application(app)

    # 3. Вход в устройство (локальная служба Control Win V3)
    print("Logging in to PLC service...")
    onlineapp.login(OnlineChangeOption.Try, True)

    # 4. Запуск, если еще не запущен
    if onlineapp.application_state != ApplicationState.run:
        print("Starting PLC...")
        onlineapp.start()

    # 5. Ждем выполнения тестов coUnit (10 секунд)
    print("Executing tests... please wait...")
    system.delay(10000)

    # 6. ЧТЕНИЕ ТВОЕЙ ПЕРЕМЕННОЙ (xErrorTestDI)
    value = onlineapp.read_value("PLC_PRG.xErrorTestDI")
    print("Result PLC_PRG.xErrorTestDI = " + str(value))

    # 7. Вердикт для Jenkins
    if str(value) == "True":
        print("TEST FAILED!")
        onlineapp.logout()
        proj.close()
        system.exit(1) # Jenkins выдаст ошибку
    else:
        print("TEST PASSED!")

    # 8. Завершение
    onlineapp.logout()
    proj.close()
    print("--- CI/CD FINISHED SUCCESSFULLY ---")
else:
    print("ERROR: Project file not found at " + path)
    system.exit(1)

system.exit()