import requests
import json
import db.models as mod
from db.config import base_url_traffic_magnet, username_traffic_magnet
from resources.api_logs import (logger_admitad, logger_finline, logger_teleport, logger_finstorm, logger_ecpc,
                                logger_credit_yes, logger_traffic_magnit)
import urllib3
import base64
from Crypto.Cipher import AES
from urllib.parse import quote_plus

import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def generate_token_admitad(p_base_header, p_client_id):
    print("Генерація токену")
    try:
        headers = {
                   'Authorization': f'Basic {p_base_header}',
                   'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
                   }
        payload = f'grant_type=client_credentials&client_id={p_client_id}&scope=advcampaigns_for_website%20arecords%20broker_application%20manage_advcampaigns%20websites%20advcampaigns%20manage_broker_application'
        response = requests.request("POST", url=mod.url_token_admitad, headers=headers, data=payload, verify=False)
        resp_data = json.loads(response.text)
        token_data = [resp_data['access_token'], resp_data['expires_in']]

        return token_data
    except TypeError as err:
        logger_admitad.error("[TypeError] generate_token_admitad: " + str(err))
    except ValueError as err:
        print("[ValueError] generate_token_admitad: " + str(err))
    except Exception as err:
        print("[Exception] generate_token_admitad: " + str(err))


def change(a):
    print(a)
    b = a.encode('latin1', 'ignore')
    c = b.decode('cp1251', 'ignore')
    return c


