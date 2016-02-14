@echo off
title  Scout Camp Builder
color e1
echo.
echo  Checking Python
python --version
echo.
echo  Checking PyInstaller...
pip install pyinstaller
pyinstaller -v
echo.
echo  Building ScoutCamp...
echo.
python scout.py -v
echo.
echo  Unpacked version...
pyinstaller -i py.ico scout.py
echo.
echo  Packed version...
pyinstaller -F -i py.ico scout.py
echo. >> build-log.txt
echo  -- Build done -- >> build-log.txt
echo  %date% >> build-log.txt
echo  %time% >> build-log.txt
echo.
echo  Build Done.
pause >nul
