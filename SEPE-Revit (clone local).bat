@echo off
setlocal
chcp 65001 >nul

title Instalador Plugin-Revit

echo.
echo  SSSSS  EEEEE  PPPPP   EEEEE
echo SS      EE     PP  PP  EE
echo  SSSS   EEEE   PPPPP   EEEE
echo     SS  EE     PP      EE
echo SSSSS   EEEEE  PP      EEEEE
echo.
echo Governo do Estado de Pernambuco
echo Secretaria de Projetos Estrategicos
echo.
echo Bem-vindos ao Plugin da SEPE!
echo.

set SCRIPT_DIR=%~dp0
set INSTALLER=%SCRIPT_DIR%pyRevit_CLI_6.4.0.26100_signed.exe

set CLONE_NAME=sepe
set CLONE_PATH=%APPDATA%\pyRevit\%CLONE_NAME%

set EXT_NAME=plugin-revit
set EXT_URL=https://github.com/sepe-gov-pe/plugin-revit.git

REM Verifica se pyRevit CLI existe
pyrevit clones >nul 2>nul

if errorlevel 1 (
    echo Executando instalador do pyRevit...

    if not exist "%INSTALLER%" (
        echo Instalador nao encontrado:
        echo %INSTALLER%
        pause
        exit /b 1
    )

    start /wait "" "%INSTALLER%"
    echo Verificando instalacao do pyRevit...
    timeout /t 10 /nobreak >nul

    pyrevit clones >nul 2>nul

    if errorlevel 1 (
        echo pyRevit ainda nao foi encontrado.
        echo Feche a janela e tente novamente.
        pause
        exit /b 1
    )
)

REM Verifica se clone ja existe
pyrevit clones | findstr /i /c:"%CLONE_NAME%" >nul

if errorlevel 1 (
    if exist "%CLONE_PATH%" (
        rmdir /s /q "%CLONE_PATH%"
    )

    mkdir "%APPDATA%\pyRevit" >nul 2>nul

    xcopy "%SCRIPT_DIR%pyRevitCopy" "%CLONE_PATH%" /E /I /Y >nul

    pyrevit clones add "%CLONE_NAME%" "%CLONE_PATH%"

    if errorlevel 1 (
        echo Falha ao registrar clone.
        pause
        exit /b 1
    )
)

echo Conectando clone ao Revit...
pyrevit attach "%CLONE_NAME%" default --installed

if errorlevel 1 (
    echo Falha ao conectar o clone ao Revit.
    pause
    exit /b 1
)

echo Instalando a extensao da SEPE...
pyrevit extend ui "%EXT_NAME%" "%EXT_URL%" --branch=main

if errorlevel 1 (
    echo Falha na instalacao da extensao. Continuando...
)

echo.
echo Instalacao concluida!
echo Bons projetos! :)
echo.

pause