def send_request_admitad(p_camp_id, p_fisr_name, p_last_name, p_middle_name, p_birth_day, p_mobile_phone, p_mob_phone,
                         p_full_mob_phone, p_occupaion, p_work_salary, p_work_organization, p_work_adress,
                         p_work_phone, p_work_occupation, p_work_region_name, p_work_city_name, p_work_street,
                         p_work_house, p_inn, p_passport, p_passport_date, p_passport_title, p_fact_region_name,
                         p_fact_city_name, p_fact_street, p_fact_house, p_fact_flat, p_reg_region_name,
                         p_reg_city_name, p_reg_street, p_reg_house, p_reg_flat, p_credit_sum, p_credit_days, p_id,
                         p_credit_id, p_personal_data_agent, p_application_received_date_by_client, p_subid, p_email,
                         p_lead_id, p_type, p_token, p_stream_id, p_arg, p_profile_id, p_birthday_novy):
    try:

        headers = {
            'Authorization': f'Bearer {p_token}',
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
        url = f'https://api.admitad.com/website/{p_profile_id}/broker/applications/create/'
        # Тестовий режим
        p_test_mode = 0
        # Згода на обробку персональних даних
        p_user_notified = 1

        if p_type == 1:
            # -- містить короткий тип телефону v_mob_phone
            payload = f'campaigns=%5B{p_camp_id}%5D&user_notified={p_user_notified}&test_mode={p_test_mode}&first_name={p_fisr_name}&last_name={p_last_name}&middle_name={p_middle_name}&birth_date={p_birth_day}&mobile_phone={p_mob_phone}&occupation={p_occupaion}&work_salary={p_work_salary}&work_organization={p_work_organization}&work_phone={p_work_phone}&work_occupation={p_work_occupation}&work_region_name={p_work_region_name}&work_city_name={p_work_city_name}&work_street={p_work_street}&inn={p_inn}&work_house={p_work_house}&email={p_email}&passport={p_passport}&passport_date={p_passport_date}&passport_title={p_passport_title}&fact_region_name={p_fact_region_name}&fact_city_name={p_fact_city_name}&fact_street={p_fact_street}&fact_house={change(p_fact_house)}&fact_flat={p_fact_flat}&reg_region_name={p_reg_region_name}&reg_city_name={p_reg_city_name}&reg_house={p_reg_house}&reg_flat={p_reg_flat}&credit_sum={p_credit_sum}&credit_days={p_credit_days}&personal_data_agent={p_personal_data_agent}&application_received_date_by_client={p_application_received_date_by_client}'
        elif p_type == 2:
            # -- містить довгий тип телефону v_mobile_phone
            payload = f'campaigns=%5B{p_camp_id}%5D&user_notified={p_user_notified}&test_mode={p_test_mode}&first_name={p_fisr_name}&last_name={p_last_name}&middle_name={p_middle_name}&birth_date={p_birth_day}&mobile_phone=%2B{p_mobile_phone}&occupation={p_occupaion}&work_salary={p_work_salary}&work_organization={p_work_organization}&work_phone={p_work_phone}&work_occupation={p_work_occupation}&work_region_name={p_work_region_name}&work_city_name={p_work_city_name}&work_street={p_work_street}&inn={p_inn}&work_house={p_work_house}&email={p_email}&passport={p_passport}&passport_date={p_passport_date}&passport_title={p_passport_title}&fact_region_name={p_fact_region_name}&fact_city_name={p_fact_city_name}&fact_street={p_fact_street}&fact_house={change(p_fact_house)}&fact_flat={p_fact_flat}&reg_region_name={p_reg_region_name}&reg_city_name={p_reg_city_name}&reg_house={p_reg_house}&reg_flat={p_reg_flat}&credit_sum={p_credit_sum}&credit_days={p_credit_days}&personal_data_agent={p_personal_data_agent}&application_received_date_by_client={p_application_received_date_by_client}'
        elif p_type == 3:
            # -- містить короткий тип телефону v_mob_phone та поле v_subid - це дата народження в форматі 1992-10-10
            payload = f'campaigns=%5B{p_camp_id}%5D&user_notified={p_user_notified}&test_mode={p_test_mode}&first_name={p_fisr_name}&last_name={p_last_name}&middle_name={p_middle_name}&birth_date={p_birth_day}&mobile_phone={p_mob_phone}&occupation={p_occupaion}&work_salary={p_work_salary}&work_organization={p_work_organization}&work_phone={p_work_phone}&work_occupation={p_work_occupation}&work_region_name={p_work_region_name}&work_city_name={p_work_city_name}&work_street={p_work_street}&inn={p_inn}&work_house={p_work_house}&email={p_email}&passport={p_passport}&passport_date={p_passport_date}&passport_title={p_passport_title}&fact_region_name={p_fact_region_name}&fact_city_name={p_fact_city_name}&fact_street={p_fact_street}&fact_house={change(p_fact_house)}&fact_flat={p_fact_flat}&reg_region_name={p_reg_region_name}&reg_city_name={p_reg_city_name}&reg_house={p_reg_house}&reg_flat={p_reg_flat}&credit_sum={p_credit_sum}&credit_days={p_credit_days}&personal_data_agent={p_personal_data_agent}&application_received_date_by_client={p_application_received_date_by_client}&subid={p_subid}'
        elif p_type == 4:
            # -- містить довгий тип телефону v_mobile_phone
            payload = f'campaigns=%5B{p_camp_id}%5D&user_notified={p_user_notified}&test_mode={p_test_mode}&first_name={p_fisr_name}&last_name={p_last_name}&middle_name={p_middle_name}&birth_date={p_birth_day}&mobile_phone=%2B{p_mob_phone}&occupation={p_occupaion}&work_salary={p_work_salary}&work_organization={p_work_organization}&work_phone={p_work_phone}&work_occupation={p_work_occupation}&work_region_name={p_work_region_name}&work_city_name={p_work_city_name}&work_street={p_work_street}&inn={p_inn}&work_house={p_work_house}&email={p_email}&passport={p_passport}&passport_date={p_passport_date}&passport_title={p_passport_title}&fact_region_name={p_fact_region_name}&fact_city_name={p_fact_city_name}&fact_street={p_fact_street}&fact_house={change(p_fact_house)}&fact_flat={p_fact_flat}&reg_region_name={p_reg_region_name}&reg_city_name={p_reg_city_name}&reg_house={p_reg_house}&reg_flat={p_reg_flat}&credit_sum={p_credit_sum}&credit_days={p_credit_days}&personal_data_agent={p_personal_data_agent}&application_received_date_by_client={p_application_received_date_by_client}&subid={p_birthday_novy}'
        elif p_type == 5:
            # -- містить короткий тип телефону v_mob_phone та поле v_subid - це дата народження в форматі 1992-10-10
            payload = f'campaigns=%5B{p_camp_id}%5D&user_notified={p_user_notified}&test_mode={p_test_mode}&first_name={p_fisr_name}&last_name={p_last_name}&middle_name={p_middle_name}&birth_date={p_birth_day}&mobile_phone={p_mob_phone}&occupation={p_occupaion}&work_salary={p_work_salary}&work_organization={p_work_organization}&work_phone={p_work_phone}&work_occupation={p_work_occupation}&work_region_name={p_work_region_name}&work_city_name={p_work_city_name}&work_street={p_work_street}&inn={p_inn}&work_house={p_work_house}&email={p_email}&passport={p_passport}&passport_date={p_passport_date}&passport_title={p_passport_title}&fact_region_name={p_fact_region_name}&fact_city_name={p_fact_city_name}&fact_street={p_fact_street}&fact_house={change(p_fact_house)}&fact_flat={p_fact_flat}&reg_region_name={p_reg_region_name}&reg_city_name={p_reg_city_name}&reg_house={p_reg_house}&reg_flat={p_reg_flat}&credit_sum={p_credit_sum}&credit_days={p_credit_days}&personal_data_agent={p_personal_data_agent}&application_received_date_by_client={p_application_received_date_by_client}&subid={p_birthday_novy}'
        response = requests.request("POST", url=url, headers=headers, data=payload.encode('utf-8'), verify=False)

        logger_admitad.info("URL: " + str(url))
        logger_admitad.info("BODY: " + str(payload))

        logger_admitad.info("RESPONSE_STATUS: " + str(response))
        resp_data = json.loads(response.text)
        logger_admitad.info("RESPONSE_JSON :" + str(resp_data))

        if response.json()['id'] is None:
            logger_admitad.warning("ID від партнера не отримано")
            logger_admitad.warning("ERROR_MESSAGE: " + str(response.json()['errors'][0]['message']))
            mod.update_lead(p_lead_id, p_camp_id, 0, 'error', 1, 0, p_stream_id, None)
        else:
            v_id = resp_data['id']
            v_campaign = resp_data['responses'][0]['campaign_id']
            v_status = resp_data['responses'][0]['status']
            v_order_id = resp_data['responses'][0]['order_id']
            if not resp_data['errors']:
                v_errors = resp_data['errors']
                logger_admitad.error("LEAD_ID: " + str(p_lead_id) + " - " + str(v_errors))
                mod.update_lead(p_lead_id, p_camp_id, v_id, v_status, 0, 0, p_stream_id, None)
            else:
                v_errors = resp_data['errors']
                mod.update_lead(p_lead_id, p_camp_id, v_id, v_status, 1, 0, p_stream_id, None)
                logger_admitad.error("LEAD_ID: " + str(p_lead_id) + " - " + str(v_errors))
    except ValueError as err:
        logger_admitad.error("[ValueError] send_request_admitad: " + str(err))
    except KeyError as err:
        logger_admitad.error("[KeyError] send_request_admitad: " + str(err))
    except Exception as err:
        logger_admitad.error("[Exception] send_request_admitad: " + str(err))


def get_status_admitad(p_partner_id, p_partner_uuid, p_profile_id, p_lead_id, p_token, p_stream_id):
    try:
        logger_admitad.info("\nОтримання статусу по loan_id - " + str(p_lead_id))

        url = f"https://api.admitad.com/website/{p_profile_id}/broker/applications/?offset=0&limit=200&id={p_partner_uuid}&campaigns={p_partner_id}"
        token = p_token
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
        }

        logger_admitad.info("URL ST_UPDATE: " + str(url))
        logger_admitad.info("TOKEN ST_UPDATE: " + str(token))
        logger_admitad.info("HEADERS ST_UPDATE: " + str(headers))

        response = requests.request("GET", url=url, headers=headers, data=(), verify=False)
        resp = json.loads(response.text)

        logger_admitad.info("RESPONSE ST_UPDATE: " + str(resp))
        try:
            stat_new = resp['results'][0]['responses'][0]['status']
        except KeyError as err:
            stat_new = "new"
            logger_admitad.error("Помилка api.py: " + str(err))

        if stat_new == "declined":
            if resp.get('data') is None:
                error_text = resp['results'][0]['responses'][0]['server_response']
            else:
                error_text = resp['results'][0]['responses'][0]['server_response']['data']
            logger_admitad.error("ERROR: " + str(error_text))
            mod.upd_lead(p_lead_id, p_partner_id, stat_new, 1, p_stream_id)
        else:
            mod.upd_lead(p_lead_id, p_partner_id, stat_new, 0, p_stream_id)
    except ValueError as err:
        logger_admitad.error("Помилка api.py - get_status_admitad (ValueError): " + str(err))
    except KeyError as err:
        logger_admitad.error("Помилка api.py - get_status_admitad (KeyError): " + str(err))
    except Exception as err:
        logger_admitad.error("Помилка api.py - get_status_admitad (Exception): " + str(err))


