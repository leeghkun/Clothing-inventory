import sqlite3

def create_db():
    con=sqlite3.connect(database=r'ims.db')
    cur=con.cursor()
    
    # Employee table
    cur.execute("""CREATE TABLE IF NOT EXISTS employee(
        eid TEXT PRIMARY KEY,
        name text,
        email text,
        gender text,
        contact text,
        dob text,
        pass text,
        utype text,
        address text,
        salary text
    )""")
    con.commit()
    
    # Other tables remain the same
    cur.execute("CREATE TABLE IF NOT EXISTS supplier(invoice INTEGER PRIMARY KEY AUTOINCREMENT,name text,contact text,desc text)")
    con.commit()
    
    cur.execute("CREATE TABLE IF NOT EXISTS category(cid INTEGER PRIMARY KEY AUTOINCREMENT,name text)")
    con.commit()
    
    cur.execute("""CREATE TABLE IF NOT EXISTS product(
        pid INTEGER PRIMARY KEY AUTOINCREMENT,
        Category text,
        Supplier text,
        name text,
        size text,
        color text,
        season text,
        collection text,
        price text,
        qty text,
        status text,
        reorder_level integer
    )""")
    con.commit()

    # Create attendance table
    cur.execute("""CREATE TABLE IF NOT EXISTS attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id text,
        date text,
        time_in text,
        time_out text,
        hours_worked real,
        status text
    )""")
    con.commit()

    # Add test admin user if not exists
    cur.execute("SELECT * FROM employee WHERE eid='E001'")
    if not cur.fetchone():
        cur.execute("""INSERT INTO employee (eid, name, email, pass, utype) 
                      VALUES ('E001', 'Admin', 'admin@test.com', 'admin123', 'Admin')""")
        con.commit()

create_db()