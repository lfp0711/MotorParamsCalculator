# 乾勤电机参数计算器

## 1. create venv
python -m venv .venv

## 2. activate (PowerShell)
.venv\Scripts\Activate.ps1

## 3. upgrade pip and install requirements
python -m pip install --upgrade pip
pip install -r requirements.txt

## 4. run app
python main.py


# Docker
To build and run the container locally:
```
docker build -t motor-calculator:latest .
docker run -p 5000:5000 motor-calculator:latest

docker run -p 80:80 nginx

docker compose up
```

