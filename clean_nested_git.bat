@echo off
setlocal
REM Pindah ke folder file ini (root project)
pushd "%~dp0"

REM Jalankan PowerShell script tanpa terganjal ExecutionPolicy
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0clean_nested_git.ps1"

popd
pause

