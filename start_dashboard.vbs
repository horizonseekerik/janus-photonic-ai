Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

currentDir = fso.GetParentFolderName(WScript.ScriptFullName)
simDir = currentDir & "\janus_mini16_sim"
WshShell.CurrentDirectory = simDir

pythonwPath = "C:\Users\hp\AppData\Local\Programs\Python\Python312\pythonw.exe"
If Not fso.FileExists(pythonwPath) Then
    pythonwPath = "pyw.exe"
End If

' 1. Start Python server
WshShell.Run """" & pythonwPath & """ run_dashboard.py", 0, False

' 2. Wait for server startup
WScript.Sleep 1500

' 3. Open browser
WshShell.Run "http://127.0.0.1:8080"

Set WshShell = Nothing