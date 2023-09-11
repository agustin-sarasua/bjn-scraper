from pathlib import Path
from datetime import datetime

import scrapy


class BJNSpider(scrapy.Spider):
    name = "bjn"

    start_urls = ['http://bjn.poderjudicial.gub.uy/BJNPUBLICA/busquedaSelectiva.seam']

    # def start_requests(self):
    #     urls = [
    #         "https://quotes.toscrape.com/page/1/",
    #         "https://quotes.toscrape.com/page/2/",
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        timestamp = int(datetime.timestamp(datetime.now()))
        filename = f'response_{timestamp}.html'

        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')


        # Parse the initial page here
        if "Ajax-Response" in response.meta.get("response_head", ""):
            location = response.xpath('//meta[@name="Location"]/@content').extract_first()
            new_url = response.urljoin(location)
            yield scrapy.Request(new_url, callback=self.parse_redirected)

        # Simulate form submission for next page
        form_data = {
            'AJAXREQUEST': '_viewRoot',
            'formBusqueda:j_id18': 'true',
            'formBusqueda:j_id20:j_id23:fechaDesdeCalInputDate': '01/08/2023',
            'formBusqueda:j_id20:j_id23:fechaDesdeCalInputCurrentDate': '08/2023',
            'formBusqueda:j_id20:decorProcedimiento:ayudanteProc': '',
            'formBusqueda:j_id20:decorProcedimiento:suggestAyudante_selection': '',
            'formBusqueda:j_id20:decorMateria:cbxMateriacomboboxField': 'AND',
            'formBusqueda:j_id20:decorMateria:cbxMateria': 'AND',
            'formBusqueda:j_id20:decorMateria:MateriaBox': '',
            'formBusqueda:j_id20:decorMateria:suggestMateria_selection': '',
            'formBusqueda:j_id20:decorFirmante:cbxFirmantecomboboxField': 'AND',
            'formBusqueda:j_id20:decorFirmante:cbxFirmante': 'AND',
            'formBusqueda:j_id20:decorFirmante:FirmanteBox': '',
            'formBusqueda:j_id20:decorFirmante:suggestFirmante_selection': '',
            'formBusqueda:j_id20:decorDiscorde:j_id94comboboxField': 'AND',
            'formBusqueda:j_id20:decorDiscorde:j_id94': 'AND',
            'formBusqueda:j_id20:decorDiscorde:DiscordeBox': '',
            'formBusqueda:j_id20:decorDiscorde:suggestDiscorde_selection': '',
            'formBusqueda:j_id20:j_id105:todosLosTipos': 'on',
            'formBusqueda:j_id20:j_id120:cajaQuery': '',
            'formBusqueda:j_id20:j_id147:fechaHastaCalInputDate': '27/08/2023',
            'formBusqueda:j_id20:j_id147:fechaHastaCalInputCurrentDate': '08/2023',
            'formBusqueda:j_id20:j_id160:ayudanteResumen': '',
            'formBusqueda:j_id20:decorRedactor:cbxRedactorcomboboxField': 'AND',
            'formBusqueda:j_id20:decorRedactor:cbxRedactor': 'AND',
            'formBusqueda:j_id20:decorRedactor:RedactorBox': '',
            'formBusqueda:j_id20:decorRedactor:suggestRedactor_selection': '',
            'formBusqueda:j_id20:decorNumero:ayudanteNumero': '',
            'formBusqueda:j_id20:decorImportancia:todasLasImportancias': 'on',
            'formBusqueda:j_id20:j_id223:cantPagcomboboxField': '10',
            'formBusqueda:j_id20:j_id223:cantPag': '10',
            'formBusqueda:j_id20:j_id240:j_id248': 'RELEVANCIA',
            'formBusqueda:formBusqueda': '',
            'autoScroll': '',
            'javax.faces.ViewState': 'j_id2',
            'formBusqueda:j_id20:Search': 'formBusqueda:j_id20:Search',
            'AJAX:EVENTS_COUNT': '1',
        }
        yield scrapy.FormRequest(url=response.url, formdata=form_data, callback=self.parse_next_page)
    
    def parse_redirected(self, response):
        # Now you can parse the redirected page here
        # You can implement the parsing logic for the redirected page in this function
        pass

    def parse_next_page(self, response):
        
        # response.headers.get("Ajax-Response", "").decode('utf-8') == 'redirect'
        # response.headers.get("Location", "").decode('utf-8')
        # '/BJNPUBLICA/busquedaSimple.seam?searchPattern=&cid=196712'

        if "Ajax-Response" in response.meta.get("response_head", ""):
            location = response.xpath('//meta[@name="Location"]/@content').extract_first()
            new_url = response.urljoin(location)
            yield scrapy.Request(new_url, callback=self.parse_redirected)

        timestamp = int(datetime.timestamp(datetime.now()))
        filename = f'response_{timestamp}.html'

        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
        # Form data for the next page request
        next_page_form_data = {
            'AJAXREQUEST': '_viewRoot',
            'formBusqueda:j_id18': 'true',
            'formBusqueda:j_id20:j_id23:fechaDesdeCalInputDate': '01/07/2023',
            'formBusqueda:j_id20:j_id23:fechaDesdeCalInputCurrentDate': '07/2023',
            'formBusqueda:j_id20:decorProcedimiento:ayudanteProc': '',
            'formBusqueda:j_id20:decorProcedimiento:suggestAyudante_selection': '',
            'formBusqueda:j_id20:decorMateria:cbxMateriacomboboxField': 'AND',
            'formBusqueda:j_id20:decorMateria:cbxMateria': 'AND',
            'formBusqueda:j_id20:decorMateria:MateriaBox': '',
            'formBusqueda:j_id20:decorMateria:suggestMateria_selection': '',
            'formBusqueda:j_id20:decorFirmante:cbxFirmantecomboboxField': 'AND',
            'formBusqueda:j_id20:decorFirmante:cbxFirmante': 'AND',
            'formBusqueda:j_id20:decorFirmante:FirmanteBox': '',
            'formBusqueda:j_id20:decorFirmante:suggestFirmante_selection': '',
            'formBusqueda:j_id20:decorDiscorde:j_id94comboboxField': 'AND',
            'formBusqueda:j_id20:decorDiscorde:j_id94': 'AND',
            'formBusqueda:j_id20:decorDiscorde:DiscordeBox': '',
            'formBusqueda:j_id20:decorDiscorde:suggestDiscorde_selection': '',
            'formBusqueda:j_id20:j_id105:todosLosTipos': 'on',
            'formBusqueda:j_id20:j_id120:cajaQuery': '',
            'formBusqueda:j_id20:j_id147:fechaHastaCalInputDate': '27/08/2023',
            'formBusqueda:j_id20:j_id147:fechaHastaCalInputCurrentDate': '08/2023',
            'formBusqueda:j_id20:j_id160:ayudanteResumen': '',
            'formBusqueda:j_id20:decorRedactor:cbxRedactorcomboboxField': 'AND',
            'formBusqueda:j_id20:decorRedactor:cbxRedactor': 'AND',
            'formBusqueda:j_id20:decorRedactor:RedactorBox': '',
            'formBusqueda:j_id20:decorRedactor:suggestRedactor_selection': '',
            'formBusqueda:j_id20:decorNumero:ayudanteNumero': '',
            'formBusqueda:j_id20:decorImportancia:todasLasImportancias': 'on',
            'formBusqueda:j_id20:j_id223:cantPagcomboboxField': '10',
            'formBusqueda:j_id20:j_id223:cantPag': '10',
            'formBusqueda:j_id20:j_id240:j_id248': 'RELEVANCIA',
            'formBusqueda:formBusqueda': '',
            'autoScroll': '',
            'javax.faces.ViewState': 'j_id2',
            'formBusqueda:j_id20:Search': 'formBusqueda:j_id20:Search',
            'AJAX:EVENTS_COUNT': '1',
        }
        
        # Send the form request for the next page
        yield scrapy.FormRequest(url=response.url, formdata=next_page_form_data, callback=self.parse_next_page)