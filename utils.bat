@chcp 65001 > nul
:: Set coding = UTF-8
@echo off
setlocal enabledelayedexpansion

:: %1 always function
if "%1"=="-h" call :Usage & exit /b 0
if "%1"=="" call :Usage & exit /b 1

:: Set environment
for /f "delims=" %%i in ('findstr /v /b "#" "config.txt"') do set %%i
call :SET_ENV
set func=%1
shift /1

:get_args
shift /1
if "%1"=="" (
	for /f %%i in ('type %0 ^| findstr /v /b "::" ^| findstr /b ":"') do (
		if "%%i"==":!func!" (
			set func_exist=true
		)
	)
	if "!func_exist!"=="true" (
		goto :!func!
	) else (
		echo Function does not exist...
		exit /b 1
	)
) else (
exit /b 1
)

:Usage
echo Usage:
echo  utils.bat ^<Function^> args
goto :eof

:SET_ENV
for %%i in ("!USE_PATH!") do set USE_PATH=%%~dpi
set "PATH=!USE_PATH!;%PATH%"
echo %PATH%
goto :eof

:test
echo test
goto :eof

:pysetup
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
goto :eof
