from db.models import get_source, get_partner_token, get_lead_list
from resources.api_logs import logger_traffic_magnit
from resources.api import send_request_traffic_magnit
#import urllib3
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os

conf = get_source()
#token = get_partner_token()

if __name__ == "__main__":
    try:
        for i in conf:
            if i["global_name"] == "TrafficMagnit" and i["is_active"] == 1:
                token = get_partner_token(i['partner_dict_id'], i['global_name'], i['stream_id'], i['base_header'], i['client_id'])
                leads = get_lead_list(i['partner_id'], i['stream_id'])
                for row in leads:

                    p_lead_id = row['lead_id']
                    p_partner_id = row['partner_id']
                    p_sample_type = row['sample_type']
                    p_contact_number = row['client_phone']
                    p_first_name = row['first_name']
                    p_last_name = row['last_name']
                    p_patronymic = row['middle_name']
                    p_sub3 = 'FinX'
                    p_sub4 = 'FinX'


                    send_request_traffic_magnit(p_lead_id, p_partner_id, p_sample_type, token, p_contact_number, p_first_name,
                                                p_last_name, p_patronymic, p_sub3, p_sub4)
    except TypeError as err:
        logger_traffic_magnit.error("[TypeError] traffic_magnit.py: " + str(err))
    except ValueError as err:
        logger_traffic_magnit.error("[ValueError] traffic_magnit.py: " + str(err))
    except KeyError as err:
        logger_traffic_magnit.error("[KeyError] traffic_magnit.py: " + str(err))
    except Exception as err:
        logger_traffic_magnit.error("[Exception] traffic_magnit.py: " + str(err))
