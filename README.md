# SEO Blog Generator (English)

🚀 Generate SEO-optimized blog posts for Google ranking using AI.

## Features

- ✅ **Google E-E-A-T Compliant**: Experience, Expertise, Authoritativeness, Trustworthiness
- ✅ **Keyword Optimization**: Natural keyword distribution, proper density
- ✅ **Proper Structure**: H1/H2/H3 hierarchy, meta tags, semantic HTML
- ✅ **Comprehensive Content**: 2000+ word articles with real depth
- ✅ **Product Research**: Auto-research via Google Search
- ✅ **Image Suggestions**: Placeholder prompts for visuals

## Installation

```bash
pip install google-genai
```

## Quick Start

### Python API

```python
from seo_blog import SEOBlogGenerator

# Initialize with your Gemini API key
generator = SEOBlogGenerator(api_key="your-api-key")

# Generate blog post
result = generator.generate(
    url="https://mvland.com",
    topic="AI music video generator",
    keywords=["AI music video", "music video maker", "AI MV generator"]
)

if result['success']:
    print(result['content'])
    print(f"Word count: {result['metadata']['word_count']}")
```

### Command Line

```bash
# Set API key
export GEMINI_API_KEY="your-api-key"

# Generate blog
python seo_blog.py --url https://mvland.com --topic "AI music video" --output blog.md

# With keywords
python seo_blog.py -u https://example.com -t "Product review" -k "keyword1" "keyword2" -o output.md
```

## API Reference

### `SEOBlogGenerator`

#### `__init__(api_key: str, model: str = "gemini-2.0-flash")`

Initialize the generator.

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_key` | str | Google Gemini API key |
| `model` | str | Model to use (default: gemini-2.0-flash) |

#### `generate(url, topic, keywords, word_count, include_images) -> Dict`

Generate an SEO-optimized blog post.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | str | None | Product/service URL |
| `topic` | str | "" | Topic or context |
| `keywords` | list | None | Target keywords |
| `word_count` | int | 2000 | Target word count |
| `include_images` | bool | True | Include image placeholders |

**Returns:**
```python
{
    "success": True,
    "content": "# Blog Title\n\n...",
    "metadata": {
        "title": "SEO Title",
        "meta_description": "Meta description...",
        "word_count": 2500,
        "h2_sections": 5,
        "url": "https://...",
        "topic": "..."
    }
}
```

#### `research_product(url: str, topic: str = "") -> str`

Research a product using Google Search.

## Output Format

The generated blog follows this structure:

```markdown
**Title:** SEO-Optimized Title (50-60 chars)
**Meta Description:** Compelling description (150-160 chars)
**Primary Keyword:** main keyword
**Secondary Keywords:** related, keywords, here

# Main Title with Keyword

## Introduction
[Hook + problem statement + preview]

## What is [Product]?
[Definition + core value]

## Key Features

### Feature 1
[Detailed explanation]

### Feature 2
[Detailed explanation]

## How to Use: Step-by-Step
[Numbered walkthrough]

## Real-World Use Cases
[Specific examples]

## Pricing
[If available]

## Conclusion
[Summary + CTA]
```

## SEO Best Practices Applied

| Practice | Implementation |
|----------|----------------|
| Title Length | 50-60 characters |
| Meta Description | 150-160 characters |
| Keyword in H1 | ✅ Yes |
| Keyword in H2s | ✅ Yes |
| Content Length | 2000+ words |
| Keyword Density | 1-2% |
| E-E-A-T Signals | ✅ Included |
| Image Alt Text | ✅ Placeholders |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Google Gemini API key |
| `GOOGLE_API_KEY` | Alternative API key name |

## License

MIT

## Author

MarketingClaw Team
