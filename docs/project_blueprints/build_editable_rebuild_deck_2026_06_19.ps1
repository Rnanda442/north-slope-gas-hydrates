param(
    [string]$OutputPath = "docs/project_blueprints/EDITABLE_REBUILD_North_Slope_Gas_Hydrate_ML_Workflow_2026-06-19.pptx"
)

$ErrorActionPreference = "Stop"

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$AssetDir = Join-Path $Root "docs/project_blueprints/presentation_assets/editable_rebuild_2026_06_19"
$ExportDir = Join-Path $AssetDir "rendered_slides"
$OutputFullPath = Join-Path $Root $OutputPath
$QaCsv = Join-Path $AssetDir "editable_rebuild_shape_audit_2026_06_19.csv"

New-Item -ItemType Directory -Force -Path $AssetDir, $ExportDir | Out-Null
& python (Join-Path $Root "docs/project_blueprints/render_editable_rebuild_assets_2026_06_19.py") --pt | Out-Host

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
$msoBringToFront = 0

function Color($r, $g, $b) {
    return [int]($r + ($g -shl 8) + ($b -shl 16))
}

$NAVY = Color 15 23 42
$SLATE = Color 71 85 105
$MUTED = Color 100 116 139
$LIGHT = Color 248 250 252
$WHITE = Color 255 255 255
$TEAL = Color 15 118 110
$TEAL_LIGHT = Color 236 253 245
$BLUE = Color 29 78 216
$BLUE_LIGHT = Color 239 246 255
$AMBER = Color 180 83 9
$AMBER_LIGHT = Color 255 251 235
$RED = Color 185 28 28
$RED_LIGHT = Color 254 242 242
$PURPLE = Color 109 40 217
$PURPLE_LIGHT = Color 245 243 255
$GREEN = Color 22 101 52
$GREEN_LIGHT = Color 240 253 244
$GRAY_LINE = Color 203 213 225
$DARK_GRAY = Color 51 65 85

$SlideW = 960
$SlideH = 540

function Set-TextStyle($Shape, [string]$Text, [int]$Size, [int]$FontColor, [bool]$Bold = $false, [int]$Align = 1) {
    $Shape.TextFrame.TextRange.Text = $Text
    $Shape.TextFrame.MarginLeft = 6
    $Shape.TextFrame.MarginRight = 6
    $Shape.TextFrame.MarginTop = 4
    $Shape.TextFrame.MarginBottom = 4
    $Shape.TextFrame.WordWrap = $msoTrue
    $Shape.TextFrame.TextRange.Font.Name = "Aptos"
    $Shape.TextFrame.TextRange.Font.Size = $Size
    $Shape.TextFrame.TextRange.Font.Bold = $(if ($Bold) { $msoTrue } else { $msoFalse })
    $Shape.TextFrame.TextRange.Font.Color.RGB = $FontColor
    $Shape.TextFrame.TextRange.ParagraphFormat.Alignment = $Align
}

function Add-Textbox($Slide, [double]$X, [double]$Y, [double]$W, [double]$H, [string]$Text, [int]$Size, [int]$FontColor, [bool]$Bold = $false, [int]$Align = 1) {
    $shape = $Slide.Shapes.AddTextbox($msoTextOrientationHorizontal, $X, $Y, $W, $H)
    Set-TextStyle $shape $Text $Size $FontColor $Bold $Align
    $shape.Line.Visible = $msoFalse
    return $shape
}

function Add-Box($Slide, [double]$X, [double]$Y, [double]$W, [double]$H, [string]$Text, [int]$Fill, [int]$Line, [int]$FontColor = $NAVY, [int]$Size = 16, [bool]$Bold = $false) {
    $shape = $Slide.Shapes.AddShape($msoShapeRoundedRectangle, $X, $Y, $W, $H)
    $shape.Fill.ForeColor.RGB = $Fill
    $shape.Line.ForeColor.RGB = $Line
    $shape.Line.Weight = 1.4
    Set-TextStyle $shape $Text $Size $FontColor $Bold 1
    return $shape
}

function Add-PlainBox($Slide, [double]$X, [double]$Y, [double]$W, [double]$H, [int]$Fill, [int]$Line) {
    $shape = $Slide.Shapes.AddShape($msoShapeRectangle, $X, $Y, $W, $H)
    $shape.Fill.ForeColor.RGB = $Fill
    $shape.Line.ForeColor.RGB = $Line
    $shape.Line.Weight = 1
    return $shape
}

