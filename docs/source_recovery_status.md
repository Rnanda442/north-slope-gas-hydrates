# Source Recovery Status

Last checked: 2026-06-07

## Summary

The connected Google Drive contains several supporting research documents and
presentations, but it does not currently expose the named North Slope project
PowerPoint, the project Word-draft filenames, or the intended migrated source
library.

The June 6 migration did not upload the source library to Google Drive. It used
a local `fake-google-drive/Codex Project Reference Library` test directory
rather than a real Google Drive destination.

Its report recorded 212 files considered, 211 missing, and 1 blocked. Most
source paths referred to a separate Windows profile on the source laptop.

## Confirmed Original Locations

- PowerPoint: source laptop `Downloads/Alaska_North_Slope_Wireline_ML_Presentation_Scaffold_outline.pptx`
- Research-paper draft: source laptop `Gas hydrates unclassified info/project_blueprints/Alaska_North_Slope_Wireline_ML_Research_Paper_Draft.docx`
- Broader manuscript: source laptop `Downloads/Manuscript North Slope of Alaska Gas hydrates draft.docx`
- Equation map: source laptop `Downloads/hydrate_wireline_equation_map.docx`
- Overburden framework: source laptop `Downloads/north_slope_overburden_framework_field_oriented.docx`
- Source index: source laptop `Gas hydrates unclassified info/source_library/source_index.md`
- Original project workspace: source laptop `Gas hydrates unclassified info/north-slope-gas-hydrates`

## Files Already Recovered Locally

- `docs/project_blueprints/Alaska_North_Slope_Wireline_ML_Research_Paper_Draft.docx`
- `docs/project_blueprints/Alaska_North_Slope_Wireline_ML_Classification_Methods_Draft.docx`
- `docs/source_library_index/source_index.md`
- `docs/source_library_index/source_manifest.csv`
- The public website, notebooks, GIS layers, and well-log runtime scaffold

## Relevant Files Found on Connected Google Drive

- [Geomechanical relationship with Wireline Logging AN](https://docs.google.com/document/d/1tsbqkQZ0nJzLgjifWcgTL3rpshHEpdvqp6CXp8rkYpc)
- [new query with all stuff](https://docs.google.com/document/d/1MSvV3WP-aoFS11Br_JiQaamUccU908cK5dAlgkAna84)
- [pdf combined](https://docs.google.com/document/d/1UVQsrCSfl9HU6PG01hU6NH-aWvAH-1p_Hdp-oz8m69Q)
- [PDF notes reorganized](https://docs.google.com/document/d/1UDGUQI6pGWXPkzJebWs2-Kstrl_oLUO_5I0378oVEgE)
- [pdf notes](https://docs.google.com/document/d/1q03hzDpoMsnw3jcb6t2BHMMTspzgkKvafTV89oA8gJw)
- [Alaska Seismotech portfolio](https://docs.google.com/presentation/d/1kYlm6-a58kCpQe6T5-21cWgzO058dEj0QU-N0ix9b6M)

These are supporting sources, not confirmed substitutes for the missing North
Slope presentation.

## Recovery Actions

1. Access the Google account used on the source laptop and search for the exact
   filenames above.
2. If they are not in Drive, recover them directly from the confirmed
   source-laptop paths.
3. Place public/unclassified project artifacts into this official repository
   under `docs/project_blueprints/` or `references/`.
4. Keep restricted or approved-environment-only data outside Git and use the
   authorized runtime folders.
5. Re-run the migration only after verifying the true source paths and a real
   Google Drive destination.
