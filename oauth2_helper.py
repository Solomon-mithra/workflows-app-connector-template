#!/usr/bin/env python3
"""
OAuth2 Helper for Google Sheets API

This script helps you get an OAuth2 access token for the Google Sheets API.
Use this token in your create_google_sheet module.

Instructions:
1. Replace CLIENT_ID and CLIENT_SECRET with your values
2. Run: python oauth2_helper.py
3. Follow the browser prompt to authorize
4. Copy the access token that's printed
"""

import webbrowser
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import json

# Replace these with your OAuth2 credentials from Google Cloud Console
CLIENT_ID = "1075481901804-v015ks00020fsnn4ptv1f1bjibvgqoh0.apps.googleusercontent.com"
CLIENT_SECRET = "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"  # Your actual client secret

# OAuth2 configuration
REDIRECT_URI = "http://localhost:8080/callback"
SCOPES = "https://www.googleapis.com/auth/spreadsheets https://www.googleapis.com/auth/drive.file"

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/callback'):
            # Parse the authorization code from the callback
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            
            if 'code' in params:
                auth_code = params['code'][0]
                print(f"Authorization code received: {auth_code}")
                
                # Exchange authorization code for access token
                token_data = {
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET,
                    'code': auth_code,
                    'grant_type': 'authorization_code',
                    'redirect_uri': REDIRECT_URI
                }
                
                response = requests.post('https://oauth2.googleapis.com/token', data=token_data)
                
                if response.status_code == 200:
                    token_info = response.json()
                    access_token = token_info.get('access_token', '')
                    refresh_token = token_info.get('refresh_token', '')
                    expires_in = token_info.get('expires_in', '')
                    
                    print("\n" + "="*60)
                    print("SUCCESS! OAuth2 tokens received:")
                    print("="*60)
                    print(f"Access Token: {access_token}")
                    print(f"Refresh Token: {refresh_token}")
                    print(f"Expires in: {expires_in} seconds")
                    print("="*60)
                    print("\nCopy the Access Token above and use it in your create_google_sheet module!")
                    print("Note: Access tokens expire. Use the refresh token to get new ones.")
                    
                    # Send success response to browser
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b'''
                    <html><body>
                    <h2>Authorization Successful!</h2>
                    <p>You can close this window and return to your terminal.</p>
                    <p>Your access token has been printed in the terminal.</p>
                    </body></html>
                    ''')
                    
                    # Store tokens for later use
                    with open('oauth_tokens.json', 'w') as f:
                        json.dump(token_info, f, indent=2)
                    print(f"\nTokens also saved to: oauth_tokens.json")
                    
                else:
                    print(f"Error getting access token: {response.text}")
                    self.send_response(400)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b'<html><body><h2>Error getting access token</h2></body></html>')
            
            elif 'error' in params:
                error = params['error'][0]
                print(f"Authorization error: {error}")
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f'<html><body><h2>Authorization Error: {error}</h2></body></html>'.encode())

def main():
    if CLIENT_SECRET == "PASTE_YOUR_CLIENT_SECRET_HERE":
        print("ERROR: Please replace CLIENT_SECRET with your actual client secret!")
        print("You can find it in your Google Cloud Console OAuth2 credentials.")
        return
    
    print("Google Sheets OAuth2 Helper")
    print("="*30)
    print(f"Client ID: {CLIENT_ID}")
    print(f"Redirect URI: {REDIRECT_URI}")
    print(f"Scopes: {SCOPES}")
    print()
    
    # Build authorization URL
    auth_params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPES,
        'response_type': 'code',
        'access_type': 'offline',  # Get refresh token
        'prompt': 'consent'  # Force consent screen to get refresh token
    }
    
    auth_url = 'https://accounts.google.com/o/oauth2/auth?' + urllib.parse.urlencode(auth_params)
    
    print("Step 1: Starting local callback server...")
    httpd = HTTPServer(('localhost', 8080), CallbackHandler)
    
    print("Step 2: Opening browser for authorization...")
    print(f"If browser doesn't open, visit: {auth_url}")
    webbrowser.open(auth_url)
    
    print("Step 3: Waiting for authorization callback...")
    print("(Complete the authorization in your browser)")
    
    # Handle one request (the callback)
    httpd.handle_request()
    httpd.server_close()
    
    print("\nDone! Server stopped.")

if __name__ == "__main__":
    main()
