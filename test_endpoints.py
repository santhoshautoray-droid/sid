import requests
import json

def test_endpoints():
    test_prompt = "professional female doctor in clinic"
    
    # 1. Test pollinations with different params
    print("Testing pollinations...")
    url = f"https://image.pollinations.ai/prompt/{test_prompt}?width=1280&height=720&nologo=true&enhance=false"
    try:
        r = requests.get(url, timeout=20)
        print("Pollinations status:", r.status_code, "len:", len(r.content))
    except Exception as e:
        print("Pollinations err:", e)

if __name__ == '__main__':
    test_endpoints()
