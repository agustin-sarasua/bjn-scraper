import os
from typing import List
import scrapy
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup
from pydantic import BaseModel

class ParsedDocument(BaseModel):
    materias: List[List[str]]
    firmantes: List[List[str]]
    redactores: List[List[str]]
    abstract: List[List[str]]
    descriptores: List[List[str]]
    resumen: List[List[str]]
    sentencia: str
    numero: str
    sede: str
    importancia: str
    tipo: str
    fecha: str
    ficha: str
    procedimiento: str


class LocalSpider(scrapy.Spider):
    name = 'local_spider'

    def start_requests(self):
        # Get the absolute path to the html_files directory relative to the spider script
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../data'))
        print(f'base_dir: {base_dir}')
        for dir in os.listdir(base_dir):
            if os.path.isdir(os.path.join(base_dir, dir)):
                print(f'processing dir: {dir}')
                for file in os.listdir(os.path.join(base_dir, dir)):
                    url = 'file://' + os.path.join(base_dir, dir, file)
                    # ex = os.path.exists(url)
                    yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        parsed_path = "parsed_data".join(response.url.split("data"))
        parsed_path = parsed_path[len('file://'):-4]+"json"

        if os.path.exists(parsed_path):
            print(f"File '{parsed_path}' already exists.")
            return
        
        # Process the HTML content as needed
        parsed_data = self.parse_data_from_html(response)

        # Create the parsed directory path based on the original file structure
        # original_path = response.url[len('file://'):]
        # relative_path = os.path.relpath(original_path, start=self.settings.attributes['FILES_STORE'].value)
        # parsed_directory = os.path.join(self.settings.attributes['FILES_STORE'].value, 'data_parsed', relative_path)
        # os.makedirs(parsed_directory, exist_ok=True)
        

        self.create_file_with_directories(parsed_path, parsed_data.json())

    def create_file_with_directories(self, path, content):
        directory = os.path.dirname(path)

        # Create directories if they don't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Create the file if it doesn't exist
        if not os.path.exists(path):
            with open(path, 'w') as file:
                file.write(content)
            print(f"File '{path}' created.")
        else:
            print(f"File '{path}' already exists.")
    
    def get_row_data_from_table(self, soup, table_id):
        # Find the table containing the data
        rows = []
        if len(soup.select(table_id)) > 0:
            table = soup.select(table_id)[0]
            # Initialize a list to store the rows
            # Iterate through each row in the table's body
            for row in table.select('tbody tr'):
                cells = row.find_all('td')  # Find all cell elements in the row
                row_data = [cell.get_text(strip=True) for cell in cells]  # Extract text from each cell
                rows.append(row_data)  # Append the row data to the list
        return rows
    

    def parse_data_from_html(self, response) -> ParsedDocument:
        # Implement your HTML parsing logic here
        # Return the parsed data as a string
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting text from specific elements using CSS selectors
        numero_element = soup.select('#j_id3\\:0\\:j_id13')[0]
        sede_element = soup.select('#j_id3\\:0\\:j_id15')[0]
        importancia_element = soup.select('#j_id3\\:0\\:j_id17')[0]
        tipo_element = soup.select('#j_id3\\:0\\:j_id19')[0]
        fecha_element = soup.select('#j_id21\\:0\\:j_id29')[0]
        ficha_element = soup.select('#j_id21\\:0\\:j_id31')[0]
        procedimiento_element = soup.select('#j_id21\\:0\\:j_id33')[0]

        # Find the table containing the data
        materias = self.get_row_data_from_table(soup, '#j_id35')
        firmantes = self.get_row_data_from_table(soup, '#gridFirmantes')
        redactores = self.get_row_data_from_table(soup, '#gridRedactores')
        abstract = self.get_row_data_from_table(soup, '#j_id77')
        descriptores = self.get_row_data_from_table(soup, '#j_id89')
        resumen = self.get_row_data_from_table(soup, '#j_id107')

        # Find the span tag you're interested in
        span_tag = soup.select('#textoSentenciaBox')[0]

        # Extract all text content from the span, including its children
        span_text = span_tag.get_text(separator='\n\n', strip=True)

        numero_text = numero_element.get_text(strip=True)
        sede_text = sede_element.get_text(strip=True)
        importancia_text = importancia_element.get_text(strip=True)
        tipo_text = tipo_element.get_text(strip=True)
        fecha_text = fecha_element.get_text(strip=True)
        ficha_text = ficha_element.get_text(strip=True)
        procedimiento_text = procedimiento_element.get_text(strip=True)

        doc = ParsedDocument(
            materias=materias,
            firmantes=firmantes,
            redactores=redactores,
            abstract=abstract,
            descriptores=descriptores,
            resumen=resumen,
            sentencia=span_text,
            numero=numero_text,
            sede=sede_text,
            importancia=importancia_text,
            tipo=tipo_text,
            fecha=fecha_text,
            ficha=ficha_text,
            procedimiento=procedimiento_text,
        )

        return doc