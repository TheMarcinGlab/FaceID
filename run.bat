@echo off
SETLOCAL

echo -------------------------------
echo 🔍 Sprawdzanie, czy Python 3.10 jest dostępny...

py -3.10 --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo ❌ Python 3.10 nie jest zainstalowany!
    echo 🔽 Pobierz go z: https://www.python.org/downloads/release/python-3100/
    echo LUB zainstaluj przez Microsoft Store lub Winget:
    echo     winget install --id=Python.Python.3.10
    echo -----------------------------------------------
    pause
    exit /b 1
)

echo ✅ Python 3.10 jest dostępny!

echo -------------------------------
echo 🛠 Tworzenie środowiska wirtualnego...
py -3.10 -m venv venv

echo -------------------------------
echo 📦 Instalowanie zależności...
call venv\Scripts\python.exe -m pip install --upgrade pip || goto error
call venv\Scripts\python.exe -m pip install -r requirements.txt || goto error

REM Naprawa problemu z Pillow (_imaging)
echo -------------------------------
echo 💊 Naprawa Pillow: odinstalowywanie aktualnej wersji...
call venv\Scripts\pip uninstall -y pillow
echo 💊 Instalowanie Pillow 9.5.0...
call venv\Scripts\pip install pillow==9.5.0 || goto error

REM Naprawa problemu z dlib (_dlib_pybind11)
echo -------------------------------
echo 💊 Naprawa dlib: odinstalowywanie aktualnej wersji...
call venv\Scripts\pip uninstall -y dlib
echo 💊 Instalowanie prekompilowanej wersji dlib...
call venv\Scripts\pip install https://github.com/RvTechiin/dlib-install/releases/download/v19.24.0/dlib-19.24.0-cp310-cp310-win_amd64.whl || goto dlib_error

REM Instalacja face_recognition_models
echo -------------------------------
echo 💊 Instalacja face_recognition_models...
call venv\Scripts\python.exe -m pip install git+https://github.com/ageitgey/face_recognition_models || goto error

echo -------------------------------
echo 🚀 Uruchamianie programu...
call venv\Scripts\python.exe Home.py || goto error

echo -------------------------------
echo ✅ Program zakończony pomyślnie. Naciśnij dowolny klawisz...
pause
exit /b 0

:dlib_error
echo -------------------------------
echo ❌ Błąd przy instalacji dlib.
echo Prekompilowany pakiet dlib dla Python 3.10 (64-bit) nie został znaleziony pod podanym URL.
echo Proszę pobrać ręcznie odpowiednią wersję dlib z:
echo    https://www.lfd.uci.edu/~gohlke/pythonlibs/#dlib
echo Następnie zainstaluj go, wpisując:
echo    venv\Scripts\pip install sciezka\do\pobranej\dlib_whl_file.whl
pause
exit /b 1

:error
echo -------------------------------
echo ❌ Wystąpił błąd. Sprawdź komunikaty powyżej.
pause
exit /b 1
