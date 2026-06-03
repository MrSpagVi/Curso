import urllib.request
import json

url = "https://api.github.com/repos/MrSpagVi/Curso/actions/runs?per_page=5"
print(f"Fetching runs from {url}...")
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    response = urllib.request.urlopen(req)
    data = json.loads(response.read().decode('utf-8'))
    for run in data.get('workflow_runs', []):
        print(f"Run ID: {run.get('id')}")
        print(f"Event: {run.get('event')}")
        print(f"Status: {run.get('status')}")
        print(f"Conclusion: {run.get('conclusion')}")
        print(f"Commit message: {run.get('head_commit', {}).get('message')}")
        print(f"Created at: {run.get('created_at')}")
        print("-" * 40)
except Exception as e:
    print(f"Error fetching runs: {e}")
