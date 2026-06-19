param(
    [string]$OutputPath = "docs/project_blueprints/EDITABLE_VISUAL_MATCH_North_Slope_Gas_Hydrate_ML_Workflow_2026-06-19.pptx"
)

$ErrorActionPreference = "Stop"

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$AssetDir = Join-Path $Root "docs/project_blueprints/presentation_assets/editable_visual_match_2026_06_19"
$CropDir = Join-Path $AssetDir "cropped_reference_assets"
$ExportDir = Join-Path $AssetDir "rendered_slides"
$OutputFullPath = Join-Path $Root $OutputPath
$QaCsv = Join-Path $AssetDir "editable_visual_match_shape_audit_2026_06_19.csv"
$MapOnly = Join-Path $Root "docs/project_blueprints/presentation_assets/website_well_maps_2026_06_18/unified_north_slope_well_stability_context_map_2026_06_18.png"

New-Item -ItemType Directory -Force -Path $AssetDir, $CropDir, $ExportDir | Out-Null
& python (Join-Path $Root "docs/project_blueprints/render_editable_visual_match_assets_2026_06_19.py") --crop | Out-Host

Add-Type -AssemblyName System.Drawing

$msoFalse = 0
$msoTrue = -1
$ppLayoutBlank = 12
$ppSaveAsOpenXMLPresentation = 24
$msoTextOrientationHorizontal = 1
$msoShapeRectangle = 1
$msoShapeRoundedRectangle = 5
$msoShapeOval = 9
$msoShapeIsoscelesTriangle = 7
$msoConnectorStraight = 1
$msoArrowheadTriangle = 3
$msoSendToBack = 1

function Color($r, $g, $b) {
    return [int]($r + ($g -shl 8) + ($b -shl 16))
}

function S([double]$v) {
    return [double]($v * 0.6)
}

function F([double]$v) {
    return [double]([Math]::Max(5, $v * 0.58))
}

$NAVY = Color 15 34 48
$SLATE = Color 73 92 103
$MUTED = Color 83 103 112
$WHITE = Color 255 255 255
$LIGHT = Color 248 252 253
$LINE = Color 173 207 216
$TEAL = Color 16 129 143
$TEAL_DARK = Color 0 121 134
$TEAL_LIGHT = Color 224 248 250
$BLUE = Color 55 134 207
$BLUE_LIGHT = Color 236 246 255
$GREEN = Color 35 158 112
$GREEN_LIGHT = Color 235 250 244
$AMBER = Color 224 161 45
$AMBER_LIGHT = Color 255 246 222
$RED = Color 217 55 58
$RED_LIGHT = Color 255 239 239
$PURPLE = Color 112 95 195
$PURPLE_LIGHT = Color 245 238 255

$SlideW = 960
$SlideH = 540

function Set-TextStyle($Shape, [string]$Text, [double]$Size, [int]$FontColor, [bool]$Bold = $false, [int]$Align = 1) {
    $Shape.TextFrame.TextRange.Text = $Text
    $Shape.TextFrame.MarginLeft = 4
    $Shape.TextFrame.MarginRight = 4
    $Shape.TextFrame.MarginTop = 2
    $Shape.TextFrame.MarginBottom = 2
    $Shape.TextFrame.WordWrap = $msoTrue
    $Shape.TextFrame.TextRange.Font.Name = "Arial"
    $Shape.TextFrame.TextRange.Font.Size = $Size
    $Shape.TextFrame.TextRange.Font.Bold = $(if ($Bold) { $msoTrue } else { $msoFalse })
    $Shape.TextFrame.TextRange.Font.Color.RGB = $FontColor
    $Shape.TextFrame.TextRange.ParagraphFormat.Alignment = $Align
}

function Add-TextboxPx($Slide, [double]$X, [double]$Y, [double]$W, [double]$H, [string]$Text, [double]$SizePx, [int]$FontColor, [bool]$Bold = $false, [int]$Align = 1) {
    $shape = $Slide.Shapes.AddTextbox($msoTextOrientationHorizontal, (S $X), (S $Y), (S $W), (S $H))
    Set-TextStyle $shape $Text (F $SizePx) $FontColor $Bold $Align
    $shape.Line.Visible = $msoFalse
    return $shape
}

function Add-CardPx($Slide, [double]$X1, [double]$Y1, [double]$X2, [double]$Y2, [int]$Fill = $WHITE, [int]$Line = $LINE, [double]$Weight = 1.2) {
    $shape = $Slide.Shapes.AddShape($msoShapeRoundedRectangle, (S $X1), (S $Y1), (S ($X2 - $X1)), (S ($Y2 - $Y1)))
    $shape.Fill.ForeColor.RGB = $Fill
    $shape.Line.ForeColor.RGB = $Line
    $shape.Line.Weight = $Weight
    return $shape
}

function Add-RectPx($Slide, [double]$X1, [double]$Y1, [double]$X2, [double]$Y2, [int]$Fill, [int]$Line = $Fill) {
    $shape = $Slide.Shapes.AddShape($msoShapeRectangle, (S $X1), (S $Y1), (S ($X2 - $X1)), (S ($Y2 - $Y1)))
    $shape.Fill.ForeColor.RGB = $Fill
    $shape.Line.ForeColor.RGB = $Line
    $shape.Line.Weight = 0.5
    return $shape
}

function Add-PillPx($Slide, [double]$X1, [double]$Y1, [double]$X2, [double]$Y2, [string]$Text, [int]$Fill, [int]$FontColor) {
    $shape = Add-CardPx $Slide $X1 $Y1 $X2 $Y2 $Fill $Fill 0.8
    Set-TextStyle $shape $Text (F 13) $FontColor $true 2
    return $shape
}

function Add-ImagePx($Slide, [string]$Path, [double]$X1, [double]$Y1, [double]$X2, [double]$Y2) {
    if (-not (Test-Path $Path)) {
        throw "Missing image: $Path"
    }
    return $Slide.Shapes.AddPicture($Path, $msoFalse, $msoTrue, (S $X1), (S $Y1), (S ($X2 - $X1)), (S ($Y2 - $Y1)))
}

function Add-LinePx($Slide, [double]$X1, [double]$Y1, [double]$X2, [double]$Y2, [int]$Color = $LINE, [double]$Weight = 1.2, [bool]$Arrow = $false) {
    $line = $Slide.Shapes.AddConnector($msoConnectorStraight, (S $X1), (S $Y1), (S $X2), (S $Y2))
    $line.Line.ForeColor.RGB = $Color
    $line.Line.Weight = $Weight
    if ($Arrow) { $line.Line.EndArrowheadStyle = $msoArrowheadTriangle }
    return $line
}

function Add-OvalPx($Slide, [double]$X1, [double]$Y1, [double]$X2, [double]$Y2, [int]$Fill, [int]$Line = $Fill) {
    $shape = $Slide.Shapes.AddShape($msoShapeOval, (S $X1), (S $Y1), (S ($X2 - $X1)), (S ($Y2 - $Y1)))
    $shape.Fill.ForeColor.RGB = $Fill
    $shape.Line.ForeColor.RGB = $Line
    $shape.Line.Weight = 1
    return $shape
}

