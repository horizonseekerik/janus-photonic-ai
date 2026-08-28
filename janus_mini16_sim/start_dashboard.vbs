Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "c:\Users\hp\Desktop\Janus Update\janus_mini16_sim"

' 1. Start the Python dashboard server silently in the background
WshShell.Run "C:\Users\hp\AppData\Local\Programs\Python\Python312\pythonw.exe run_dashboard.py", 0, False

' 2. Wait 1200ms for the local server port to bind
WScript.Sleep 1200

' 3. Automatically launch the default web browser to the dashboard
WshShell.Run "http://127.0.0.1:8080"

Set WshShell = Nothing