function Add-Chip($Slide, [double]$X, [double]$Y, [double]$W, [string]$Text, [int]$Fill, [int]$Line, [int]$FontColor = $NAVY) {
    return Add-Box $Slide $X $Y $W 24 $Text $Fill $Line $FontColor 10 $true
}

function Add-Arrow($Slide, [double]$X1, [double]$Y1, [double]$X2, [double]$Y2, [int]$LineColor = $SLATE, [double]$Weight = 2.2) {
    $line = $Slide.Shapes.AddConnector($msoConnectorStraight, $X1, $Y1, $X2, $Y2)
    $line.Line.ForeColor.RGB = $LineColor
    $line.Line.Weight = $Weight
    $line.Line.EndArrowheadStyle = $msoArrowheadTriangle
    return $line
}

function Add-Line($Slide, [double]$X1, [double]$Y1, [double]$X2, [double]$Y2, [int]$LineColor = $SLATE, [double]$Weight = 2.0) {
    $line = $Slide.Shapes.AddConnector($msoConnectorStraight, $X1, $Y1, $X2, $Y2)
    $line.Line.ForeColor.RGB = $LineColor
    $line.Line.Weight = $Weight
    return $line
}

function Add-ImageFit($Slide, [string]$Path, [double]$X, [double]$Y, [double]$W, [double]$H) {
    if (-not (Test-Path $Path)) {
        throw "Missing image: $Path"
    }
    $img = [System.Drawing.Image]::FromFile($Path)
    try {
        $scale = [Math]::Min($W / $img.Width, $H / $img.Height)
        $picW = $img.Width * $scale
        $picH = $img.Height * $scale
    } finally {
        $img.Dispose()
    }
    $picX = $X + (($W - $picW) / 2)
    $picY = $Y + (($H - $picH) / 2)
    $shape = $Slide.Shapes.AddPicture($Path, $msoFalse, $msoTrue, $picX, $picY, $picW, $picH)
    return $shape
}

function Add-Title($Slide, [string]$Title, [string]$Subtitle = "") {
    Add-Textbox $Slide 42 22 760 40 $Title 26 $NAVY $true | Out-Null
    if ($Subtitle -ne "") {
        Add-Textbox $Slide 44 61 760 28 $Subtitle 12 $MUTED $false | Out-Null
    }
    Add-Line $Slide 42 88 918 88 $GRAY_LINE 1.2 | Out-Null
}

function Add-Footer($Slide, [string]$Text = "Context/orientation only. No hydrate proof, occurrence prediction, saturation prediction, trained metric, or sweet-spot ranking.") {
    Add-Textbox $Slide 42 506 876 18 $Text 8 $MUTED $false 2 | Out-Null
}

function Set-Background($Slide) {
    $bg = $Slide.Shapes.AddShape($msoShapeRectangle, 0, 0, $SlideW, $SlideH)
    $bg.Fill.ForeColor.RGB = $LIGHT
    $bg.Line.Visible = $msoFalse
    $bg.ZOrder($msoSendToBack)
}

function Add-Notes($Slide, [string]$Text) {
    try {
        $Slide.NotesPage.Shapes.Placeholders(2).TextFrame.TextRange.Text = $Text
    } catch {
        # Some PowerPoint templates expose notes placeholders differently; skip rather than failing the build.
    }
}

function Add-TrackCurve($Slide, [double]$BaseX, [double]$TopY, [double]$Height, [double[]]$Values, [int]$Color, [string]$Label) {
    $count = $Values.Length
    $lastX = $null
    $lastY = $null
    for ($i = 0; $i -lt $count; $i++) {
        $x = $BaseX + $Values[$i]
        $y = $TopY + ($Height * $i / ($count - 1))
        if ($lastX -ne $null) {
            Add-Line $Slide $lastX $lastY $x $y $Color 2.4 | Out-Null
        }
        $lastX = $x
        $lastY = $y
    }
    Add-Textbox $Slide ($BaseX - 8) ($TopY - 26) 74 18 $Label 8 $Color $true 2 | Out-Null
}

function Add-FractionEquation($Slide, [double]$X, [double]$Y, [string]$Left, [string]$Num, [string]$Den, [string]$RightText = "") {
    Add-Textbox $Slide $X $Y 44 35 $Left 24 $NAVY $true 2 | Out-Null
    Add-Textbox $Slide ($X + 52) ($Y - 2) 58 22 $Num 18 $BLUE $true 2 | Out-Null
    Add-Line $Slide ($X + 55) ($Y + 22) ($X + 106) ($Y + 22) $NAVY 1.8 | Out-Null
    Add-Textbox $Slide ($X + 52) ($Y + 23) 58 22 $Den 18 $PURPLE $true 2 | Out-Null
    if ($RightText -ne "") {
        Add-Textbox $Slide ($X + 120) ($Y + 4) 130 30 $RightText 18 $NAVY $true 1 | Out-Null
    }
}

