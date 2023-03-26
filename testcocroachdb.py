##test cockroachdb



COCKROACHSTR = "dbname='amber-corgi-9722.hackabull2023' user='hackers' password='REDACTED' host='amber-corgi-9722.7tt.cockroachlabs.cloud' port='26257'"



import psycopg2

conn = psycopg2.connect(COCKROACHSTR)

with conn.cursor() as cur:
    cur.execute("SELECT now()")
    res = cur.fetchall()
    conn.commit()
    print(res)
    
    # cur.execute("DROP TABLE READINGS")
    # conn.commit()
    
