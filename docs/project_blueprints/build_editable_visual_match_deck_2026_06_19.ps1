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
    Add-TextboxPx $Slide $X $Y $W 18 $Top 14 $NAVY $true 2 | Out-Null
    Add-LinePx $Slide ($X + 8) ($Y + 22) ($X + $W - 8) ($Y + 22) $Color 2.1 | Out-Null
    Add-TextboxPx $Slide $X ($Y + 26) $W 24 $Bottom 10 $MUTED $false 2 | Out-Null
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
    Add-PanelTitle $s "Gas Hydrates And Why The North Slope Matters" "Source-backed context only: hydrate structure, North Slope setting, and the pressure-temperature gate used before any ML claim."
    Add-CardPx $s 60 138 610 790 $WHITE $LINE | Out-Null
    Add-SectionHeader $s 60 138 "1" "What gas hydrate is" $TEAL
    Add-TextboxPx $s 84 198 480 28 "Water cages can trap gas under cold, high-pressure conditions." 14 $MUTED $true | Out-Null
    Add-PillPx $s 84 228 370 260 "methane Structure I = current baseline" $TEAL_LIGHT $TEAL | Out-Null
    Add-ImagePx $s (Join-Path $CropDir "slide02_hydrate_structure_panel.png") 84 274 586 604 | Out-Null
    $circle = Add-OvalPx $s 372 283 505 417 (Color 255 255 255) $TEAL
    $circle.Fill.Transparency = 1
    $circle.Line.Weight = 2.5
    Add-SourceLabel $s 84 274 586 604 "World Atlas Fig. 1.1 after Warrier et al. 2016; sI highlighted"
    Add-CardPx $s 84 626 242 704 $TEAL_LIGHT $TEAL | Out-Null
    Add-TextboxPx $s 96 636 132 24 "Structure I" 14 $TEAL $true | Out-Null
    Add-TextboxPx $s 96 662 132 24 "methane baseline" 11 $NAVY $true | Out-Null
    Add-CardPx $s 256 626 414 704 $AMBER_LIGHT $AMBER | Out-Null
    Add-TextboxPx $s 268 636 132 24 "Structure II" 14 $AMBER $true | Out-Null
    Add-TextboxPx $s 268 662 132 24 "larger gases" 11 $NAVY $true | Out-Null
    Add-CardPx $s 428 626 586 704 $PURPLE_LIGHT $PURPLE | Out-Null
    Add-TextboxPx $s 440 636 132 24 "Structure H" 14 $PURPLE $true | Out-Null
    Add-TextboxPx $s 440 662 132 24 "scenario chemistry" 11 $NAVY $true | Out-Null
    Add-TextboxPx $s 84 732 482 30 "Structure II/H are kept as gas-composition sensitivity, not the current baseline." 11 $MUTED $true | Out-Null

    Add-CardPx $s 620 138 1245 790 $WHITE $LINE | Out-Null
    Add-SectionHeader $s 620 138 "2" "Why the North Slope" $BLUE
    Add-TextboxPx $s 644 198 565 40 "The updated 2D stability-screen map uses OSL-staged DNR units, roads, TAPS, communities, and field labels." 13 $MUTED $true | Out-Null
    Add-ImagePx $s (Join-Path $CropDir "slide02_north_slope_map_panel.png") 632 238 1233 640 | Out-Null
    Add-SourceLabel $s 632 238 1233 640 "OSL/website 2D stability-screen map; DNR units + AKDOT roads + TAPS overlays"
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
    Add-SectionHeader $s 1255 138 "3" "P-T gate" $GREEN
    Add-TextboxPx $s 1273 198 230 38 "Stability screens whether hydrate is physically admissible under the selected assumptions." 12 $MUTED $true | Out-Null
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
    Add-FooterPx $s "Slide 2 sources: World Atlas Fig. 1.1 hydrate structure crop; OSL/website 2D stability-screen map with public GIS overlays; selected USGS/DOE stability figure. Stability is not hydrate proof."
    Add-Notes $s "Use this slide to set context. The P-T panel is a gate/admissibility screen only."
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
    Add-PanelTitle $s "Full Complex Project Workflow V5.5" "The complete architecture stays in the main sequence: public sources, approved runtime later, stability context, feature engineering, target rail, split controls, validation, and exports."
    Add-ImagePx $s (Join-Path $CropDir "slide04_architecture_body.png") 0 92 1600 842 | Out-Null
    Add-FooterPx $s "Expanded architecture reference inside the deck: slides 5, 6, 8, and 9 provide readable zoom explanations."
    Add-Notes $s "Keep this as the complete project architecture plate. It is a complex figure; downstream slides explain it in smaller editable pieces."
}

