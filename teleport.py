from db.models import get_source, get_partner_token, get_lead_list, check_status_admitad
from resources.api import send_request_admitad, get_status_admitad, send_request_finline, send_request_teleport
from resources.api_logs import logger_teleport
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

conf = get_source()

if __name__ == "__main__":
    try:
        for i in conf:
            if i["global_name"] == "Teleport" and i["is_active"] == 1:
                leads = get_lead_list(i['partner_id'], i['stream_id'])
                for row in leads:
                    p_lead_id = row['lead_id']
                    p_first_name = row['first_name']
                    p_last_name = row['last_name']
                    p_middle_name = row['middle_name']
                    p_phone = row['client_phone2']
                    p_birthday = row['birthday_finme']
                    p_subid = row['subid_finline']
                    p_inn = row['inn']
                    p_pass_serial = row['passport_serial']
                    p_pass_num = row['passport_num']
                    p_pass_dt = row['passport_date_new']
                    p_reg_region = row['reg_region_name']
                    p_reg_city = row['reg_city_name']
                    p_reg_street = row['reg_street']
                    p_reg_house = row['reg_house']
                    p_reg_apartment = row['reg_flat']

                    p_fact_region = row['fact_region_name']
                    p_fact_city = row['fact_city_name']
                    p_fact_street = row['fact_street']
                    p_fact_house = row['fact_house']
                    p_fact_apartment = row['fact_flat']

                    p_sample_type = row['sample_type']
                    send_request_teleport(p_lead_id, p_first_name, p_last_name, p_middle_name, p_phone,
                                          p_birthday,
                                          p_subid, p_inn, p_pass_serial, p_pass_num, p_pass_dt, p_reg_region,
                                          p_reg_city, p_reg_street, p_reg_house, p_reg_apartment, p_fact_region,
                                          p_fact_city, p_fact_street, p_fact_house, p_fact_apartment, i['partner_id'],
                                          p_sample_type)
    except TypeError as err:
        logger_teleport.error("[TypeError] teleport.py: " + str(err))
    except ValueError as err:
        logger_teleport.error("[ValueError] teleport.py: " + str(err))
    except Exception as err:
        logger_teleport.error("[Exception] teleport.py: " + str(err))