function Add-ArrowHeadPx($Slide, [double]$X, [double]$Y, [int]$Color) {
    $shape = $Slide.Shapes.AddShape($msoShapeIsoscelesTriangle, (S $X), (S $Y), (S 24), (S 24))
    $shape.Fill.ForeColor.RGB = $Color
    $shape.Line.ForeColor.RGB = $Color
    $shape.Rotation = 90
    return $shape
}

function Set-Background($Slide) {
    $bg = Add-RectPx $Slide 0 0 1600 900 $WHITE $WHITE
    $bg.ZOrder($msoSendToBack)
    Add-RectPx $Slide 0 0 18 900 $TEAL $TEAL | Out-Null
}

function Add-PanelTitle($Slide, [string]$Title, [string]$Subtitle) {
    Add-TextboxPx $Slide 60 38 1180 48 $Title 38 $NAVY $true | Out-Null
    Add-TextboxPx $Slide 63 91 1390 34 $Subtitle 17 $MUTED | Out-Null
}

function Add-FooterPx($Slide, [string]$Text) {
    Add-LinePx $Slide 54 842 1546 842 $LINE 1.0 | Out-Null
    Add-TextboxPx $Slide 58 850 1420 28 $Text 12 $MUTED | Out-Null
}

function Add-Notes($Slide, [string]$Text) {
    try { $Slide.NotesPage.Shapes.Placeholders(2).TextFrame.TextRange.Text = $Text } catch {}
}

function Add-SectionHeader($Slide, [double]$X, [double]$Y, [string]$Number, [string]$Heading, [int]$Color) {
    $oval = Add-OvalPx $Slide ($X + 20) ($Y + 20) ($X + 54) ($Y + 54) $Color $Color
    Set-TextStyle $oval $Number (F 16) $WHITE $true 2
    Add-TextboxPx $Slide ($X + 66) ($Y + 24) 430 40 $Heading 21 $NAVY $true | Out-Null
}

function Add-SourceLabel($Slide, [double]$X1, [double]$Y1, [double]$X2, [double]$Y2, [string]$Text) {
    Add-RectPx $Slide $X1 ($Y2 - 24) $X2 $Y2 (Color 11 35 48) (Color 11 35 48) | Out-Null
    Add-TextboxPx $Slide ($X1 + 10) ($Y2 - 21) ($X2 - $X1 - 20) 18 $Text 10 $WHITE $true | Out-Null
}

function Add-UnderLabel($Slide, [double]$X, [double]$Y, [double]$W, [string]$Top, [string]$Bottom, [int]$Color) {
    Add-TextboxPx $Slide $X $Y $W 22 $Top 18 $NAVY $true 2 | Out-Null
    Add-LinePx $Slide ($X + 8) ($Y + 27) ($X + $W - 8) ($Y + 27) $Color 2.3 | Out-Null
    Add-TextboxPx $Slide $X ($Y + 32) $W 34 $Bottom 13 $MUTED $false 2 | Out-Null
}

function Add-CageIconPx($Slide, [double]$X, [double]$Y, [int]$Color) {
    $water = Color 119 201 210
    $pts = @(
        @(0,-30), @(27,-15), @(27,15), @(0,30), @(-27,15), @(-27,-15)
    )
    for ($i = 0; $i -lt $pts.Count; $i++) {
        $a = $pts[$i]
        $b = $pts[($i + 1) % $pts.Count]
        Add-LinePx $Slide ($X + $a[0]) ($Y + $a[1]) ($X + $b[0]) ($Y + $b[1]) (Color 107 142 149) 1.2 | Out-Null
    }
    foreach ($p in $pts) {
        Add-OvalPx $Slide ($X + $p[0] - 7) ($Y + $p[1] - 7) ($X + $p[0] + 7) ($Y + $p[1] + 7) $water (Color 91 148 155) | Out-Null
    }
    Add-OvalPx $Slide ($X - 15) ($Y - 15) ($X + 15) ($Y + 15) $Color $Color | Out-Null
}

function Add-FeatureCard($Slide, [double]$X1, [double]$Y1, [double]$X2, [double]$Y2, [string]$Head, [string]$Body, [string]$Small, [int]$Color) {
    Add-CardPx $Slide $X1 $Y1 $X2 $Y2 $WHITE $Color 1.2 | Out-Null
    Add-TextboxPx $Slide ($X1 + 16) ($Y1 + 12) ($X2 - $X1 - 32) 26 $Head 16 $Color $true | Out-Null
    Add-TextboxPx $Slide ($X1 + 16) ($Y1 + 42) ($X2 - $X1 - 32) 34 $Body 13 $NAVY $true | Out-Null
    Add-TextboxPx $Slide ($X1 + 16) ($Y2 - 28) ($X2 - $X1 - 32) 20 $Small 10 $MUTED $true | Out-Null
}

function Add-ParameterBar($Slide, [double]$Y, [string]$Label, [string]$Left, [string]$Right, [double]$Start, [double]$End, [string]$Direction, [string]$Opposite, [string]$Mimic, [string]$Role, [int]$Color, [bool]$Target = $false) {
    $fill = $(if ($Target) { $RED_LIGHT } else { $WHITE })
    $line = $(if ($Target) { $RED } else { $LINE })
    Add-CardPx $Slide 58 $Y 1542 ($Y + 70) $fill $line 1.0 | Out-Null
    Add-TextboxPx $Slide 82 ($Y + 13) 190 30 $Label 16 ($(if ($Target) { $RED } else { $NAVY })) $true | Out-Null
    if ($Target) {
        Add-TextboxPx $Slide 298 ($Y + 15) 190 30 "Y-only target rail" 16 $RED $true | Out-Null
        Add-TextboxPx $Slide 520 ($Y + 15) 610 34 "Labels supervise training and validation, but never enter X_allowed." 15 $NAVY $true | Out-Null
        Add-PillPx $Slide 1260 ($Y + 18) 1495 ($Y + 48) $Role $RED_LIGHT $RED | Out-Null
        return
    }
    $ax0 = 300; $ax1 = 900
    Add-LinePx $Slide $ax0 ($Y + 36) $ax1 ($Y + 36) (Color 220 234 238) 7.5 | Out-Null
    $gx0 = $ax0 + (($ax1 - $ax0) * $Start)
    $gx1 = $ax0 + (($ax1 - $ax0) * $End)
    Add-LinePx $Slide $gx0 ($Y + 36) $gx1 ($Y + 36) $Color 8.2 $false | Out-Null
    Add-ArrowHeadPx $Slide ($gx1 - 2) ($Y + 24) $Color | Out-Null
    Add-LinePx $Slide $gx0 ($Y + 24) $gx0 ($Y + 48) $Color 2 | Out-Null
    Add-TextboxPx $Slide $ax0 ($Y + 9) 150 18 $Left 11 $MUTED $true | Out-Null
    Add-TextboxPx $Slide ($ax1 - 150) ($Y + 9) 150 18 $Right 11 $MUTED $true 3 | Out-Null
    Add-TextboxPx $Slide 926 ($Y + 8) 130 24 $Direction 13 $Color $true | Out-Null
    Add-TextboxPx $Slide 1068 ($Y + 8) 160 24 $Opposite 12 $NAVY $true | Out-Null
    Add-TextboxPx $Slide 1235 ($Y + 8) 170 24 $Mimic 12 $MUTED $true | Out-Null
    Add-PillPx $Slide 1414 ($Y + 20) 1516 ($Y + 50) $Role $TEAL_LIGHT $TEAL | Out-Null
}

