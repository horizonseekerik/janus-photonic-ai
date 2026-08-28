# update script
import re

with open('PROJECT_JANUS_STRATEGIC_ROADMAP.md', 'r', encoding='utf-8') as f:
    content = f.read()

print('Original length:', len(content))