$MapUnified = Join-Path $Root "docs/project_blueprints/presentation_assets/website_well_maps_2026_06_18/unified_north_slope_well_stability_context_map_2026_06_18.png"
$MapCallout = Join-Path $Root "docs/project_blueprints/presentation_assets/website_well_maps_2026_06_18/unified_north_slope_slide_export_callout_space_2026_06_18.png"
$HydrateStructure = Join-Path $Root "docs/evidence/slide02_source_bundle_2026_06_17/slide02_selected_14_world_atlas_fig1_1_structure_types_clean.png"
$CrossSection = Join-Path $Root "docs/evidence/slide02_source_bundle_2026_06_17/slide02_selected_06_usgs_arctic_alaska_cross_section_fig2_crop.png"
$PTDiagram = Join-Path $Root "docs/project_blueprints/presentation_assets/editable_rebuild_2026_06_19/slide_02_pt_diagram_from_recovered_csv_2026_06_19.png"

$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = $msoTrue
$presentation = $ppt.Presentations.Add($msoTrue)
$presentation.PageSetup.SlideWidth = $SlideW
$presentation.PageSetup.SlideHeight = $SlideH

# Slide 1
$s1 = $presentation.Slides.Add(1, $ppLayoutBlank)
Set-Background $s1
Add-Textbox $s1 58 55 560 62 "North Slope Gas Hydrate ML Workflow" 34 $NAVY $true | Out-Null
Add-Textbox $s1 61 124 560 35 "Public-source context + approved-runtime pathway" 17 $SLATE | Out-Null
Add-Textbox $s1 61 174 470 50 "Editable rebuild for mentor review" 22 $TEAL $true | Out-Null
Add-Box $s1 62 256 285 78 "Goal: connect regional geology, stability context, well logs, lithology/core calibration, and guarded ML outputs." $WHITE $GRAY_LINE $NAVY 15 $false | Out-Null
Add-Box $s1 365 256 240 78 "Today: no hydrate proof, no trained metrics, no occurrence/saturation predictions." $AMBER_LIGHT (Color 245 158 11) $AMBER 15 $true | Out-Null
$photo = Add-PlainBox $s1 690 86 190 245 $WHITE $GRAY_LINE
Add-Textbox $s1 708 190 154 44 "Editable photo placeholder" 16 $MUTED $true 2 | Out-Null
Add-Textbox $s1 690 348 190 44 "Replace manually with a professional photo" 11 $MUTED $false 2 | Out-Null
Add-Chip $s1 62 433 154 "No rap-caviar content" $TEAL_LIGHT $TEAL $TEAL | Out-Null
Add-Chip $s1 230 433 176 "All text is selectable" $BLUE_LIGHT $BLUE $BLUE | Out-Null
Add-Footer $s1 "Editable deck rebuild; source figures remain separate image objects where scientific content must be preserved."
Add-Notes $s1 "Open cleanly, establish the purpose, and tell the audience this is a workflow and review deck, not a final results deck. The photo slot is intentionally blank for manual replacement."

# Slide 2
$s2 = $presentation.Slides.Add(2, $ppLayoutBlank)
Set-Background $s2
Add-Title $s2 "Methane Hydrate + North Slope Context" "What hydrate is, why North Slope matters, and why P-T stability is only the first screen"
Add-ImageFit $s2 $HydrateStructure 44 104 265 170 | Out-Null
$circle = $s2.Shapes.AddShape($msoShapeOval, 78, 129, 70, 70)
$circle.Fill.Visible = $msoFalse
$circle.Line.ForeColor.RGB = $RED
$circle.Line.Weight = 3.2
Add-Textbox $s2 54 277 245 32 "Structure I is the methane baseline; Structure II/H require gas-composition context." 10 $NAVY $false | Out-Null
Add-ImageFit $s2 $CrossSection 45 329 300 124 | Out-Null
Add-Textbox $s2 54 457 292 24 "Cross-section context: stratigraphy and structure shape the stability setting." 10 $SLATE $false | Out-Null
Add-ImageFit $s2 $MapUnified 360 104 350 235 | Out-Null
Add-Box $s2 375 112 182 28 "Unified North Slope map" $WHITE $GRAY_LINE $NAVY 10 $true | Out-Null
Add-ImageFit $s2 $PTDiagram 720 111 198 157 | Out-Null
Add-Box $s2 724 272 190 54 "P-T diagram: pressure-temperature admissibility only; not occurrence or saturation evidence." $TEAL_LIGHT $TEAL $TEAL 10 $true | Out-Null
Add-Box $s2 363 360 270 96 "North Slope hydrate interpretation needs three things together: reservoir-quality sands, P-T context, and log/core calibration." $WHITE $GRAY_LINE $NAVY 14 $true | Out-Null
Add-Box $s2 646 360 245 96 "Biogenic and thermogenic gas sources can both matter; gas composition policy remains a mentor/runtime decision." $AMBER_LIGHT (Color 245 158 11) $AMBER 13 $false | Out-Null
Add-Footer $s2 "Source figures and map are image objects; labels, circle, callouts, title, and caveat are editable."
Add-Notes $s2 "Use this slide to define methane hydrate, frame the Alaska North Slope, and explain that P-T stability is a necessary context screen, not proof. Detailed citations belong in the companion notes."

