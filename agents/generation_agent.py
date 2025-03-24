import openai
import os
import re
from pytrends.request import TrendReq


class ContentGenerationAgent:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.tone_guidelines = """
            - Professional yet approachable
            - Use active voice
            - Avoid jargon
            - Target audience: HR professionals
            - Reading level: College graduate
        """

    def generate_section(self, prompt):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Generation error: {e}")
            return "Content generation failed for this section."

    def generate_content(self, outline, research):
        print("📝 Writing blog content...")
        content = f"# {outline['title']}\n\n"

        for section in outline['sections']:
            if section['type'] == 'introduction':
                prompt = f"""Write an engaging introduction about {research['primary_topic']} that:
                - Highlights current trends
                - States the article's purpose
                - Includes statistics if available
                {self.tone_guidelines}"""

                content += f"\n## Introduction\n{self.generate_section(prompt)}\n"

            elif section['type'] == 'section':
                prompt = f"""Write 300 words about {section['title']}. Include:
                - {', '.join(section['subpoints'])}
                - Data from recent studies
                - Practical examples
                {self.tone_guidelines}"""

                content += f"\n## {section['title']}\n{self.generate_section(prompt)}\n"

            elif section['type'] == 'case_study':
                prompt = f"""Create a real-world case study about {research['primary_topic']}:
                - Company background
                - Challenges faced
                - Implemented solutions
                - Results achieved
                {self.tone_guidelines}"""

                content += f"\n## Case Study: {section['title']}\n{self.generate_section(prompt)}\n"

        # Add conclusion
        conclusion_prompt = f"""Write a compelling conclusion about {research['primary_topic']} that:
            - Summarizes key points
            - Provides actionable takeaways
            - Encourages further reflection
            {self.tone_guidelines}"""

        content += f"\n## Conclusion\n{self.generate_section(conclusion_prompt)}\n"
        return content