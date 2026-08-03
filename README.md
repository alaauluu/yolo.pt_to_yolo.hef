# 📌 Конвертация YOLO (.pt) → Hailo (.hef) на Ubuntu

Пошаговая инструкция по конвертации модели YOLO (`.pt`) в формат `.onnx`, а затем в `.hef` для запуска на **Hailo-8**.

<p>
  <img src="https://img.shields.io/badge/OS-Ubuntu-E95420?style=flat-square&logo=ubuntu&logoColor=white" alt="Ubuntu">
  <img src="https://img.shields.io/badge/Python-3.10-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.10">
  <img src="https://img.shields.io/badge/YOLO-Ultralytics-00FFFF?style=flat-square&logo=yolo&logoColor=black" alt="Ultralytics">
  <img src="https://img.shields.io/badge/Hailo-8-1a1a1a?style=flat-square&logo=hackthebox&logoColor=00C7B7" alt="Hailo-8">
  <img src="https://img.shields.io/badge/HailoRT-4.21.0-lightgrey?style=flat-square" alt="HailoRT 4.21.0">
  <img src="https://img.shields.io/badge/DFC-3.31.0-lightgrey?style=flat-square" alt="Dataflow Compiler 3.31.0">
  <img src="https://img.shields.io/badge/status-active-brightgreen?style=flat-square" alt="Status">
</p>

## 📑 Содержание

- [Требования](#требования)
- [1. Установка Python 3.10 и системных зависимостей](#1-установка-python-310-и-системных-зависимостей)
- [2. Создание виртуального окружения](#2-создание-виртуального-окружения)
- [3. Установка Ultralytics](#3-установка-ultralytics)
- [4. Конвертация .pt → .onnx](#4-конвертация-pt--onnx)
- [5. Установка Hailo Dataflow Compiler и HailoRT](#5-установка-hailo-dataflow-compiler-и-hailort)
- [6. Установка Hailo Model Zoo](#6-установка-hailo-model-zoo)
- [7. Компиляция .onnx → .hef](#7-компиляция-onnx--hef)

## 🧩 Требования

- 🐧 Ubuntu (x86_64)
- 🔑 Аккаунт на [Hailo Developer Zone](https://hailo.ai/developer-zone/software-downloads/)
- 🎯 Целевое устройство: **Hailo-8**

---

## 1. Установка Python 3.10 и системных зависимостей

```bash
sudo apt install -y python3.10 python3.10-dev python3.10-venv python3.10-distutils \
    python3-pip python3-tk graphviz libgraphviz-dev libgl1-mesa-glx \
    python-is-python3 build-essential nano git
```

## 2. Создание виртуального окружения

```bash
python3.10 -m venv .venv
source .venv/bin/activate
```

## 3. Установка Ultralytics

```bash
pip install ultralytics
```

## 4. Конвертация .pt → .onnx

```python
from ultralytics import YOLO

model = YOLO("yolov8m.pt")
model.export(format="onnx", imgsz=640, opset=19)
```

## 5. Установка Hailo Dataflow Compiler и HailoRT

Создайте аккаунт на [Hailo Developer Zone](https://hailo.ai/developer-zone/software-downloads/) и скачайте для **Hailo-8** следующие пакеты:

- `hailort_4.21.0_amd64.deb`
- `hailort-4.21.0-cp310-cp310-linux_x86_64.whl`
- `hailo_dataflow_compiler-3.31.0-py3-none-linux_x86_64.whl`

> ⚠️ **Важно:** для успешной сборки нужно принудительно установить `jaxlib-0.4.13-cp310-cp310-manylinux2014_x86_64.whl` **до** установки Dataflow Compiler.

```bash
pip install jaxlib-0.4.13-cp310-cp310-manylinux2014_x86_64.whl

sudo dpkg -i ./hailort_4.21.0_amd64.deb

pip install hailort-4.21.0-cp310-cp310-linux_x86_64.whl

pip install hailo_dataflow_compiler-3.31.0-py3-none-linux_x86_64.whl
```

## 6. Установка Hailo Model Zoo

```bash
git clone https://github.com/hailo-ai/hailo_model_zoo.git
cd hailo_model_zoo
git checkout 64a65cbcbc0a80d7e55aca5035c3b2651351bac5
pip install -e .

export USER=hailo

hailomz --version
```

## 7. Компиляция .onnx → .hef

Переместите вашу модель `.onnx` и калибровочный датасет в директорию `hailo_model_zoo`, после чего запустите компиляцию:

```bash
hailomz compile \
    --ckpt yolov8m_640_01082026.onnx \
    --calib-path calib_dataset \
    --yaml hailo_model_zoo/cfg/networks/yolov8m.yaml \
    --classes 2 \
    --hw-arch hailo8 \
    --end-node-names \
        /model.22/cv2.0/cv2.0.2/Conv \
        /model.22/cv3.0/cv3.0.2/Conv \
        /model.22/cv2.1/cv2.1.2/Conv \
        /model.22/cv3.1/cv3.1.2/Conv \
        /model.22/cv2.2/cv2.2.2/Conv \
        /model.22/cv3.2/cv3.2.2/Conv
```

Осталось только дождаться завершения компиляции — на выходе получите готовый файл `.hef`. ✅🚀
