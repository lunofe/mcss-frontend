import datetime
import os
import re
import shutil

import markdown
from bs4 import BeautifulSoup

# Define pages and mapping
pages = {
    "java-vanilla": "java/VANILLA.md",
    "java-plugins": "java/PLUGINS.md",
    "java-mods": "java/MODS.md",
    "java-hybrid": "java/MODS+PLUGINS.md",
    "java-proxies": "java/PROXIES.md",
    "java-regionized": "java/FOLIA.md",
    "java-limbo": "java/LIMBO.md",
    "bedrock-vanilla": "bedrock/VANILLA.md",
    "bedrock-plugins": "bedrock/PLUGINS.md",
    "bedrock-proxies": "bedrock/PROXIES.md",
    "miscellaneous": "OTHERS.md"
}

# Prepare directories
if os.path.exists("mcss-frontend/build"):
    shutil.rmtree("mcss-frontend/build")
os.makedirs("mcss-frontend/build", exist_ok=True)
shutil.copytree("mcss-frontend/assets/", "mcss-frontend/build/assets/")

# Load components
with open("mcss-frontend/commit.txt", "r") as f:
    commit = f.read().strip()
with open("mcss-frontend/components/header.html", "r") as f:
    header = f.read()
with open("mcss-frontend/components/landing.html", "r") as f:
    landing = f.read()
with open("mcss-frontend/components/catalog.html", "r") as f:
    catalog = f.read()
with open("mcss-frontend/components/footer.html", "r") as f:
    footer = f.read().format(current_date=datetime.datetime.now().strftime("%Y-%m-%d"), commit=commit)

# Build landing page
with open("mcss-frontend/build/index.html", "w") as f:
    with open("RECOMMEND.md", "r") as g:
        recommended = markdown.markdown(g.read())
        # Replace GitHub anchors with internal anchors
        for name, path in pages.items():
            recommended = recommended.replace(path, f"{name}/index.html")
    f.write(header.format(path="") + landing.format(recommended=recommended) + footer)

# Build catalog pages
for page in pages:
    # Prepare directories
    os.makedirs(f"mcss-frontend/build/{page}", exist_ok=True)
    # Load content and do basic replacements
    with open(pages[page], "r") as f:
        content = f.read().replace("###", "#####").replace("-->", "➜").replace("> **NOTE:**", "ℹ️ ").replace("**Plugins:** _Folia_", "**Plugins:** <abbr title='The Folia API is an extension of the Paper API which itself is based on Spigot and Bukkit. Bukkit, Spigot and Paper plugins should mostly be compatible, but have to specify compatibility manually.'>Folia</abbr>")
    # Parse content
    active = [item.replace("<article>", "<article class='note'>") if "h5" not in item else item for item in [f"<article>{markdown.markdown(item)}</article>" for item in content.split("# ✔️ Active Development")[1].split("# ❌ Inactive Development")[0].split("\n\n") if item and item != "\n"]]
    inactive = [f"<article class='warning'>{markdown.markdown(item)}</article>" for item in content.split("# ❌ Inactive Development")[1].split("\n\n") if item and item != "\n"]
    # Add IDs to anchors for direct linking
    for lists in [active, inactive]:
        for i, item in enumerate(lists):
            soup = BeautifulSoup(item, "html.parser")
            for a in soup.find_all("a"):
                a["id"] = re.sub(r"[^a-zA-Z0-9-]", "", a.get_text().lower().replace(" ", "-"))
            lists[i] = str(soup)
    # Write to file
    with open(f"mcss-frontend/build/{page}/index.html", "w") as f:
        f.write(header.format(path="../") + catalog.format(title=page.replace("-", " ").title(), active="".join(active), inactive="".join(inactive), hide_start="<!--" if len(inactive) == 0 else "", hide_end="-->" if len(inactive) == 0 else "") + footer)
