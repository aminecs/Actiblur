from pydantic import BaseSettings

class Settings(BaseSettings): 
    SQLALCHEMY_URI: str 
    class Config: 
        env_file = '.env'
    
settings = Settings()