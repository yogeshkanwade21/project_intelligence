import logging
from fastapi import FastAPI, HTTPException, status, Query, Request
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
import httpx
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser, JsonOutputParser
from fastapi.middleware.cors import CORSMiddleware
from app.routes import jira
from app.orchestrator.intent_extractor import extract_intent
from app.orchestrator.jql_generator import generate_jql
from app.services import jira_service
from app.config import settings


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Project Intelligence Backend",
    version="0.1.0",
)

# CORS Middleware
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(jira.router)

prompt2 = PromptTemplate(
    template="You are a project assistant" \
    "Extract the summary for each Jira object which is referenced as 'fields' -> 'summary' inside the object ."  \
    "Extract the status for each Jira object which is referenced as 'fields' -> 'status' -> 'name' inside the object ."  \
    "Extract the story point estimate for each Jira object which is referenced as 'fields' -> 'customfield_10016' inside the object ."  \
    "I want you to provide insights about the project from this data JIRA API Response: {jira_api_response}."  \
    "This is aimed at helping users understand the current state of the project and help them make informed decisions."  \
    "You must only respond with your insights based on input data and nothing else. Do not give extracted Data." \
    "Your output must not be more than 200 words.", \
    input_variables=["jira_api_response"],
)

prompt1 = PromptTemplate(
    template="You are a JIRA expert. Based on the following user query, generate a valid JQL string only." \
    "User query: {user_query}" \
    "Your output must be a valid string and nothing else.",
    input_variables=["user_query"],
)

llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=settings.GOOGLE_GENERATIVE_AI_KEY,
        temperature=0,
        tool_choice="auto",
    )

# 1 query -> jql
jql_chain = prompt1 | llm

# 2 jira api -> insights
chain = prompt2 | llm

# Auth ----------------------

