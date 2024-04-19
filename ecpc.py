from db.models import get_source, get_partner_token, get_lead_list
from resources.api_logs import logger_ecpc
from resources.api import send_request_ecpc
#import urllib3
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os

url = "https://zaimer.com.ua/api/create_user/"

conf = get_source()
#token = get_partner_token()

if __name__ == "__main__":
    try:
        for i in conf:
            if i["global_name"] == "ECPC100" and i["is_active"] == 1:
                token = get_partner_token(i['partner_dict_id'], i['global_name'], i['stream_id'], i['base_header'], i['client_id'])
                leads = get_lead_list(i['partner_id'], i['stream_id'])
                for row in leads:
                    print(row)

                    p_lead_id = row['lead_id']
                    p_first_name = row['first_name']
                    p_last_name = row['last_name']
                    p_middle_name = row['middle_name']
                    p_phone = row['client_phone2']
                    p_inn = row['inn']
                    p_camp_id = row['partner_id']
                    p_sample_type = row['sample_type']

                    send_request_ecpc(token, p_lead_id, p_first_name, p_last_name, p_middle_name, p_phone, p_inn,
                                      p_camp_id, p_sample_type)
    except TypeError as err:
        logger_ecpc.error("[TypeError] ecpc.py: " + str(err))
    except ValueError as err:
        logger_ecpc.error("[ValueError] ecpc.py: " + str(err))
    except KeyError as err:
        logger_ecpc.error("[KeyError] ecpc.py: " + str(err))
    except Exception as err:
        logger_ecpc.error("[Exception] ecpc.py: " + str(err))
