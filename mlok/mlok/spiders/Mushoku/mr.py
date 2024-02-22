import scrapy
import re

class MrSpider(scrapy.Spider):
    name = "mr"
    allowed_domains = ["kolnovel.me"]
    start_urls = [r"https://kolnovel.me/smushoku-tenseiz-181995/"]

    def parse(self, response):
        # Extract paragraphs
        content = response.xpath('//div[@id="kol_content"]/p/text()')
        paragraphs = [i.get().strip() for i in content]

        # Extract title
        title = response.xpath('//div[@class="epheader"]/h1/text()').get().strip()

        # Extract chapter number from the title
        try:
            numbers = re.findall(r'[0-9٠١٢٣٤٥٦٧٨٩]+\.?[0-9٠١٢٣٤٥٦٧٨٩]*', title)[-1]
        except IndexError:
            numbers = "unknown"

        # Format title as LaTeX chapter
        latex_content = f"\\chapter{{{title}}}\n\n"

        # Add each paragraph as a separate line in LaTeX
        for para in paragraphs:
            latex_content += f"{para}\n\n"

        # Print the LaTeX formatted content to the console for debugging
        print(latex_content)

        # Save the content in a .tex file
        try:
            with open(f'{numbers}.tex', 'w', encoding='utf-8') as f:
                f.write(latex_content)
        except Exception as e:
            print(f"Error writing file: {e}")

        # Find the link to the next page and follow it
        next_page = response.xpath('//div[@id="Bottum_Down"]//a[@rel="next"]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
