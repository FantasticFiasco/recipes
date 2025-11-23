# Recipe Importer

A Python script to import recipes from online sources and convert them to the Docusaurus recipe site's Markdown format.

## Features

- ✅ Scrapes recipes from 100+ supported recipe websites (via [recipe-scrapers](https://github.com/hhursev/recipe-scrapers))
- ✅ Automatically detects recipe category (fisk, nöt, kyckling, fläsk, vegetariskt, bröd, sås, sött)
- ✅ Infers appropriate tags based on content (meal type, cuisine, etc.)
- ✅ Downloads recipe images or generates SVG placeholders
- ✅ Formats recipes in the site's Markdown structure with frontmatter
- ✅ Batch processes multiple URLs
- ✅ Handles duplicate filenames and errors gracefully

## Installation

1. Install Python 3.8 or higher
2. Install dependencies:

    ```bash
    cd scripts
    pip install -r requirements.txt
    ```

## Usage

### Import a single recipe

```bash
python import_recipes.py https://www.example.com/recipe
```

### Import multiple recipes

```bash
python import_recipes.py https://site1.com/recipe1 https://site2.com/recipe2
```

### Import from a file

Create a text file with URLs (one per line):

```text
# urls.txt
https://www.example.com/recipe1
https://www.example.com/recipe2
https://www.example.com/recipe3
```

Then import:

```bash
python import_recipes.py --file urls.txt
```

### Auto-detect category (no prompts)

```bash
python import_recipes.py --auto-category https://www.example.com/recipe
```

## How It Works

1. **Scrape**: Extracts recipe data (title, ingredients, instructions, image) from the URL
2. **Detect Category**: Analyzes content to determine which folder to save to (fisk, nöt, etc.)
3. **Infer Tags**: Automatically adds relevant tags like `middag`, `lunch`, `italien`, `mexikanskt`
4. **Download Image**: Downloads the recipe's main image, or generates an SVG placeholder if unavailable
5. **Format Markdown**: Creates a properly formatted `.md` file with frontmatter
6. **Save**: Saves both the Markdown file and image to the appropriate category folder

## Output Structure

For a recipe titled "Boeuf Bourguignon", the script creates:

```text
docs/nöt/
  ├── boeuf-bourguignon.md
  └── boeuf-bourguignon.jpg
```

The Markdown file will have this structure:

```markdown
---
tags:
    - france
    - middag
---
# Boeuf Bourguignon

![image](./boeuf-bourguignon.jpg)

Optional description paragraph...

## Ingredienser

- 1 kg högrev
- 2 morötter
- ...

## Gör så här

1. First step...
2. Second step...
...
```

## Supported Websites

The script uses [recipe-scrapers](https://github.com/hhursev/recipe-scrapers) which supports 100+ recipe websites including:

- AllRecipes
- BBC Food
- Bon Appétit
- Epicurious
- Food Network
- ICA.se
- Jamie Oliver
- Serious Eats
- And many more...

## Troubleshooting

### "Failed to scrape recipe"

The website may not be supported by recipe-scrapers. Check the [supported sites list](https://github.com/hhursev/recipe-scrapers#scrapers-available-for).

### Image download failed

The script will automatically generate an SVG placeholder. You can manually replace it later with a proper image.

### Category detection incorrect

Run without `--auto-category` flag to manually select the category when prompted.

## Examples

Import Swedish recipes:

```bash
python import_recipes.py https://www.ica.se/recept/some-recipe
```

Import with manual category selection:

```bash
python import_recipes.py https://www.example.com/recipe
# You'll be prompted to select: fisk, nöt, kyckling, etc.
```

Batch import from file:

```bash
python import_recipes.py --file batch-recipes.txt
```

## Notes

- Recipe URLs must be from websites supported by the recipe-scrapers library
- Duplicate filenames will prompt for confirmation before overwriting
- Tags are automatically inferred but can be manually edited in the generated Markdown files
- Images are saved with the same filename as the Markdown file (e.g., `recipe-name.md` + `recipe-name.jpg`)