def send_request_finline(p_partner_id, p_phone, p_inn, p_occupation, p_last_name, p_first_name,
                                     p_middle_name, p_agree_time, p_birthday, p_amount, p_aim, p_city, p_lead_id,
                                     p_sample_id, p_lead, p_uid):


    agree = 1
    p_url = "https://finx.com.ua"
    url_finline = f"https://finline.ua/api/lead/create/{p_uid}/1"

    data = {
        'phone': p_phone,
        'identCode': p_inn,
        'employment': p_occupation,
        'lastName': p_last_name,
        'firstName': p_first_name,
        'middleName': p_middle_name,
        'agree': agree,
        'url': p_url,
        'agreeTime': p_agree_time,
        'birthDate': p_birthday,
        'amount': p_amount,
        'aim': p_aim,
        'city': p_city
    }

    print(data)

    logger_finline.info("LEAD_ID: " + str(p_lead))
    logger_finline.info("URL: " + str(url_finline))
    logger_finline.info("BODY: " + str(data))

    response = requests.request('POST', url_finline, data=data, verify=False)

    dat = json.loads(response.text)
    logger_finline.info("RESPONSE_JSON: " + str(dat))

    result_check = dat['result']
    partner_lead_id = dat['leadID']
    declined_check = dat['declined']
    declined_reason = dat['declineReason']

    if result_check:
        if not declined_check:
            mod.update_lead(p_lead_id, p_partner_id, partner_lead_id, 'True', 0, 0, p_sample_id, None)

        elif declined_check:
            mod.update_lead(p_lead_id, p_partner_id, partner_lead_id, 'False', 1, 1, p_sample_id, None)
    else:
        mod.update_lead(p_lead_id, p_partner_id, partner_lead_id, 'False', 1, 0, p_sample_id, None)


