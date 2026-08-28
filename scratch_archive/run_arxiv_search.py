import subprocess, json, sys
sys.stdout.reconfigure(encoding="utf-8")

queries = [
    'all:"residue number system" AND all:multiplier',
    'all:"residue number system" AND all:hierarchical',
    'all:"residue number system" AND all:"Karatsuba"',
    'all:"residue number system" AND all:"dynamic range"',
    'all:"multi-channel" AND all:"residue number system"'
]

for q in queries:
    print(f"=== QUERY: {q} ===")
    cmd = [
        'uv', 'run', '--directory', r'C:\Users\hp\.gemini\config\plugins\science\skills\literature_search_arxiv',
        'scripts/search_arxiv.py',
        '--query', q,
        '--max_results', '5'
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    try:
        data = json.loads(res.stdout)
        papers = data.get('papers', []) if isinstance(data, dict) else data
        for p in papers:
            print(f"[{p.get('id')}] {p.get('title')}")
            print(f"  URL: {p.get('pdf_url')}")
            print(f"  Summary: {p.get('summary')[:250].replace(chr(10), ' ')}...")
    except Exception as e:
        print("Error parsing:", e)
