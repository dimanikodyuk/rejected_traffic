from db.models import get_source, get_partner_token, get_lead_list, check_status_admitad
from resources.api import send_request_admitad, get_status_admitad, send_request_finline
from resources.api_logs import logger_finline
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

conf = get_source()

if __name__ == "__main__":
    try:
        for i in conf:
            if i["global_name"] == "Finline" and i["is_active"] == 1:
                p_uid = i['uid']

                leads = get_lead_list(i['partner_id'], i['stream_id'])
                for row in leads:
                    p_phone = row['client_phone2']
                    p_inn = row['inn']
                    p_occupation = row['occupation_finline']
                    p_last_name = row['last_name']
                    p_first_name = row['first_name']
                    p_middle_name = row['middle_name']
                    p_agree_time = row['agree_time']
                    p_birthday = row['birthday']
                    p_amount = row['amount_finline']
                    p_aim = row['purpose_finline']
                    p_city = row['fact_city_name']
                    p_loan_id = row['lead_id']
                    p_sample_id = row['sample_type']
                    p_lead_id = row['lead_id']
                    send_request_finline(i['partner_id'], p_phone, p_inn, p_occupation, p_last_name, p_first_name,
                                         p_middle_name, p_agree_time, p_birthday, p_amount, p_aim, p_city, p_loan_id,
                                         p_sample_id, p_lead_id, p_uid)
    except TypeError as err:
        logger_finline.error("[TypeError] finline.py: " + str(err))
    except ValueError as err:
        logger_finline.error("[ValueError] finline.py: " + str(err))
    except Exception as err:
        logger_finline.error("[Exception] finline.py: " + str(err))
