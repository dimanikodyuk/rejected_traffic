from db.models import get_source, get_partner_token, get_lead_list, check_status_admitad
from resources.api import send_request_admitad, get_status_admitad, send_request_finline, send_request_finstorm
from resources.api_logs import logger_finline, logger_finstorm
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

conf = get_source()

if __name__ == "__main__":
    try:
        for i in conf:

            if i["global_name"] == "Finstorm" and i["is_active"] == 1:
                p_uid = i['uid']
                logger_finstorm.info("UID: " + str(i['uid']))
                leads = get_lead_list(i['partner_id'], i['stream_id'])

                for row in leads:
                    p_phone = row['client_phone2']
                    p_inn = row['inn']
                    p_first_name = row['first_name']
                    p_last_name = row['last_name']
                    p_middle_name = row['middle_name']
                    p_email = row['email']
                    p_uuid = row['lead_id']
                    p_sample_type = row['sample_type']
                    p_camp_id = i['partner_id']
                    p_city = row['fact_city_name']
                    print(row)

                    send_request_finstorm(p_phone, p_inn, p_first_name, p_last_name, p_middle_name, p_uuid,
                                          p_city, p_sample_type, p_camp_id)

    except TypeError as err:
        logger_finstorm.error("[TypeError] finstorm.py: " + str(err))
    except ValueError as err:
        logger_finstorm.error("[ValueError] finstorm.py: " + str(err))
    except Exception as err:
        logger_finstorm.error("[Exception] finstorm.py: " + str(err))
