from django.conf import settings
import requests


def check_majic_export_api (communes, secret, request_id, mode={}) :
    """
    Here in this method we connect to the API EXTRACT, 
    @param   'communes': liste de communes, separés par virgules
    @param   'secret': user id ?
    @param   'request_id': 
    @param optionnel  'mode': split: 1 fichier par commune),
                     group: 1 fichier pour toutes les communes ,
                     both: 1 fichier par commune et 1 fichier groupé,
    
    @return  a text with a URL for check status
    """
    
    statut_and_url = {}

    if mode:
        url = settings.MAJIC_API + 'export_majic'
    else:
        url = settings.MAJIC_API + 'export_lme'

    payload = {
        'communes': communes, 
        'secret': secret,
        'mode': mode,
        'request_id': request_id,
        }

    res = requests.post(url,
                        data= payload,
                        )
    import logging
    logging.error(res.text)
    logging.error(url)

    if res.status_code == 200:
        try:
            url_tmp = res.text.split('at ')[1].split('?')
            url = url_tmp[0]
            request_id = url_tmp[1].split('request_id=')[1]
            statut_and_url = check_url(url, request_id)
        except:
            pass
    else:
        statut_and_url = {
            'statut': 'error',
            'url':'',
        }
    return statut_and_url

def check_url(url, request_id):
    """
    @param  url: url to get status and url for download extract
    @param  request_id: 
    
    @return  statut: OK or pending
    @return  url: Optionnel
    """
    params = {'request_id': request_id}
    res = requests.get(url, params= params)

    # REMOVE IN PROD
    import logging
    logging.error(res.text)
    logging.error(res.url)

    try:
        statut = res.text.split()[0]
    except:
        statut = 'error'

    if statut != None and statut == 'OK':
        url = res.text.split()[2]

    json_res = {
        'statut': statut,
        'url': url,
    }
    return json_res

def download_file(request_id, type_ext):
    import logging
    logging.error(type_ext)
    url = settings.MAJIC_API + 'download_' + type_ext

    params = {'request_id': request_id}
    res = requests.get(url, params= params)
    # REMOVE IN PROD
    
    logging.error(res)
    logging.error(params)
    logging.error(res.status_code)
    logging.error(url)

    return res