@app.get("/login")
async def login():
    """
    Initiates the login flow by asking the Login Microservice for the Zoho auth URL.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.LOGIN_MICROSERVICE_URL}/auth-initiate",
                params={"product_redirect_uri": settings.MAIN_BACKEND_ZOHO_CALLBACK_URI}
            )
            response.raise_for_status()
            data = response.json()
            zoho_auth_url = data.get("auth_url")

            if not zoho_auth_url:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Login Microservice did not return auth_url"
                )

            print(f"Main Backend: Redirecting browser to Zoho Auth URL: {zoho_auth_url}")
            return RedirectResponse(zoho_auth_url, status_code=status.HTTP_302_FOUND)

    except httpx.RequestError as e:
        print(f"Main Backend ERROR: Failed to get auth URL from Login Microservice due to network error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initiate login due to network error: {e}"
        )
    except httpx.HTTPStatusError as e:
        print(f"Main Backend ERROR: Login Microservice returned HTTP error: {e.response.status_code} - {e.response.text}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login Microservice returned an error: {e.response.status_code}"
        )
    except Exception as e:
        print(f"Main Backend ERROR: Unexpected error during login initiation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}"
        )

@app.get("/oauth/callback")
async def oauth_callback(code: str = None):
    """
    Handles the callback from Zoho, exchanges code via Login Microservice,
    and redirects to frontend with user info in URL parameters.
    """
    print(f"Main Backend: /oauth/callback endpoint hit. Code received: {code[:10]}...")

    if not code:
        print("Main Backend: No code received. Redirecting to frontend with error.")
        return RedirectResponse(f"{settings.FRONTEND_URL}/chat?error=no_auth_code", status_code=status.HTTP_302_FOUND)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.LOGIN_MICROSERVICE_URL}/auth-exchange",
                json={
                    "code": code,
                    "redirect_uri": settings.MAIN_BACKEND_ZOHO_CALLBACK_URI
                }
            )
            response.raise_for_status()
            tokens_and_user_info = response.json()
            print(f"Main Backend: Received tokens and user info from Login Microservice.")
            print(f"Main Backend: User info: {tokens_and_user_info}")

            # --- IMPORTANT: Session Management (Next Step) ---
            # With SessionMiddleware removed, we are NOT setting a server-side session cookie here.
            # The user info is passed directly to the frontend via URL parameters.
            # For a production app, you MUST implement proper session management (e.g.,
            # set a secure HttpOnly cookie with a session ID, or issue your own JWT)
            # after confirming this basic redirect works.

            user_info_params = {
                'email': tokens_and_user_info.get('email'),
                'name': tokens_and_user_info.get('name'),
                'sub': tokens_and_user_info.get('sub')
            }
            user_info_params = {k: v for k, v in user_info_params.items() if v is not None}
            redirect_url_with_params = f"{settings.FRONTEND_URL}/chat"

            print(f"Main Backend: Final redirecting browser to frontend: {redirect_url_with_params}")
            return RedirectResponse(url=redirect_url_with_params, status_code=status.HTTP_302_FOUND)

    except httpx.RequestError as e:
        print(f"Main Backend ERROR: Failed to exchange code with Login Microservice due to network error: {e}")
        return RedirectResponse(f"{settings.FRONTEND_URL}/chat?error=token_exchange_failed", status_code=status.HTTP_302_FOUND)
    except httpx.HTTPStatusError as e:
        print(f"Main Backend ERROR: Login Microservice returned HTTP error: {e.response.status_code} - {e.response.text}")
        return RedirectResponse(f"{settings.FRONTEND_URL}/chat?error=token_exchange_failed", status_code=status.HTTP_302_FOUND)
    except Exception as e:
        print(f"Main Backend ERROR: Unexpected error during callback processing: {e}")
        return RedirectResponse(f"{settings.FRONTEND_URL}/chat?error=internal_server_error", status_code=status.HTTP_302_FOUND)


@app.post("/query/handle")
async def analyze_query(payload: dict):
    logger.info(f"Received payload: {payload}")
    query = payload.get("query")
    if not query:
        logger.error("Query not provided in payload")
        raise HTTPException(status_code=400, detail="Query not provided")

    jql_response = jql_chain.invoke({"user_query": query})
    logger.info(f"jql_response: {jql_response}")

    jql = jql_response.content
    
    # logger.info(f"Extracting intent from query: {query}")
    # intent = extract_intent(query)
    # if not intent:
    #     logger.error(f"Could not extract intent from query: {query}")
    #     raise HTTPException(status_code=400, detail="Could not understand the query")

    # logger.info(f"Extracted intent: {intent}")
    # jql = generate_jql(intent)
    # if not jql:
    #     logger.error(f"Could not generate JQL for intent: {intent}")
    #     raise HTTPException(status_code=400, detail="Could not generate JQL for the given intent")

    logger.info(f"Generated JQL: {jql}")
    try:
        response = await jira_service.search_issues(jql)
        formatted_issues = "\n".join(
            f"- {i['key']}: {i['fields']['summary']} (Status: {i['fields']['status']['name']}) (Story Point Estimate: {i['fields']['customfield_10016']} ) (Status: {i['fields']['status']['name']})"
            for i in response["issues"]
        )
        response_data_for_frontend = []
        # logger.info(f"Successfully fetched {len(response.get('issues', []))} issues")
        logger.info(f"Successfully fetched formatted_issues: {formatted_issues}")
        # return formatted_issues
        results = chain.invoke({"jira_api_response": response})
        logger.info(f"results from llm: {results}")

        # result = chain.invoke({"jira_api_response": formatted_issues})
        # result = llm.invoke({"capital of india"})
        return results.content
        for issue in response.get('issues', []):
            issue_key = issue.get('key', 'UnknownKey')
            summary = issue.get('fields', {}).get('summary', 'No summary')
            response_data_for_frontend.append({
                'summary': summary,
                'issue_key': issue_key,
                'type': 'bug'
            })
        return response_data_for_frontend
    except Exception as e:
        logger.error(f"Error fetching issues from Jira: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"message": "FastAPI backend is running"}