function Build-Slide1($Presentation) {
    $s = $Presentation.Slides.Add(1, $ppLayoutBlank)
    Set-Background $s
    Add-TextboxPx $s 60 48 1250 58 "Gas Hydrate Occurrence and Saturation Prediction" 40 $NAVY $true | Out-Null
    Add-TextboxPx $s 63 103 820 28 "Alaska North Slope permafrost reservoirs using physics-constrained AI/ML" 19 $MUTED | Out-Null
    Add-TextboxPx $s 66 160 760 60 "Goal: combine approved well logs, NMR, core context, and public GIS without`nexposing runtime-only data." 20 $MUTED | Out-Null
    Add-PillPx $s 65 230 214 268 "source-backed" $TEAL $WHITE | Out-Null
    Add-PillPx $s 240 230 390 268 "9 slides" (Color 214 231 236) $NAVY | Out-Null
    Add-PillPx $s 415 230 565 268 "runtime-safe" (Color 233 221 185) $NAVY | Out-Null
    Add-TextboxPx $s 66 322 240 35 "About me" 25 $NAVY $true | Out-Null
    Add-ImagePx $s (Join-Path $CropDir "slide01_drawing.png") 66 359 434 727 | Out-Null
    Add-ImagePx $s (Join-Path $CropDir "slide01_rap_caviar.png") 463 359 684 584 | Out-Null
    Add-ImagePx $s (Join-Path $CropDir "slide01_world_cup.png") 463 604 684 728 | Out-Null
    Add-ImagePx $s (Join-Path $CropDir "slide01_photo.png") 984 133 1468 751 | Out-Null
    Add-TextboxPx $s 170 746 170 28 "drawing" 14 $MUTED $true 2 | Out-Null
    Add-TextboxPx $s 520 746 120 28 "World Cup" 14 $MUTED $true 2 | Out-Null
    Add-PillPx $s 725 637 835 682 "gym" (Color 232 242 245) $NAVY | Out-Null
    Add-PillPx $s 856 637 965 682 "running" (Color 232 242 245) $NAVY | Out-Null
    Add-FooterPx $s "Personal images from 2026-06-11 Gmail instruction; public deck only."
    Add-Notes $s "Use this opener as personal context only; no scientific claims are made here."
}

function Build-Slide2($Presentation) {
    $s = $Presentation.Slides.Add(2, $ppLayoutBlank)
    Set-Background $s
    Add-PanelTitle $s "Gas Hydrates And Why The North Slope Matters" "Source-backed context only: hydrate structure, North Slope setting, and the pressure-temperature diagram used before any ML claim."
    Add-CardPx $s 60 138 610 790 $WHITE $LINE | Out-Null
    Add-SectionHeader $s 60 138 "1" "What gas hydrate is" $TEAL
    Add-TextboxPx $s 84 198 480 28 "Water cages can trap gas under cold, high-pressure conditions." 14 $MUTED $true | Out-Null
    Add-PillPx $s 84 228 370 260 "methane Structure I = current baseline" $TEAL_LIGHT $TEAL | Out-Null
    Add-CardPx $s 84 274 586 604 $WHITE $LINE 1.0 | Out-Null
    Add-TextboxPx $s 106 292 430 24 "Editable hydrate structure schematic" 16 $NAVY $true | Out-Null
    Add-LinePx $s 106 327 560 327 $LINE 1.0 | Out-Null
    Add-CageIconPx $s 132 365 $TEAL
    Add-TextboxPx $s 190 337 130 28 "Structure I" 18 $TEAL $true | Out-Null
    Add-TextboxPx $s 190 367 330 34 "methane-dominant baseline for this project" 14 $NAVY $true | Out-Null
    Add-LinePx $s 106 421 560 421 $LINE 1.0 | Out-Null
    Add-CageIconPx $s 132 459 $AMBER
    Add-TextboxPx $s 190 431 130 28 "Structure II" 18 $AMBER $true | Out-Null
    Add-TextboxPx $s 190 461 330 34 "larger hydrocarbons or mixed gas context" 14 $NAVY $true | Out-Null
    Add-LinePx $s 106 515 560 515 $LINE 1.0 | Out-Null
    Add-CageIconPx $s 132 553 $PURPLE
    Add-TextboxPx $s 190 525 130 28 "Structure H" 18 $PURPLE $true | Out-Null
    Add-TextboxPx $s 190 555 330 34 "larger molecule and scenario-chemistry context" 14 $NAVY $true | Out-Null
    Add-CardPx $s 84 626 242 704 $TEAL_LIGHT $TEAL | Out-Null
    Add-TextboxPx $s 96 636 132 24 "Structure I" 14 $TEAL $true | Out-Null
    Add-TextboxPx $s 96 662 132 24 "methane baseline" 11 $NAVY $true | Out-Null
    Add-CardPx $s 256 626 414 704 $AMBER_LIGHT $AMBER | Out-Null
    Add-TextboxPx $s 268 636 132 24 "Structure II" 14 $AMBER $true | Out-Null
    Add-TextboxPx $s 268 662 132 24 "larger gases" 11 $NAVY $true | Out-Null
    Add-CardPx $s 428 626 586 704 $PURPLE_LIGHT $PURPLE | Out-Null
    Add-TextboxPx $s 440 636 132 24 "Structure H" 14 $PURPLE $true | Out-Null
    Add-TextboxPx $s 440 662 132 24 "scenario chemistry" 11 $NAVY $true | Out-Null
    Add-TextboxPx $s 84 732 482 30 "Structure II and H can host larger hydrocarbons or mixed gas; methane Structure I is the project baseline." 11 $MUTED $true | Out-Null

    Add-CardPx $s 620 138 1245 790 $WHITE $LINE | Out-Null
    Add-SectionHeader $s 620 138 "2" "Why the North Slope" $BLUE
    Add-TextboxPx $s 644 198 565 40 "The updated 2D stability-screen map uses OSL-staged DNR units, roads, TAPS, communities, and field labels." 13 $MUTED $true | Out-Null
    Add-ImagePx $s (Join-Path $CropDir "slide02_north_slope_map_panel.png") 632 238 1233 640 | Out-Null
    Add-SourceLabel $s 632 238 1233 640 "Public 2D context map: DNR units + AKDOT roads + TAPS overlays"
    $layers = @(
        @(632,662,813,704,"#","DNR units"),
        @(828,662,1029,704,"|","Dalton + TAPS"),
        @(1044,662,1233,704,"o","field labels")
    )
    foreach ($layer in $layers) {
        Add-CardPx $s $layer[0] $layer[1] $layer[2] $layer[3] $LIGHT $LINE 0.8 | Out-Null
        Add-TextboxPx $s ($layer[0] + 12) ($layer[1] + 9) 24 24 $layer[4] 18 $TEAL $true 2 | Out-Null
        Add-TextboxPx $s ($layer[0] + 42) ($layer[1] + 13) ($layer[2] - $layer[0] - 52) 20 $layer[5] 13 $NAVY $true | Out-Null
    }
    Add-TextboxPx $s 632 728 585 30 "Map layers locate the public scaffold; they do not claim occurrence or saturation." 11 $RED $true | Out-Null

    Add-CardPx $s 1255 138 1540 790 $WHITE $LINE | Out-Null
    Add-SectionHeader $s 1255 138 "3" "P-T diagram" $GREEN
    Add-TextboxPx $s 1273 198 230 38 "The diagram screens whether hydrate is physically admissible under selected assumptions." 12 $MUTED $true | Out-Null
    Add-ImagePx $s (Join-Path $CropDir "slide02_stability_curve_panel.png") 1273 244 1518 496 | Out-Null
    Add-SourceLabel $s 1273 244 1518 496 "Selected USGS/DOE North Slope hydrate stability figure"
    Add-CardPx $s 1273 520 1518 580 (Color 217 247 249) $TEAL | Out-Null
    Add-TextboxPx $s 1287 535 210 20 "Current assumption" 13 $TEAL $true | Out-Null
    Add-TextboxPx $s 1287 560 210 22 "methane / Structure I / 5 ppt" 13 $NAVY $true | Out-Null
    Add-CardPx $s 1273 594 1518 652 $GREEN_LIGHT $GREEN | Out-Null
    Add-TextboxPx $s 1287 608 210 18 "Meaning" 13 $GREEN $true | Out-Null
    Add-TextboxPx $s 1287 632 210 18 "admissible under assumptions" 13 $NAVY $true | Out-Null
    Add-CardPx $s 1273 666 1518 724 $RED_LIGHT $RED | Out-Null
    Add-TextboxPx $s 1287 680 210 18 "Guardrail" 13 $RED $true | Out-Null
    Add-TextboxPx $s 1287 704 210 18 "not proof; not saturation" 13 $NAVY $true | Out-Null
    Add-CardPx $s 60 805 1540 835 $LIGHT $LINE | Out-Null
    Add-TextboxPx $s 80 813 1420 16 "Why this project: North Slope methane hydrate needs integrated geology + stability + well-log/core evidence before occurrence or saturation ML can make reviewed claims." 12 $NAVY $true | Out-Null
    Add-FooterPx $s "Context only: hydrate structure, public North Slope map layers, and a P-T stability diagram. Stability is not hydrate proof."
    Add-Notes $s "Use this slide to set context. The hydrate structure image has no drawn circle. The P-T panel is an admissibility diagram only."
}

