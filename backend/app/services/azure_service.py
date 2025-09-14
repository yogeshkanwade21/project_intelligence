import logging
import httpx
import base64
from app.config import settings

logger = logging.getLogger(__name__)

AZURE_API_BASE = f"https://dev.azure.com/{settings.AZURE_ORGANIZATION}/{settings.AZURE_PROJECT}/_apis/wit/wiql"

async def search_issues(query: str):
  url = f"{AZURE_API_BASE}"
  auth_string = f":{settings.AZURE_PAT}"
  encoded_auth = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")
  other_headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Basic {encoded_auth}",  
    }
  params = {
    "api-version": "7.1",
  }

  logger.info(f"API URL: {url}")
  logger.info(f"API params: {params}")

  import urllib.parse

  full_url_with_params = f"{url}?{urllib.parse.urlencode(params)}"
  logger.info(f"Full URL sent: {full_url_with_params}")

  async with httpx.AsyncClient() as client:
    response = await client.post(url, headers=other_headers, params=params, json={"query": "SELECT [System.Id], [System.Title], [System.AssignedTo] FROM WorkItems WHERE [System.AssignedTo] = 'Yogesh Kanwade'"})
    response.raise_for_status()
    return response.json()
