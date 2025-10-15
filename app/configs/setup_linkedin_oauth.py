import os
from dotenv import load_dotenv, set_key
import webbrowser
from urllib.parse import urlencode, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

load_dotenv()

CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")

REDIRECT_URI = "http://localhost:8888/callback"

SCOPES = ["openid", "profile", "w_member_social"]


class CallbackHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if '?' in self.path:
            query = parse_qs(self.path.split('?')[1])
            auth_code = query.get('code', [None])[0]
            error = query.get('error', [None])[0]
            
            if error:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                error_desc = query.get('error_description', ['Unknown error'])[0]
                self.wfile.write(f"<h1>Authorization failed!</h1><p>{error}: {error_desc}</p>".encode())
                self.server.auth_code = None
            elif auth_code:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<h1>Authorization successful!</h1><p>You can close this window and return to terminal.</p>")
                self.server.auth_code = auth_code
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<h1>No authorization code received!</h1>")
                self.server.auth_code = None
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass


def check_configuration():
    print("=" * 60)
    print("Checking Configuration")
    print("=" * 60)
    
    if not CLIENT_ID:
        print("LINKEDIN_CLIENT_ID not found in .env")
        return False
    
    if not CLIENT_SECRET:
        print("LINKEDIN_CLIENT_SECRET not found in .env")
        return False
    
    print(f"Client ID: {CLIENT_ID[:10]}...")
    print(f"Client Secret: {CLIENT_SECRET[:10]}...")
    print(f"Redirect URI: {REDIRECT_URI}")
    
    return True


def configure_linkedin_app():
    print("\n" + "=" * 60)
    print("⚠️  IMPORTANT: Configure LinkedIn App First!")
    print("=" * 60)
    
    print("\n1. Go to: https://www.linkedin.com/developers/apps")
    print("2. Click on your app")
    print("3. Go to 'Auth' tab")
    print("4. Under 'OAuth 2.0 settings' → 'Redirect URLs'")
    print(f"5. Add EXACTLY this URL: {REDIRECT_URI}")
    print("6. Click 'Update'")
    print("\nThe redirect URI must match EXACTLY (including http:// and port)")
    print("=" * 60)
    
    response = input("\nHave you added the redirect URI to LinkedIn app? (yes/no): ")
    return response.lower() in ['yes', 'y']


def get_linkedin_access_token():
    print("\n" + "=" * 60)
    print("LinkedIn OAuth Setup")
    print("=" * 60)
    
    if not check_configuration():
        print("\n❌ Please add LinkedIn credentials to .env file:")
        print("LINKEDIN_CLIENT_ID=your_client_id")
        print("LINKEDIN_CLIENT_SECRET=your_client_secret")
        print("\nGet them from: https://www.linkedin.com/developers/apps")
        return
    
    if not configure_linkedin_app():
        print("\n⚠️  Please configure the redirect URI first, then run this script again.")
        return
    
    auth_params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": " ".join(SCOPES)
    }
    
    auth_url = f"https://www.linkedin.com/oauth/v2/authorization?{urlencode(auth_params)}"
    
    print("\n" + "=" * 60)
    print("Step 1: Authorization")
    print("=" * 60)
    print("\nOpening browser for LinkedIn authorization...")
    print(f"\nIf browser doesn't open automatically, copy this URL:")
    print(f"\n{auth_url}\n")
    
    try:
        webbrowser.open(auth_url)
        print("Browser opened")
    except:
        print("Could not open browser automatically")
        print("Please copy the URL above and open it manually")
    
    print("\n" + "=" * 60)
    print("Step 2: Waiting for callback...")
    print("=" * 60)
    print(f"Local server started on http://localhost:8888")
    print("Authorize the app in your browser...")
    
    try:
        server = HTTPServer(('localhost', 8888), CallbackHandler)
        server.auth_code = None
        server.handle_request()
        
        if not server.auth_code:
            print("\nAuthorization failed or was cancelled!")
            print("\nPossible reasons:")
            print("1. You clicked 'Cancel' in the browser")
            print("2. The redirect URI doesn't match")
            print("3. Network/firewall issue")
            return
        
        print("Authorization code received")
        
    except OSError as e:
        if "Address already in use" in str(e):
            print("\nPort 8888 is already in use!")
            print("\nSolution: Stop any program using port 8888, or edit REDIRECT_URI in this script")
            print("Example: Change to http://localhost:8889/callback and update LinkedIn app")
        else:
            print(f"\nServer error: {e}")
        return

    print("\n" + "=" * 60)
    print("Step 3: Exchanging code for access token...")
    print("=" * 60)
    
    token_params = {
        "grant_type": "authorization_code",
        "code": server.auth_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    
    try:
        response = requests.post(
            "https://www.linkedin.com/oauth/v2/accessToken",
            data=token_params,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10
        )
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            expires_in = token_data.get("expires_in", "unknown")
            
            print(f"\nAccess token obtained!")
            print(f"Token length: {len(access_token)} characters")
            print(f"Expires in: {expires_in} seconds ({int(expires_in)//86400} days)" if expires_in != "unknown" else "")
            
            env_path = ".env"
            set_key(env_path, "LINKEDIN_ACCESS_TOKEN", access_token)
            
            print(f"\nToken saved to {env_path}")
            print(f"\nToken preview: {access_token[:30]}...{access_token[-10:]}")
            print("\n" + "=" * 60)
            print("Step 4: Testing token...")
            print("=" * 60)
            
            test_response = requests.get(
                "https://api.linkedin.com/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=10
            )
            
            if test_response.status_code == 200:
                user_data = test_response.json()
                print(f"Token works!")
                print(f"Name: {user_data.get('name', 'N/A')}")
                print(f"Email: {user_data.get('email', 'N/A')}")
                print(f"Sub: {user_data.get('sub', 'N/A')}")
                
                print("\n" + "=" * 60)
                print("Setup Complete!")
                print("=" * 60)
                print("\nYou can now use the LinkedIn posting functionality.")
                print("Run: python test_linkedin_posting.py")
                
            else:
                print(f"Token test failed: {test_response.status_code}")
                print(f"Response: {test_response.text}")
                print("\nToken was saved but might not have correct permissions.")
                print("Check 'Products' tab in LinkedIn app - ensure 'Share on LinkedIn' is approved")
        else:
            print(f"\nToken exchange failed!")
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if "invalid_redirect_uri" in response.text:
                print("\nREDIRECT URI MISMATCH!")
                print(f"Make sure this EXACT URL is in your LinkedIn app: {REDIRECT_URI}")
            
    except requests.exceptions.RequestException as e:
        print(f"\nNetwork error: {e}")


if __name__ == "__main__":
    get_linkedin_access_token()