function Build-Slide3($Presentation) {
    $s = $Presentation.Slides.Add(3, $ppLayoutBlank)
    Set-Background $s
    Add-PanelTitle $s "Parameters And Expected Hydrate Ranges" "Working normalized screening envelopes only: direction, opposite meaning, mimic risk, and ML role."
    $headers = @(
        @(82,"family"), @(300,"range direction"), @(926,"supports"), @(1068,"opposite"), @(1235,"mimic / mask"), @(1420,"role")
    )
    foreach ($h in $headers) { Add-TextboxPx $s $h[0] 125 150 20 $h[1] 12 $MUTED $true | Out-Null }
    $rows = @(
        @("GR clean sand","clean","shaly",0.00,0.35,"clean sand","shale/clay","radioactive minerals","input",$GREEN,$false),
        @("Density / porosity","tight","porous",0.45,0.75,"porous","tight/shale","gas, washout","input",$BLUE,$false),
        @("Deep resistivity","conductive","resistive",0.65,0.98,"resistive","wet/saline","ice/free gas/tight","input",$RED,$false),
        @("NMR separation","mobile water","separation",0.60,0.90,"separation","water/clay","processing/depth","input/Y guard",$PURPLE,$false),
        @("Vp/Vs/AI elastic","soft","stiff",0.25,0.88,"stiff contrast","soft/gas","compaction/cement","derived",$PURPLE,$false),
        @("Caliper QC","in gauge","washout",0.00,0.25,"trust gate","bad hole","tool standoff","QC",$AMBER,$false),
        @("Stability context","outside","inside",0.60,1.00,"admissible","unstable","gas/depth/temp","context",$TEAL,$false),
        @("Occurrence / saturation","predictor","target",0.0,0.0,"Y-only","leakage","fake performance","Y-only",$RED,$true)
    )
    $y = 154
    foreach ($r in $rows) {
        Add-ParameterBar $s $y $r[0] $r[1] $r[2] $r[3] $r[4] $r[5] $r[6] $r[7] $r[8] $r[9] $r[10]
        $y += 76
    }
    Add-FooterPx $s "Source: data/public_ml_products/public_parameter_evidence_registry_2026-06-16.csv. Ranges are working envelopes unless source-locked; none prove hydrate."
    Add-Notes $s "Explain directional movement, not final thresholds. Target labels stay out of X_allowed."
}

