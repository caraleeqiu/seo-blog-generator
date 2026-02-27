from setuptools import setup, find_packages

setup(
    name="seo-blog-generator",
    version="1.0.0",
    description="Generate SEO-optimized blog posts for Google ranking using AI",
    author="MarketingClaw",
    py_modules=["seo_blog"],
    install_requires=[
        "google-genai>=0.3.0",
    ],
    entry_points={
        "console_scripts": [
            "seo-blog=seo_blog:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
