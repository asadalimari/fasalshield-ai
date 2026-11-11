@echo off
cd /d "%~dp0"
echo ============================================
echo   FasalShield AI - Setup + Run (Fixed v5)
echo   Ye file khud Python 3.12 dhoondh kar use karegi
echo ============================================
echo.

REM --- onnxruntime sirf Python 3.12 / 3.13 par milta hai, 3.15 par nahi ---
set PYCMD=
py -3.12 --version >nul 2>nul && set PYCMD=py -3.12
if not defined PYCMD py -3.13 --version >nul 2>nul && set PYCMD=py -3.13
if not defined PYCMD goto :wrongpython

echo [1/3] Sahi Python mil gaya:
%PYCMD% --version
echo.
echo [2/3] Libraries install ho rahi hain (pehli dafa 2-3 minute, window band NA karein)...
%PYCMD% -m pip install -r requirements.txt
if errorlevel 1 goto :piperror
echo.
echo [3/3] App khul raha hai - browser mein http://localhost:8501 khud khulega
echo.
%PYCMD% -m streamlit run app.py
pause
exit /b

:wrongpython
echo.
echo *** MASLA: Is PC par Python 3.15 hai, lekin onnxruntime (Leaf AI library)
echo *** Python 3.15 ke liye abhi bani hi nahi hai.
echo *** HAL: Python 3.12 install karein - 3.15 ko delete karne ki zarurat NAHI,
echo *** dono saath reh sakte hain. Phir yehi run.bat dobara chalaiye,
echo *** ye khud 3.12 utha lega.
echo.
pause
exit /b

:piperror
echo.
echo *** MASLA: Libraries install nahi huin - internet check karke dobara try karein,
echo *** ya error ki photo Muse ko bhejein.
echo.
pause
exit /b
