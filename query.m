let
    // 1. Define your endpoint and request payload
    apiUrl = "http://localhost:5000/",
    requestBody = [
        created_at = DateTime.FixedLocalNow(),
        created_by = "SOME_ID",
        creator_ver = "0.0.0"
    ],
    // 2. Convert the payload into a binary JSON string
    jsonPayload = Json.FromValue(requestBody),
    // 3. Define headers and execute the POST request
    httpResponse = Web.Contents(
        apiUrl,
        [
            Headers = [#"Content-Type" = "application/json"],
            Content = jsonPayload
        ]
    )
in
    httpResponse