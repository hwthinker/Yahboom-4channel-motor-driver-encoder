# clean_nested_git.ps1
Set-StrictMode -Version Latest

# Pastikan working directory = lokasi skrip
Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Path)

$root = (Get-Location).Path
Write-Host "Root path: $root"

# Temukan semua .git yang bukan milik root
$nested = Get-ChildItem -Recurse -Force -ErrorAction SilentlyContinue |
  Where-Object { $_.Name -eq '.git' -and $_.FullName -ne (Join-Path $root '.git') }

if (-not $nested) {
  Write-Host "Tidak ada .git bersarang ditemukan."
  exit 0
}

foreach ($n in $nested) {
  Write-Host "Menghapus: $($n.FullName)"
  if ($n.PSIsContainer) {
    Remove-Item -Recurse -Force $n.FullName
  } else {
    # beberapa repo bersarang pakai file `.git` (pointer submodule)
    Remove-Item -Force $n.FullName
  }
}

Write-Host "Selesai. Semua .git bersarang sudah dihapus."

