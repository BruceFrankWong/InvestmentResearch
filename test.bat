@echo off
REM Run pytest.

set PYTHONPATH=%~dp0src
python -m pytest -v