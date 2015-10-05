@echo off
title  Scout Camp Builder
color e1
echo.
echo  Building Scout Camp...
pyinstaller -i py.ico scout.py
echo. >> build-log.txt
echo  -- Build done -- >> build-log.txt
echo  %date% >> build-log.txt
echo  %time% >> build-log.txt
echo.
echo  Build Done.
pause >nul
