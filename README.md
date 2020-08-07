# Archive Projects

Сервер для портфолио устаревших работ.

Для сборки этих проектов необходимо в папку, где находится этот проект, разместить папки следующих проектов с их оригинальными (т.е. как на Github) названиями:

1. [Визитка команды `portfolio`](https://github.com/dev-center-mpu/portfolio).
2. [Конфигуратор для грузовика `truck-forge`](https://github.com/dev-center-mpu/truck-forge).
3. [Старое облако `mpu-cloud-old`](https://github.com/dev-center-mpu/mpu-cloud-old).
4. [Старый ИЭТР на Autodesk Forge `ietm-forge-old`](https://github.com/dev-center-mpu/ietm-forge-old).

`python3 build.py` - сборка всего проекта. Результат, который уже можно использовать, искать в `/archive-projects/build/`.

Возможные опции сборки:

`--os=win` - Выбор ОС для сборки (Windows по-умолчанию). Также принимает значения `macos` и `linux`.

`--arch=x64` - Выбор архитектуры процессора (x64 по-умолчанию). Также принимает значение `x86`.
