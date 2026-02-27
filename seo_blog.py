"""
SEO Blog Generator - English Version
Generate SEO-optimized blog posts for Google ranking.

Usage:
    from seo_blog import SEOBlogGenerator

    generator = SEOBlogGenerator(api_key="your-gemini-api-key")
    result = generator.generate("https://mvland.com", "AI music video generator")
"""

import re
import json
from typing import Optional, Dict, Any

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


# SEO Blog System Prompt
SEO_BLOG_PROMPT = """You are a senior tech blogger who writes **in-depth, valuable** long-form content optimized for Google SEO.

## Google E-E-A-T Guidelines

Your content must demonstrate:
- **Experience**: Real user experiences and practical insights
- **Expertise**: Deep product/topic knowledge
- **Authoritativeness**: Reference official sources, accurate information
- **Trustworthiness**: Honest, balanced, factual content

## SEO Best Practices

### Title Tag (H1)
- 50-60 characters maximum
- Include main keyword near the beginning
- Make it compelling and clickable

### Meta Description
- 150-160 characters
- Include main keyword
- Clear value proposition
- Call to action

### Content Structure
- Use H2 for main sections (3-5 sections)
- Use H3 for subsections
- Short paragraphs (2-3 sentences)
- Bullet points for lists
- Bold important keywords

### Keyword Strategy
- Primary keyword in: title, first paragraph, H2s, conclusion
- Secondary keywords distributed naturally
- Keyword density: 1-2% (natural, not stuffed)
- LSI keywords for context

### Content Length
- Minimum 2000 words for comprehensive coverage
- Each section: 300-500 words
- Include specific examples, data, and actionable steps

## Avoid AI Clichés
❌ "In the rapidly evolving digital landscape..."
❌ "In today's fast-paced world..."
❌ "It's important to note that..."
❌ "Let's dive in..."
✅ Start with specific facts, data, or scenarios

## Article Structure Template

```markdown
# [H1: Main Keyword + Value Proposition]

[Meta description: 150-160 chars with keyword and CTA]

## Introduction
[300+ words: Hook with problem/opportunity, preview of what reader will learn]

## What is [Product/Topic]?
[300+ words: Clear definition, core value, why it matters]

## Key Features/Benefits

### [Feature 1]
[300+ words: What it does, how to use it, real benefits]

### [Feature 2]
[300+ words]

### [Feature 3]
[300+ words]

## How to Use [Product]: Step-by-Step
[Detailed walkthrough with numbered steps]

## Real-World Use Cases
[Specific examples with outcomes]

## Pricing and Plans (if applicable)
[Clear breakdown]

## Pros and Cons
[Balanced analysis]

## Conclusion
[Summary + CTA + final keyword mention]
```

## Image Guidelines
Include [IMAGE: description] placeholders for:
- Hero image (above the fold)
- Feature screenshots or illustrations
- Step-by-step visuals
- Comparison charts (if applicable)
"""


