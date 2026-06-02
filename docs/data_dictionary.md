# North Slope Atlas Data Dictionary

## Boundary Label

Every dataset documented here belongs to the public-source regional atlas and is
tagged with this operational repository label:

```text
PUBLIC-SOURCE ATLAS
```

This label identifies the repository boundary. It is not a formal classification
determination. Future approved restricted inputs, derived restricted outputs,
credentials, and sensitive metadata must stay outside this hosted repository.

## Regional Layers

| Layer | Role | Source category | Records | Boundary tag |
| --- | --- | --- | ---: | --- |
| Well-bottom-hole locations | Regional well inventory | Public-source GIS | 10,250 | PUBLIC-SOURCE ATLAS |
| 2D seismic coverage | Regional line coverage | Public-source GIS | 26 surveys | PUBLIC-SOURCE ATLAS |
| 3D seismic inventory | Survey footprint coverage | Public-source GIS | 36 surveys | PUBLIC-SOURCE ATLAS |
| North Slope assessment units | Petroleum-system framework | Public-source geology | 6 units | PUBLIC-SOURCE ATLAS |
| North Slope extent | Study-area outline | Project-derived boundary | 1 boundary | PUBLIC-SOURCE ATLAS |

## Structural Layers

| Code | Plain-language label | Meaning | Boundary tag |
| --- | --- | --- | --- |
| `NStopo` | Topographic reference | Near-surface reference horizon used to orient the structural stack. | PUBLIC-SOURCE ATLAS |
| `NSLCU` | Lower Cretaceous unconformity | Regional unconformity surface used as a structural reference. | PUBLIC-SOURCE ATLAS |
| `NSshublik` | Shublik surface | Regional Shublik structural horizon used for deeper framework context. | PUBLIC-SOURCE ATLAS |
| `NSbasement` | Basement surface | Deep basement structural reference for regional basin geometry. | PUBLIC-SOURCE ATLAS |
| `NStopo-LCU` | Topography to LCU interval | Thickness-style grid between topography and LCU. | PUBLIC-SOURCE ATLAS |
| `NSLCU-Shublik` | LCU to Shublik interval | Thickness-style grid between LCU and Shublik. | PUBLIC-SOURCE ATLAS |
| `NSshublik-basement` | Shublik to basement interval | Thickness-style grid between Shublik and basement. | PUBLIC-SOURCE ATLAS |
| `NStopo-basement` | Topography to basement interval | Full reference interval between topography and basement. | PUBLIC-SOURCE ATLAS |

## Quality Notes

- The public well inventory contains `10,250` records.
- `9,894` records have usable point geometry.
- `356` records currently lack usable geometry and must remain visible as a
  quality-control count rather than being silently treated as mappable.
- The lightweight structural viewer samples the processed structural master table
  for responsive exploration. It does not alter or discard the underlying source
  surfaces.
