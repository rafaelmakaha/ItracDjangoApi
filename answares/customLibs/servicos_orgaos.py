import itertools
import dicttoxml
import requests
import declxml as xml
from pprint import pprint

class ServicosOrgaos:
    def generate_codes(l, n):
        yield from itertools.product(*([l] * n))


    def write_file(name, data):
        text_file = open(name, "w")
        text_file.write(data)
        text_file.close()


    def get_serivcos_orgaos(input):
        result = []
        for i in input:
            servico_id = i['id'].split('/')[6]
            servico_nome = i['nome']
            orgao_id = i['orgao']['id'].split('/')[5]
            orgao_nome = i['orgao']['nomeOrgao']
            result.append(
                {'servico_id': servico_id, 'servico_nome': '{0}'.format(servico_nome), 'orgao_id': orgao_id, 'orgao_nome': '{0}'.format(orgao_nome)})

        return result


    def get_orgaos(input):
        result = {}
        for i in input:
            servico_id = i['id'].split('/')[6]
            servico_nome = i['nome']
            orgao_id = i['orgao']['id'].split('/')[5]
            orgao_nome = i['orgao']['nomeOrgao']
            if orgao_id in result:
                result[orgao_id].append({'servico_id': servico_id, 'servico_nome': '{0}'.format(servico_nome), 'orgao_nome': '{0}'.format(orgao_nome,),
                                        'orgao_id': orgao_id.zfill(8)})
            else:
                result[orgao_id] = [{'servico_id': servico_id, 'servico_nome': '{0}'.format(servico_nome), 'orgao_nome': '{0}'.format(orgao_nome),
                                    'orgao_id': orgao_id.zfill(8)}]

        return result


    def create_codes(orgaos, qid_orgao, qid_serv, language):
        count_orgao = 1
        count_serv = 1
        orgaos_output = {'rows': []}
        servicos_output = {'rows': []}

        for o in orgaos:
            orgaos_output['rows'].append({
                'qid': "<![CDATA[{0}]]>".format(qid_orgao),
                'code': "<![CDATA[{0}]]>".format(orgaos[o][0]['orgao_id']),
                'answer': "<![CDATA[{0}]]>".format(orgaos[o][0]['orgao_nome']),
                'sortorder': "<![CDATA[{0}]]>".format(count_orgao),
                'language': "<![CDATA[{0}]]>".format(language),
                'assessment_value': "<![CDATA[0]]>",
                'scale_id': "<![CDATA[0]]>"
            })
            count_orgao = count_orgao + 1

            for s in orgaos[o]:
                servicos_output['rows'].append({
                    'qid': "<![CDATA[{0}]]>".format(qid_serv),
                    'code': "<![CDATA[{0}{1}]]>".format(s['orgao_id'], s['servico_id']),
                    'answer': "<![CDATA[{0}]]>".format(s['servico_nome']),
                    'sortorder': "<![CDATA[{0}]]>".format(count_serv),
                    'language': "<![CDATA[{0}]]>".format(language),
                    'assessment_value': "<![CDATA[0]]>",
                    'scale_id': "<![CDATA[0]]>"
                })
                count_serv = count_serv + 1

        return orgaos_output, servicos_output


    def json2cdata(input):
        author_processor = xml.dictionary('rows', [
            xml.array(xml.dictionary('row', [
                xml.string('qid'),
                xml.integer('code'),
                xml.string('answer'),
                xml.integer('sortorder'),
                xml.integer('assessment_value'),
                xml.integer('language'),
                xml.integer('scale_id'),
            ]), alias='rows')
        ])
        xmlstr = xml.serialize_to_string(author_processor, input, indent='   ')
        return xmlstr

    def returnResponse():
        url = 'https://www.servicos.gov.br/api/v1/servicos/'
        return requests.get(url)
    
    def returnOrgaos():
        return ServicosOrgaos.get_orgaos(ServicosOrgaos.returnResponse().json()['resposta'])

    def returnServicos():
        servicos = []
        data = ServicosOrgaos.returnOrgaos()
        for key in data:
            for i in range(len(data[key])):
                servicos.append(data[key][i]['servico_nome'])
        return servicos
    def returnServicosObjects():
        servicos = []
        data = ServicosOrgaos.returnOrgaos()
        for key in data:
            for i in range(len(data[key])):
                servico = {}
                servico['servico_nome'] = data[key][i]['servico_nome']
                servico['servico_id'] = data[key][i]['servico_id']
                # servicos[data[key][i]['servico_nome']] = data[key][i]['servico_id']
                servicos.append(servico)
        return servicos
    def returnOrgaosObjects():
        orgaos = []
        data = ServicosOrgaos.returnOrgaos()
        for key in data:
            orgao = {}
            orgao['orgao_nome'] = data[key][0]['orgao_nome']
            orgao['orgao_id'] = data[key][0]['orgao_id']
            servicos = []
            for serv in data[key]:
                servico = {}
                servico['servico_nome'] = serv['servico_nome']
                servico['servico_id'] = serv['servico_id']
                servicos.append(servico)
            orgao['servicos'] = servicos
            # orgaos[data[key][i]['servico_nome']] = data[key][i]['servico_id']
            orgaos.append(orgao)
        return orgaos

# url = 'https://www.servicos.gov.br/api/v1/servicos/'
# response = requests.get(url)
# orgaos_set = ServicosOrgaos.get_orgaos(response.json()['resposta'])

# orgaos_set = ServicosOrgaos.returnOrgaos()