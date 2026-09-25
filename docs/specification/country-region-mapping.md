# Country-to-region mapping

`dim_country.region` is assigned from the fixed mapping below ([`dim_country`](dimensions.md#dim_country)). The mapping follows the region level of the United Nations geoscheme (UNSD M49): Africa, Asia, Europe, Oceania, Northern America, and Latin America and the Caribbean.

| Stored value | Legacy label | Countries |
|--------------|--------------|-----------|
| `Northern America` | `América del Norte` (English: "North America") | United States, Canada |
| `Europe` | `Europa` (English: "Europe") | United Kingdom, Germany, France, Netherlands, Sweden, Denmark, Finland, Switzerland, Belgium, Ireland, Poland, Portugal, Greece, Italy, Czech Republic, Croatia, Bosnia and Herzegovina, Russia, Moldova |
| `Asia` | `Asia` (English: "Asia") | India, Philippines, Thailand, Singapore, Israel, Georgia |
| `Oceania` | `Oceanía` (English: "Oceania") | Australia, New Zealand |
| `Africa` | `África` (English: "Africa") | Nigeria, South Africa |
| `Latin America and the Caribbean` | `América Latina` (English: "Latin America") | Brazil, Colombia, Costa Rica, Mexico |

The mapping has 35 entries (2 + 19 + 6 + 2 + 2 + 4).

## Differences from the legacy mapping

Two entries differ: Mexico (legacy: `América del Norte` (English: "North America"); here: `Latin America and the Caribbean`) and Georgia (legacy: `Europa` (English: "Europe"); here: `Asia`). Both were verified against the UNSD table; the other 33 entries are pending check A11 of the [legacy audit](../audit/legacy-audit.md).

## Rules

* The mapping is a fixed table in the pipeline, not inferred from data.
* A staged country absent from the mapping aborts the load. There is no default region.
* The number of countries present in staging, against the 35 entries here and the 36 stated in the legacy report, is established by check A8 of the legacy audit.
