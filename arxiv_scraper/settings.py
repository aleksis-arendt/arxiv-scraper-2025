# Scrapy settings for arxiv_scraper project
# ----------------------------------------

BOT_NAME = "arxiv_scraper"

SPIDER_MODULES = ["arxiv_scraper.spiders"]
NEWSPIDER_MODULE = "arxiv_scraper.spiders"

ADDONS = {}

# ---------------------------------------------------------
# IMPORTANT: arXiv API is NOT a normal website.
# We must behave like a polite academic script.
# ---------------------------------------------------------

# Identify yourself clearly (arXiv recommendation)
USER_AGENT = (
    "arXiv API client (academic use); "
    "contact: your_email@domain.com"
)

# arXiv API does not rely on robots.txt for API usage
ROBOTSTXT_OBEY = False

# ---------------------------------------------------------
# Throttling & concurrency (VERY IMPORTANT)
# ---------------------------------------------------------

# One request at a time
CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1

# Slow down requests (arXiv-friendly)
DOWNLOAD_DELAY = 5

# Disable retries (arXiv hates retries)
RETRY_ENABLED = False

# Avoid redirects (use https directly in spider)
REDIRECT_ENABLED = False

# ---------------------------------------------------------
# Headers (tell arXiv what we accept)
# ---------------------------------------------------------

DEFAULT_REQUEST_HEADERS = {
    "Accept": "application/atom+xml",
}

# ---------------------------------------------------------
# Logging (keep INFO, not DEBUG)
# ---------------------------------------------------------

LOG_LEVEL = "INFO"

# ---------------------------------------------------------
# Feed export
# ---------------------------------------------------------

FEED_EXPORT_ENCODING = "utf-8"
