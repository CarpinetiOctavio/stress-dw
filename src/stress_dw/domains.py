"""Value domains of the modeled source columns, and the country-to-region mapping.

Transcribed from docs/specification/sources.md#value-domains and
docs/specification/country-region-mapping.md, which remain the home of both;
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

# Enumerated domain of each modeled source column except `Timestamp`, keyed by
# source column name.
DOMAINS: dict[str, tuple[str, ...]] = {
    "Gender": ("Male", "Female"),
    "Country": tuple(COUNTRY_REGION),
    "Occupation": ("Business", "Corporate", "Housewife", "Others", "Student"),
    "family_history": ("Yes", "No"),
    "treatment": ("Yes", "No"),
    "Days_Indoors": (
        "Go out Every day",
        "1-14 days",
        "15-30 days",
        "31-60 days",
        "More than 2 months",
    ),
    "Growing_Stress": ("Yes", "No", "Maybe"),
    "Mood_Swings": ("Low", "Medium", "High"),
    "Coping_Struggles": ("Yes", "No"),
    "Social_Weakness": ("Yes", "No", "Maybe"),
    "mental_health_interview": ("Yes", "No", "Maybe"),
    "care_options": ("Yes", "No", "Not sure"),
}

# Format of `Timestamp`, confirmed by check A12.
TIMESTAMP_FORMAT = "%m/%d/%Y %H:%M"
