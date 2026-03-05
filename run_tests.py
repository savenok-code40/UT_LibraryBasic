# encoding:utf-8
from __future__ import print_function
import os
import sys

print("--- CODESYS CI/CD: FINAL START ---")

# 1. Очистка памяти перед запуском
if projects.primary:
    projects.primary.close()

# 2. Определение путей
project_name = "UT_LibraryBasic.project"
path = os.path.join(os.getcwd(), project_name)

if os.path.exists(path):
    print("Opening project: " + path)
    proj = projects.open(path)
    
    # Берем активное приложение (как в твоем примере)
    app = proj.active_application
    if not app:
        print("ERROR: No active application found in project!")
        system.exit(1)
        
    print("Active Application: " + app.get_name(False))

    # 3. НАСТРОЙКА СВЯЗИ (устраняем ошибку NullReference)
    # Находим родительское устройство для приложения
    device = app
    while device and not device.is_device:
        device = device.parent
    
    if device:
        print("Setting communication path for device: " + device.get_name(False))
        # Устанавливаем шлюз 'Gateway' и адрес 'localhost' (стандарт для службы Win V3)
        device.set_gateway_and_address('Gateway', 'localhost')
    else:
        print("WARNING: Could not find parent device for application.")

    # 4. СОЗДАНИЕ ОНЛАЙН-ПРИЛОЖЕНИЯ
    onlineapp = online.create_online_application(app)

    # 5. ВХОД В ПЛК (ЛОГИН)
    print("Logging in to CODESYS Control Win V3...")
    try:
        # Используем Force, чтобы Jenkins всегда загружал свежий код тестов
        onlineapp.login(OnlineChangeOption.Force, True)
        print("Login successful!")
    except Exception as e:
        print("LOGIN ERROR: " + str(e))
        proj.close()
        system.exit(1)

    # 6. ЗАПУСК ПЛК (START)
    if onlineapp.application_state != ApplicationState.run:
        print("Starting PLC Application...")
        onlineapp.start()

    # 7. ОЖИДАНИЕ ВЫПОЛНЕНИЯ ТЕСТОВ (10 секунд)
    print("Executing tests... please wait...")
    system.delay(10000)

    # 8. ЧТЕНИЕ РЕЗУЛЬТАТА (твоя переменная xErrorTestDI)
    try:
        value = onlineapp.read_value("PLC_PRG.xErrorTestDI")
        print("RESULT: PLC_PRG.xErrorTestDI = " + str(value))
        
        # Анализ результата для Jenkins
        if str(value) == "True":
            print(">>> CRITICAL: UNIT TESTS FAILED! <<<")
            onlineapp.logout()
            proj.close()
            system.exit(1) # Это заставит Jenkins "покраснеть"
        else:
            print(">>> SUCCESS: ALL TESTS PASSED! <<<")
            
    except Exception as e:
        print("READ ERROR: Could not read test variable. " + str(e))
        system.exit(1)

    # 9. ЗАВЕРШЕНИЕ
    onlineapp.logout()
    proj.close()
    print("--- CODESYS CI/CD: FINISHED SUCCESSFULLY ---")

else:
    print("ERROR: Project file not found at " + path)
    system.exit(1)

system.exit()