# Slide 3
$s3 = $presentation.Slides.Add(3, $ppLayoutBlank)
Set-Background $s3
Add-Title $s3 "Log Signals, Lithology, And Core Calibration" "Directional curve movements are evidence to review, not standalone hydrate proof"
$panel = Add-PlainBox $s3 54 113 492 340 $WHITE $GRAY_LINE
Add-Textbox $s3 66 122 40 18 "Depth" 9 $SLATE $true 2 | Out-Null
Add-Line $s3 104 142 104 425 $DARK_GRAY 1.2 | Out-Null
foreach ($tick in 0..4) {
    $y = 151 + $tick * 66
    Add-Line $s3 98 $y 110 $y $DARK_GRAY 1 | Out-Null
    Add-Textbox $s3 59 ($y - 8) 37 14 ("{0}" -f (500 + $tick * 150)) 7 $SLATE $false 2 | Out-Null
}
$lithX = 122
Add-Textbox $s3 $lithX 122 68 18 "Lithology" 9 $NAVY $true 2 | Out-Null
Add-PlainBox $s3 $lithX 146 58 64 (Color 229 231 235) $GRAY_LINE | Out-Null
Add-Textbox $s3 ($lithX + 4) 169 50 18 "shale / mixed" 7 $SLATE $false 2 | Out-Null
Add-PlainBox $s3 $lithX 210 58 92 (Color 254 243 199) $GRAY_LINE | Out-Null
Add-Textbox $s3 ($lithX + 5) 242 48 26 "clean sand" 8 $AMBER $true 2 | Out-Null
Add-PlainBox $s3 $lithX 302 58 54 (Color 229 231 235) $GRAY_LINE | Out-Null
Add-Textbox $s3 ($lithX + 4) 318 50 18 "mixed" 7 $SLATE $false 2 | Out-Null
Add-PlainBox $s3 $lithX 356 58 69 (Color 254 243 199) $GRAY_LINE | Out-Null
Add-Textbox $s3 ($lithX + 5) 379 48 22 "sand" 8 $AMBER $true 2 | Out-Null
$trackTop = 152
$trackHeight = 265
Add-TrackCurve $s3 217 $trackTop $trackHeight ([double[]](42,36,31,24,21,18,20,35,50,44,31,20,18,19,28,43)) $GREEN "GR"
Add-TrackCurve $s3 299 $trackTop $trackHeight ([double[]](20,25,30,48,62,68,63,35,26,32,54,69,73,62,38,28)) $RED "Res."
Add-TrackCurve $s3 383 $trackTop $trackHeight ([double[]](32,33,37,50,59,66,61,45,38,40,55,67,70,65,47,35)) $BLUE "Vp/Vs"
Add-TrackCurve $s3 467 $trackTop $trackHeight ([double[]](52,49,44,36,31,27,31,42,47,43,34,29,30,36,45,51)) $PURPLE "NMR/den."
$coreX = 515
Add-Textbox $s3 503 122 34 18 "Core" 9 $NAVY $true 2 | Out-Null
foreach ($yy in @(225, 381)) {
    Add-PlainBox $s3 $coreX $yy 14 44 $TEAL_LIGHT $TEAL | Out-Null
}
Add-Textbox $s3 64 431 463 18 "Sand intervals are log-response targets for review; core/NMR/pressure-core evidence calibrates labels and uncertainty." 9 $MUTED $false 2 | Out-Null
Add-Box $s3 574 115 318 54 "Lower GR suggests cleaner sand; it is a lithology cue, not hydrate proof." $GREEN_LIGHT (Color 34 197 94) $GREEN 12 $true | Out-Null
Add-Arrow $s3 575 142 244 225 $GREEN 1.8 | Out-Null
Add-Box $s3 574 182 318 64 "Resistivity can rise when hydrate replaces conductive pore water, but tight rock, gas, salinity, invasion, and borehole effects can mimic it." $RED_LIGHT $RED $RED 11 $false | Out-Null
Add-Arrow $s3 574 211 350 219 $RED 1.8 | Out-Null
Add-Box $s3 574 260 318 62 "Vs matters because shear response ties to the solid frame, contacts, cementation, and hydrate-bearing stiffness." $BLUE_LIGHT $BLUE $BLUE 12 $true | Out-Null
Add-Arrow $s3 574 288 429 230 $BLUE 1.8 | Out-Null
Add-Box $s3 574 338 318 54 "Density, neutron, and NMR separations give context for pore fluids and pore solids, not a final saturation claim." $PURPLE_LIGHT $PURPLE $PURPLE 11 $false | Out-Null
Add-Arrow $s3 574 362 496 246 $PURPLE 1.8 | Out-Null
Add-Box $s3 574 408 318 43 "Core/coring/NMR strip: calibration and target authority after source review." $TEAL_LIGHT $TEAL $TEAL 11 $true | Out-Null
Add-Footer $s3
Add-Notes $s3 "Walk left to right: lithology first, then curve movement, then core calibration. Emphasize that signals are complementary and mimic-prone. No equation or ML architecture belongs on this slide."

