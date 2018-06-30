@IF EXIST "%~dp0\python.exe" (
  "%~dp0\python.exe"  "%~dp0\node_modules\korean-sentiment-analyzer\morphemeServer.py" %*
) ELSE (
  @SETLOCAL
  @SET PATHEXT=%PATHEXT:;.JS;=;%
  python  "%~dp0\node_modules\korean-sentiment-analyzer\morphemeServer.py" %*
)