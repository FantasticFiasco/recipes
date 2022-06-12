---
layout: default
---
{% assign recipes = site.recipes | where: "parent", page.title %}

{% for recipe in recipes %}
- [{{ recipe.title }}]({{ recipe.url }}) xxx
{% endfor %}
