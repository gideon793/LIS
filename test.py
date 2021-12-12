conn = psycopg2.connect(database="SAN-KER", user='odoo', password='', host='192.168.2.100', port='5432')
cursor = conn.cursor()
cursor.execute("select id from public.labconnect_test where labno = %s;", (self.labno,))
