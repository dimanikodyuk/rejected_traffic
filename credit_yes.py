from db.models import get_source, get_partner_token, get_lead_list
from resources.api_logs import logger_credit_yes
from resources.api import send_request_credit_yes
#import urllib3
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os

conf = get_source()
#token = get_partner_token()

if __name__ == "__main__":
    try:
        for i in conf:
            if i["global_name"] == "CreditYes_API" and i["is_active"] == 1:
                token = get_partner_token(i['partner_dict_id'], i['global_name'], i['stream_id'], i['base_header'], i['client_id'])
                leads = get_lead_list(i['partner_id'], i['stream_id'])
                for row in leads:
                    #print(row)

                    p_partner_id = row['partner_id']
                    p_sample_type = row['sample_type']
                    p_product = 'e4acc42b4b1d33058a52601922daff95'
                    p_utm_medium = ''
                    p_utm_campaign = ''
                    p_utm_term = ''
                    p_user_ip = ''
                    p_user_agent = ''
                    p_custom_identifier = row['lead_id']
                    p_name = row['first_name']
                    p_second_name = row['last_name']
                    p_surname = row['middle_name']
                    p_phone = row['client_phone3'][1:10]
                    p_pers_id = row['inn']
                    p_loan_amount = 1000
                    p_loan_period = 3
                    p_short_consent = True

                    send_request_credit_yes(p_partner_id, p_sample_type, token, p_product, p_utm_medium, p_utm_campaign, p_utm_term, p_user_ip,
                                      p_user_agent, p_custom_identifier, p_name, p_second_name, p_surname,
                                      p_phone, p_pers_id, p_loan_amount, p_loan_period, p_short_consent)
    except TypeError as err:
        logger_credit_yes.error("[TypeError] credit_yes.py: " + str(err))
    except ValueError as err:
        logger_credit_yes.error("[ValueError] credit_yes.py: " + str(err))
    except KeyError as err:
        logger_credit_yes.error("[KeyError] credit_yes.py: " + str(err))
    except Exception as err:
        logger_credit_yes.error("[Exception] credit_yes.py: " + str(err))
