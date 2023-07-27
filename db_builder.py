import sqlite3 as sql

db = './data/biocycle_tracking.db'


def create_database_file(db_name: str = db) -> None:
    """
    Creates an empty database file with the given name.
    :param db_name: name of the database file
    :return: None
    """
    try:
        conn = sql.connect(db_name)
        conn.close()
    except sql.Error as e:
        print(e)

    return None


def get_db_connection(db_name: str = db) -> sql.connect:
    conn = None
    try:
        conn = sql.connect(db_name)
    except sql.Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sql.Error as e:
        print(e)


def create_schema(db_path: str = db) -> None:
    con = get_db_connection(db_path)

    sessions_table = '''
        CREATE TABLE IF NOT EXISTS sessions (
            note TEXT,
            n_experiments INTEGER,
            responsible TEXT,
            start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_date TIMESTAMP,
            session_id TEXT PRIMARY KEY,
            UNIQUE (session_id));
        '''
    create_table(con, sessions_table)

    containers_table = '''
        CREATE TABLE IF NOT EXISTS containers (
            material_type TEXT,
            container_id TEXT PRIMARY KEY,
            company TEXT,
            location TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            note TEXT,
            UNIQUE (container_id));
        '''
    create_table(con, containers_table)

    experiments_table = '''
        CREATE TABLE IF NOT EXISTS experiments (
            experiment_id TEXT PRIMARY KEY,
            container_id TEXT,
            n_objects INTEGER,
            session_id TEXT, 
            file_path TEXT,
            FOREIGN KEY(session_id) REFERENCES sessions(session_id),
            FOREIGN KEY(container_id) REFERENCES containers(container_id),
            UNIQUE (experiment_id));
            '''
    create_table(con, experiments_table)

    objects_table = '''
        CREATE TABLE IF NOT EXISTS objects (
            object_id TEXT PRIMARY KEY, 
            polymer_type TEXT,
            length REAL,
            texture TEXT,
            stiffness REAL,
            color TEXT,
            contamination TEXT,
            form TEXT,
            note TEXT,
            reference_image TEXT,
            UNIQUE (object_id));
            '''
    create_table(con, objects_table)

    experiments_table = '''
        CREATE TABLE IF NOT EXISTS experiment_objects (
            experiment_id TEXT, 
            object_id TEXT, 
            PRIMARY KEY (experiment_id, object_id), 
            FOREIGN KEY(experiment_id) REFERENCES experiments(experiment_id), 
            FOREIGN KEY(object_id) REFERENCES objects(object_id),
            UNIQUE (experiment_id, object_id));
            '''
    create_table(con, experiments_table)
    return None


def get_next_experiment_id(db_path: str = db) -> str:
    con = get_db_connection(db_path)
    query = '''
        SELECT experiment_id FROM experiments ORDER BY experiment_id DESC LIMIT 1;
        '''
    result = con.execute(query).fetchone()
    con.close()

    if result is None:
        return 'E0000'
    else:
        return f'E{int(result[0][1:]) + 1:04}'


def get_next_session_id(db_path: str = db) -> str:
    con = get_db_connection(db_path)
    query = '''
        SELECT session_id FROM sessions ORDER BY session_id DESC LIMIT 1;
        '''
    result = con.execute(query).fetchone()
    con.close()

    if result is None:
        return 'S0000'
    else:
        return f'S{int(result[0][1:]) + 1:04}'


if __name__ == '__main__':
    create_database_file()
    create_schema()
