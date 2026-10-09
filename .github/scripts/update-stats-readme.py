"""Show the stats section only after both cards have been generated successfully."""

from pathlib import Path
import xml.etree.ElementTree as ET


for filename in ("stats.svg", "stats-dark.svg"):
    root = ET.parse(Path("profile") / filename).getroot()
    if root.tag != "{http://www.w3.org/2000/svg}svg":
        raise ValueError(f"{filename} is not a valid SVG card")
    title = root.find("{http://www.w3.org/2000/svg}title")
    if title is None or "GitHub Stats" not in (title.text or ""):
        raise ValueError(f"{filename} did not contain a GitHub stats card")

readme_path = Path("README.md")
readme = readme_path.read_text(encoding="utf-8")
start = "<!-- github-stats:start -->"
end = "<!-- github-stats:end -->"
if readme.count(start) != 1 or readme.count(end) != 1:
    raise ValueError("README must contain exactly one pair of stats markers")
before, rest = readme.split(start, 1)
_, after = rest.split(end, 1)

section = '''
<h2 align="center">GitHub stats &amp; rank</h2>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/bsoding/bsoding/main/profile/stats-dark.svg" />
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/bsoding/bsoding/main/profile/stats.svg" />
    <img src="https://raw.githubusercontent.com/bsoding/bsoding/main/profile/stats.svg" alt="bsoding's GitHub stats and letter rank, including private repository activity" />
  </picture>
</p>
'''

readme_path.write_text(before + start + "\n" + section + end + after, encoding="utf-8")