def send_request_teleport(p_lead_id, p_first_name, p_last_name, p_middle_name, p_phone, p_birthday, p_subid,
                          p_inn, p_pass_serial, p_pass_num, p_pass_dt, p_reg_region, p_reg_city, p_reg_street,
                          p_reg_house, p_reg_apartment, p_fact_region, p_fact_city, p_fact_street, p_fact_house,
                          p_fact_apartment, p_camp_id, p_sample_type, p_uid):

    url_teleport = "https://gate.ua.tlpt.io/sendrequest"

    logger_teleport.info("LEAD_ID: " + str(p_lead_id))
    logger_teleport.info("URL: " + str(url_teleport))

    data = {
        'uid': f'{p_uid}',
        'id': p_lead_id,
        'subid': p_subid,
        'last_name': p_last_name,
        'first_name': p_first_name,
        'middle_name': p_middle_name,
        'phone': p_phone,
        'birthday': p_birthday,
        'inn_number': p_inn,
        'residential_region': p_fact_region,
        'residential_city': p_fact_city,
        'residential_street': p_fact_street,
        'residential_house': p_fact_house,
        'residential_building': '',
        'residential_apartment': p_fact_apartment,
        'passport_series_ua_old': p_pass_serial,
        'passport_number_ua_old': p_pass_num,
        'passport_date_of_issue': p_pass_dt,
        'registration_region': p_reg_region,
        'registration_city': p_reg_city,
        'registration_street': p_reg_street,
        'registration_house': p_reg_house,
        'registration_building': '',
        'registration_apartment': p_reg_apartment
    }

    logger_teleport.info("BODY: " + str(data))

    response = requests.request('POST', url=url_teleport, data=data, verify=False)
    res = response.text

    logger_teleport.info("RESPONSE: " + str(res))
    if res == "succeed":
        mod.update_lead(p_lead_id, p_camp_id, 0, res, 0, 0, p_sample_type, None)
    else:
        mod.update_lead(p_lead_id, p_camp_id, 0, res, 1, 0, p_sample_type, None)


