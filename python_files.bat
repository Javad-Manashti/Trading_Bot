@echo off
SetLocal EnableDelayedExpansion

:: Define the output file path
set "outputFile=D:\OneDrive\myproject\TradePilot\trading_bot\component.txt"

:: Clear the output file initially
break > "%outputFile%"

:: Add a header message
echo Please read carefully codes and structures and send 'OK' and wait for the next prompt. >> "%outputFile%"
echo. >> "%outputFile%"

:: Generate the tree structure of the src, test, and config folders and save it to the outputFile
echo 1- Tree of src folder: >> "%outputFile%"
tree "D:\OneDrive\myproject\TradePilot\trading_bot\src" /f /a >> "%outputFile%"
echo. >> "%outputFile%"
echo 1- Tree of test folder: >> "%outputFile%"
tree "D:\OneDrive\myproject\TradePilot\trading_bot\tests" /f /a >> "%outputFile%"
echo. >> "%outputFile%"
echo 1- Tree of config folder: >> "%outputFile%"
tree "D:\OneDrive\myproject\TradePilot\trading_bot\config" /f /a >> "%outputFile%"
echo. >> "%outputFile%"

:: Append the header for the code section
echo 2- Code of listed files: >> "%outputFile%"
echo. >> "%outputFile%"

:: Define the directories to scan for Python files
set "srcDir=D:\OneDrive\myproject\TradePilot\trading_bot\src"
set "testDir=D:\OneDrive\myproject\TradePilot\trading_bot\TEST"
set "configDir=D:\OneDrive\myproject\TradePilot\trading_bot\CONFIG"

:: Iterate over each file in the src, test, and config directories and append its path and contents to the outputFile
for /r "%srcDir%" %%i in (*.py) do (
    echo %%i >> "%outputFile%"
    type "%%i" >> "%outputFile%"
    echo ------------------ >> "%outputFile%"
)

for /r "%testDir%" %%i in (*.py) do (
    echo %%i >> "%outputFile%"
    type "%%i" >> "%outputFile%"
    echo ------------------ >> "%outputFile%"
)

for /r "%configDir%" %%i in (*.py) do (
    echo %%i >> "%outputFile%"
    type "%%i" >> "%outputFile%"
    echo ------------------ >> "%outputFile%"
)
echo Done. Output is in "%outputFile%".

EndLocal
