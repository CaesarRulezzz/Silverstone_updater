$drive_label = "REGIST"

Write-Host "Downloading updates"
python main.py

$scriptDriveLetter = (Get-Volume -FileSystemLabel $drive_label).DriveLetter
$outputPath = "${scriptDriveLetter}:\"
if ($scriptDriveLetter.length -gt 0)
{
    Write-Host "Extracting from " ${env:TEMP}"\"$filename " to " ${outputPath}
    Get-ChildItem -Filter *.zip | Expand-Archive -DestinationPath ${outputPath} -Force | Remove-Item -recurse
    Get-ChildItem -Filter *.zip | Remove-Item -recurse
    Get-ChildItem ${outputPath} -Filter *.doc | Remove-Item -recurse
}
else {
    Write-Output "No drive found!"
}