def send_request_finstorm(p_phone, p_inn, p_first_name, p_last_name, p_middle_name, p_uuid, p_city,
                          p_sample_type, p_camp_id):
    try:
        url_finstorm = "https://p2p.finhub.ua/api/upload/ohjouYNIufg)vm__werf"   #"https://api.finbroker.biz.ua/api/upload/ohjouYNIufg)vm__werf"
	
        logger_finstorm.info("LEAD_ID: " + str(p_uuid))
        logger_finstorm.info("URL: " + str(url_finstorm))

        payload = {"phone": f"{p_phone}",
                   "city": f"{p_city}",
                   "first_name": f"{p_first_name}",
                   "last_name": f"{p_last_name}",
                   "middle_name": f"{p_middle_name}",
                   "inn": f"{p_inn}",
                   "uuid": f"{p_uuid}"
        }

        time.sleep(1)
        print(payload)
        logger_finstorm.info("BODY: " + str(payload))
        response = requests.request('POST', url=url_finstorm, data=payload, verify=False)
        #res = response.text
        status = response.status_code
        print("RESPONSE: " + str(response) + "\n" + str(status))

        if status == 200:
            result = json.loads(response.text)
            #print(response)
            logger_finstorm.info("RESPONSE JSON: " + str(response).replace('\'', '`'))
            if result['status']:
                status = 'True'
                mod.update_lead(p_uuid, p_camp_id, 0, status, 0, 0, p_sample_type, None)
            else:
                status = 'False'
                mod.update_lead(p_uuid, p_camp_id, 0, status, 1, 0, p_sample_type, None)
    except TypeError as err:
        logger_finstorm.error("[TypeError] api.py - send_request_finstorm: " + str(err))
    except ValueError as err:
        logger_finstorm.error("[ValueError] api.py - send_request_finstorm: " + str(err))
    except Exception as err:
        logger_finstorm.error("[Exception] api.py - send_request_finstorm: " + str(err))

def send_request_ecpc(p_token, p_trigger_id, p_first_name, p_last_name, p_middle_name, p_phone, p_inn, p_camp_id, p_sample_type):
    try:
        url_ecpc = "https://zaimer.com.ua/api/create_user/"

        logger_ecpc.info("LEAD_ID: " + str(p_trigger_id))
        logger_ecpc.info("URL: " + str(url_ecpc))

        payload = {"access_token": f"{p_token}",
                   #"trigger_id": f"{p_trigger_id}", # відключено за проханням партнера
                   "first_name": f"{p_first_name}",
                   "second_name": f"{p_last_name}",
                   "middle_name": f"{p_middle_name}",
                   "phone": f"{p_phone}",
                   "inn": f"{p_inn}"
                   }

        #time.sleep(1)
        print(payload)
        logger_ecpc.info("BODY: " + str(payload))
        response = requests.request('POST', url=url_ecpc, data=payload, verify=False)
        res = response.text
        status = response.status_code
        print("RESPONSE: " + str(response) + "\n" + str(status))
        logger_ecpc.info("RESPONSE FULL: " + str(res).replace('\'', '`'))
        if status == 200:
            result = json.loads(response.text)
            # print(response)
            logger_ecpc.info("RESPONSE JSON: " + str(response).replace('\'', '`'))
            if result['status']:
                status = 'Success'
                partner_aliase_id = result['aliase']
                mod.update_lead(p_trigger_id, p_camp_id, 0, status, 0, 0, p_sample_type, partner_aliase_id)
            else:
                status = 'Error'
                mod.update_lead(p_trigger_id, p_camp_id, 0, status, 1, 0, p_sample_type, None)
        else:
            logger_ecpc.info("RESPONSE JSON ERROR: " + str(response).replace('\'', '`'))

    except TypeError as err:
        logger_ecpc.error("[TypeError] api.py - send_request_ecpc: " + str(err))
    except ValueError as err:
        logger_ecpc.error("[ValueError] api.py - send_request_ecpc: " + str(err))
    except Exception as err:
        logger_ecpc.error("[Exception] api.py - send_request_ecpc: " + str(err))



