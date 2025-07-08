# Generate Folder Structure Script
# This script generates a markdown file with the complete folder structure of the js-codebase repository

param(
    [string]$OutputPath = "folder_structure.md",
    [string]$RootPath = $PWD,
    [switch]$IncludeFiles = $false
)

function Get-FolderStructure {
    param(
        [string]$Path,
        [string]$Prefix = "",
        [int]$Depth = 0,
        [int]$MaxDepth = 20
    )
    
    if ($Depth -gt $MaxDepth) {
        return @()
    }
    
    $items = @()
    
    try {
        # Get directories, excluding virtual environments, cache directories, and other generated files
        $directories = Get-ChildItem -Path $Path -Directory -ErrorAction SilentlyContinue | 
            Where-Object { 
                $_.Name -notmatch "^\.venv$|^\.venv-master$|^__pycache__$|^\.pytest_cache$|^node_modules$|^\.git$|^\.vs$|^bin$|^obj$|^target$|^build$|^dist$" -and
                $_.Name -notmatch "\.egg-info$" -and
                $_.FullName -notmatch "\\\.venv\\|\\__pycache__\\|\.pytest_cache\\|\\node_modules\\|\.git\\" -and
                $_.FullName -notmatch "\.venv-master\\"
            } | 
            Sort-Object Name
        
        $directoryCount = $directories.Count
        
        for ($i = 0; $i -lt $directoryCount; $i++) {
            $dir = $directories[$i]
            $isLast = ($i -eq ($directoryCount - 1))
            
            # Determine the tree symbols (using ASCII characters for compatibility)
            if ($isLast) {
                $currentPrefix = "+-- "
                $nextPrefix = $Prefix + "    "
            } else {
                $currentPrefix = "|-- "
                $nextPrefix = $Prefix + "|   "
            }
            
            # Add current directory
            $items += "$Prefix$currentPrefix$($dir.Name)/"
            
            # Recursively get subdirectories
            $subdirs = Get-FolderStructure -Path $dir.FullName -Prefix $nextPrefix -Depth ($Depth + 1) -MaxDepth $MaxDepth
            $items += $subdirs
        }
        
        # Optionally include files (disabled by default to keep structure clean)
        if ($IncludeFiles) {
            $files = Get-ChildItem -Path $Path -File -ErrorAction SilentlyContinue | 
                Where-Object { 
                    $_.Name -notmatch "\.(pyc|pyo|pyd|log|tmp|temp)$" -and
                    $_.Name -notmatch "^\.DS_Store$|^Thumbs\.db$"
                } | 
                Sort-Object Name
            
            foreach ($file in $files) {
                $items += "$Prefix|-- $($file.Name)"
            }
        }
    }
    catch {
        Write-Warning "Error accessing path: $Path - $($_.Exception.Message)"
    }
    
    return $items
}

function Generate-MarkdownContent {
    param(
        [string]$RootPath,
        [array]$FolderStructure
    )
    
    $rootName = Split-Path -Leaf $RootPath
    $currentDate = Get-Date -Format "MMMM d, yyyy"
    
    # Build content as array and join at the end
    $contentLines = @()
    $contentLines += "# JS-Codebase Repository Folder Structure"
    $contentLines += ""
    $contentLines += "This document contains the complete folder structure of the js-codebase repository, excluding virtual environments, cache directories, and other generated files."
    $contentLines += ""
    $contentLines += "Last updated: $currentDate"
    $contentLines += ""
    $contentLines += "## Root Structure"
    $contentLines += ""
    $contentLines += "``````"
    $contentLines += "$rootName/"
    
    foreach ($line in $FolderStructure) {
        $contentLines += $line
    }
    
    $contentLines += "``````"
    $contentLines += ""
    $contentLines += "## Notes"
    $contentLines += ""
    $contentLines += "- This structure excludes virtual environments (''.venv''), cache directories (''__pycache__'', ''.pytest_cache''), and other generated files"
    $contentLines += ""
    $contentLines += "``````"
    
    return $contentLines -join "`n"
}

# Main execution
Write-Host "Generating folder structure for: $RootPath" -ForegroundColor Green
Write-Host "Output file: $OutputPath" -ForegroundColor Yellow

try {
    # Get the folder structure
    $structure = Get-FolderStructure -Path $RootPath
    
    # Generate markdown content
    $markdownContent = Generate-MarkdownContent -RootPath $RootPath -FolderStructure $structure
    
    # Write to file
    $markdownContent | Out-File -FilePath $OutputPath -Encoding UTF8 -Force
    
    Write-Host "Success! Folder structure generated successfully!" -ForegroundColor Green
    Write-Host "Output saved to: $(Resolve-Path $OutputPath)" -ForegroundColor Cyan
    Write-Host "Total directories processed: $($structure.Count)" -ForegroundColor Magenta
}
catch {
    Write-Error "Failed to generate folder structure: $($_.Exception.Message)"
    exit 1
}

# Display usage information
Write-Host ""
Write-Host "Usage Examples:" -ForegroundColor Blue
Write-Host "  .\scripts\generate_folder_structure_fixed.ps1                           # Generate with default settings" -ForegroundColor Gray
Write-Host "  .\scripts\generate_folder_structure_fixed.ps1 -IncludeFiles             # Include individual files" -ForegroundColor Gray
Write-Host "  .\scripts\generate_folder_structure_fixed.ps1 -OutputPath 'custom.md'   # Custom output file" -ForegroundColor Gray
Write-Host "  .\scripts\generate_folder_structure_fixed.ps1 -RootPath 'C:\other\path' # Different root directory" -ForegroundColor Gray
