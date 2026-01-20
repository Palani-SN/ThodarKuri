@echo off
set PYTHONPATH=..\SRCS;%PYTHONPATH%
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "fullstamp=%YYYY%-%MM%-%DD%_%HH%-%Min%-%Sec%"
echo Testing ... [ ThodarKuri ]
echo ****************************************************************************************
coverage run --source=..\..\ThodarKuri\SRCS -m pytest --template=html1/index.html --report=..\REPORTS\TestCaseResults.html > ..\REPORTS\run_%fullstamp%.txt
IF %ERRORLEVEL%==0 echo Test Execution Completed
coverage html -d ..\REPORTS\htmlcov
echo ****************************************************************************************
echo Check Log file ... [ ..\REPORTS\run_%fullstamp%.txt ]
echo Check Test Execution Results ... [ ..\REPORTS\TestCaseResults.html ]
echo Check Test Execution Coverage ... [ ..\REPORTS\htmlcov ]
echo ****************************************************************************************
@REM pause