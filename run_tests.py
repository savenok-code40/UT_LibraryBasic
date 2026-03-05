# encoding:utf-8
from __future__ import print_function
import os
import sys
import time

print("--- CODESYS CI/CD: LOCAL SERVICE MODE ---")

project_name = "UT_LibraryBasic.project"
path = os.path.join(os.getcwd(), project_name)

if os.path.exists(path):
    proj = projects.open(path)
    app = proj.find("Application", True)
    
    # 1. Компиляция перед загрузкой
    print("Building project...")
    proj.rebuild()
    
    # 2. ПОДКЛЮЧЕНИЕ К СЛУЖБЕ (БЕЗ ЭМУЛЯЦИИ)
    print("Connecting to CODESYS Control Win V3 service...")
    onlineapp = online.create_online_application(app)
    
    try:
        # Пытаемся залогиниться. Force — для полной перезагрузки кода тестов.
        onlineapp.login(OnlineChangeOption.Force, True)
        print("Login successful!")
        
        # 3. ЗАПУСК ТЕСТОВ
        print("Starting PLC Application...")
        onlineapp.start()
        
        # Даем coUnit время (например, 15 секунд) прогнать все тесты
        print("Tests are running in background service...")
        time.sleep(15) 
        
        # 4. ПРОВЕРКА РЕЗУЛЬТАТА (твоя переменная)
        error_status = onlineapp.read_value("PLC_PRG.xErrorTestDI")
        print("Result of xErrorTestDI: " + str(error_status))
        
        if str(error_status) == "True":
            print("FAILURE: Unit tests failed in CODESYS Control Win V3!")
            onlineapp.stop()
            system.exit(1)
        else:
            print("SUCCESS: All tests passed on local service.")

        onlineapp.logout()
        
    except Exception as e:
        print("CONNECTION ERROR: Is Control Win V3 service running? " + str(e))
        system.exit(1)

    proj.close()
    print("--- CI/CD FINISHED ---")
else:
    print("Project file not found!")
    system.exit(1)

system.exit()