def send_request_credit_yes(p_partner_id, p_sample_type, p_token, p_product, p_utm_medium, p_utm_campaign, p_utm_term,
                            p_user_ip, p_user_agent, p_custom_identifier, p_name, p_second_name, p_surname,
                            p_phone, p_pers_id, p_loan_amount, p_loan_period, p_short_consent):
    try:

        #test_url
        #url_credit_yes = "https://dev.credityes.com.ua/registrationExternal"
        #prod_url
        url_credit_yes = "https://www.credityes.com.ua/registrationExternal"

        logger_credit_yes.info("LEAD_ID: " + str(p_custom_identifier))
        logger_credit_yes.info("URL: " + str(url_credit_yes))

        payload = json.dumps({
              "apiKey": f"{p_token}",
              "product": f"{p_product}",
              "customIdentifier": f"{p_custom_identifier}",
              "utm_medium": f"{p_utm_medium}",
              "utm_campaign": f"{p_utm_campaign}",
              "utm_term": f"{p_utm_term}",
              "userIP": f"{p_user_ip}",
              "userAgent": f"{p_user_agent}",
              "fields": {
                "name": f"{p_name}",
                "secondName": f"{p_second_name}",
                "surname": f"{p_surname}",
                #"email": "test@gmail.com",
                "phone": f"{p_phone}",
                "persId": p_pers_id,
                "loanAmount": p_loan_amount,
                "loanPeriod": p_loan_period,
                "consentRules": p_short_consent
              }
            })
        # time.sleep(1)
        print(payload)
        logger_credit_yes.info("BODY: " + str(payload))

        response = requests.request('POST', url=url_credit_yes, data=payload, verify=False)

        res = response.text

        status = response.status_code
        print("RESPONSE: " + str(response) + "\n" + str(status))

        logger_credit_yes.info("RESPONSE FULL: " + str(res).replace('\'', '`'))

        if status == 200:
            result = json.loads(response.text)
            # print(response)
            logger_credit_yes.info("RESPONSE JSON: " + str(response).replace('\'', '`'))
            if result['status'] == 'Success':
                status = 'Success'
                order_id = result['orderId']
                print(f"ORDER_ID: {order_id}")
                mod.update_lead(p_custom_identifier, p_partner_id, 0, status, 0, 0, p_sample_type, order_id)
            elif result['status'] == 'Rejected':
                status = 'Rejected'
                mod.update_lead(p_custom_identifier, p_partner_id, 0, status, 0, 0, p_sample_type, None)
            else:
                status = 'Error'
                mod.update_lead(p_custom_identifier, p_partner_id, 0, status, 1, 0, p_sample_type, None)
        else:
            logger_credit_yes.info("RESPONSE JSON ERROR: " + str(response).replace('\'', '`'))

    except TypeError as err:
        logger_credit_yes.error("[TypeError] api.py - send_request_credit_yes: " + str(err))
    except ValueError as err:
        logger_credit_yes.error("[ValueError] api.py - send_request_credit_yes: " + str(err))
    except Exception as err:
        logger_credit_yes.error("[Exception] api.py - send_request_credit_yes: " + str(err))



