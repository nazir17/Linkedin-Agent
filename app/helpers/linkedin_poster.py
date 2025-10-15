import requests
from app.configs.config import settings



HEADERS = {
    'Authorization': f'Bearer {settings.LINKEDIN_ACCESS_TOKEN}',
    'Content-Type': 'application/json',
    'X-Restli-Protocol-Version': '2.0.0'
}



def post_to_linkedin(content: str):
    me_resp = requests.get('https://api.linkedin.com/v2/me', headers=HEADERS, timeout=20)
    if me_resp.status_code != 200:
        return {'success': False, 'status_code': me_resp.status_code, 'detail': me_resp.text}
    me = me_resp.json()
    author = f"urn:li:person:{me.get('id')}"


    body = {
        "author": author,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": content
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    resp = requests.post('https://api.linkedin.com/v2/ugcPosts', headers=HEADERS, json=body, timeout=30)
    if resp.status_code in (201, 200):
        return {'success': True, 'response': resp.json()}
    else:
        return {'success': False, 'status_code': resp.status_code, 'detail': resp.text}