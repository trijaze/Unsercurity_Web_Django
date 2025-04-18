function Show-Tree {
    param (
        [string]$Path = ".",
        [string]$Prefix = ""
    )

    $items = Get-ChildItem -Path $Path
    for ($i = 0; $i -lt $items.Count; $i++) {
        $item = $items[$i]
        $isLast = $i -eq $items.Count - 1
        $connector = if ($isLast) { "+-- " } else { "|-- " }

        Write-Output "$Prefix$connector$($item.Name)"

        if ($item.PSIsContainer) {
            $extension = if ($isLast) { "    " } else { "|   " }
            Show-Tree -Path $item.FullName -Prefix ($Prefix + $extension)
        }
    }
}

# Gọi hàm - sửa đường dẫn nếu cần
Show-Tree "D:\University_Folders\Nam_2\LT_Python\Final\Web_sc\Django-WebApp-master\django_web_app"
