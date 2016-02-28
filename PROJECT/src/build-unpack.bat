@echo off
title  Scout Camp Builder
echo.
echo  Checking Python
python --version
echo.
echo  Checking PyInstaller...
pyinstaller -v
echo.
echo  Building ScoutCamp...
echo.
python main.py -v
echo.
echo  Unpacked version...
pyinstaller -i scicon.ico -n camp main.py
echo. >> build-log.txt
echo  -- Build done -- >> build-log.txt
echo  %date% >> build-log.txt
echo  %time% >> build-log.txt
echo.
echo  Build Done.
pause >nul
