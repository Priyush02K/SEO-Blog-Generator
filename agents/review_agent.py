import language_tool_python
import openai
import os


class ReviewAgent:
    def __init__(self):
        self.grammar_tool = language_tool_python.LanguageTool('en-US')
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def review_content(self, content):
        print("🔎 Checking for errors...")
        # Grammar and spelling check
        corrected = self._check_grammar(content)

        # Style improvement
        return self._improve_style(corrected)

    def _check_grammar(self, text):
        matches = self.grammar_tool.check(text)
        return language_tool_python.utils.correct(text, matches)

    def _improve_style(self, text):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "user",
                    "content": f"Improve the writing style of this blog post while maintaining technical accuracy:\n\n{text}"
                }],
                temperature=0.4
            )
            return response.choices[0].message.content
        except:
            return text