function Build-Slide4($Presentation) {
    $s = $Presentation.Slides.Add(4, $ppLayoutBlank)
    Set-Background $s
    Add-PanelTitle $s "Four-Well Workflow: Audience Version" "The full architecture is reduced to editable steps: source intake, QC, leakage guardrails, model path, validation, and reviewed outputs."

    Add-CardPx $s 60 145 1540 420 $LIGHT $LINE | Out-Null
    Add-TextboxPx $s 86 166 450 28 "Editable main flow" 19 $TEAL $true | Out-Null
    $steps = @(
        @("1","Inputs","approved logs + core/NMR + lithology + public GIS context",$TEAL),
        @("2","Prepare","preserve headers, units, depth axis, and missingness flags",$BLUE),
        @("3","Leakage barrier","remove saturation and occurrence labels from predictors",$RED),
        @("4","Model path","occurrence and saturation stay linked but separate",$PURPLE),
        @("5","Validate","whole-well or geography-aware split before metrics",$GREEN),
        @("6","Review outputs","figures, uncertainty, maps, and manuscript exports",$AMBER)
    )
    $x = 84
    foreach ($step in $steps) {
        Add-CardPx $s $x 210 ($x + 218) 370 $WHITE $step[3] 1.4 | Out-Null
        $dot = Add-OvalPx $s ($x + 15) 226 ($x + 49) 260 $step[3] $step[3]
        Set-TextStyle $dot $step[0] (F 16) $WHITE $true 2
        Add-TextboxPx $s ($x + 60) 223 130 30 $step[1] 18 $step[3] $true | Out-Null
        Add-TextboxPx $s ($x + 18) 276 180 70 $step[2] 14 $NAVY $true 2 | Out-Null
        if ($x -lt 1300) { Add-LinePx $s ($x + 222) 290 ($x + 242) 290 $MUTED 2.0 $true | Out-Null }
        $x += 244
    }

    Add-CardPx $s 60 470 520 775 $WHITE $TEAL | Out-Null
    Add-TextboxPx $s 90 498 380 32 "What is collapsed from the full diagram" 22 $TEAL $true | Out-Null
    $collapsed = @(
        "source library and workbook intake detail",
        "schema mapping and unit normalization",
        "feature families and runtime branches",
        "export packaging for Word, slides, and website"
    )
    $y = 550
    foreach ($item in $collapsed) {
        Add-OvalPx $s 92 ($y + 5) 106 ($y + 19) $TEAL $TEAL | Out-Null
        Add-TextboxPx $s 122 $y 330 34 $item 15 $NAVY $true | Out-Null
        $y += 46
    }

    Add-CardPx $s 570 470 1040 775 $WHITE $RED | Out-Null
    Add-TextboxPx $s 600 498 380 32 "What stays out of predictor inputs" 22 $RED $true | Out-Null
    $blocked = @(
        "hydrate saturation labels",
        "core hydrate observations",
        "pressure-core saturation",
        "occurrence labels and final interpretations"
    )
    $y = 550
    foreach ($item in $blocked) {
        Add-OvalPx $s 602 ($y + 5) 616 ($y + 19) $RED $RED | Out-Null
        Add-TextboxPx $s 632 $y 340 34 $item 15 $NAVY $true | Out-Null
        $y += 46
    }
    Add-CardPx $s 612 715 998 754 $RED_LIGHT $RED | Out-Null
    Add-TextboxPx $s 632 724 345 18 "Y-only evidence supports labels, calibration, validation, and review." 12 $RED $true 2 | Out-Null

    Add-CardPx $s 1090 470 1540 775 $WHITE $PURPLE | Out-Null
    Add-TextboxPx $s 1120 498 350 32 "Two-minute talk-track structure" 22 $PURPLE $true | Out-Null
    $talk = @(
        "Start with what data are allowed.",
        "Explain how source names and units survive QC.",
        "Show why targets are separated from features.",
        "End with reviewed outputs, not unsupported results."
    )
    $y = 550
    foreach ($item in $talk) {
        Add-OvalPx $s 1122 ($y + 5) 1136 ($y + 19) $PURPLE $PURPLE | Out-Null
        Add-TextboxPx $s 1152 $y 330 34 $item 15 $NAVY $true | Out-Null
        $y += 46
    }

    Add-CardPx $s 60 805 1540 835 $LIGHT $LINE | Out-Null
    Add-TextboxPx $s 80 813 1410 16 "This slide explains process, not final ML performance. Approved runtime outputs are reviewed later against lithology, core/NMR calibration, uncertainty, and false positives." 12 $NAVY $true | Out-Null
    Add-FooterPx $s "Sources: project revision base, science-to-ML logic ladder, baseline source ledger, and editable rebuild source-of-truth notes."
    Add-Notes $s "Two-minute script: first, the workflow begins with approved logs and core/NMR/lithology evidence while public GIS remains context only. Second, every header, unit, and depth axis is preserved so features are traceable. Third, saturation and occurrence labels are locked into the Y-only rail and cannot leak into X_allowed. Fourth, occurrence and saturation can be modeled as linked but separate outputs after validation. Close by saying the current deck explains the review system, not final hydrate results."
}

function Build-Slide5($Presentation) {
    $s = $Presentation.Slides.Add(5, $ppLayoutBlank)
    Set-Background $s
    Add-PanelTitle $s "Equation Checks For The Four-Well Workflow" "Large editable checks only: source-backed quantities, real fraction bars, readable words under each symbol, and no result claim."
    Add-PillPx $s 1010 51 1135 84 "log input" $WHITE $GREEN | Out-Null
    Add-PillPx $s 1155 51 1280 84 "core/lab" $WHITE $AMBER | Out-Null
    Add-PillPx $s 1300 51 1430 84 "stability" $WHITE $BLUE | Out-Null
    Add-PillPx $s 1450 51 1550 84 "check" $WHITE $PURPLE | Out-Null

    Add-CardPx $s 60 145 541 415 $LIGHT $BLUE | Out-Null
    Add-RectPx $s 60 145 541 190 $BLUE $BLUE | Out-Null
    Add-TextboxPx $s 78 158 430 26 "Hydrostatic pressure-depth relation" 18 $WHITE $true | Out-Null
    Add-TextboxPx $s 86 224 250 42 "Pabs(z) = P0 +" 30 $NAVY $true 2 | Out-Null
    Add-TextboxPx $s 335 214 180 32 "rho w g z" 25 $NAVY $true 2 | Out-Null
    Add-LinePx $s 348 252 502 252 $NAVY 2.2 | Out-Null
    Add-TextboxPx $s 365 262 120 28 "1e6" 25 $NAVY $true 2 | Out-Null
    Add-UnderLabel $s 88 320 82 "Pabs" "absolute`npressure" $BLUE
    Add-UnderLabel $s 171 320 64 "P0" "surface`npressure" $BLUE
    Add-UnderLabel $s 250 320 82 "rho w" "fluid`ndensity" $BLUE
    Add-UnderLabel $s 340 320 52 "g" "gravity" $BLUE
    Add-UnderLabel $s 402 320 48 "z" "depth" $BLUE
    Add-UnderLabel $s 456 320 78 "1e6" "Pa to MPa" $PURPLE

    Add-CardPx $s 570 145 1016 415 $LIGHT $GREEN | Out-Null
    Add-RectPx $s 570 145 1016 190 $GREEN $GREEN | Out-Null
    Add-TextboxPx $s 588 158 250 26 "Velocity ratio" 18 $WHITE $true | Out-Null
    Add-TextboxPx $s 635 230 130 48 "VpVs =" 36 $NAVY $true 2 | Out-Null
    Add-TextboxPx $s 790 207 96 38 "Vp" 36 $NAVY $true 2 | Out-Null
    Add-LinePx $s 790 252 886 252 $NAVY 2.2 | Out-Null
    Add-TextboxPx $s 790 260 96 38 "Vs" 36 $NAVY $true 2 | Out-Null
    Add-UnderLabel $s 625 320 90 "VpVs" "velocity`nratio" $PURPLE
    Add-UnderLabel $s 755 320 95 "Vp" "P wave`nvelocity" $GREEN
    Add-UnderLabel $s 885 320 95 "Vs" "S wave`nvelocity" $GREEN

    Add-CardPx $s 1045 145 1541 415 $LIGHT $TEAL | Out-Null
    Add-RectPx $s 1045 145 1541 190 $TEAL $TEAL | Out-Null
    Add-TextboxPx $s 1063 158 260 26 "Acoustic impedance" 18 $WHITE $true | Out-Null
    Add-TextboxPx $s 1125 238 335 48 "AI = RHOB * Vp" 36 $NAVY $true 2 | Out-Null
    Add-UnderLabel $s 1100 320 92 "AI" "acoustic`nimpedance" $PURPLE
    Add-UnderLabel $s 1250 320 108 "RHOB" "bulk`ndensity" $GREEN
    Add-UnderLabel $s 1415 320 90 "Vp" "P wave`nvelocity" $GREEN

    Add-CardPx $s 60 455 542 742 $LIGHT $PURPLE | Out-Null
    Add-RectPx $s 60 455 542 500 $PURPLE $PURPLE | Out-Null
    Add-TextboxPx $s 78 468 260 26 "Shear rigidity" 18 $WHITE $true | Out-Null
    Add-TextboxPx $s 145 555 310 48 "G = RHOB * Vs^2" 36 $NAVY $true 2 | Out-Null
    Add-UnderLabel $s 100 638 92 "G" "shear`nmodulus" $PURPLE
    Add-UnderLabel $s 255 638 108 "RHOB" "bulk`ndensity" $GREEN
    Add-UnderLabel $s 415 638 90 "Vs" "S wave`nvelocity" $GREEN

    Add-CardPx $s 570 455 1541 742 $LIGHT $AMBER | Out-Null
    Add-RectPx $s 570 455 1541 500 $AMBER $AMBER | Out-Null
    Add-TextboxPx $s 588 468 690 26 "Electrical saturation baseline - optional review check only" 18 $WHITE $true | Out-Null
    Add-TextboxPx $s 632 535 135 44 "Sw^n =" 34 $NAVY $true 2 | Out-Null
    Add-TextboxPx $s 792 516 160 36 "a * Rw" 34 $NAVY $true 2 | Out-Null
    Add-LinePx $s 786 558 960 558 $NAVY 2.2 | Out-Null
    Add-TextboxPx $s 778 566 190 36 "Rt * phi^m" 34 $NAVY $true 2 | Out-Null
    Add-TextboxPx $s 1038 548 270 44 "Sh ~= 1 - Sw" 34 $NAVY $true 2 | Out-Null
    $labels = @(
        @(610,"Sw","water`nsaturation",$PURPLE), @(720,"n","saturation`nexponent",$AMBER), @(830,"a","Archie`nconstant",$AMBER),
        @(940,"Rw","water`nresistivity",$AMBER), @(1050,"Rt","deep`nresistivity",$GREEN), @(1160,"phi","porosity",$GREEN),
        @(1270,"m","cementation`nexponent",$AMBER), @(1380,"Sh","review`nestimate",$PURPLE)
    )
    foreach ($lab in $labels) { Add-UnderLabel $s $lab[0] 638 96 $lab[1] $lab[2] $lab[3] }

    Add-CardPx $s 60 770 1541 832 $RED_LIGHT $RED | Out-Null
    Add-TextboxPx $s 118 790 1300 27 "Guardrail: equations convert or compare quantities. They do not prove hydrate occurrence, final stability, saturation, producibility, or ranking." 18 $RED $true 2 | Out-Null
    Add-FooterPx $s "Sources: stability calculation plan; email equation set; science logic ladder; baseline source ledger; well-log requirements map."
    Add-Notes $s "Use this slide as equation checks only. Words under symbols are intentionally large and editable. Do not present equations as hydrate proof or final results."
}

