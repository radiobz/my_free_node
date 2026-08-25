import requests
import base64
import re

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
    
    # 导出为 base64
    merged_str = "\n".join(nodes)
    encoded_str = base64.b64encode(merged_str.encode('utf-8')).decode('utf-8')
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write(encoded_str)

    # 简易组装一个完整 Clash YAML 配置（免第三方转换）
    clash_config = f"""port: 7890
socks-port: 7891
allow-lan: true
mode: rule
log-level: info
proxy-providers:
  my-provider:
    type: http
    url: "https://cdn.jsdelivr.net/gh/radiobz/my_free_node@main/sub.txt"
    interval: 3600
    path: ./my-provider.yaml
    health-check:
      enable: true
      interval: 600
      url: http://www.gstatic.com/generate_204
proxy-groups:
  - name: "节点选择"
    type: select
    use:
      - my-provider
rules:
  - GEOIP,CN,DIRECT
  - MATCH,节点选择
"""
    with open("clash.yaml", "w", encoding="utf-8") as f:
        f.write(clash_config)