# Slide 4
$s4 = $presentation.Slides.Add(4, $ppLayoutBlank)
Set-Background $s4
Add-Title $s4 "Four-Well Workflow: Audience Version" "The complex architecture reduces to six editable steps"
$boxes = @(
    @{x=54;y=147;w=120;h=83;t="Inputs`nlogs + core/NMR + lithology + public context";f=$BLUE_LIGHT;l=$BLUE},
    @{x=200;y=147;w=120;h=83;t="Prepare`npreserve headers, units, depth alignment, QC";f=$TEAL_LIGHT;l=$TEAL},
    @{x=346;y=147;w=120;h=83;t="Leakage barrier`ninputs separate from saturation and occurrence labels";f=$RED_LIGHT;l=$RED},
    @{x=492;y=147;w=120;h=83;t="Model path`noccurrence and saturation are linked but separate";f=$PURPLE_LIGHT;l=$PURPLE},
    @{x=638;y=147;w=120;h=83;t="Validate`nwhole-well or geography-aware split before metrics";f=$AMBER_LIGHT;l=(Color 245 158 11)},
    @{x=784;y=147;w=120;h=83;t="Review outputs`nfigures, uncertainty, maps, manuscript exports";f=$GREEN_LIGHT;l=(Color 34 197 94)}
)
for ($i=0; $i -lt $boxes.Count; $i++) {
    $b = $boxes[$i]
    Add-Box $s4 $b.x $b.y $b.w $b.h $b.t $b.f $b.l $NAVY 12 $true | Out-Null
    if ($i -lt $boxes.Count - 1) {
        Add-Arrow $s4 ($b.x + $b.w + 4) ($b.y + 42) ($boxes[$i+1].x - 4) ($b.y + 42) $SLATE 2 | Out-Null
    }
}
Add-Box $s4 66 282 238 82 "What collapsed from the full diagram: source intake, schema, QC, feature engineering, target registry, model runner, tracker, and export panels." $WHITE $GRAY_LINE $NAVY 13 $false | Out-Null
Add-Box $s4 344 282 238 82 "What stays in Word/appendix: full architecture poster, detailed runtime package names, and all source-code/module wiring." $WHITE $GRAY_LINE $NAVY 13 $false | Out-Null
Add-Box $s4 622 282 238 82 "Two-minute story: protect the data boundary, align variables by depth, train only after leakage checks, then review claims with core/lithology evidence." $TEAL_LIGHT $TEAL $TEAL 13 $true | Out-Null
Add-Footer $s4 "This is an implementation plan, not a trained model result."
Add-Notes $s4 "Two-minute script: First, the project takes public regional context and approved well data separately. Second, every curve keeps its original header and unit before normalization. Third, saturation and occurrence evidence are held behind a leakage barrier. Fourth, occurrence classification and saturation regression are separate model heads. Fifth, no metric is meaningful until the split is by complete well or geography. Finally, outputs are reviewed figures and uncertainty summaries, not automatic hydrate claims."

