import openai
import json
import os


class ContentPlanningAgent:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.default_template = {
            "title": "",
            "sections": [
                {"type": "introduction", "subpoints": []},
                {"type": "section", "title": "", "subpoints": []},
                {"type": "case_study", "title": "", "subpoints": []},
                {"type": "conclusion", "subpoints": []}
            ]
        }

    def create_outline(self, research_data):
        print("📑 Structuring content outline...")
        prompt = f"""Create a detailed blog outline about {research_data['primary_topic']} with:
        - Engaging introduction
        - 3 main sections with 3 subpoints each
        - Real-world case study
        - Practical conclusion
        - SEO-friendly meta description
        Format as JSON"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5
            )
            return json.loads(response.choices[0].message.content)
        except:
            print("⚠️ Using default outline template")
            self.default_template['title'] = f"Comprehensive Guide to {research_data['primary_topic']}"
            return self.default_template