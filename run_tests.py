# -*- coding: utf-8 -*-
import sys

print("--- CODESYS SCRIPT START ---")
print("Hello from CODESYS Internal Python!")
print("Script arguments: " + str(sys.argv))

# В будущем здесь будет команда открытия TestProject.project
# и запуск тестов через coUnit

print("--- CODESYS SCRIPT FINISH ---")
# Закрываем CODESYS после выполнения скрипта
system.exit()