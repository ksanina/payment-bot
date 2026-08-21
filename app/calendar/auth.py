from pathlib import Path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CREDENTIALS_FILE = PROJECT_ROOT / "credentials.json"
TOKEN_FILE = PROJECT_ROOT / "token.json"

SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
]

def get_credentials() -> Credentials:
    if TOKEN_FILE.exists():
        return Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES,
        )

    flow = InstalledAppFlow.from_client_secrets_file(
        CREDENTIALS_FILE,
        SCOPES,
    )
    credentials = flow.run_local_server(port=0)
    TOKEN_FILE.write_text(credentials.to_json())

    return credentials
