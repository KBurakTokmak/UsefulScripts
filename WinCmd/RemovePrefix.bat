::RemovePrefix.bat  prefix  fileMask
@echo off
setlocal
for %%A in ("%~1%~2") do (
  set "fname=%%~A"
  call ren "%%fname%%" "%%fname:*%~1=%%"
)
::Suppose you had files named like "prefixName.txt", then you would use the script by executing RemovePrefix  "prefix"  "*.txt"
