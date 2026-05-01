from collections import deque

import numpy as np
from astropy.time import Time
import requests
import json as j
from docxtpl import DocxTemplate, InlineImage  # pip install docxtpl
from docx.shared import Mm
import os
from datetime import datetime, timedelta
from Calendars import RapidYear
import matplotlib.pyplot as plt

plt.rcParams['savefig.dpi'] = 600


def getDateFromMJD(MJD):
    tmjd = Time(MJD, format='mjd')
    stringdate = Time(tmjd.to_value('iso'), out_subfmt='date_hm').iso
    return datetime.fromisoformat(stringdate).date()


def getProperNumber(number):
    roundednumber = round(number)
    res = number
    param = abs(number - roundednumber)
    if param <= 0.1:
        res = roundednumber
    return res


def getConvertedDateFromIsoString(isodatestring):
    isodate = datetime.strptime(str(isodatestring), "%Y-%m-%d").date()
    return str(isodate.strftime("%d/%m/%Y"))


def saveVerticalBarGraphImage(utcrDataparam, limit):
    mjdvalues = list(utcrDataparam['x'])
    mjdvalues.reverse()
    difereVar = list(utcrDataparam['y'])
    difereVar.reverse()
    pos = np.arange(len(mjdvalues))
    limitforline = limit + 2
    posvert = np.arange(-limitforline, limitforline + 1)

    colors = ['gray' if e >= 0 else 'gray' for e in difereVar]
    fig, ax = plt.subplots()
    plt.figure(figsize=(8, 10))
    rects = plt.barh(pos, difereVar, color=colors, edgecolor='black')
    plt.yticks(pos, mjdvalues, fontsize=9)
    plt.xticks(posvert, fontsize=9)
    ax.set_aspect(1.2 / 1)
    plt.grid(True, which='minor')
    plt.axvline(x=0, color='k', linewidth='1')
    # ax.axvline(x=0, color='k')
    plt.axvline(x=10, color='r', linestyle='-', linewidth='1')
    plt.axvline(x=-10, color='r', linestyle='-', linewidth='1')
    for rect, label in zip(rects, difereVar):
        height = rect.get_width()
        translabel = "{:.1f}".format(label).replace('.', ',')
        if height > 0:
            plt.text(limitforline - 1, rect.get_y() + rect.get_height() / 6, translabel, ha="center", va="bottom",
                     fontsize=9)
        else:
            plt.text(-(limitforline + 1), rect.get_y() + rect.get_height() / 6, translabel, ha="center", va="bottom",
                     fontsize=9)
    plt.ylabel('MJD', fontsize=12)
    plt.xlabel('UTCR - UTC(INXE) (ns)', fontsize=12)
    plt.savefig('templates/verticalbarchartimage.png', format='png', bbox_inches='tight')
    plt.savefig('templates/verticalbarchartimage.svg', format='svg', bbox_inches='tight')