class SEOBlogGenerator:
    """Generate SEO-optimized blog posts using Gemini AI."""

    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        """
        Initialize the generator.

        Args:
            api_key: Google Gemini API key
            model: Model to use (default: gemini-2.0-flash)
        """
        if not GENAI_AVAILABLE:
            raise ImportError("google-genai package not installed. Run: pip install google-genai")

        self.api_key = api_key
        self.model = model
        self.client = genai.Client(api_key=api_key)

    def research_product(self, url: str, topic: str = "") -> str:
        """
        Research a product/topic using Google Search.

        Args:
            url: Product URL to research
            topic: Additional topic context

        Returns:
            Research results as string
        """
        # Extract product name from URL
        product_name = ""
        if url:
            import urllib.parse
            parsed = urllib.parse.urlparse(url)
            domain_parts = parsed.netloc.replace('www.', '').split('.')
            if domain_parts:
                product_name = domain_parts[0].upper()

        search_query = f"{product_name} {url} {topic}".strip()

        prompt = f"""
Research this product/website and provide detailed information in English:

{search_query}

Please provide:
1. What is this product/service? Core features and functionality
2. Target users and problems it solves
3. Key benefits and unique selling points
4. How it works (user workflow)
5. Pricing information (if available)
6. Competitors and alternatives
7. User reviews or testimonials (if found)
"""

        try:
            config = types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config
            )
            return response.text
        except Exception as e:
            return f"Research failed: {str(e)}"

    def generate(
        self,
        url: Optional[str] = None,
        topic: str = "",
        keywords: Optional[list] = None,
        word_count: int = 2000,
        include_images: bool = True
    ) -> Dict[str, Any]:
        """
        Generate an SEO-optimized blog post.

        Args:
            url: Product/service URL to write about
            topic: Topic or additional context
            keywords: List of target keywords
            word_count: Target word count (default: 2000)
            include_images: Whether to include image placeholders

        Returns:
            Dictionary with blog content and metadata
        """
        # Research if URL provided
        research = ""
        if url:
            research = self.research_product(url, topic)

        # Build keywords section
        keywords_text = ""
        if keywords:
            keywords_text = f"\n**Target Keywords:** {', '.join(keywords)}"

        # Build prompt
        prompt = f"""{SEO_BLOG_PROMPT}

---

## Your Task

Write a comprehensive, SEO-optimized blog post about:

**URL:** {url or 'N/A'}
**Topic:** {topic or 'Product review and guide'}
{keywords_text}

**Target Word Count:** {word_count}+ words

## Research Data
{research if research else 'No research data available. Write based on general knowledge.'}

---

## Output Requirements

1. Start with SEO metadata:
   - **Title:** (50-60 characters, keyword-rich)
   - **Meta Description:** (150-160 characters)
   - **Primary Keyword:**
   - **Secondary Keywords:**

2. Then write the full article following the structure template

3. Include [IMAGE: description] placeholders where visuals would help

4. End with a clear call-to-action

Write in English. Be comprehensive, specific, and SEO-focused.
"""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            content = response.text

            # Extract metadata if possible
            title = self._extract_title(content)
            meta_desc = self._extract_meta(content)
            word_count_actual = len(content.split())
            h2_count = content.count('## ')

            return {
                "success": True,
                "content": content,
                "metadata": {
                    "title": title,
                    "meta_description": meta_desc,
                    "word_count": word_count_actual,
                    "h2_sections": h2_count,
                    "url": url,
                    "topic": topic
                }
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _extract_title(self, content: str) -> str:
        """Extract title from content."""
        # Try to find title in metadata section
        match = re.search(r'\*\*Title:\*\*\s*(.+)', content)
        if match:
            return match.group(1).strip()

        # Try to find H1
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()

        return ""

    def _extract_meta(self, content: str) -> str:
        """Extract meta description from content."""
        match = re.search(r'\*\*Meta Description:\*\*\s*(.+)', content)
        if match:
            return match.group(1).strip()
        return ""


# CLI interface
def main():
    """Command-line interface for SEO Blog Generator."""
    import argparse
    import os

    parser = argparse.ArgumentParser(description='Generate SEO-optimized blog posts')
    parser.add_argument('--url', '-u', help='Product URL to write about')
    parser.add_argument('--topic', '-t', help='Topic or additional context')
    parser.add_argument('--keywords', '-k', nargs='+', help='Target keywords')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--api-key', help='Gemini API key (or set GEMINI_API_KEY env var)')

    args = parser.parse_args()

    api_key = args.api_key or os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        print("Error: No API key provided. Set GEMINI_API_KEY or use --api-key")
        return 1

    generator = SEOBlogGenerator(api_key=api_key)
    result = generator.generate(
        url=args.url,
        topic=args.topic or '',
        keywords=args.keywords
    )

    if result['success']:
        content = result['content']

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Blog saved to: {args.output}")
        else:
            print(content)

        print(f"\n--- Metadata ---")
        print(f"Title: {result['metadata']['title']}")
        print(f"Word Count: {result['metadata']['word_count']}")
        print(f"H2 Sections: {result['metadata']['h2_sections']}")
    else:
        print(f"Error: {result['error']}")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
