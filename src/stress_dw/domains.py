"""Value domains of the modeled source columns, and the fixed dimension mappings.

Transcribed from docs/specification/sources.md#value-domains,
docs/specification/country-region-mapping.md, and
docs/specification/dimensions.md#dim_isolation, which remain the home of each;
a change there is a change here.
"""

# Region of each of the 35 countries, per country-region-mapping.md.
COUNTRY_REGION: dict[str, str] = {
    "United States": "Northern America",
    "Canada": "Northern America",
    "United Kingdom": "Europe",
    "Germany": "Europe",
    "France": "Europe",
    "Netherlands": "Europe",
    "Sweden": "Europe",
    "Denmark": "Europe",
    "Finland": "Europe",
    "Switzerland": "Europe",
    "Belgium": "Europe",
    "Ireland": "Europe",
    "Poland": "Europe",
    "Portugal": "Europe",
    "Greece": "Europe",
    "Italy": "Europe",
    "Czech Republic": "Europe",
    "Croatia": "Europe",
    "Bosnia and Herzegovina": "Europe",
    "Russia": "Europe",
    "Moldova": "Europe",
    "India": "Asia",
    "Philippines": "Asia",
    "Thailand": "Asia",
    "Singapore": "Asia",
    "Israel": "Asia",
    "Georgia": "Asia",
    "Australia": "Oceania",
    "New Zealand": "Oceania",
    "Nigeria": "Africa",
    "South Africa": "Africa",
    "Brazil": "Latin America and the Caribbean",
    "Colombia": "Latin America and the Caribbean",
    "Costa Rica": "Latin America and the Caribbean",
    "Mexico": "Latin America and the Caribbean",
}

# `sort_order` and `duration_band` of each `days_indoors` level, per
# dimensions.md#dim_isolation.
ISOLATION_LEVELS: dict[str, tuple[int, str]] = {
    "Go out Every day": (1, "Low"),
    "1-14 days": (2, "Low"),
    "15-30 days": (3, "Medium"),
    "31-60 days": (4, "High"),
    "More than 2 months": (5, "High"),
}

# Enumerated domain of each modeled source column except `Timestamp`, keyed by
# source column name.
DOMAINS: dict[str, tuple[str, ...]] = {
    "Gender": ("Male", "Female"),
    "Country": tuple(COUNTRY_REGION),
    "Occupation": ("Business", "Corporate", "Housewife", "Others", "Student"),
    "family_history": ("Yes", "No"),
    "treatment": ("Yes", "No"),
    "Days_Indoors": tuple(ISOLATION_LEVELS),
    "Growing_Stress": ("Yes", "No", "Maybe"),
    "Mood_Swings": ("Low", "Medium", "High"),
    "Coping_Struggles": ("Yes", "No"),
    "Social_Weakness": ("Yes", "No", "Maybe"),
    "mental_health_interview": ("Yes", "No", "Maybe"),
    "care_options": ("Yes", "No", "Not sure"),
}

# Format of `Timestamp`, confirmed by check A12.
TIMESTAMP_FORMAT = "%m/%d/%Y %H:%M"
