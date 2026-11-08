
@echo off
setlocal

REM Move to the folder containing this BAT file
cd /d "%~dp0"

REM Set the actual path to MMDAgent-EX.exe
set "MMDA_EXE=C:\ここにMMDAgent-EX.exeの実際のパス"

REM Check required files
if not exist "%MMDA_EXE%" (
    echo [ERROR] MMDAgent-EX.exe not found.
    echo %MMDA_EXE%
    pause
    exit /b 1
)

if not exist "demo.fst" (
    echo [ERROR] demo.fst not found.
    pause
    exit /b 1
)

if not exist "chat_input.py" (
    echo [ERROR] chat_input.py not found.
    pause
    exit /b 1
)

REM Start MMDAgent-EX
start "LoveGene - MMDAgent" "%MMDA_EXE%" "%CD%\demo.fst"

REM Wait for MMDAgent-EX to initialize
timeout /t 5 /nobreak >nul

REM Start Python chat window
start "LoveGene - Chat" py "%CD%\chat_input.py"

endlocal
