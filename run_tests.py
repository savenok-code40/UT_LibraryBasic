# encoding:utf-8
from __future__ import print_function
import os
import sys

print("--- CODESYS PROJECT ANALYSIS START ---")

# 1. Путь к проекту (используем твое имя файла)
project_name = "UT_LibraryBasic.project"
path = os.path.join(os.getcwd(), project_name)

if os.path.exists(path):
    print("Opening project: " + path)
    proj = projects.open(path)
    
    # 2. Навигация по дереву (упрощенная версия твоего примера)
    print("Listing devices in project:")
    
    # Рекурсивная функция для поиска устройств
    def look_for_devices(obj, depth=0):
        if obj.is_device:
            name = obj.get_name(False)
            print("  " * depth + "[Device found]: " + name)
        
        # Идем глубже по дереву
        for child in obj.get_children(False):
            look_for_devices(child, depth + 1)

    # Запускаем поиск от корня проекта
    for obj in projects.primary.get_children():
        look_for_devices(obj)

    # 3. Закрываем проект
    proj.close()
    print("--- ANALYSIS FINISHED ---")
else:
    print("ERROR: Project file not found at " + path)
    system.exit(1)

system.exit()