# Slide 5
$s5 = $presentation.Slides.Add(5, $ppLayoutBlank)
Set-Background $s5
Add-Title $s5 "Equation-Only Slide: Physics Transforms And Gates" "Large equations; symbol meanings stay editable below each card"
Add-Chip $s5 620 54 82 "logs" $BLUE_LIGHT $BLUE $BLUE | Out-Null
Add-Chip $s5 710 54 82 "context" $TEAL_LIGHT $TEAL $TEAL | Out-Null
Add-Chip $s5 800 54 90 "derived" $PURPLE_LIGHT $PURPLE $PURPLE | Out-Null
Add-Box $s5 56 118 400 142 "" $WHITE $GRAY_LINE $NAVY 14 $true | Out-Null
Add-Textbox $s5 76 130 240 22 "Pressure-depth screen" 13 $NAVY $true 1 | Out-Null
Add-Textbox $s5 86 166 330 38 "P_abs = P0 + rho_w x g x z" 25 $NAVY $true 2 | Out-Null
Add-Textbox $s5 74 215 360 25 "absolute pressure   surface pressure   water density   gravity   depth" 9 $SLATE $false 2 | Out-Null
Add-Box $s5 504 118 400 142 "" $WHITE $GRAY_LINE $NAVY 14 $true | Out-Null
Add-Textbox $s5 524 130 240 22 "Acoustic impedance" 13 $NAVY $true 1 | Out-Null
Add-Textbox $s5 560 166 278 38 "AI = rho_b x Vp" 28 $NAVY $true 2 | Out-Null
Add-Textbox $s5 555 215 300 25 "impedance   bulk density   compressional velocity" 9 $SLATE $false 2 | Out-Null
Add-Box $s5 56 292 400 142 "" $WHITE $GRAY_LINE $NAVY 14 $true | Out-Null
Add-Textbox $s5 76 304 240 22 "Velocity ratio" 13 $NAVY $true 1 | Out-Null
Add-FractionEquation $s5 138 335 "R =" "Vp" "Vs" "velocity ratio"
Add-Textbox $s5 83 392 342 24 "compressional velocity over shear velocity; compare frame and pore-fluid response" 9 $SLATE $false 2 | Out-Null
Add-Box $s5 504 292 400 142 "" $WHITE $GRAY_LINE $NAVY 14 $true | Out-Null
Add-Textbox $s5 524 304 260 22 "Elastic attributes from logs" 13 $NAVY $true 1 | Out-Null
Add-Textbox $s5 525 328 360 28 "mu-rho = rho_b x Vs^2" 21 $NAVY $true 2 | Out-Null
Add-Textbox $s5 525 365 360 28 "lambda-rho = rho_b x (Vp^2 - 2Vs^2)" 18 $NAVY $true 2 | Out-Null
Add-Textbox $s5 522 405 365 24 "shear / lambda-rho features from density, Vp, and Vs; not proof by themselves" 9 $SLATE $false 2 | Out-Null
Add-Box $s5 170 459 620 31 "Equations transform logs and context into review features. They do not create final hydrate occurrence or saturation claims." $AMBER_LIGHT (Color 245 158 11) $AMBER 12 $true | Out-Null
Add-Footer $s5 "No map, no ML diagram, no trained metrics, and no approved rows on this slide."
Add-Notes $s5 "Keep this slide about what each equation converts. The user can edit every equation label and card. Saturation equations are deliberately not included until exact source equation, units, and target/input role are approved."

