@echo off
cd "C:\Program Files (x86)\QRes"

for /f %%a in ('powershell -command "(Get-CimInstance Win32_VideoController).CurrentHorizontalResolution"') do set W=%%a

if "%W%"=="1920" (
    QRes.exe /x:2560 /y:1440
) else (
    QRes.exe /x:1920 /y:1080
)