function Build-Slide6($Presentation) {
    $s = $Presentation.Slides.Add(6, $ppLayoutBlank)
    Set-Background $s
    Add-PanelTitle $s "Equations, Feature Engineering, And Unit Gate" "Equation features enter X_allowed only after source, unit, depth, QC, and leakage checks."
    Add-CardPx $s 58 145 350 790 $LIGHT $TEAL | Out-Null
    Add-TextboxPx $s 84 174 240 32 "Unit and leakage gate" 24 $TEAL $true | Out-Null
    $steps = @("source header preserved","units visible or mapped","depth axis aligned","caliper/QC first","derived formula`nprovenance","Y-only fields removed","X_allowed matrix")
    $y = 228
    for ($i=0; $i -lt $steps.Count; $i++) {
        $oval = Add-OvalPx $s 86 ($y + 1) 116 ($y + 31) $TEAL $TEAL
        Set-TextStyle $oval ([string]($i + 1)) (F 14) $WHITE $true 2
        Add-TextboxPx $s 130 $y 160 36 $steps[$i] 14 $NAVY $true | Out-Null
        if ($i -lt $steps.Count - 1) { Add-LinePx $s 101 ($y + 38) 101 ($y + 65) $TEAL 2.2 $true | Out-Null }
        $y += 74
    }
    Add-FeatureCard $s 390 145 725 249 "GR clean/shale" "GR_clean = low-GR reservoir proxy" "input/gate; not hydrate by itself" $GREEN
    Add-FeatureCard $s 760 145 1096 249 "Density porosity" "phi_D = (rho_ma - RHOB)/(rho_ma - rho_f)" "requires matrix/fluid assumptions" $BLUE
    Add-FeatureCard $s 390 274 725 377 "Resistivity" "log_Rt = log10(Rt); Archie only if a,m,n,Rw approved" "hydrate support, not proof" $RED
    Add-FeatureCard $s 760 274 1096 377 "Vp from sonic" "Vp = 304800 / DT_us_per_ft" "unit conversion must be explicit" $PURPLE
    Add-FeatureCard $s 390 402 725 506 "Vs where available" "Vs from shear sonic or approved source" "missingness flag if absent" $PURPLE
    Add-FeatureCard $s 760 402 1096 506 "Vp/Vs" "VpVs = Vp / Vs" "derived crossplot feature" $PURPLE
    Add-FeatureCard $s 390 531 725 634 "Acoustic impedance" "AI = RHOB * Vp" "inherits density and sonic QC" $TEAL
    Add-FeatureCard $s 760 531 1096 634 "Elastic moduli" "G = rho*Vs^2; K = rho*(Vp^2 - 4Vs^2/3)" "unit-consistent physics only" $TEAL
    Add-FeatureCard $s 390 658 725 761 "lambda-rho / mu-rho" "lambda_rho = rho*(Vp^2 - 2Vs^2); mu_rho = rho*Vs^2" "elastic contrast, not label" $TEAL
    Add-FeatureCard $s 760 658 1096 761 "NMR-density separation" "sep = phi_D - NMRPHI" "NMR_SAT/Sgh/Sh remain Y-only" $AMBER
    Add-CardPx $s 1150 145 1540 790 $LIGHT $AMBER | Out-Null
    Add-TextboxPx $s 1178 174 300 34 "Stability context chip" 24 $AMBER $true | Out-Null
    Add-FeatureCard $s 1178 231 1513 338 "Hydrostatic pressure" "P_abs(z) = P_surface + rho_w*g*z_m/1e6" "assumption, not measured reservoir pressure" $AMBER
    Add-FeatureCard $s 1178 372 1513 477 "Phase check" "admissible = T_model <= T_eq(P, CH4, 5 ppt)" "context/mask only; no occurrence claim" $AMBER
    Add-CardPx $s 1178 536 1513 700 $WHITE $RED | Out-Null
    Add-TextboxPx $s 1204 564 250 34 "Leakage stop" 24 $RED $true | Out-Null
    Add-TextboxPx $s 1204 604 260 78 "Sgh, S_h, Sh, NMR_SAT, hydrate saturation, Swr/S_wr, and phase labels stay out of X_allowed." 17 $NAVY $true | Out-Null
    Add-FooterPx $s "Sources: processing slide 6 direction, WELL_LOG_REQUIREMENTS_MAP, approved intake spec, stability calculation plan, and parameter evidence registry."
    Add-Notes $s "This is the gate between source variables and model-ready features. Keep targets out of X_allowed."
}

