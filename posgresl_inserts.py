import psycopg2
from random import randint
con = psycopg2.connect("""dbname='test1'
                          user='admin'
                          host='localhost'
                          password='admin'""")

cur = con.cursor()
cur.execute("""CREATE TABLE users(
                id SERIAL PRIMARY KEY,
                name TEXT)""")
cur.execute("""CREATE TABLE groups(
                id SERIAL PRIMARY KEY,
                name TEXT)""")
cur.execute("""CREATE TABLE perms(
                id SERIAL PRIMARY KEY,
                name TEXT,
                example TEXT)""")
# table rels

cur.execute("""CREATE TABLE USERS_GROUPS(
            id SERIAL PRIMARY KEY NOT NULL,
            id_user INTEGER,
            id_group INTEGER,
            CONSTRAINT fk_id_user
                FOREIGN KEY (id_user) REFERENCES users (id),
            CONSTRAINT fk_id_group
                FOREIGN KEY (id_group) REFERENCES groups (id))""")

cur.execute("""CREATE TABLE GROUPS_PERMS(
            id SERIAL PRIMARY KEY NOT NULL,
            id_group INTEGER,
            id_perm INTEGER,
            CONSTRAINT fk_id_perm
                FOREIGN KEY (id_perm) REFERENCES perms (id),
            CONSTRAINT fk_id_group
                FOREIGN KEY (id_group) REFERENCES groups (id))
            """)

cur.execute("""CREATE INDEX USERS_GROUPSIndex
                ON USERS_GROUPS (id_user, id_group);""")
cur.execute("""CREATE INDEX GROUPS_PERMSIndex
                ON GROUPS_PERMS (id_group, id_perm);""")
for x in range(10000):
    cur.execute("INSERT INTO perms (name) VALUES (%s)", ("perm_%s" % x,))

for x in range(10000):
    cur.execute("INSERT INTO groups (name) VALUES (%s)", ("group_%s" % x,))

for x in range(1, 10001):
    for y in range(10):
        cur.execute("""INSERT INTO GROUPS_PERMS (id_group, id_perm)
                            VALUES (%s, %s)""", (x, randint(1, 10000)))

for x in range(1000000):
    cur.execute("INSERT INTO users (name) VALUES (%s)", ("user_%s" % x,))
#     for y in range(10):
#         cur.execute("""INSERT INTO USERS_GROUPS (id_user, id_group)
#                             VALUES (%d, %d)""", (x, randint(1, 10000)))

for x in range(1, 1000001):
    for y in range(10):
        cur.execute("""INSERT INTO USERS_GROUPS (id_user, id_group)
                            VALUES (%s, %s)""", (x, randint(1, 10000)))

con.commit()


def get_info_user(_id):
    cur.execute("""SELECT * FROM users
                            JOIN USERS_GROUPS ON
                                USERS_GROUPS.id_user = users.id
                            JOIN groups ON
                                USERS_GROUPS.id_group = groups.id
                            JOIN GROUPS_PERMS ON
                                GROUPS_PERMS.id_group = groups.id
                            JOIN perms ON
                                GROUPS_PERMS.id_perm = perms.id
                            WHERE users.id={0}""".format(_id))
    return cur.fetchall()
