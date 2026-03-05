# encoding:utf-8
from __future__ import print_function
import sys

print("--- CODESYS API DIAGNOSTICS ---")

# 1. Проверяем, что видит объект 'projects'
print("\n[Project methods]:")
print(dir(projects))

# 2. Проверяем, что видит объект 'online'
print("\n[Online methods]:")
print(dir(online))

print("\n--- DIAGNOSTICS FINISHED ---")
system.exit()