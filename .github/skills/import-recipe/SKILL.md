---
name: import-recipe
description: "Import/scrape a recipe from a URL into the Docusaurus recipe site. Use when: scraping a recipe, importing a recipe, adding a recipe from a URL, downloading a recipe from a website."
argument-hint: "Provide one or more recipe URLs to import"
---

# Import Recipe

Scrape one or more recipes from online sources and save them as Markdown files in the `docs/` folder using the project's Python importer script.

## When to Use

- User wants to import/scrape a recipe from a URL
- User wants to add a recipe from a website
- User wants to batch-import several recipe URLs

## Prerequisites

The script requires a Python 3.8+ virtual environment with dependencies installed. The setup script at `scripts/setup.sh` creates and configures this automatically.

**Dependencies** (from `scripts/requirements.txt`):
- `requests>=2.31.0`
- `beautifulsoup4>=4.12.0`
- `recipe-scrapers>=14.50.0`

## Procedure

### 1. Ensure the virtual environment is ready

Run the following from the `scripts/` directory:

```bash
cd scripts
```

If `scripts/venv/` does not exist, create it:

```bash
bash setup.sh
```

If it already exists, just activate it:

```bash
source venv/bin/activate
```

### 2. Run the importer

For one or more URLs, run:

```bash
python import_recipes.py --auto-category <url1> [url2] ...
```

The `--auto-category` flag skips interactive category prompts by auto-detecting the category from recipe content.

Alternatively, import from a file of URLs (one per line, `#` comments allowed):

```bash
python import_recipes.py --auto-category --file urls.txt
```

### 3. Verify output

The script will:
1. Scrape recipe data (title, ingredients, instructions, image)
2. Auto-detect the category folder (`fisk`, `nöt`, `kyckling`, `fläsk`, `vegetariskt`, `bröd`, `sås`, `sött`)
3. Download the recipe image (or generate an SVG placeholder)
4. Save a `.md` file with frontmatter, image reference, ingredients, and instructions into the appropriate `docs/<category>/` folder

Check the summary output for any failures.

### 4. Build the site

From the repository root, build the Docusaurus site to verify the new recipe integrates correctly:

```bash
cd /path/to/repo
npm run build
```

The build must succeed with no errors. If the build fails, fix the generated Markdown file(s) and re-run the build until it passes.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | Run `bash setup.sh` or `pip install -r requirements.txt` inside the venv |
| `Failed to scrape recipe` | The website may not be supported by [recipe-scrapers](https://github.com/hhursev/recipe-scrapers#scrapers-available-for) |
| Category detected incorrectly | Remove `--auto-category` to get an interactive prompt, or move the file manually after import |
| Image download fails | The script auto-generates an SVG placeholder; replace it later with a real image |

## Supported Websites

The script uses the [recipe-scrapers](https://github.com/hhursev/recipe-scrapers) library, which supports 100+ websites including AllRecipes, BBC Food, ICA.se, and many more.
