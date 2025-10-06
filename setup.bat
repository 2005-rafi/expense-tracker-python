@echo off
title Expense Tracker - Full Stack Launcher

echo.
echo ================================
echo  Launching Expense Tracker App!
echo ================================
echo.

:: Start Backend Server
echo Starting Django Backend...
start cmd /k "python backend.py"

timeout /t 3 /nobreak >nul

:: Start Frontend (Streamlit)
echo Starting Streamlit Frontend...
start cmd /k "python -m streamlit run frontend.py"

echo.
echo --------------------------------
echo  🚀 Backend running at: http://localhost:8000
echo  🚀 Frontend running at: http://localhost:8501
echo --------------------------------
echo.
exit
