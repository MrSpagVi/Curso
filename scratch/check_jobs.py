import urllib.request
import json

run_id = "26858023656"
url = f"https://api.github.com/repos/MrSpagVi/Curso/actions/runs/{run_id}/jobs"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    response = urllib.request.urlopen(req)
    data = json.loads(response.read().decode('utf-8'))
    for job in data.get('jobs', []):
        if job.get('name') == 'deploy':
            print(json.dumps(job, indent=2))
except Exception as e:
    print(f"Error: {e}")
