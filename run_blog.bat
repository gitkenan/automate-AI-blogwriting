@echo off
echo Starting AI Blog Generator...

:: Change to the script's directory
cd /d "%~dp0"

:: Activate virtual environment
call env\Scripts\activate.bat

:: Run the Python script
python daily_ai_blog.py

:: Keep the window open
pause

:: Deactivate virtual environment
deactivate