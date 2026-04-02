# Построение интерполирующего кубического сплайна

## Структура проекта

Тут структура проекта...
```
src/
    main.cpp
includes/
    idk_smtnhg.h
```

*Илюстрация архитектуры проекта*
![](Documentation/Images/Architecture.png)

---
## Инструкция по сборке

*Используемая версия Python:* **3.14**.

### 1. Создать виртуальное окружение
```Shell
py -m venv .venv
```

*Команда `py` может не работать на Linux.*
### 2. Активировать виртуальное окружение
```Shell
./.venv/Scripts/activate
```
### 3. Установить библиотеки
```Shell
pip install -r "requirements.txt"
```
### 4. Папка для сборки
```bash
mkdir build
cd build
```
### 5. Генерация файлов сборки
```bash
cmake .. 
```
### 6. Компиляция программы
```bash
cmake --build .
```
