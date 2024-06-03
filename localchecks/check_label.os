$OS = (Get-WmiObject -class Win32_OperatingSystem).Caption
$BN = (Get-WmiObject -class Win32_OperatingSystem).BuildNumber
Write-Host "0 OperatingSystem - $OS $BN"
$CONTENT = @"
<<<labels:sep(0)>>>
{"operatingsystem": "$OS"}
{"windows/buildnumber": "$BN"}
"@
$FILENAME = "c:\programdata\checkmk\agent\spool\labels"
# Prepend a newline to ensure the file starts with a new line
$CONTENT = "`n$CONTENT"

# Write the firewall status to the file
[IO.File]::WriteAllText($FILENAME, $CONTENT)
# Powershell 7
#echo $CONTENT | out-file $FILENAME -encoding utf8NoBOM
