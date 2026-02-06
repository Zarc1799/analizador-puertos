@echo off
TITLE Analizador de Puertos - Iniciando...
echo ===================================================
echo   ANALIZADOR DE PUERTOS - HACKER EDITION
echo ===================================================
echo [1/3] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no encontrado. Instala Python 3.10+ y agregalo al PATH.
    pause
    exit /b
)

echo [2/3] Instalando dependencias Backend...
pip install -r backend\requirements.txt >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Error instalando dependencias. Intentando continuar...
)

echo [3/3] Iniciando Sistema...
echo ---------------------------------------------------
echo  La interfaz se abrira automaticamente en:
echo  http://localhost:8000
echo ---------------------------------------------------

start http://localhost:8000
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

pause
