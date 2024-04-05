# ![Minecraft Server Softwares Frontend](https://raw.githubusercontent.com/lunofe/mcss-frontend/HEAD/.github/mcss-frontend.svg)

This script is designed to be used in a GitHub workflow or action to generate a static website from [`LeStegii/server-softwares`](https://github.com/LeStegii/server-softwares)' Markdown files. The generated website uses the Pico CSS library to provide a clean and modern look.

## Functionality
1. The webpages and their assignment to specific Markdown files are defined.
2. Directories are prepared and all necessary website assets are copied.
3. Various components, including the header & footer are loaded.
4. The landing page is built and GitHub anchors are replaced with internal anchors.
5. Catalog pages are constructed by loading content and performing basic replacements.
6. The content is divided into active and inactive sections, and IDs are added to anchor tags for direct linking.
7. Finally, the generated HTML files are written to the build directory.

## Requirements
- Python 3.11
- BeautifulSoup4
- Markdown

## Set up development environment
1. Clone [`LeStegii/server-softwares`](https://github.com/LeStegii/server-softwares)
2. Clone this repository into `sever-softwares/mcss-frontend` directory
3. `pip install markdown beautifulsoup4`
4. Run `python mcss-frontend/build.py` (your working directory needs to be `server-softwares`) to generate the website
