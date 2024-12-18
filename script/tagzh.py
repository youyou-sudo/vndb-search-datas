import requests
import os
import json
import subprocess

# 目标 JS 文件 URL
js_url = "https://update.greasyfork.org/scripts/445990/1315038/VNDBTranslatorLib_.js"
output_js_file = "VNDBTranslatorLib_.js"
output_json_file = "otherPageRules_output.json"

# 下载 JS 文件
response = requests.get(js_url)
if response.status_code == 200:
    with open(output_js_file, "wb") as file:
        file.write(response.content)
    print(f"Downloaded {output_js_file}")
else:
    print(f"Failed to download JS file, status code: {response.status_code}")
    exit(1)

# 在文件尾部追加代码
additional_code = f"""
const fs = require('fs');
fs.writeFileSync('{output_json_file}', JSON.stringify(otherPageRules, null, 2));
console.log('otherPageRules has been saved to {output_json_file}');
"""
with open(output_js_file, "a", encoding="utf-8") as file:
    file.write("\n" + additional_code)

print(f"Modified {output_js_file} to include otherPageRules export.")

# 使用 Node.js 运行修改后的 JS 文件
try:
    result = subprocess.run(["node", output_js_file], capture_output=True, text=True)
    print("Node.js output:")
    print(result.stdout)
    if result.stderr:
        print("Node.js error:")
        print(result.stderr)
except FileNotFoundError:
    print("Node.js is not installed or not in the PATH. Please install Node.js to proceed.")
    exit(1)

# 检查 JSON 文件是否生成
if os.path.exists(output_json_file):
    print(f"{output_json_file} has been created successfully.")
    with open(output_json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
        print("已输出成功")
else:
    print(f"Failed to create {output_json_file}.")
