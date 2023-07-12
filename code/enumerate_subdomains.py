import psycopg2
from termcolor import colored


def return_subdomains(domain):
    '''
    Uses the Crt.sh database to find subdomains based on certificates
    '''
    try:
        conn = psycopg2.connect(
            database="certwatch",
            user='guest',
            host='crt.sh',
            port='5432',
        )
        conn.set_session(autocommit=True)

        cursor = conn.cursor()
        query = f"select distinct(lower(name_value)) FROM certificate_and_identities cai WHERE plainto_tsquery('{domain}') @@ identities(cai.CERTIFICATE) AND lower(cai.NAME_VALUE) LIKE ('%.{domain}')"
        cursor.execute(query)

        # Dirty compehension to convert array of tuples into plain array and filter out wildcard subdomains.
        data = [i[0].replace('www.', '')
                for i in cursor.fetchall() if i[0][0] != '*']

        conn.close()
        data = list(set(data))
        for entry in data:
            if entry.startswith('www.'):
                data.remove(entry)
        return data
    except psycopg2.errors.SerializationFailure as e:
        print(colored(
            '\n[ERROR] Problem connecting to the Crt.sh database, this can likely be fixed by waiting a few minutes', 'red'))
        exit()
