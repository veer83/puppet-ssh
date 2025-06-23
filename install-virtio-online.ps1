# Run this as Administrator

# Step 1: Download the VirtIO ISO
$isoUrl = "https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/virtio-win.iso"
$isoPath = "$env:TEMP\virtio-win.iso"

Invoke-WebRequest -Uri $isoUrl -OutFile $isoPath
Write-Host "✅ Downloaded VirtIO ISO to $isoPath"

# Step 2: Mount the ISO
$mount = Mount-DiskImage -ImagePath $isoPath -PassThru
$driveLetter = ($mount | Get-Volume).DriveLetter + ":"

Write-Host "📀 Mounted VirtIO ISO as drive $driveLetter"

# Step 3: Define paths and install drivers
$osVersion = "2k19\amd64"
$driverFolders = @("NetKVM", "vioscsi", "vioblk")

foreach ($folder in $driverFolders) {
    $path = Join-Path "$driveLetter\$folder\$osVersion" "*.inf"
    $infFiles = Get-ChildItem $path -ErrorAction SilentlyContinue

    foreach ($inf in $infFiles) {
        Write-Host "🔧 Installing driver: $($inf.FullName)"
        pnputil /add-driver "$($inf.FullName)" /install
    }
}

# Step 4: Dismount the ISO
Dismount-DiskImage -ImagePath $isoPath
Write-Host "📤 ISO dismounted."

# Step 5: Clean up
Remove-Item $isoPath -Force
Write-Host "`n🎉 VirtIO drivers installed and cleanup complete. Please reboot the VM." -ForegroundColor Cyan