# Slide 6
$s6 = $presentation.Slides.Add(6, $ppLayoutBlank)
Set-Background $s6
Add-Title $s6 "Evidence And Unit Gate Before Modeling" "A high-level gate keeps measurements, derived features, and targets separate"
Add-Textbox $s6 86 112 790 35 "One sentence takeaway: the model is only credible after units, curve roles, lithology context, and target-only labels are separated." 17 $NAVY $true 2 | Out-Null
$gateBoxes = @(
    @{x=70;y=186;t="1. Original headers`nDEPTH, GR, RHOB, RES, Vp, Vs, NMR";c=$BLUE;f=$BLUE_LIGHT},
    @{x=276;y=186;t="2. Units + depth`nfeet/meters and curve alignment preserved";c=$TEAL;f=$TEAL_LIGHT},
    @{x=482;y=186;t="3. Feature role`nmeasured, derived, QC, context";c=$PURPLE;f=$PURPLE_LIGHT},
    @{x=688;y=186;t="4. Target barrier`nSgh / Sh / NMR_SAT stay Y-only";c=$RED;f=$RED_LIGHT}
)
foreach ($g in $gateBoxes) {
    Add-Box $s6 $g.x $g.y 166 112 $g.t $g.f $g.c $NAVY 13 $true | Out-Null
}
Add-Arrow $s6 238 242 272 242 $SLATE 2 | Out-Null
Add-Arrow $s6 444 242 478 242 $SLATE 2 | Out-Null
Add-Arrow $s6 650 242 684 242 $SLATE 2 | Out-Null
Add-Box $s6 112 342 225 72 "Four-well scope: go deeper on lithology/core review instead of claiming broad model coverage." $WHITE $GRAY_LINE $NAVY 13 $false | Out-Null
Add-Box $s6 368 342 225 72 "False positives are expected: gas, tight rock, salinity, borehole washout, and missing curves must be reviewed." $WHITE $GRAY_LINE $NAVY 13 $false | Out-Null
Add-Box $s6 624 342 225 72 "Outputs stay review-ready: plots, uncertainty, source notes, and mentor decisions before final claims." $WHITE $GRAY_LINE $NAVY 13 $false | Out-Null
Add-Footer $s6
Add-Notes $s6 "This slide should be explained in less than one minute. Detailed source tables, exact screenshots, and header lists belong in the companion material."

# Slide 7
$s7 = $presentation.Slides.Add(7, $ppLayoutBlank)
Set-Background $s7
Add-Title $s7 "Unified North Slope Well + Stability Context Map" "Regional context for discussion only; this is not an ML overlay"
Add-ImageFit $s7 $MapCallout 42 103 660 372 | Out-Null
Add-Box $s7 724 115 178 75 "What it combines`npublic wells, USGS hydrate AUs, GGD223 controls, DNR units, roads, TAPS, field labels" $WHITE $GRAY_LINE $NAVY 11 $false | Out-Null
Add-Box $s7 724 210 178 75 "What colors mean`nstability-screen status categories, not hydrate occurrence classes" $TEAL_LIGHT $TEAL $TEAL 11 $true | Out-Null
Add-Box $s7 724 305 178 75 "What it cannot claim`nno saturation, no producibility, no sweet-spot ranking, no trained-model evidence" $RED_LIGHT $RED $RED 11 $true | Out-Null
Add-Box $s7 724 400 178 47 "Use as Slide 7 context and as a discussion anchor for source gaps." $AMBER_LIGHT (Color 245 158 11) $AMBER 10 $false | Out-Null
Add-Footer $s7 "Context/orientation only. Stability-screen status does not prove hydrate occurrence, saturation, or trained-model evidence."
Add-Notes $s7 "Say that this map organizes public context: field labels, roads, TAPS, permafrost controls, hydrate AU outlines, and stability-screen status. Do not use it as a prediction or discovery map."

# Slide 8
$s8 = $presentation.Slides.Add(8, $ppLayoutBlank)
Set-Background $s8
Add-Title $s8 "Planned Four-Well Results Review Logic" "Editable placeholders for DOE exports; no fake results"
$wellCards = @(
    @{x=56;name="MTE / Mount Elbert";tag="header verified"},
    @{x=278;name="IGS / Ignik Sikumi";tag="header verified"},
    @{x=500;name="Hydrate-01";tag="source-case anchor"},
    @{x=722;name="HYDRATE 02";tag="source-case anchor"}
)
foreach ($w in $wellCards) {
    Add-Box $s8 $w.x 112 178 58 ($w.name + "`n" + $w.tag) $WHITE $GRAY_LINE $NAVY 12 $true | Out-Null
}
$steps = @(
    @{x=70;y=238;t="DOE runtime export`nrow-free review figures after approved execution";f=$BLUE_LIGHT;l=$BLUE},
    @{x=258;y=238;t="Lithology/core calibration`nclean sand vs shale/mixed facies";f=$TEAL_LIGHT;l=$TEAL},
    @{x=446;y=238;t="False-positive review`nresistivity, gas, salinity, washout, tight rock";f=$AMBER_LIGHT;l=(Color 245 158 11)},
    @{x=634;y=238;t="Separate outputs`noccurrence review and saturation review are not merged";f=$PURPLE_LIGHT;l=$PURPLE}
)
foreach ($st in $steps) {
    Add-Box $s8 $st.x $st.y 160 100 $st.t $st.f $st.l $NAVY 12 $true | Out-Null
}
for ($i=0; $i -lt $steps.Count - 1; $i++) {
    Add-Arrow $s8 ($steps[$i].x + 162) 288 ($steps[$i+1].x - 4) 288 $SLATE 2 | Out-Null
}
Add-Box $s8 166 386 620 48 "Future slots: per-well log panels, calibration table, uncertainty flags, and reviewed map/table exports. Leave blank until DOE/Yubi access and mentor target authority are available." $RED_LIGHT $RED $RED 12 $true | Out-Null
Add-Footer $s8 "No trained metrics, occurrence probabilities, saturation predictions, or rankings are shown."
Add-Notes $s8 "Frame this as a results-review plan. The audience should understand what will be produced later, how false positives are controlled, and why occurrence and saturation remain separate."

