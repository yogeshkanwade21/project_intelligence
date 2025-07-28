from fastapi import FastAPI, HTTPException, status, Query, Request
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from config import Config
import requests
from jose import jwt
from pydantic import BaseModel

app = FastAPI(
    title="Auth Service",
    version="0.1.0",
)

# enable CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"message": "Auth service is running"}

# Auth ----------------------

# Pydantic model (class) for the token exchange request from Main Backend
class TokenExchangeRequest(BaseModel):
    code: str
    redirect_uri: str

# Pydantic model for the token exchange response to Main Backend
class TokenExchangeResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    id_token: str | None = None
    email: str | None = None
    sub: str | None = None
    name: str | None = None

@app.get("/auth-initiate")
async def auth_initiate(
    product_redirect_uri: str = Query(..., description="The callback URL of the backend initiating the login.")
):
    """
    Generates the Zoho authorization URL using the provided product_redirect_uri.
    """
    print(f"In Login Microservice: /auth-initiate")

    zoho_auth_url = (
        f"{Config.ZOHO_ACCOUNTS_URL}/oauth/v2/auth?"
        f"scope=WorkDrive.files.ALL,WorkDrive.teamfolders.READ,openid,email,profile&"
        f"client_id={Config.CLIENT_ID}&"
        f"response_type=code&"
        f"access_type=offline&"
        f"redirect_uri={product_redirect_uri}&"
        f"prompt=consent"
    )
    print(f"Login Microservice: Generated Zoho Auth URL for {product_redirect_uri}: {zoho_auth_url}")
    return {"auth_url": zoho_auth_url}

@app.post("/auth-exchange", response_model=TokenExchangeResponse)
async def auth_exchange(request_body: TokenExchangeRequest):
    """
    Exchanges the authorization code with Zoho for tokens, using the provided redirect_uri.
    """
    code = request_body.code
    product_redirect_uri = request_body.redirect_uri
    print(f"Login Microservice: Received code for exchange: {code[:10]}... with redirect_uri: {product_redirect_uri}")

    token_url = f"{Config.ZOHO_ACCOUNTS_URL}/oauth/v2/token"
    data = {
        'client_id': Config.CLIENT_ID,
        'client_secret': Config.CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': product_redirect_uri,
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    try:
        res = requests.post(token_url, data=data, headers=headers)
        res.raise_for_status()
        tokens = res.json()
        print(f"Login Microservice: Successfully received tokens from Zoho.")

        id_token = tokens.get('id_token')
        access_token = tokens.get('access_token')
        refresh_token = tokens.get('refresh_token')

        user_info = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'id_token': id_token,
        }

        if id_token:
            try:
                decoded = jwt.get_unverified_claims(id_token)
                user_info['email'] = decoded.get('email', '')
                user_info['sub'] = decoded.get('sub', '')
                user_info['name'] = decoded.get('name', '')
                print(f"Login Microservice: Decoded ID token user info.")
            except Exception as e:
                print(f"Login Microservice ERROR: Error decoding ID token: {e}")
                pass

            return user_info
        
    except requests.exceptions.RequestException as e:
        print(f"Login Microservice ERROR: Token exchange failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to exchange code for tokens with Zoho: {e}"
        )
    except Exception as e:
        print(f"Login Microservice ERROR: Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}"
        )
