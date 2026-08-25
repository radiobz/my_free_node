import requests
import base64
import yaml

# 高星且每日自动更新的公开节点源
SOURCES = [
    "https://raw.githubusercontent.com/freefq/free/master/v2",
    "https://raw.githubusercontent.com/m2ray/v2rayN-share/main/sub/sub_merge.txt",
    "https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub"
]

def get_nodes():
    all_nodes = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for url in SOURCES:
        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                content = res.text.strip()
                try:
                    decoded = base64.b64decode(content + '==').decode('utf-8', errors='ignore')
                    lines = decoded.splitlines()
                except Exception:
                    lines = content.splitlines()
                
                for line in lines:
                    line = line.strip()
                    if any(line.startswith(p) for p in ['vmess://', 'vless://', 'ss://', 'trojan://', 'hy2://']):
                        if line not in all_nodes:
                            all_nodes.append(line)
        except Exception as e:
            print(f"Fetch error: {e}")
            
    return all_nodes

if __name__ == "__main__":
    nodes = get_nodes()
    # 写入裸 base64
    merged_str = "\n".join(nodes)
    encoded_str = base64.b64encode(merged_str.encode('utf-8')).decode('utf-8')
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write(encoded_str)
