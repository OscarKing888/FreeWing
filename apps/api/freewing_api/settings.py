from pathlib import Path
import os

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "FreeWing"
    data_dir: Path = Path(os.getenv("FREEWING_DATA_DIR", "data"))
    db_path: Path = Path(os.getenv("FREEWING_DB_PATH", "data/db/freewing.db"))

    jwt_secret: str = os.getenv("FREEWING_JWT_SECRET", "dev-secret-change-me")
    jwt_issuer: str = "freewing"
    jwt_ttl_minutes: int = int(os.getenv("FREEWING_JWT_TTL_MINUTES", "10080"))

    cookie_name: str = os.getenv("FREEWING_COOKIE_NAME", "freewing_token")
    cookie_secure: bool = os.getenv("FREEWING_COOKIE_SECURE", "false").lower() == "true"

    cors_origin: str = os.getenv("FREEWING_CORS_ORIGIN", "http://localhost:3000")


settings = Settings()
