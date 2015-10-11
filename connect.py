import psycopg2

try:
    conn = psycopg2.connect(
            "dbname='test1' user='admin' host='localhost' password='admin'")
except:
    print "No conecta!!!!"
cur = conn.cursor()
try:
    cur.execute("""SELECT * FROM user""")
except:
    print "No se puede hacer SELECT"
