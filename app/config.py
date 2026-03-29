from typing import List, Optional
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    ROOT_PATH: str = os.getenv("ROOT_PATH", None)
    DATABASE_URL: str = os.getenv("DATABASE_URL", None)
    DATABAE_ECHO: bool = False
    DEBUG: bool = os.getenv("DEBUG", None)
    ENV: str = os.getenv("ENV", 'env')
    ALLOW_ORIGINS: List[str] = []
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            if field_name == "ALLOW_ORIGINS":
                try:
                    return json.loads(raw_val)
                except:
                    return [origin.strip() for origin in raw_val.split(",")]
            return raw_val    
    
    @property
    def isDev(self) -> bool:
        return self.ENV == "dev" or self.ENV == "DEV" 
    
    @property
    def isProd(self) -> bool:
        return self.ENV == "prod" or self.ENV == "PROD"
    
settings = Settings()