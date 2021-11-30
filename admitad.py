from db.models import get_source, get_partner_token, get_lead_list, check_status_admitad
from resources.api import send_request_admitad, get_status_admitad
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

conf = get_source()


if __name__ == "__main__":
    try:
        for i in conf:
            if i["global_name"] == "Admitad" and i["is_active"] == 1:
                token = get_partner_token(i['partner_dict_id'], i['global_name'], i['stream_id'], i['base_header'], i['client_id'])
                leads = get_lead_list(i['partner_id'], i['stream_id'])
                for row in leads:
                    p_camp_id = row['partner_id']
                    p_fisr_name = row['first_name']
                    p_last_name = row['last_name']
                    p_middle_name = row['middle_name']
                    p_birth_day = row['birthday']
                    p_birthday_novy = row['birthday_finme']
                    p_mobile_phone = row['client_phone2']
                    p_mob_phone = row['client_phone3']
                    p_full_mob_phone = row['client_phone']
                    p_occupaion = row['occupation']
                    p_work_salary = row['work_salary']
                    p_work_organization = row['work_organization']
                    p_work_adress = row['work_adress']
                    p_work_phone = row['work_phone']
                    p_work_occupation = row['work_occupation']
                    p_work_region_name = row['work_region_name']
                    p_work_city_name = row['work_city_name']
                    p_work_street = row['work_street']
                    p_work_house = row['work_house']
                    p_inn = row['inn']
                    p_passport = row['passport']
                    p_passport_date = row['passport_date']
                    p_passport_title = row['passport_title']
                    p_fact_region_name = row['fact_region_name']
                    p_fact_city_name = row['fact_city_name']
                    p_fact_street = row['fact_street']
                    p_fact_house = row['fact_house']
                    p_fact_flat = row['fact_flat']
                    p_reg_region_name = row['reg_region_name']
                    p_reg_city_name = row['reg_city_name']
                    p_reg_street = row['reg_street']
                    p_reg_house = row['reg_house']
                    p_reg_flat = row['reg_flat']
                    p_credit_sum = row['credit_sum']
                    p_credit_days = row['credit_days']
                    p_id = row['CID']
                    p_credit_id = row['lead_id']
                    p_personal_data_agent = row['CID']
                    p_application_received_date_by_client = row['application_received_date_by_client']
                    client = row['CID']
                    p_subid = row['subid']
                    p_email = row['email']
                    p_lead_id = row['lead_id']
                    p_type = i['data_type']
                    p_token = token
                    p_sample_type = row['sample_type']
                    p_arg = 0
                    p_profile_id = i['profile_id']

                    send_request_admitad(p_camp_id, p_fisr_name, p_last_name, p_middle_name, p_birth_day, p_mobile_phone,
                                         p_mob_phone,
                                         p_full_mob_phone, p_occupaion, p_work_salary, p_work_organization, p_work_adress,
                                         p_work_phone, p_work_occupation, p_work_region_name, p_work_city_name,
                                         p_work_street,
                                         p_work_house, p_inn, p_passport, p_passport_date, p_passport_title,
                                         p_fact_region_name,
                                         p_fact_city_name, p_fact_street, p_fact_house, p_fact_flat, p_reg_region_name,
                                         p_reg_city_name, p_reg_street, p_reg_house, p_reg_flat, p_credit_sum,
                                         p_credit_days, p_id,
                                         p_credit_id, p_personal_data_agent, p_application_received_date_by_client, p_subid,
                                         p_email,
                                         p_lead_id, p_type, p_token, p_sample_type, p_arg, p_profile_id, p_birthday_novy)

                lead_check = check_status_admitad(i['partner_id'], i['stream_id'])
                lead_check = []
                for j in lead_check:
                    print(j['partner_id'],  j['partner_uuid'], i['profile_id'],  i['client_id'], j['lead_id'], token, i['stream_id'])
                    get_status_admitad(j['partner_id'],  j['partner_uuid'], i['profile_id'],  j['lead_id'], token, i['stream_id'])

    except TypeError as err:
        print("[TypeError] admitad.py: " + str(err))
    except ValueError as err:
        print("[ValueError] admitad.py: " + str(err))
    except Exception as err:
        print("[Exception] admitad.py: " + str(err))
