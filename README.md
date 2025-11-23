# Recipes

[![CI](https://github.com/FantasticFiasco/recipes/actions/workflows/ci.yml/badge.svg)](https://github.com/FantasticFiasco/recipes/actions/workflows/ci.yml)
[![pages-build-deployment](https://github.com/FantasticFiasco/recipes/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/FantasticFiasco/recipes/actions/workflows/pages/pages-build-deployment)

A Docusaurus-based recipe website with support for importing recipes from online sources.

## Recipe importer

Import recipes from 100+ supported websites automatically. The importer:

- Scrapes recipe data (title, ingredients, instructions, images)
- Automatically detects categories and infers tags
- Downloads images or generates placeholders
- Formats everything in the site's Markdown structure

See [scripts/README.md](scripts/README.md) for detailed usage instructions.

**Quick start:**

```bash
cd scripts
./setup.sh                                      # Install dependencies
source venv/bin/activate                        # Activate environment
python import_recipes.py <recipe-url>           # Import a recipe
```
