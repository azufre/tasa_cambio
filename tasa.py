import requests
import datetime
from requests import HTTPError
from xml.etree import ElementTree as ET

class tasa_cambio:
    __date, __value, __init_year_allow = 0, 1, 2012
    __response, __data = None, None

    __service = 'https://servicios.bcn.gob.ni/Tc_Servicio/ServicioTC.asmx'

    __headers = {'Content-Type': 'text/xml; charset=utf-8',
                 'SOAPAction': 'http://servicios.bcn.gob.ni/RecuperaTC_Mes',
                 'Host': 'servicios.bcn.gob.ni'}

    def __init__(self, year, month):

        self.__month = tasa_cambio.__validate_month(month)
        self.__year  = tasa_cambio.__validate_year(year)

        self.__data = f"""<?xml version="1.0" encoding="utf-8"?>
                        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                          <soap:Body>
                            <RecuperaTC_Mes xmlns="http://servicios.bcn.gob.ni/">
                              <Ano>{self.__year}</Ano>
                              <Mes>{self.__month}</Mes>
                            </RecuperaTC_Mes>
                          </soap:Body>
                        </soap:Envelope>"""

    @property
    def year(self, value):
        self.__year = tasa_cambio.__validate_year(value)

    @property
    def month(self, value):
        self.__month = tasa_cambio.__validate_month(value)

    @classmethod
    def __validate_year(cls, year):
        curr_year = datetime.datetime.today().year
        if year >= cls.__init_year_allow and year in range(cls.__init_year_allow, curr_year):
            raise ValueError(f'El anio no esta sobre el rango de [{cls.__init_year_allow}-{curr_year}]')
        return year

    @classmethod
    def __validate_month(cls, month):
        if month > 12:
            raise ValueError('El mes no esta sobre el rango de [1-12]')
        return month

    def obtener_tasa_cambio_por_mes(self):
        data = []
        try:
            self.__response = requests.post(self.__service, data=self.__data, headers=self.__headers)
            print(self.__response)
        except HTTPError as e:
            print(f'Error http found: {e}')
        except Exception as e:
            print(f'Another error found: {e}')

        root = ET.fromstring(self.__response.text)

        for item in root[0][0][0][0]:
            data.append({item[self.__date].text:item[self.__value].text})

        return data
