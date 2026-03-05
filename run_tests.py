# encoding:utf-8
from __future__ import print_function
import os
import sys

print("--- CODESYS UNIT TEST: STARTING ---")

project_name = "UT_LibraryBasic.project"
path = os.path.join(os.getcwd(), project_name)

if os.path.exists(path):
    proj = projects.open(path)
    app = proj.find("Application", True)
    
    # 1. Подготовка и запуск в симуляторе
    online.set_simulation_mode(True)
    onlineapp = online.create_online_application(app)
    onlineapp.login(OnlineChangeOption.Force, True)
    onlineapp.start()
    
    # 2. Ожидание выполнения тестов coUnit
    # 10 секунд обычно хватает для простых юнит-тестов
    print("Executing CoUnit tests... please wait...")
    system.delay(10000) 
    
    # 3. ЧТЕНИЕ ТВОЕЙ ПЕРЕМЕННОЙ (со скриншота)
    try:
        # Читаем статус ошибки из PLC_PRG
        test_failed = onlineapp.read_value("PLC_PRG.xErrorTestDI")
        print("Variable PLC_PRG.xErrorTestDI = " + str(test_failed))
        
        # В IronPython BOOL читается как строка 'True' или 'False'
        if str(test_failed) == "True":
            print("FAILED: coUnit detected errors in SensDI tests!")
            # Останавливаем ПЛК и выходим с ошибкой для Jenkins
            onlineapp.stop()
            system.exit(1) 
        else:
            print("PASSED: All SensDI tests completed successfully.")
            
    except Exception as e:
        print("ERROR: Could not read variable from PLC. " + str(e))
        system.exit(1)

    # 4. Завершение работы
    onlineapp.logout()
    proj.close()
    print("--- CODESYS UNIT TEST: FINISHED ---")
else:
    print("CRITICAL ERROR: Project file not found!")
    system.exit(1)

system.exit()