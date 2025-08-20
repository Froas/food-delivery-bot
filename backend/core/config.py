from pydantic_settings import BaseSettings
from pydantic import Field
from urllib.parse import quote_plus

class Settings(BaseSettings):
    db_user: str = Field(..., alias="DB_USER")
    db_pass: str = Field(..., alias="DB_PASS")
    db_host: str = Field(..., alias="DB_HOST")
    db_port: int = Field(..., alias="DB_PORT")
    db_name: str = Field(..., alias="DB_NAME")
    secret_key: str = Field(..., alias="PASS_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    grid_size: int = 9
    restaurant_order_limit: int = 3

    environment: str = "development"
    debug: bool = True
    

    max_bots: int = 5
    max_orders_per_bot: int = 3
    restaurant_order_limit: int = 3
    restaurant_time_window: int = 30  

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def database_url(self) -> str:
        user = quote_plus(self.db_user)
        pwd  = quote_plus(self.db_pass)  
        return (
            f"postgresql+psycopg2://{user}:{pwd}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

settings = Settings()
