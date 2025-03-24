import os
from dotenv import load_dotenv
from agents.research_agent import ResearchAgent
from agents.planning_agent import ContentPlanningAgent
from agents.generation_agent import ContentGenerationAgent
from agents.seo_agent import SEOOptimizationAgent
from agents.review_agent import ReviewAgent
import time

load_dotenv()


class BlogGenerator:
    def __init__(self):
        self.researcher = ResearchAgent()
        self.planner = ContentPlanningAgent()
        self.writer = ContentGenerationAgent()
        self.seo_engineer = SEOOptimizationAgent()
        self.editor = ReviewAgent()

    def generate_blog_post(self):
        print("🚀 Starting blog generation process...")

        # Research Phase
        print("\n🔍 Stage 1: Researching trending HR topics...")
        research_data = self.researcher.execute()

        # Planning Phase
        print("\n📝 Stage 2: Creating content outline...")
        outline = self.planner.create_outline(research_data)

        # Writing Phase
        print("\n✍️ Stage 3: Generating content...")
        raw_content = self.writer.generate_content(outline, research_data)

        # SEO Optimization
        print("\n🔧 Stage 4: Optimizing for SEO...")
        optimized_content = self.seo_engineer.enhance_seo(raw_content)

        # Review Phase
        print("\n✅ Stage 5: Quality assurance...")
        final_content = self.editor.review_content(optimized_content)

        return final_content


if __name__ == "__main__":
    start_time = time.time()
    generator = BlogGenerator()
    blog_post = generator.generate_blog_post()

    # Save output
    with open("output.md", "w", encoding="utf-8") as f:
        f.write(blog_post)

    print(f"\n🎉 Blog post generated in {time.time() - start_time:.2f} seconds!")
    print("📄 Output saved to output.md")