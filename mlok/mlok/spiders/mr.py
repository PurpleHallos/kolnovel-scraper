import scrapy
import re

class MrSpider(scrapy.Spider):
    name = "mr"
    allowed_domains = ["kolnovel.me"]
    start_urls = [r"https://kolnovel.me/semperor-has-returnedz-128097/"]

    def parse(self, response):
        # Extract the chapter title
        chapter_title = response.xpath('//blockquote/p/text()').get().strip()

        # Format the chapter title for LaTeX
        latex_chapter_title = f"\\chapter{{{chapter_title}}}\n\n"

        # Extract content paragraphs
        content = response.xpath('//div[@id="kol_content"]/p/text()')
        paragraphs = [i.get().strip() for i in content]

        # Extract numbers (e.g., chapter number) from the main title for file naming
        title = response.xpath('//div[@class="epheader"]/h1/text()').get().strip()
        try:
            numbers = re.findall(r'[0-9٠١٢٣٤٥٦٧٨٩]+\.?[0-9٠١٢٣٤٥٦٧٨٩]*', title)[-1]
        except IndexError:
            numbers = "unknown"  # Fallback if no number is found

        # Prepare LaTeX formatted content
        latex_content = latex_chapter_title
        for para in paragraphs:
            # Escape LaTeX special characters in the paragraph text
            para = para.replace('&', '\\&').replace('%', '\\%').replace('$', '\\$')
            # Ensure no more than one empty line between paragraphs
            latex_content += f"{para}\n\n".rstrip() + "\n"

        # Print to console for debugging
        print(latex_content)

        # Save to a .tex file
        file_name = f'{numbers}.tex'
        with open(file_name, 'w', encoding='utf-8') as f:  # Changed 'a' to 'w' to overwrite existing content
            f.write(latex_content)

        # Find the link to the next page and follow it
        next_page = response.xpath('//div[@id="Bottum_Down"]//a[@rel="next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
