Function TELEMETRIA()
    Set client = CreateObject("MSXML2.ServerXMLHTTP")
    client.Open "POST", "http://localhost:5000/", False
    client.setRequestHeader "Accept", "Application/Json"
    client.setRequestHeader "Content-Type", "Application/Json"
    client.send "{""created_at"":""" & Now & """,""created_by"":""SOME_ID"",""creator_ver"":""0.0.0""}"
    TELEMETRIA = client.ResponseText
End Function