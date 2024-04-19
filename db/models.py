import pymssql
from db.config import host_delta, user_delta, password_delta, database_delta, url_token_admitad
from resources.api import generate_token_admitad


conn = pymssql.connect(host=host_delta, user=user_delta, password=password_delta, database=database_delta, as_dict=True,
                       autocommit=False, charset='cp1251')


# Отримання конфігурації з БД
def get_source():
    conf = conn.cursor()
    conf_sql = "select * from crm..ext_partner_config;"
    conf.execute(conf_sql)
    res = conf.fetchall()
    conf.close()
    return res


# Отримання токена і внутрішні перевірки статуса дії токена
def get_partner_token(p_partner_id, p_partner_name, p_stream_id, p_base_header, p_client_id):
    token = conn.cursor()
    token.execute("EXEC crm..ext_partner_get_token %s, %s;", (p_partner_id, p_stream_id))
    status = token.fetchone()

    print("EXEC crm..ext_partner_get_token %s, %s;", (p_partner_id, p_stream_id))

    if status['status'] == 0:
        print("Токен відсутній")
        gen_token = generate_token_admitad(p_base_header, p_client_id)
        ins_partner_token(p_partner_id, p_partner_name, gen_token[0], gen_token[1], p_stream_id)
        token = gen_token[0]
    elif status['status'] == 1:
        gen_token = generate_token_admitad(p_base_header, p_client_id)
        upd_partner_token(p_partner_id, p_partner_name, gen_token[0], gen_token[1], p_stream_id)
        token = gen_token[0]
    else:
        print("Токен активний")
        token = status['token']

    return token


# Вставка токена
def ins_partner_token(p_partner_id, p_partner_name, p_access_token, p_expires_in, p_stream_id):
    ins = conn.cursor()
    ins.execute('EXEC crm..ext_partner_ins_token %s, %s, %s, %s, %s;', (p_partner_id, p_partner_name, p_access_token, p_expires_in, p_stream_id))
    conn.commit()
    ins.close()


# Оновлення токена
def upd_partner_token(p_partner_id, p_partner_name, p_access_token, p_expires_in, p_stream_id):
    upd = conn.cursor()
    upd.execute('EXEC crm..ext_partner_upd_token %s, %s, %s, %s, %s;', (p_partner_id, p_partner_name, p_access_token, p_expires_in, p_stream_id))
    conn.commit()
    upd.close()


# Отримання списку лідів на відправку
def get_lead_list(p_partner_id, p_stream_id):
    try:
        lead = conn.cursor()
        print(f'exec crm..ext_partner_select {p_partner_id}, {p_stream_id};')
        lead_sql = f'exec crm..ext_partner_select {p_partner_id}, {p_stream_id};'
        #lead.execute('EXEC crm..ext_partner_select %s, %s;', (p_partner_id, p_stream_id))
        lead.execute(lead_sql)
        lead_list = lead.fetchall()
        lead.close()
        return lead_list
    except TypeError as err:
        print("[TypeError] models.py - get_lead_list: " + str(err))
    except ValueError as err:
        print("[ValueError] models.py - get_lead_list: " + str(err))
    except Exception as err:
        print("[Exception] models.py - get_lead_list: " + str(err))


# Оновлення ліда в таблиці
def update_lead(p_lead_id, p_partner_id, p_partner_uuid, p_lead_status, p_partner_error, p_dublicate, p_stream_id):
    try:
        upd = conn.cursor()
        upd.execute("EXEC crm..ext_partner_upd_lead_table %s, %s, %s, %s, %s, %s, %s;",
                (p_lead_id, p_partner_uuid, p_lead_status, p_partner_error, p_dublicate, p_partner_id, p_stream_id))
        print("EXEC crm..ext_partner_upd_lead_table %s, %s, %s, %s, %s, %s, %s;",
                (p_lead_id, p_partner_uuid, p_lead_status, p_partner_error, p_dublicate, p_partner_id, p_stream_id))
        conn.commit()
        upd.close()
    except TypeError as err:
        print("[TypeError] models.py - update_lead_table: " + str(err))
    except ValueError as err:
        print("[ValueError] models.py - update_lead_table: " + str(err))
    except Exception as err:
        print("[Exception] models.py - update_lead_table: " + str(err))


def upd_lead(p_lead_id, p_partner_id, p_partner_status, p_error, p_stream_id):
    upd = conn.cursor()
    upd.execute("EXEC crm..ext_partner_upd_lead %s, %s, %s, %s, %s, %s;",
                               (p_lead_id, p_partner_status, p_error, p_partner_id, p_partner_status, p_stream_id))
    conn.commit()
    upd.close()


# Вибірка лідів по яким потрібна повторна перевірка статусу
def check_status_admitad(p_partner_id, p_type_send):
        che = conn.cursor()
        che.execute('''select partner_id, partner_uuid, lead_id, sample_type from crm..ext_partner_leads
                        where lead_status in ('new', 'waiting', 'processing') and isnull(partner_uuid,0) != 0
                        and partner_id = %s and type_send = %s; ''', (p_partner_id, p_type_send,))
        res = che.fetchall()
        che.close()
        return res