def saveHorizontalBarGraphImage(utcrDataparam, nominal_limit, process_limit):
    global paddinglow
    mjdvalues = utcrDataparam['x']
    pos = np.arange(len(mjdvalues))
    difereVar = utcrDataparam['y']
    posvertmax = max(max(map(abs, difereVar)), process_limit) + 0
    posvertmin = max(abs(min(difereVar)), process_limit) + 0
    if posvertmax > process_limit * 1.6:
        paddinglow = 2
    else:
        paddinglow = 4
    posvert = np.arange(-posvertmin - 10, posvertmax + 20, 10)
    fig, ax = plt.subplots()
    larg = 10
    alt = 10
    plt.figure(figsize=(larg, alt))
    plt.grid(True, which='major', zorder=0, color='gray', alpha=0.5)
    rects = plt.bar(pos, difereVar, color='gray', edgecolor='black', zorder=3, alpha=0.7)
    plt.xticks(pos, mjdvalues, rotation='vertical', fontsize=10)
    plt.yticks(posvert, fontsize=8)
    ax.set_aspect(np.divide(larg, 10) / np.divide(alt, 10))
    plt.axhline(y=0, color='k', linewidth='1')
    # ax.axvline(x=0, color='k')
    plt.axhline(y=nominal_limit, color='orange', linestyle='-', linewidth='1')
    plt.axhline(y=process_limit, color='r', linestyle='-', linewidth='1')
    plt.axhline(y=-nominal_limit, color='orange', linestyle='-', linewidth='1')
    plt.axhline(y=-process_limit, color='r', linestyle='-', linewidth='1')
    for rect, label in zip(rects, difereVar):
        translabel = "{:.1f}".format(label).replace('.', ',')
        height = rect.get_height()
        if height > 0:
            plt.text(rect.get_x() + rect.get_width() / 2, +(nominal_limit + paddinglow + 0.45), translabel, ha="center",
                     va="bottom",
                     fontsize=9, rotation="vertical")
        else:
            plt.text(rect.get_x() + rect.get_width() / 2, -(nominal_limit + 2.5 * paddinglow + 0.45), translabel,
                     ha="center",
                     va="bottom",
                     fontsize=9, rotation="vertical")
    plt.xlabel('MJD', fontfamily='Arial', fontsize=12, labelpad=10)
    plt.ylabel('UTCR - UTC(INXE) (ns)', fontfamily='Arial', fontsize=12)
    # plt.title('ABCDEF', fontsize=20)
    plt.savefig('templates/horizontalbarchartimage.png', format='png', bbox_inches='tight')
    plt.savefig('templates/horizontalbarchartimage.svg', format='svg', bbox_inches='tight')


def getCircTDates(mesrefparam):
    numerodias = 7
    dictresp = {}
    for mes in range(1, 13):
        if mes == mesrefparam:
            circTQDates = list(map(getDateFromMJD, list(listaplana)[0:numerodias]))
            pubdate = circTQDates[-1] + timedelta(days=12)
            apos = 3
            larguraJanela = 4
            iniciaJanela = pubdate + timedelta(days=apos)
            terminaJanela = pubdate + timedelta(days=apos + larguraJanela)
            servicewindow = [iniciaJanela.isoformat(), terminaJanela.isoformat()]
            dictresp["circtMJD"] = list(listaplana)[0:numerodias]
            dictresp["circTQDates"] = circTQDates
            dictresp["publishDate"] = servicewindow
        listaplana.rotate(-(numerodias - 1))
    return dictresp


dictCircTProperties = {1: (535, 433, "Janeiro", "2024-02-12"), 2: (536, 434, "Fevereiro", "2024-03-12"),
                       3: (537, 435, "Março", "2024-04-12"), 4: (538, 436, "Abril", "2024-05-14"),
                       5: (539, 437, "Maio", "2024-06-10"), 6: (540, 438, "Junho", "2024-07-10"),
                       7: (541, 439, "Julho", "2024-08-08"), 8: (542, 440, "Agosto", "2024-09-11"),
                       9: (000, 441, "Setembro", "2024-09-12"), 10: (000, 442, "Outubro", "2024-10-12"),
                       11: (000, 443, "Novembro", "2024-11-12"), 12: (000, 444, "Dezembro", "2024-12-12")
                       }

listofmonths = np.array(list(dictCircTProperties.values()))[:, 2]
listofCirtTpublishedDates = np.array(list(dictCircTProperties.values()))[:, 3]
# print(listofCirtTpublishedDates)

###########################################################################################################

monthOfCertificateNum = 9
circTmonth = monthOfCertificateNum - 1
anoRef = 2024
circTPublishedDate = getConvertedDateFromIsoString(listofCirtTpublishedDates[circTmonth - 1])

calibrationDate = getConvertedDateFromIsoString(dictCircTProperties[circTmonth][3])

environment_vars_context = {'tempValue': "22,5", 'tempDeviation': "0,5", 'humValue': "40,0".format(), 'humDeviation': "10"}

############################################################################################################


rapidyear = RapidYear(anoRef)
lista_dias_circT = rapidyear.getCirctMonthList()
listaplana = deque()
listaplana.extend(lista_dias_circT)

dictresplocal = getCircTDates(circTmonth)

