#!/usr/bin/env python3
"""
Recipe Importer for Docusaurus Recipe Site

This script scrapes recipes from online sources and converts them to the site's
Markdown format with appropriate frontmatter and images.

Usage:
    python import_recipes.py <url1> [url2] [url3] ...
    python import_recipes.py --file urls.txt
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from recipe_scrapers import scrape_me


def slugify(text: str) -> str:
    """Convert text to kebab-case slug suitable for filenames."""
    # Remove special characters and convert to lowercase
    text = text.lower()
    # Replace Swedish characters
    text = text.replace('å', 'a').replace('ä', 'a').replace('ö', 'o')
    text = text.replace('é', 'e').replace('è', 'e')
    # Remove any non-alphanumeric characters except spaces and hyphens
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    # Replace spaces with hyphens
    text = re.sub(r'[\s_]+', '-', text)
    # Remove multiple consecutive hyphens
    text = re.sub(r'-+', '-', text)
    # Strip leading/trailing hyphens
    return text.strip('-')


def detect_category(title: str, ingredients: str, instructions: str) -> str:
    """
    Detect the appropriate category folder based on recipe content.
    Returns one of: fisk, nöt, kyckling, fläsk, vegetariskt, bröd, sås, sött
    """
    content = f"{title} {ingredients} {instructions}".lower()

    # Check for keywords in order of specificity
    fish_keywords = ['fisk', 'lax', 'torsk', 'räk', 'sej', 'tonfisk', 'matjessill', 'sill']
    beef_keywords = ['nöt', 'högrev', 'oxfilé', 'biff', 'entrecote', 'oxfile', 'oxkött', 'nötkött']
    chicken_keywords = ['kyckling', 'kalkon']
    pork_keywords = ['fläsk', 'bacon', 'sidfläsk', 'karré', 'kotlett', 'pulled pork']
    bread_keywords = ['bröd', 'limpa', 'pizza', 'focaccia', 'bagel', 'knäcke', 'deg']
    sauce_keywords = ['sås', 'såsen', 'dressing']
    dessert_keywords = ['dessert', 'efterrätt', 'kaka', 'tårta', 'brownie', 'pannkak', 'våffl',
                       'maräng', 'choklad', 'glass', 'mousse']
    vegetarian_keywords = ['vegetarisk', 'vegan', 'tofu', 'halloumi', 'grönsaksgr']

    # Check each category
    if any(keyword in content for keyword in fish_keywords):
        return 'fisk'
    elif any(keyword in content for keyword in chicken_keywords):
        return 'kyckling'
    elif any(keyword in content for keyword in pork_keywords):
        return 'fläsk'
    elif any(keyword in content for keyword in beef_keywords):
        return 'nöt'
    elif any(keyword in content for keyword in dessert_keywords):
        return 'sött'
    elif any(keyword in content for keyword in bread_keywords):
        return 'bröd'
    elif any(keyword in content for keyword in sauce_keywords):
        return 'sås'
    elif any(keyword in content for keyword in vegetarian_keywords):
        return 'vegetariskt'

    # Default to asking user
    return None


def infer_tags(title: str, ingredients: str, instructions: str, category: str) -> List[str]:
    """Infer appropriate tags based on recipe content."""
    content = f"{title} {ingredients} {instructions}".lower()
    tags = []

    # Meal type
    if any(word in content for word in ['middag', 'huvudrätt']):
        tags.append('middag')
    elif any(word in content for word in ['lunch']):
        tags.append('lunch')
    elif any(word in content for word in ['frukost', 'breakfast']):
        tags.append('frukost')
    elif any(word in content for word in ['brunch']):
        tags.append('brunch')
    elif any(word in content for word in ['förrätt', 'appetizer']):
        tags.append('förrätt')
    elif any(word in content for word in ['efterrätt', 'dessert']):
        tags.append('efterrätt')
    elif any(word in content for word in ['fika', 'mellanmål']):
        tags.append('fika')

    # Cuisine/origin
    cuisine_map = {
        'italien': ['italien', 'italian', 'pasta', 'risotto', 'pizza'],
        'frankrike': ['fransk', 'french', 'bourguignon'],
        'mexico': ['mexikansk', 'mexican', 'taco', 'fajita', 'burrito'],
        'asien': ['asiatisk', 'asian', 'wok'],
        'kina': ['kinesisk', 'chinese'],
        'thailand': ['thailändsk', 'thai'],
        'japan': ['japansk', 'japanese', 'sushi'],
        'indien': ['indisk', 'indian', 'curry'],
        'grekland': ['grekisk', 'greek', 'moussaka', 'tzatziki'],
        'sverige': ['svensk', 'swedish'],
        'amerika': ['amerikansk', 'american'],
        'vietnam': ['vietnamesisk', 'vietnamese', 'banh'],
        'sydkorea': ['koreansk', 'korean', 'kimchi'],
    }

    for tag, keywords in cuisine_map.items():
        if any(keyword in content for keyword in keywords):
            tags.append(tag)
            break

    # Food type
    if category == 'fisk':
        tags.append('lax') if 'lax' in content else None
    elif category in ['nöt', 'fläsk', 'kyckling']:
        tags.append('kött')
    elif category == 'vegetariskt':
        tags.append('vegetariskt')

    # Special occasions
    if 'påsk' in content:
        tags.append('påsk')
    elif 'jul' in content:
        tags.append('jul')

    # Remove None values
    tags = [t for t in tags if t]

    # Default to middag if no meal type found
    if not any(t in ['middag', 'lunch', 'frukost', 'brunch', 'förrätt', 'efterrätt', 'fika'] for t in tags):
        tags.append('middag')

    return tags


def scrape_recipe(url: str) -> Dict:
    """Scrape recipe data from a URL using recipe-scrapers library."""
    try:
        scraper = scrape_me(url)

        # Extract basic information
        recipe_data = {
            'title': scraper.title(),
            'ingredients': scraper.ingredients(),
            'instructions': scraper.instructions(),
            'image_url': None,
            'description': None,
        }

        # Try to get image
        try:
            recipe_data['image_url'] = scraper.image()
        except Exception:
            pass

        # Try to get description
        try:
            recipe_data['description'] = scraper.description()
        except Exception:
            pass

        return recipe_data

    except Exception as e:
        raise Exception(f"Failed to scrape recipe from {url}: {str(e)}")


def download_image(url: str, output_path: Path) -> bool:
    """Download image from URL to the specified path."""
    try:
        response = requests.get(url, timeout=30, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            f.write(response.content)

        return True
    except Exception as e:
        print(f"  Warning: Failed to download image: {str(e)}")
        return False


def generate_image_placeholder(output_path: Path, title: str) -> bool:
    """
    Generate a placeholder image when download fails.
    For now, this creates a simple SVG placeholder.
    In the future, this could be replaced with AI image generation.
    """
    try:
        svg_content = f'''<svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
  <rect width="800" height="600" fill="#f0f0f0"/>
  <text x="50%" y="50%" font-family="Arial, sans-serif" font-size="24"
        fill="#666" text-anchor="middle" dominant-baseline="middle">
    {title}
  </text>
  <text x="50%" y="55%" font-family="Arial, sans-serif" font-size="16"
        fill="#999" text-anchor="middle" dominant-baseline="middle">
    Placeholder Image
  </text>
</svg>'''

        # Save as SVG (can be converted to PNG later if needed)
        output_path = output_path.with_suffix('.svg')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)

        return True
    except Exception as e:
        print(f"  Warning: Failed to generate placeholder image: {str(e)}")
        return False


def format_markdown(recipe_data: Dict, tags: List[str], image_filename: str) -> str:
    """Format recipe data into the site's Markdown structure."""
    lines = []

    # Frontmatter
    lines.append('---')
    if tags:
        lines.append('tags:')
        for tag in tags:
            lines.append(f'    - {tag}')
    lines.append('---')

    # Title
    lines.append(f"# {recipe_data['title']}")
    lines.append('')

    # Image
    lines.append(f"![image](./{image_filename})")
    lines.append('')

    # Description (if available)
    if recipe_data.get('description'):
        lines.append(recipe_data['description'])
        lines.append('')

    # Ingredients
    lines.append('## Ingredienser')
    lines.append('')

    ingredients = recipe_data['ingredients']
    if isinstance(ingredients, list):
        for ingredient in ingredients:
            lines.append(f"- {ingredient}")
    else:
        # If it's a string, split by newlines
        for ingredient in ingredients.split('\n'):
            if ingredient.strip():
                lines.append(f"- {ingredient.strip()}")
    lines.append('')

    # Instructions
    lines.append('## Gör så här')
    lines.append('')

    instructions = recipe_data['instructions']
    if isinstance(instructions, str):
        # Split into steps
        steps = [s.strip() for s in instructions.split('\n') if s.strip()]
        for i, step in enumerate(steps, 1):
            # Remove existing numbering if present
            step = re.sub(r'^\d+[\.\)]\s*', '', step)
            lines.append(f"{i}. {step}")
    else:
        # If it's already a list
        for i, step in enumerate(instructions, 1):
            lines.append(f"{i}. {step}")

    return '\n'.join(lines) + '\n'


