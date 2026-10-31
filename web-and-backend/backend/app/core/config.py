import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    app_env: str = os.getenv("APP_ENV", "development")
    data_gov_api_key: str = os.getenv("DATA_GOV_API_KEY", "")
    data_gov_resource_id: str = os.getenv(
        "DATA_GOV_RESOURCE_ID", "9ef84268-d588-465a-a308-a864a43d0070"
    )
    data_gov_base_url: str = os.getenv(
        "DATA_GOV_BASE_URL",
        "https://api.data.gov.in/resource"
    )
    api_timeout_seconds: int = int(os.getenv("API_TIMEOUT_SECONDS", "25"))
    api_page_size: int = min(int(os.getenv("API_PAGE_SIZE", "1000")), 1000)
    ai_api_key: str = os.getenv("AI_API_KEY", "")
    ai_base_url: str = os.getenv("AI_BASE_URL", "https://api.openai.com/v1")
    ai_model: str = os.getenv("AI_MODEL", "gpt-4o-mini")
    frontend_origins: str = os.getenv(
        "FRONTEND_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000"
    )
    stale_after_days: int = int(os.getenv("STALE_AFTER_DAYS", "3"))


settings = Settings()
