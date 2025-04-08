from typing import Optional
from pydantic import BaseSettings
from supabase import create_client, Client

class SupabaseSettings(BaseSettings):
    """Supabase configuration settings."""
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_JWT_SECRET: str
    
    class Config:
        env_file = ".env"
        case_sensitive = True

class SupabaseClient:
    """Singleton class for Supabase client."""
    _instance: Optional[Client] = None
    _settings: Optional[SupabaseSettings] = None
    
    @classmethod
    def get_client(cls) -> Client:
        """Get or create Supabase client instance."""
        if cls._instance is None:
            cls._settings = SupabaseSettings()
            cls._instance = create_client(
                cls._settings.SUPABASE_URL,
                cls._settings.SUPABASE_KEY
            )
        return cls._instance
    
    @classmethod
    def get_settings(cls) -> SupabaseSettings:
        """Get Supabase settings."""
        if cls._settings is None:
            cls._settings = SupabaseSettings()
        return cls._settings 