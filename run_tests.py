# encoding:utf-8
from __future__ import print_function
import os
import sys
import time

print("--- CODESYS CI/CD: RUNNING TESTS ---")

project_name = "UT_LibraryBasic.project"
path = os.path.join(os.getcwd(), project_name)

if os.path.exists(path):
    proj = projects.open(path)
    app = proj.find("Application", True)
    
    print("Target Application found: " + app.get_name())
    
    # 1. ПОДКЛЮЧЕНИЕ К СЛУЖБЕ CONTROL WIN V3
    print("Connecting to local PLC service...")
    onlineapp = online.create_online_application(app)
    
    try:
        # Login сам скомпилирует проект перед загрузкой
        onlineapp.login(OnlineChangeOption.Force, True)
        print("Login & Download successful!")
        
        # 2. ЗАПУСК ПЛК
        print("Starting Application...")
        onlineapp.start()
        
        # Даем время тестам coUnit отработать (15 сек)
        print("Tests are running in background...")
        time.sleep(15) 
        
        # 3. ЧТЕНИЕ РЕЗУЛЬТАТА (твоя переменная)
        # Обрати внимание: имя должно точно совпадать (с учетом регистра)
        error_status = onlineapp.read_value("PLC_PRG.xErrorTestDI")
        print("Variable xErrorTestDI value: " + str(error_status))
        
        if str(error_status) == "True":
            print("FAILURE: Unit tests failed!")
            onlineapp.stop()
            system.exit(1) # Красный статус в Jenkins
        else:
            print("PASSED: All unit tests successful.")

        onlineapp.logout()
        
    except Exception as e:
        print("CRITICAL ERROR during execution: " + str(e))
        system.exit(1)

    proj.close()
    print("--- CI/CD FINISHED ---")
else:
    print("ERROR: Project file not found at " + path)
    system.exit(1)

system.exit()