# Slide 9
$s9 = $presentation.Slides.Add(9, $ppLayoutBlank)
Set-Background $s9
Add-Title $s9 "Built, Not Claimed, And Next Actions" "Close with a defensible status instead of unsupported results"
Add-Box $s9 62 122 250 296 "Built now`n`n- Public GIS/stability scaffold`n- Unified map and source inventory`n- Header-only workbook mapping`n- Public well/API anchors`n- Equation and feature-role logic`n- DOE runtime skeleton and tracker" $GREEN_LIGHT (Color 34 197 94) $GREEN 13 $true | Out-Null
Add-Box $s9 355 122 250 296 "Not claimed yet`n`n- Hydrate proof`n- Final stability intervals`n- Occurrence prediction`n- Saturation prediction`n- Trained metrics`n- Sweet-spot ranking`n- Final target-label authority" $RED_LIGHT $RED $RED 13 $true | Out-Null
Add-Box $s9 648 122 250 296 "Next actions`n`n- Regain DOE/Yubi access`n- Download public papers/supplements to Drive/OSL`n- Run header/runtime audit`n- Export row-free figures`n- Review target authority with mentor`n- Update Word companion" $BLUE_LIGHT $BLUE $BLUE 13 $true | Out-Null
Add-Box $s9 167 450 626 33 "Final message: the project is ready for approved-runtime execution and mentor review, not final hydrate claims." $AMBER_LIGHT (Color 245 158 11) $AMBER 13 $true | Out-Null
Add-Footer $s9 "All slide text, boxes, dividers, and status cards are editable."
Add-Notes $s9 "Close by saying the project has the public context, source discipline, and workflow skeleton ready. The remaining step is approved runtime execution and mentor target authority, not embellishing results."

$presentation.SaveAs($OutputFullPath, $ppSaveAsOpenXMLPresentation)

# Export rendered slides and build a shape audit.
$audit = New-Object System.Collections.Generic.List[object]
for ($i = 1; $i -le $presentation.Slides.Count; $i++) {
    $slide = $presentation.Slides.Item($i)
    $exportPath = Join-Path $ExportDir ("slide_{0:D2}_editable_rebuild.png" -f $i)
    $slide.Export($exportPath, "PNG", 1920, 1080)

    $pictureCount = 0
    $textCount = 0
    $shapeCount = 0
    $fullSlidePictureCount = 0
    foreach ($shape in $slide.Shapes) {
        $shapeCount += 1
        if ($shape.Type -eq 13) {
            $pictureCount += 1
            if (($shape.Width -gt ($SlideW * 0.92)) -and ($shape.Height -gt ($SlideH * 0.92))) {
                $fullSlidePictureCount += 1
            }
        }
        try {
            if ($shape.HasTextFrame -and $shape.TextFrame.HasText) {
                $textCount += 1
            }
        } catch {}
    }
    $audit.Add([pscustomobject]@{
        slide = $i
        shape_count = $shapeCount
        text_shape_count = $textCount
        picture_shape_count = $pictureCount
        full_slide_picture_count = $fullSlidePictureCount
        only_full_slide_image = (($shapeCount -eq 1) -and ($fullSlidePictureCount -eq 1))
        exported_png = $exportPath
    }) | Out-Null
}
$audit | Export-Csv -Path $QaCsv -NoTypeInformation

$presentation.Close()
$ppt.Quit()

[System.Runtime.InteropServices.Marshal]::ReleaseComObject($presentation) | Out-Null
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) | Out-Null
[GC]::Collect()
[GC]::WaitForPendingFinalizers()

& python (Join-Path $Root "docs/project_blueprints/render_editable_rebuild_assets_2026_06_19.py") --contact-sheet | Out-Host

Write-Host "PPTX: $OutputFullPath"
Write-Host "QA: $QaCsv"
Write-Host "Rendered slides: $ExportDir"