function Build-Slide7($Presentation) {
    $s = $Presentation.Slides.Add(7, $ppLayoutBlank)
    Set-Background $s
    Add-PanelTitle $s "Unified North Slope Well + Stability Context Map" "Regional context only: public GIS layers and stability-screen status for discussion, not an ML overlay or hydrate proof."
    Add-CardPx $s 52 145 1105 720 $WHITE $LINE | Out-Null
    Add-ImagePx $s (Join-Path $CropDir "slide07_unified_map_only_panel.png") 70 168 1088 665 | Out-Null

    Add-CardPx $s 78 675 1080 707 $LIGHT $LINE | Out-Null
    $status = @(
        @(105,"Calculated screen interval",$BLUE),
        @(365,"Calculated, no stable interval",$NAVY),
        @(655,"Blocked: phase curve range",(Color 217 119 6)),
        @(930,"Outside public AU context",$PURPLE)
    )
    foreach ($item in $status) {
        Add-OvalPx $s $item[0] 684 ($item[0] + 14) 698 $item[2] $item[2] | Out-Null
        Add-TextboxPx $s ($item[0] + 22) 680 220 20 $item[1] 11 $NAVY $true | Out-Null
    }

    Add-CardPx $s 1140 145 1540 302 $WHITE $TEAL | Out-Null
    Add-TextboxPx $s 1166 168 300 26 "Readable orientation layers" 21 $TEAL $true | Out-Null
    Add-TextboxPx $s 1168 207 320 64 "USGS hydrate AU outlines, DNR oil/gas unit outlines, AKDOT roads, Dalton/Deadhorse roads, TAPS corridor, field labels, and public wells." 14 $NAVY $true | Out-Null

    Add-CardPx $s 1140 325 1540 482 $WHITE $BLUE | Out-Null
    Add-TextboxPx $s 1166 348 300 26 "Status points stay separate" 21 $BLUE $true | Out-Null
    Add-TextboxPx $s 1168 388 320 64 "Point colors are stability-screen status categories. They are not occurrence labels, saturation labels, or trained-model outputs." 14 $NAVY $true | Out-Null

    Add-CardPx $s 1140 505 1540 662 $WHITE $AMBER | Out-Null
    Add-TextboxPx $s 1166 528 300 26 "How to discuss it" 21 $AMBER $true | Out-Null
    Add-TextboxPx $s 1168 568 320 64 "Use the map to locate the wells and public geologic context before showing planned result-review logic." 14 $NAVY $true | Out-Null

    Add-CardPx $s 1140 690 1540 820 $RED_LIGHT $RED | Out-Null
    Add-TextboxPx $s 1166 712 305 30 "Required caveat" 21 $RED $true | Out-Null
    Add-TextboxPx $s 1168 752 325 42 "Context/orientation only. Stability-screen status does not prove hydrate occurrence, saturation, or trained-model evidence." 14 $RED $true | Out-Null

    Add-FooterPx $s "Map source: public/OSL-staged unified North Slope GIS export. Raw DNR/AKDOT/TAPS/GNIS/DGGS packages remain Drive/OSL-only when not GitHub-safe."
    Add-Notes $s "Use this map as context only. Mention public field labels, DNR units, roads, TAPS, USGS hydrate AU outlines, GGD223 controls, and stability-screen status. Do not call it an ML overlay or a hydrate occurrence map."
}

function Build-Slide8($Presentation) {
    $s = $Presentation.Slides.Add(8, $ppLayoutBlank)
    Set-Background $s
    Add-PanelTitle $s "Stability-To-ML Overlay" "Stability can help review the model as context, mask, confidence, and caveat. It is not occurrence proof or a saturation label."
    Add-CardPx $s 70 155 430 720 $LIGHT $BLUE | Out-Null
    Add-TextboxPx $s 98 180 300 32 "Public stability screen" 23 $BLUE $true | Out-Null
    $stats = @(@("8,084","public screen rows",$BLUE),@("22","calculated admissibility`nintervals",$BLUE),@("8","no-stable rows",$BLUE),@("8,054","blocked rows",$RED))
    $y = 240
    foreach ($st in $stats) {
        Add-CardPx $s 100 $y 400 ($y + 70) $WHITE $LINE | Out-Null
        Add-TextboxPx $s 120 ($y + 12) 90 28 $st[0] 21 $st[2] $true | Out-Null
        Add-TextboxPx $s 220 ($y + 15) 155 34 $st[1] 13 $NAVY $true | Out-Null
        $y += 90
    }
    Add-TextboxPx $s 98 625 300 76 "Methane 5 ppt phase curve + hydrostatic pressure + G10015 temperature model under locked public assumptions." 13 $MUTED $true | Out-Null
    Add-CardPx $s 500 155 1110 720 $WHITE $TEAL | Out-Null
    Add-TextboxPx $s 530 180 520 32 "Allowed overlay roles" 24 $TEAL $true | Out-Null
    $roles = @(
        @(535,245,795,355,"Context","Add stability status beside logs and predictions.",$TEAL),
        @(825,245,1080,355,"Mask","Filter or flag rows outside the current admissible screen.",$BLUE),
        @(535,395,795,505,"Confidence","Carry source-control labels: high, medium, low, blocked.",$GREEN),
        @(825,395,1080,505,"Caveat","Explain phase, temperature, pressure, and blocked reasons.",$AMBER)
    )
    foreach ($r in $roles) {
        Add-CardPx $s $r[0] $r[1] $r[2] $r[3] $LIGHT $r[6] | Out-Null
        Add-TextboxPx $s ($r[0]+18) ($r[1]+14) ($r[2]-$r[0]-36) 26 $r[4] 20 $r[6] $true | Out-Null
        Add-TextboxPx $s ($r[0]+18) ($r[1]+48) ($r[2]-$r[0]-36) 50 $r[5] 14 $NAVY $true | Out-Null
    }
    Add-LinePx $s 430 438 535 300 $BLUE 2.4 $true | Out-Null
    Add-LinePx $s 430 438 535 450 $GREEN 2.4 $true | Out-Null
    Add-LinePx $s 430 438 825 300 $TEAL 2.4 $true | Out-Null
    Add-LinePx $s 430 438 825 450 $AMBER 2.4 $true | Out-Null
    Add-CardPx $s 535 565 1080 680 $RED_LIGHT $RED | Out-Null
    Add-TextboxPx $s 565 590 160 28 "Blocked uses" 20 $RED $true | Out-Null
    Add-TextboxPx $s 745 585 300 60 "Do not use stability as occurrence, saturation, hydrate-present target, negative label for blocked rows, or proof." 16 $NAVY $true | Out-Null
    Add-CardPx $s 1180 155 1530 720 $LIGHT $PURPLE | Out-Null
    Add-TextboxPx $s 1208 180 290 32 "Model review layer" 23 $PURPLE $true | Out-Null
    $cards = @(
        @("Approved`nlogs/targets","drive model fit",$GREEN),
        @("Occurrence`nclassifier","future P(hydrate)",$TEAL),
        @("Saturation`nregressor","future Sh_pred",$BLUE),
        @("Stability overlay","context only",$AMBER),
        @("Public summary","reviewed later",$RED)
    )
    $y = 245
    foreach ($c in $cards) {
        Add-CardPx $s 1210 $y 1500 ($y + 66) $WHITE $c[2] | Out-Null
        Add-TextboxPx $s 1230 ($y + 10) 120 40 $c[0] 15 $c[2] $true | Out-Null
        Add-TextboxPx $s 1360 ($y + 11) 110 36 $c[1] 13 $NAVY $true | Out-Null
        if ($c[0] -ne "Public summary") { Add-LinePx $s 1355 ($y+70) 1355 ($y+84) $c[2] 2 $true | Out-Null }
        $y += 86
    }
    Add-FooterPx $s "Sources: STABILITY_CALCULATION_PLAN, public stability screen, DOE runtime tracking plan, and first model experiment plan. Stability remains admissibility context only."
    Add-Notes $s "Use stability as context/mask/confidence/caveat only, never as occurrence or saturation labels."
}