# print(f"dictresplocal = {dictresplocal}")
circtMJD = dictresplocal['circtMJD']

url = '''https://webtai.bipm.org/api/v1.0/get-data.html?scale={}&lab={}&mjd1={}&mjd2={}'''

mjdInicial = circtMJD[0]
mjdFinal = circtMJD[-1]
labOptions = ["INXE"]
labOption = labOptions[0]
urlOptions = ["utc+utcr", "utc", "utcr"]
urlOption = urlOptions[0]
incertezaTipoA = 0.2
# incertezaTipoB = 3.2
uncertNominalMargin = 40  # ns
uncertProcessLimit = 100  # ns Limite BIPM

urlforrequest = url.format(urlOption, labOption, mjdInicial, mjdFinal)
print(f"urlforrequest = {urlforrequest}")

response = requests.get(urlforrequest, stream=True)
data = response.json()

with open('httpResp.json', 'wb') as fd:
    for chunk in response.iter_content(chunk_size=128):
        fd.write(chunk)

with open("httpResp.json") as json_format_file:
    circTDict = j.load(json_format_file)

# Carrega os dados UTC
utcData = circTDict["data"][0]
# Carrega os dados UTCR
utcrData = circTDict["data"][1]

incertezaTipoB = utcrData["xmax"]

# Com base no primeiro MJD, define o mês base da CircularT
mesBaseNum = getDateFromMJD(utcData['xmin']).month
mesBase = listofmonths[mesBaseNum]

circTYear = 0

if mesBaseNum > 1:
    circTYear = anoRef

docpath = os.path.join("./docs", "MOD-Dimci-1_14_template_lab.docx")
doc = DocxTemplate(docpath)
doccontext = {}

''' Define listas de contextos '''

header_context = {'ministerio': "Ministério do Desenvolvimento, Indústria, Comércio e Serviços", 'siglamin': "MDIC"}

footer_context = {'monthpubDateofTemplate': "Mai"}

admin_context = {'adminProcess': "0052600.002901/2024-56",
                 'numCert': "{:04d}".format(dictCircTProperties[circTmonth][0]),
                 'certY': anoRef}

respPersons_context = {'respPersonMainSigner': "Rodolfo Saboia de Souza",
                       'respPersonMainSignerCapacity': "Chefe da Dmtic",
                       'respPersonLabSigner': "Rodolfo Saboia de Souza",
                       'respPersonLabSignerCapacity': "Chefe da Dmtic",
                       'respPerson1': "Fernando Alves Rodrigues",
                       'respPersonCapacity1': "Técnico Executor",
                       'respPerson2': "Mauro Vieira de Lima",
                       'respPersonCapacity2': "Técnico Executor"
                       }

administrativeData_context = {'dccSoftware': "Python",
                              'refTypeDefinitions': "",
                              'coreData': "2024",
                              'items': "",
                              'calibrationLaboratory': "",
                              'respPersons': "",
                              'statements': ""
                              }

customer_context = {'customerName': "Inmetro/Dimci/Dmtic",
                    'customerShortName': "Dmtic",
                    'customerNameAbrev': "",
                    'customerAddress': "",
                    'customerCompleteAddress': "Av. Nossa Senhora das Graças, 50 - Xerém - Duque de Caxias - RJ - CEP: 25250-020"
                    }

item_1_context = {"item1Name": "Padrão de frequência de Césio",
                  'item1Pronoum': "O",
                  'item1Manufacturer': "Microsemi",
                  'item1Serial': "US49352967",
                  'item1Model': "5071A",
                  'item1Identifier': "PR-2"
                  }

item_2_context = {"item2Name": "Gerador de fase de alta resolução",
                  'item2Pronoum': "O",
                  'item2Manufacturer': "SpectraDynamics",
                  'item2Serial': "13FS16-03",
                  'item2Model': "HROG-10",
                  'item2Identifier': "MPS"
                  }

