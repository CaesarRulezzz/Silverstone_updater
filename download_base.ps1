$alphabet = [char[]]([char]'A'..[char]'Z')
$keywords = "Normal","Emergency","Event","System Volume Information"
$global:drivefound = $false
$global:drivepath = $null

Write-Host "Downloading updates"
python main.py

foreach ($letter in $alphabet) {
    $folders = $null
    $path = $letter+":\"
    $folders = Get-ChildItem -Path $path -Directory -Force
    Write-Host $letter":\ " $folders
    if ($folders.Length -eq 4)
    {
        $global:drivefound = $true
        foreach ($folder in $folders) {
            if (-Not ($folder.Name -in $keywords))
            {
                $global:drivefound = $false
                break
            }
        }
        if ($global:drivefound -eq $true)
        {
            $global:drivepath = $folders[0].Root
            break
        }
    }
}

if ($global:drivepath.length -gt 0)
{
    Write-Host "Extracting from "$filename " to " ${global:drivepath}
    Get-ChildItem -Filter *.zip | Expand-Archive -DestinationPath ${global:drivepath} -Force | Remove-Item -recurse
    Get-ChildItem -Filter *.zip | Remove-Item -recurse
    Get-ChildItem ${global:drivepath} -Filter *.doc | Remove-Item -recurse
}
else {
    Write-Output "No drive found!"
}