function Build-Slide9($Presentation) {
    $s = $Presentation.Slides.Add(9, $ppLayoutBlank)
    Set-Background $s
    Add-PanelTitle $s "What We Have Done, What Is Not Claimed, What Is Next" "V5.5 makes the current contribution explicit while keeping every result claim inside the approved-runtime guardrails."
    $columns = @(
        @(70,150,505,700,"What we have done",$TEAL,@(
            "V5.4 deck updated into a V5.5 mentor sequence.",
            "Personal opener and source-backed hydrate/North Slope visuals preserved.",
            "Full complex workflow and ML runtime diagrams kept in the main sequence.",
            "DOE three-dataset prototype, cleaned feature audit, and Model Run Tracker explained.",
            "Stability overlay framed as context, mask, confidence, and caveat only."
        )),
        @(585,150,1020,700,"What is not claimed",$RED,@(
            "No hydrate proof.",
            "No final stability top/base/thickness claim.",
            "No public row-level approved data.",
            "No occurrence prediction or saturation prediction.",
            "No final trained ML metrics, sweet spots, producibility ranking, or target authority."
        )),
        @(1095,150,1530,700,"What is next",$AMBER,@(
            "Run DOE workflow in the approved runtime and keep outputs ignored until review.",
            "Confirm target priority for S_h, S_wr, Sh, Swr and fraction-vs-percent policy.",
            "Review feature exclusions and stability overlay settings with mentor.",
            "Assign whole-well or compartment validation before final metrics.",
            "Bring back only public-safe summaries after data-owner review."
        ))
    )
    foreach ($col in $columns) {
        Add-CardPx $s $col[0] $col[1] $col[2] $col[3] $LIGHT $col[5] | Out-Null
        Add-TextboxPx $s ($col[0]+26) ($col[1]+24) ($col[2]-$col[0]-52) 40 $col[4] 24 $col[5] $true | Out-Null
        $y = $col[1] + 85
        $idx = 1
        foreach ($item in $col[6]) {
            $oval = Add-OvalPx $s ($col[0]+28) ($y+2) ($col[0]+54) ($y+28) $col[5] $col[5]
            Set-TextStyle $oval ([string]$idx) (F 11) $WHITE $true 2
            Add-TextboxPx $s ($col[0]+70) $y ($col[2]-$col[0]-100) 58 $item 14 $NAVY $true | Out-Null
            $y += 80
            $idx += 1
        }
    }
    Add-CardPx $s 70 735 1530 812 $WHITE $LINE | Out-Null
    Add-TextboxPx $s 98 758 210 26 "Source/provenance trail" 18 $TEAL $true | Out-Null
    Add-TextboxPx $s 330 755 1110 44 "V5.5 panels are generated by build_full_workflow_diagram_deliverables.py from V5.4 panels, V5.2 authority plates, public stability products, DOE runbook/tracker docs, and source_visual_inventory." 16 $NAVY $true | Out-Null
    Add-FooterPx $s "Public scaffold: 8,084 stability rows; 22 calculated admissibility intervals; about 3/71 approved datasets visible for schema/runtime prototyping."
    Add-Notes $s "Close by emphasizing current build status, not final hydrate claims."
}

$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = $msoTrue
$presentation = $ppt.Presentations.Add($msoTrue)
$presentation.PageSetup.SlideWidth = $SlideW
$presentation.PageSetup.SlideHeight = $SlideH

Build-Slide1 $presentation
Build-Slide2 $presentation
Build-Slide3 $presentation
Build-Slide4 $presentation
Build-Slide5 $presentation
Build-Slide6 $presentation
Build-Slide7 $presentation
Build-Slide8 $presentation
Build-Slide9 $presentation

if (Test-Path $OutputFullPath) {
    Remove-Item -LiteralPath $OutputFullPath -Force
}
$presentation.SaveAs($OutputFullPath, $ppSaveAsOpenXMLPresentation)

for ($i = 1; $i -le $presentation.Slides.Count; $i++) {
    $exportPath = Join-Path $ExportDir ("slide_{0:D2}_editable_visual_match.png" -f $i)
    $presentation.Slides.Item($i).Export($exportPath, "PNG", 1600, 900)
}

$rows = @()
for ($i = 1; $i -le $presentation.Slides.Count; $i++) {
    $slide = $presentation.Slides.Item($i)
    $shapeCount = $slide.Shapes.Count
    $textCount = 0
    $pictureCount = 0
    $fullSlidePictureCount = 0
    for ($j = 1; $j -le $shapeCount; $j++) {
        $shape = $slide.Shapes.Item($j)
        try {
            if ($shape.HasTextFrame -and $shape.TextFrame.HasText) { $textCount += 1 }
        } catch {}
        try {
            if ($shape.Type -eq 13) {
                $pictureCount += 1
                if ([Math]::Abs($shape.Left) -lt 1 -and [Math]::Abs($shape.Top) -lt 1 -and [Math]::Abs($shape.Width - $SlideW) -lt 1 -and [Math]::Abs($shape.Height - $SlideH) -lt 1) {
                    $fullSlidePictureCount += 1
                }
            }
        } catch {}
    }
    $rows += [pscustomobject]@{
        slide = $i
        shape_count = $shapeCount
        text_shape_count = $textCount
        picture_shape_count = $pictureCount
        full_slide_picture_count = $fullSlidePictureCount
        only_full_slide_image = (($shapeCount -eq 1) -and ($fullSlidePictureCount -eq 1))
        exported_png = (Join-Path $ExportDir ("slide_{0:D2}_editable_visual_match.png" -f $i))
    }
}
$rows | Export-Csv -NoTypeInformation -Path $QaCsv

$presentation.Close()
$ppt.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($presentation) | Out-Null
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) | Out-Null
[GC]::Collect()
[GC]::WaitForPendingFinalizers()

Write-Host "Wrote $OutputFullPath"
Write-Host "Wrote $QaCsv"
