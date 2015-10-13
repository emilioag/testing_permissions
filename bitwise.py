import psycopg2
con = psycopg2.connect("""dbname='test2'
                          user='admin'
                          host='localhost'
                          password='admin'""")

cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS perms(
                mask bigint PRIMARY KEY,
                name TEXT,
                example TEXT,
                PRIMARY KEY (mask))""")

cur.execute("""INSERT INTO perms (mask, name, example) VALUES
                (1, 'Crear-Ticket', ''),
                (2, 'Editar-Ticket', ''),
                (4, 'Borrar-Ticket', ''),
                (8, 'Crear-Incidencia', ''),
                (16, 'Editar-Incidencia', ''),
                (32, 'Borrar-Incidencia', ''),
                (64, 'Crear-WorkOrder', ''),
                (128, 'Editar-WorkOrder', '')""")

cur.execute("""CREATE TABLE IF NOT EXISTS users(
  id serial PRIMARY KEY,
  name varchar NOT NULL,
  role bigint NOT NULL
)""")

cur.execute("""INSERT INTO users(name, role)
   VALUES ('emil', '65'),
   ('pepe', '132')""")

cur.execute("""SELECT perms.mask, perms.name
   FROM users LEFT JOIN perms ON users.role & perms.mask > 0
 WHERE users.id = 1""")
