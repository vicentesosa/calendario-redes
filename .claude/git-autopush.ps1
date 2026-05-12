$dir = 'C:\Users\USUARIO\redes\calendario'
Set-Location $dir

$changes = git status --porcelain 2>$null
if ($changes) {
    git add .
    $fecha = Get-Date -Format 'yyyy-MM-dd HH:mm'
    git commit -m "auto: $fecha"
    git push origin main
}
