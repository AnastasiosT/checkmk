### THIS is a windows local check which should be placed in plugins

# Get the firewall service details
$FW = Get-Service -Name "mpssvc"
$FWNAME = $FW.DisplayName
$FWSTATUS = $FW.Status
$date = Get-Date -UFormat %s -Millisecond 0

# Define the filename for the output
$FILENAME = "c:\programdata\checkmk\agent\spool\check_os_reboot"

# Check if the firewall service is running
if ($FWSTATUS -eq "Running") {
    Write-Host "0 Firewall - $FWNAME $FWSTATUS"
    $CONTENT = @"
<<<local:cached($date,300)>>>
0 Firewall - $FWNAME $FWSTATUS
"@
} else {
    Write-Host "2 Firewall - $FWNAME $FWSTATUS"
    $CONTENT = @"
<<<local:cached($date,300)>>>
2 Firewall - $FWNAME $FWSTATUS
"@
}

# Prepend a newline to ensure the file starts with a new line
$CONTENT = "`n$CONTENT"

# Write the firewall status to the file
[IO.File]::WriteAllText($FILENAME, $CONTENT)