itemCharacteristics_context = {
    'itemCharacteristics': "1) Padrão de frequência de Césio: com estabilidade em curto prazo (100s) de 8,5x10E-13 (Hz/Hz)."
                           "\n2) Gerador de fase de alta resolução com resolução em frequência de 5x10E-19 (Hz/Hz) e estabilidade em curto prazo de 9x10E-14 (Hz/Hz)."
                           "\n3) Receptor Geodésico multifrequencial e multiconstelação com desempenho de medições para "
                           "códigos das portadoras &#60; 0,5 ns e para fase das portadoras &#60; 5ps."}

scope_context = {
    'calibrationScope': "Calibração da base de tempo (10MHz) do dispositivo sob teste (DUT) com caracterização da "
                        "exatidão e da estabilidade em frequência."}

calibrationLaboratory_context = {'calibrationLaboratoryName': "Inmetro/Dimci/Dmtic",
                                 'calibrationLaboratoryNameAbrev': "",
                                 'calibrationLaboratoryAddress': "",
                                 'calibrationLaboratoryCompleteAddress': "Av. Nossa Senhora das Graças, 50 - Xerém - "
                                                                         "Duque de Caxias - RJ - CEP: 25250-020"
                                 }

calibration_data_context = {'receiptDate': "",
                            'beginPerformanceDate': "",
                            'endPerformanceDate': "{}".format(calibrationDate),
                            'issuedDate': "{}".format(dictCircTProperties[circTmonth][2])
                            }

traceability_context = {'traceabilityRef': "CCTF.K01-UTC",
                        'traceabilityRefDate': "{}".format(dictCircTProperties[circTmonth][2]),  # data da calibração
                        'circTRef': "Circular-T.{}".format(dictCircTProperties[circTmonth][1]),
                        'circTDate': "{}".format(circTPublishedDate),
                        'circTMonth': "{}".format(mesBase),
                        'circTYear': "{}".format(circTYear),
                        'typeAuncerT': "{}".format(str(incertezaTipoA).replace('.', ',')),
                        'typeBuncerT': "{}".format(str(incertezaTipoB).replace('.', ',')),
                        'uncertNominalMargin': "{}".format(uncertNominalMargin),
                        'uncertProcessLimit': "{}".format(uncertProcessLimit),
                        'keyCompDate': "{}".format(circTPublishedDate)
                        }

uncertainty_context = {'expandedUncertValue': "6,2"}

# circTDict = {'errorcode': 0, 'message': 'ok', 'api_version': '0.2-beta', 'data': [
#     {'xmin': 60369, 'ymin': -2.2, 'y': [1.9, -0.3, 1.4, -2.2, 10.8, 5.5], 'y_tot': 6, 'name': 'UTC-UTC(INXE)',
#      'xmax': 60399, 'x': [60369, 60374, 60379, 60384, 60389, 60399], 'ymax': 10.8, 'x_tot': 6}, {
#         'x': [60369, 60370, 60371, 60372, 60373, 60374, 60375, 60376, 60377, 60378, 60379, 60380, 60381, 60382, 60383,
#               60384, 60385, 60386, 60387, 60388, 60389, 60390, 60391, 60396, 60397, 60398, 60399], 'ymax': 11,
#         'x_tot': 27,
#         'y': [2.9, 3.5, 3.5, 5.2, 3.9, -0.7, -6, 0.4, 0.6, 0.8, -0.5, 0.8, 0.4, 0.5, 0.2, -3.3, -1.3, 1.2, 4.6, 7.2,
#               10.7, 5.8, 0.1, 8.8, 11, 0.9, 4.6], 'y_tot': 27, 'name': 'UTCR-UTC(INXE)', 'xmax': 60399, 'ymin': -6,
#         'xmin': 60369}], 'success': True}


Y = utcData['x']
W = utcData['y']
Z = utcData['unc']

limiarProcessOutlier = uncertProcessLimit
limiarNominalOutlier = uncertNominalMargin
utcRProcessOutlierCount = 0
utcRNominalOutlierCount = 0

utc_table_context = {
    'utcMeasures': []
}

utcR_table_context = {
    'utcRMeasures': []
}

