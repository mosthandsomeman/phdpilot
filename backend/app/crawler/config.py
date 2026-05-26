TARGET_COUNTRIES: dict[str, list[str]] = {
    "nordic": ["Sweden", "Norway", "Denmark", "Finland", "Iceland"],
    "germany": ["Germany"],
    "netherlands": ["Netherlands"],
    "southern_europe": ["Italy", "Spain", "Portugal", "Greece"],
}

TARGET_KEYWORDS: list[str] = [
    "PhD",
    "Doctoral",
    "Doctorate",
    "AI",
    "Artificial Intelligence",
    "Machine Learning",
    "Deep Learning",
    "Computer Science",
    "Data Science",
    "Medical AI",
    "Bioinformatics",
    "Computational Biology",
]

# EURAXESS country name -> filter slug (site-specific)
EURAXESS_COUNTRY_SLUGS: dict[str, str] = {
    "Sweden": "SE",
    "Norway": "NO",
    "Denmark": "DK",
    "Finland": "FI",
    "Iceland": "IS",
    "Germany": "DE",
    "Netherlands": "NL",
    "Italy": "IT",
    "Spain": "ES",
    "Portugal": "PT",
    "Greece": "GR",
}

# EURAXESS blocks obvious bot UAs (403). Use a standard browser UA; identify via From header.
CRAWLER_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)
CRAWLER_FROM_HEADER = "PhDPilot-Crawler/1.0 (academic aggregator; contact=admin@phdpilot.local)"

REQUEST_DELAY_SECONDS = 5.0
REQUEST_TIMEOUT_SECONDS = 30.0
MAX_RETRIES = 3
MAX_PAGES_PER_SOURCE = 5
MAX_JOBS_PER_RUN = 80

POSSIBLY_CLOSED_DAYS = 7
CLOSED_DAYS = 30
