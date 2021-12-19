@echo off
set PYTHONPATH=..\SRCS;%PYTHONPATH%
echo Running ... [ %1% ]
python37 %1%
pause