def send_request_traffic_magnit(p_lead_id, p_partner_id, p_sample_type, token, p_contact_number, p_first_name,
                                                p_last_name, p_patronymic, p_sub3, p_sub4):
    # ==== Налаштування ====
    BASE_URL = base_url_traffic_magnet
    USERNAME = username_traffic_magnet
    PASSWORD = token

    # Креденшіали для Basic Auth
    credentials = f"{USERNAME}:{PASSWORD}"
    auth_header = base64.b64encode(credentials.encode()).decode()

    headers_common = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/json"
    }

    body_data = {
            "contact_number": f"{p_contact_number}",
            "first_name": f"{p_first_name}",
            "last_name": f"{p_last_name}",
            "patronymic": f"{p_patronymic}",
            "sub3": f"{p_sub3}",
            "sub4": f"{p_sub4}",
    }

    # ==== Retry-логіка ====
    def send_with_retry(url, headers, payload, max_retries=5):
        retries = 0
        while retries <= max_retries:
            response = requests.post(url, headers=headers, json=payload)

            try:
                resp_json = response.json()
            except Exception:
                resp_json = {f"DETAIL": f"Invalid JSON in response by LID - {p_lead_id}: {response}"}
                logger_traffic_magnit.error(resp_json)

            status = response.status_code
            status_desc = resp_json.get("message")
            logger_traffic_magnit.info(f"LID: {p_lead_id}, REST_JSON: {resp_json}")

            # === Обробка кодів ===
            if status == 202:
                status_info = f"LID {p_lead_id} accepted:, {resp_json}"
                logger_traffic_magnit.info(status_info)
                # TODO: оновити статус у БД (успіх)
                mod.update_lead(p_lead_id, p_partner_id, 0, status_desc, 0, 0, p_sample_type, 0)
                #update_lead(p_lead_id, p_partner_id, p_partner_uuid, p_lead_status, p_partner_error, p_dublicate, p_stream_id, p_aliase_id)
                return resp_json

            elif status == 400:
                status_info = f"Bad Request by LID {p_lead_id}:, {resp_json}"
                logger_traffic_magnit.info(status_info)
                # TODO: оновити статус у БД (відхилено через помилку даних)
                mod.update_lead(p_lead_id, p_partner_id, 0, status_desc, 0, 0, p_sample_type, 0)
                # update_lead(p_lead_id, p_partner_id, p_partner_uuid, p_lead_status, p_partner_error, p_dublicate, p_stream_id, p_aliase_id)

                return resp_json

            elif status == 401:
                status_info = f"Unauthorized:, {resp_json}"
                logger_traffic_magnit.info(status_info)
                # TODO: лог помилки авторизації, можливо зупинити обробку
                mod.update_lead(p_lead_id, p_partner_id, 0, status_desc, 0, 0, p_sample_type, 0)
                # update_lead(p_lead_id, p_partner_id, p_partner_uuid, p_lead_status, p_partner_error, p_dublicate, p_stream_id, p_aliase_id)
                return resp_json

            elif status == 409:
                status_info = f"Conflict (duplicate LID {p_lead_id}):, {resp_json}"
                logger_traffic_magnit.info(status_info)
                # TODO: оновити статус у БД (дублікат)
                mod.update_lead(p_lead_id, p_partner_id, 0, status_desc, 0, 1, p_sample_type, 0)
                # update_lead(p_lead_id, p_partner_id, p_partner_uuid, p_lead_status, p_partner_error, p_dublicate, p_stream_id, p_aliase_id)

                return resp_json

            elif status == 429:
                wait_time = 2 ** retries  # exponential backoff: 2,4,8,16...
                status_info = f"Too Many Requests (LID {p_lead_id}). Retrying in {wait_time}s..."
                logger_traffic_magnit.info(status_info)

                time.sleep(wait_time)
                retries += 1
                continue  # повторна спроба

            else:
                status_info = f"Unexpected status (LID {p_lead_id}) {status}:, {resp_json}"
                logger_traffic_magnit.info(status_info)
                # TODO: логувати інші відповіді
                mod.update_lead(p_lead_id, p_partner_id, 0, status_desc, 0, 0, p_sample_type, 0)
                # update_lead(p_lead_id, p_partner_id, p_partner_uuid, p_lead_status, p_partner_error, p_dublicate, p_stream_id, p_aliase_id)
                return resp_json

        status_info = f"Max retries reached, LID {p_lead_id} not sent"
        logger_traffic_magnit.info(status_info)
        # TODO: логувати невдачу після всіх спроб
        mod.update_lead(p_lead_id, p_partner_id, 0, status_desc, 0, 0, p_sample_type, 0)
        # update_lead(p_lead_id, p_partner_id, p_partner_uuid, p_lead_status, p_partner_error, p_dublicate, p_stream_id, p_aliase_id)
        return None

    # ==== 1. Decrypted endpoint ====
    def submit_decrypted_lead():
        url = f"{BASE_URL}/decrypted"
        print(f"URL: {url}")
        print(f"headers_common: {headers_common}")
        print(f"body_data: {body_data}")
        return send_with_retry(url, headers_common, body_data)

    # ==== 2. Encrypted endpoint ====
    def pad(data: bytes, block_size=16) -> bytes:
        """PKCS7 padding для AES"""
        pad_len = block_size - (len(data) % block_size)
        return data + bytes([pad_len] * pad_len)

    def encrypt_aes256_ecb(data: dict, key: str) -> str:
        """Шифрує JSON у AES-256-ECB"""
        raw_json = json.dumps(data, ensure_ascii=False).encode("utf-8")
        cipher = AES.new(key.encode("utf-8"), AES.MODE_ECB)
        encrypted_bytes = cipher.encrypt(pad(raw_json, 16))
        return quote_plus(encrypted_bytes.hex())  # hex + URL encode

    def submit_encrypted_lead():
        url = f"{BASE_URL}/encrypted"

        # Ключ для шифрування (узгоджений з партнером)
        encryption_key = f"{token}"  # рівно 32 символи

        encrypted_body = {
            "request_body": encrypt_aes256_ecb(body_data, encryption_key)
        }

        headers_enc = headers_common.copy()
        headers_enc["api-key"] = "your_api_key"  # якщо потрібно
        headers_enc["X-Decryption-Key"] = encryption_key  # якщо потрібно

        print(f"URL: {url}")
        print(f"headers_enc: {headers_enc}")
        print(f"encrypted_body: {encrypted_body}")
        return send_with_retry(url, headers_enc, encrypted_body)

    submit_decrypted_lead()
    #submit_encrypted_lead()