function Build-Slide5($Presentation) {
    $s = $Presentation.Slides.Add(5, $ppLayoutBlank)
    Set-Background $s
    Add-PanelTitle $s "Equation Checks For The Four-Well Workflow" "Measured curves, core calibration, and stability context are converted into review features. These equations are not final hydrate results."
    Add-PillPx $s 1000 51 1125 84 "log input" $WHITE $GREEN | Out-Null
    Add-PillPx $s 1145 51 1266 84 "core or lab" $WHITE $AMBER | Out-Null
    Add-PillPx $s 1285 51 1408 84 "stability context" $WHITE $BLUE | Out-Null
    Add-PillPx $s 1427 51 1550 84 "derived check" $WHITE $PURPLE | Out-Null

    Add-CardPx $s 60 145 541 406 $LIGHT $BLUE | Out-Null
    Add-RectPx $s 60 145 541 187 $BLUE $BLUE | Out-Null
    Add-TextboxPx $s 78 157 435 26 "Hydrostatic pressure-depth relation" 16 $WHITE $true | Out-Null
    Add-TextboxPx $s 91 216 415 56 "P_abs(z) = P0 +  rho_w * g * z" 34 $NAVY $true 2 | Out-Null
    Add-LinePx $s 330 247 507 247 $NAVY 1.8 | Out-Null
    Add-TextboxPx $s 357 260 110 28 "1,000,000" 28 $NAVY $true 2 | Out-Null
    Add-UnderLabel $s 92 308 72 "P_abs" "absolute`npressure" $BLUE
    Add-UnderLabel $s 164 308 55 "P0" "surface`npressure" $BLUE
    Add-UnderLabel $s 237 308 62 "rho_w" "pore-fluid`ndensity" $BLUE
    Add-UnderLabel $s 309 308 60 "g" "gravity" $BLUE
    Add-UnderLabel $s 380 308 58 "z" "depth" $BLUE
    Add-UnderLabel $s 452 308 58 "10^6" "Pa to MPa" $PURPLE
    Add-TextboxPx $s 116 360 350 30 "Converts depth to pressure for phase-boundary comparison; not measured reservoir pressure." 13 $NAVY $true 2 | Out-Null

    Add-CardPx $s 570 145 1016 406 $LIGHT $GREEN | Out-Null
    Add-RectPx $s 570 145 1016 187 $GREEN $GREEN | Out-Null
    Add-TextboxPx $s 588 157 260 26 "Velocity ratio" 16 $WHITE $true | Out-Null
    Add-TextboxPx $s 657 238 110 45 "R_v =" 36 $NAVY $true 2 | Out-Null
    Add-TextboxPx $s 775 214 110 36 "V_p" 34 $NAVY $true 2 | Out-Null
    Add-LinePx $s 790 254 881 254 $NAVY 1.8 | Out-Null
    Add-TextboxPx $s 775 260 110 40 "V_s" 34 $NAVY $true 2 | Out-Null
    Add-UnderLabel $s 626 313 70 "R_v" "velocity ratio" $PURPLE
    Add-UnderLabel $s 758 313 75 "V_p" "P-wave velocity" $GREEN
    Add-UnderLabel $s 890 313 75 "V_s" "S-wave velocity" $GREEN
    Add-TextboxPx $s 600 358 360 34 "Compares compressional and shear response; useful only with unit and lithology checks." 13 $NAVY $true 2 | Out-Null

    Add-CardPx $s 1045 145 1541 406 $LIGHT $TEAL | Out-Null
    Add-RectPx $s 1045 145 1541 187 $TEAL $TEAL | Out-Null
    Add-TextboxPx $s 1063 157 260 26 "Acoustic impedance" 16 $WHITE $true | Out-Null
    Add-TextboxPx $s 1165 244 275 48 "AI = rho_b * V_p" 34 $NAVY $true 2 | Out-Null
    Add-UnderLabel $s 1108 313 80 "AI" "acoustic impedance" $PURPLE
    Add-UnderLabel $s 1258 313 85 "rho_b" "bulk density" $GREEN
    Add-UnderLabel $s 1420 313 80 "V_p" "P-wave velocity" $GREEN
    Add-TextboxPx $s 1105 358 380 26 "Combines density and velocity into an impedance contrast check." 13 $NAVY $true 2 | Out-Null

    Add-CardPx $s 60 440 542 742 $LIGHT $PURPLE | Out-Null
    Add-RectPx $s 60 440 542 483 $PURPLE $PURPLE | Out-Null
    Add-TextboxPx $s 78 452 260 26 "Shear rigidity" 16 $WHITE $true | Out-Null
    Add-TextboxPx $s 169 535 265 48 "G = rho_b * V_s^2" 34 $NAVY $true 2 | Out-Null
    Add-UnderLabel $s 120 609 75 "G" "shear modulus" $PURPLE
    Add-UnderLabel $s 265 609 75 "rho_b" "bulk density" $GREEN
    Add-UnderLabel $s 409 609 75 "V_s" "S-wave velocity" $GREEN
    Add-PillPx $s 96 668 505 702 "Highlights frame stiffness; mimics still require review." $PURPLE_LIGHT $NAVY | Out-Null

    Add-CardPx $s 570 440 1541 742 $LIGHT $AMBER | Out-Null
    Add-RectPx $s 570 440 1541 483 $AMBER $AMBER | Out-Null
    Add-TextboxPx $s 588 452 700 26 "Electrical saturation baseline - locked until parameters are approved" 16 $WHITE $true | Out-Null
    Add-TextboxPx $s 618 520 145 46 "S_w^n =" 34 $NAVY $true 2 | Out-Null
    Add-TextboxPx $s 785 506 145 34 "a * R_w" 34 $NAVY $true 2 | Out-Null
    Add-LinePx $s 780 548 930 548 $NAVY 1.8 | Out-Null
    Add-TextboxPx $s 778 555 160 34 "R_t * phi^m" 34 $NAVY $true 2 | Out-Null
    Add-TextboxPx $s 960 525 245 44 "S_h ~= 1 - S_w" 34 $NAVY $true 2 | Out-Null
    $labels = @(
        @(616,"S_w","water saturation",$PURPLE), @(731,"n","sat. exponent",$AMBER), @(846,"a","Archie constant",$AMBER),
        @(961,"R_w","water resistivity",$AMBER), @(1076,"R_t","deep resistivity",$GREEN), @(1191,"phi","porosity",$GREEN),
        @(1306,"m","cementation exp.",$AMBER), @(1421,"S_h","review estimate",$PURPLE)
    )
    foreach ($lab in $labels) { Add-UnderLabel $s $lab[0] 617 80 $lab[1] $lab[2] $lab[3] }
    Add-TextboxPx $s 690 692 720 25 "Use as a comparison baseline only after water resistivity, porosity convention, shale correction, and target role are documented." 13 $NAVY $true 2 | Out-Null

    Add-CardPx $s 60 765 1541 830 $RED_LIGHT $RED | Out-Null
    Add-TextboxPx $s 128 789 1300 30 "Guardrail: equations convert or compare source-backed quantities. They do not prove hydrate occurrence, final stability, saturation, producibility, or ranking." 19 $RED $true 2 | Out-Null
    Add-FooterPx $s "Sources: stability calculation plan; email screenshot equation set; science logic ladder; baseline source ledger; well-log requirements map."
    Add-Notes $s "Use this slide as equation checks only. Do not present equations as hydrate proof or final results."
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
    Add-PanelTitle $s "Complex ML Runtime Architecture V5.5" "Feature groups, X_allowed, target-only rail, whole-well split, train-only preprocessing, baselines, ANN/Keras candidate, dual heads, validation, and reviewed outputs remain intact."
    Add-ImagePx $s (Join-Path $CropDir "slide07_runtime_body.png") 0 92 1600 842 | Out-Null
    Add-FooterPx $s "ML runtime detail inside the deck: X_allowed, Y-only rail, split controls, output heads, validation, and reviewed outputs."
    Add-Notes $s "This is the complete runtime architecture plate. Do not call it final trained results."
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