def prompt_category() -> str:
    """Prompt user to select a category."""
    categories = ['fisk', 'nöt', 'kyckling', 'fläsk', 'vegetariskt', 'bröd', 'sås', 'sött']

    print("\nAvailable categories:")
    for i, cat in enumerate(categories, 1):
        print(f"  {i}. {cat}")

    while True:
        try:
            choice = input("\nSelect category (1-8): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(categories):
                return categories[idx]
            else:
                print("Invalid selection. Please enter a number between 1 and 8.")
        except (ValueError, KeyboardInterrupt):
            print("\nCancelled.")
            return None


def import_recipe(url: str, docs_dir: Path, auto_category: bool = False) -> bool:
    """Import a single recipe from a URL."""
    print(f"\n{'='*60}")
    print(f"Processing: {url}")
    print('='*60)

    try:
        # Scrape recipe
        print("  Scraping recipe data...")
        recipe_data = scrape_recipe(url)
        print(f"  ✓ Found: {recipe_data['title']}")

        # Detect category
        ingredients_str = ' '.join(recipe_data['ingredients']) if isinstance(recipe_data['ingredients'], list) else recipe_data['ingredients']
        instructions_str = recipe_data['instructions'] if isinstance(recipe_data['instructions'], str) else ' '.join(recipe_data['instructions'])

        category = detect_category(recipe_data['title'], ingredients_str, instructions_str)

        if not category or not auto_category:
            print(f"\n  Detected category: {category or 'unknown'}")
            category = prompt_category()
            if not category:
                print("  Skipped.")
                return False
        else:
            print(f"  ✓ Category: {category}")

        # Create category directory if it doesn't exist
        category_dir = docs_dir / category
        category_dir.mkdir(exist_ok=True)

        # Generate filename
        slug = slugify(recipe_data['title'])
        md_filename = f"{slug}.md"
        md_path = category_dir / md_filename

        # Check if file already exists
        if md_path.exists():
            response = input(f"\n  File '{md_filename}' already exists. Overwrite? (y/n): ").strip().lower()
            if response != 'y':
                print("  Skipped.")
                return False

        # Infer tags
        tags = infer_tags(recipe_data['title'], ingredients_str, instructions_str, category)
        print(f"  ✓ Tags: {', '.join(tags)}")

        # Handle image
        image_filename = None
        if recipe_data.get('image_url'):
            print(f"  Downloading image...")
            # Determine image extension from URL
            parsed = urlparse(recipe_data['image_url'])
            ext = Path(parsed.path).suffix or '.jpg'
            image_filename = f"{slug}{ext}"
            image_path = category_dir / image_filename

            if download_image(recipe_data['image_url'], image_path):
                print(f"  ✓ Image saved: {image_filename}")
            else:
                print("  Generating placeholder image...")
                image_filename = f"{slug}.svg"
                image_path = category_dir / image_filename
                if generate_image_placeholder(image_path, recipe_data['title']):
                    print(f"  ✓ Placeholder saved: {image_filename}")
                else:
                    image_filename = None
        else:
            print("  No image URL found. Generating placeholder...")
            image_filename = f"{slug}.svg"
            image_path = category_dir / image_filename
            if generate_image_placeholder(image_path, recipe_data['title']):
                print(f"  ✓ Placeholder saved: {image_filename}")
            else:
                image_filename = None

        # Generate markdown
        markdown_content = format_markdown(recipe_data, tags, image_filename or f"{slug}.jpg")

        # Save markdown file
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        print(f"  ✓ Recipe saved: {md_path.relative_to(docs_dir.parent)}")
        print("  ✓ Success!")

        return True

    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Import recipes from online sources',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python import_recipes.py https://www.example.com/recipe1 https://www.example.com/recipe2
  python import_recipes.py --file urls.txt
  python import_recipes.py --auto-category https://www.example.com/recipe1
        '''
    )

    parser.add_argument('urls', nargs='*', help='Recipe URLs to import')
    parser.add_argument('--file', '-f', help='File containing URLs (one per line)')
    parser.add_argument('--auto-category', '-a', action='store_true',
                       help='Automatically detect category without prompting')

    args = parser.parse_args()

    # Collect URLs
    urls = []
    if args.urls:
        urls.extend(args.urls)

    if args.file:
        try:
            with open(args.file, 'r') as f:
                file_urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                urls.extend(file_urls)
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found.")
            return 1

    if not urls:
        parser.print_help()
        return 1

    # Find docs directory
    script_dir = Path(__file__).parent
    docs_dir = script_dir.parent / 'docs'

    if not docs_dir.exists():
        print(f"Error: docs directory not found at {docs_dir}")
        return 1

    # Process each URL
    print(f"\nImporting {len(urls)} recipe(s)...")

    results = []
    for url in urls:
        success = import_recipe(url, docs_dir, args.auto_category)
        results.append((url, success))

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    successful = sum(1 for _, success in results if success)
    print(f"Total: {len(results)} | Success: {successful} | Failed: {len(results) - successful}")

    if successful < len(results):
        print("\nFailed URLs:")
        for url, success in results:
            if not success:
                print(f"  - {url}")

    return 0 if successful > 0 else 1


if __name__ == '__main__':
    sys.exit(main())
