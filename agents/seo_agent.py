from langchain.llms import OpenAI
import re
import os


class SEOOptimizationAgent:
    def __init__(self):
        self.llm = OpenAI(
            temperature=0.3,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.seo_rules = {
            'keyword_density': 1.5,
            'max_heading_length': 70,
            'min_paragraph_length': 100,
            'max_paragraph_length': 300
        }

    def enhance_seo(self, content):
        print("🔍 Analyzing SEO elements...")
        # Extract primary keywords
        keywords = self.llm(f"Extract 5 main SEO keywords from: {content[:500]}")
        keywords = [kw.strip().lower() for kw in keywords.split(",")][:3]

        # Optimize headings
        content = self._optimize_headings(content, keywords)

        # Add meta elements
        meta_desc = self.llm(f"Generate SEO meta description for: {content[:200]}")
        content = f"<!-- SEO Meta: {meta_desc} -->\n{content}"

        # Optimize keyword placement
        return self._insert_keywords(content, keywords)

    def _optimize_headings(self, content, keywords):
        headings = re.findall(r'## (.+)', content)
        for heading in headings:
            if len(heading) > self.seo_rules['max_heading_length']:
                new_heading = self.llm(
                    f"Shorten this heading to under {self.seo_rules['max_heading_length']} characters: {heading}")
                content = content.replace(heading, new_heading.strip())
        return content

    def _insert_keywords(self, content, keywords):
        keyword = keywords[0]
        density = content.lower().count(keyword.lower()) / (len(content.split()) / 100)

        if density < self.seo_rules['keyword_density']:
            sentences = content.split('. ')
            for i in range(0, len(sentences), 3):
                sentences[i] += f" {keyword}"
            content = '. '.join(sentences)

        return content