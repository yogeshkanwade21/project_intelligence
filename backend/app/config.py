from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    jira_host: str
    jira_protocol: str
    jira_api_token: str
    jira_email: str
    LOGIN_MICROSERVICE_URL: str
    MAIN_BACKEND_ZOHO_CALLBACK_URI: str
    FRONTEND_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
