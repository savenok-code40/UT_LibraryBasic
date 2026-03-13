# encoding:utf-8
from __future__ import print_function
import sys

# 1. Закрываем текущий проект, если он открыт, чтобы избежать конфликтов
if projects.primary:
    projects.primary.close()

# 2. Открываем ваш проект по указанному пути
# Используем r"" для корректной обработки обратных слэшей Windows
proj = projects.open(r"D:\_GitHub\UT_LibraryBasic\UT_LibraryBasic.project")

# 3. Находим объект устройства и устанавливаем адрес из скриншота
# Это уберет всплывающее окно "Выбор устройства"
device = proj.find('Device', True)[0]
device.set_gateway_and_address('Gateway-1', '0301.300A')

# 4. Определяем активное приложение и создаем онлайн-подключение
app = proj.active_application
onlineapp = online.create_online_application(app)

# 5. Логин на устройство
# OnlineChangeOption.Try — пытаемся обновить без остановки, True — принудительно

# --- АВТОРИЗАЦИЯ ---

onlineapp.login(OnlineChangeOption.Try, True)

# 6. Запуск ПЛК, если он стоит (состояние не "Run")
if onlineapp.application_state != ApplicationState.run:
    onlineapp.start()

# 7. Небольшая пауза, чтобы данные в ПЛК обновились
system.delay(1000)

# 8. Чтение значения переменной
# Убедитесь, что переменная iVar1 объявлена в PLC_PRG
res_value = onlineapp.read_value("PLC_PRG.iVar1")

# 9. Вывод результата в окно "Сообщения" CODESYS
print("--- Результат выполнения скрипта ---")
print("Переменная PLC_PRG.iVar1 =", res_value)
print("------------------------------------")

# 10. Выход из системы и закрытие проекта
onlineapp.logout()
#proj.close() # Раскомментируйте, если нужно, чтобы проект закрывался сам