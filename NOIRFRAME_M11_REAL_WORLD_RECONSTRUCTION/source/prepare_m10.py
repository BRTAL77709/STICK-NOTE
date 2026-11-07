from pathlib import Path
R=Path(__file__).resolve().parents[1]
for name in ['renders','debug','frames','reports','contact_sheets','scratch','sound','scenes','comparisons']:(R/name).mkdir(exist_ok=True)
print('M10 directories ready; existing files preserved')
