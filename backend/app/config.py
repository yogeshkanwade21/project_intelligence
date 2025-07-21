from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    jira_host: str
    jira_protocol: str
    jira_api_token: str
    jira_email: str

    class Config:
      env_file = ".env"

settings = Settings()