for mjd, difere, incerteza in zip(Y, W, Z):
    dictx = {}
    data = getDateFromMJD(mjd)
    if abs(difere) > limiarProcessOutlier:
        utcRProcessOutlierCount += 1
    if abs(difere) > limiarNominalOutlier:
        utcRNominalOutlierCount += 1
    data = str(data.strftime("%d/%m/%Y"))
    dictx['utcmeasDate'] = data
    dictx['utcmeasMJD'] = mjd
    dictx['difereValue'] = "{:.1f}".format(difere).replace('.', ',')
    dictx['uncertValue'] = "{}".format(incerteza).replace('.', ',')
    utc_table_context['utcMeasures'].append(dictx)
    # print(utc_table_context)

utcRProcessOutlierCount = 0
utcRNominalOutlierCount = 0

Y = utcrData['x']
W = utcrData['y']

for mjd, difere in zip(Y, W):
    dictxR = {}
    data = getDateFromMJD(mjd)
    if abs(difere) > limiarProcessOutlier:
        utcRProcessOutlierCount += 1
    if abs(difere) > limiarNominalOutlier:
        utcRNominalOutlierCount += 1
    data = str(data.strftime("%d/%m/%Y"))
    dictxR['utcRmeasDate'] = data
    dictxR['utcRmeasMJD'] = mjd
    dictxR['difereValue'] = "{:.1f}".format(difere).replace('.', ',')
    dictxR['uncertValue'] = "{}".format(incertezaTipoB).replace('.', ',')
    utcR_table_context['utcRMeasures'].append(dictxR)
    # print(utc_table_context)

numOfSamples = int(circTDict["data"][1]['x_tot'])

realiabilityProcess = getProperNumber(np.round((1 - np.divide(utcRProcessOutlierCount, numOfSamples)) * 100, 2))
# print(realiabilityProcess)
realiabilityNominal = getProperNumber(np.round((1 - np.divide(utcRNominalOutlierCount, numOfSamples)) * 100, 2))
# print(realiabilityNominal)

if utcRProcessOutlierCount > 0:
    outageNumberProcessString = "foram observados {}".format(utcRProcessOutlierCount)
else:
    outageNumberProcessString = "Não foram observados"

if utcRNominalOutlierCount > 0:
    outageNumberNominalString = "foram observados {}".format(utcRNominalOutlierCount)
else:
    outageNumberNominalString = "não foram observados"

results_context = {
    'difereMarginProcess': limiarProcessOutlier,
    'difereMarginNominal': limiarNominalOutlier,
    'uncertValue': "0.000004038",
    'numOfSamples': numOfSamples,
    'outageNumberProcess': outageNumberProcessString,
    'outageNumberNominal': outageNumberNominalString,
    'realiabilityProcess': f"{realiabilityProcess}".replace(".", ","),
    'realiabilityNominal': f"{realiabilityNominal}".replace(".", ",")
}

# saveVerticalBarGraphImage(utcrData, int(results_context['difereMarginNominal']), int(results_context[
# 'difereMarginProcess']))
saveHorizontalBarGraphImage(utcrData, int(results_context['difereMarginNominal']),
                            int(results_context['difereMarginProcess']))

image_context = {'barchartimage': InlineImage(doc, 'templates/horizontalbarchartimage.png', width=Mm(165))}
# image_context = {'barchartimage': InlineImage(doc, 'templates/verticalbarchartimage.png', width=Mm(120))}

measurementResults_context = {}

contextlist = [header_context,
               footer_context,
               admin_context,
               respPersons_context,
               administrativeData_context,
               customer_context,
               item_1_context,
               item_2_context,
               itemCharacteristics_context,
               scope_context,
               calibrationLaboratory_context,
               calibration_data_context,
               traceability_context,
               results_context,
               uncertainty_context,
               environment_vars_context,
               utc_table_context,
               utcR_table_context,
               image_context
               ]

for context in contextlist:
    doccontext.update(context)

doc.render(doccontext)
# filename = f"Certificado_{customer_context['customerShortName']}_{admin_context['numCert']}_{anoRef}.docx"
filename = f"DCC_DIMCI_{admin_context['numCert']}_{anoRef}.docx"
print(f"Gerando o arquivo: {filename}")
doc.save(filename)
