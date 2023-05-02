from typing import List

import pandas as pd
import db_builder

db = './data/biocycle_tracking.db'


# Session queries
def put_session(session_id: str = None,
                n_experiments: int = None,
                note: str = None,
                responsible: str = None,
                start_date: str = None,
                end_date: str = None,
                db_path: str = db) -> None:
    """
    Add a session to the database. If no session_id is given, a new one is created.
    :param session_id: str (optional), if not given, a new one is created
    :param n_experiments: int (optional), number of planned experiments in the session
    :param note: str (optional), note about the session
    :param responsible: str (optional), name of the person responsible for the session
    :param start_date: str (optional), start date of the session
    :param end_date: str (optional), end date of the session
    :param db_path: str (optional), name of the database
    :return: None
    """
    con = db_builder.get_db_connection(db_path)
    if session_id is None:
        session_id = db_builder.get_next_session_id(db_path)

    query = f'''
        INSERT INTO sessions (session_id, note, n_experiments, responsible, start_date, end_date) 
        VALUES ('{session_id}', '{note}', {n_experiments}, '{responsible}', '{start_date}', '{end_date}');
        '''
    con.execute(query)
    con.commit()
    con.close()
    return None


def put_multiple_sessions(sessions: pd.DataFrame, db_path: str = db) -> None:
    """
    Add multiple sessions to the database.
    :param sessions: pd.DataFrame, columns: session_id, n_experiments, note, responsible, start_date, end_date
    :param db_path: str (optional), name of the database
    :return: None
    """
    assert sessions.columns.tolist() == ['session_id', 'n_experiments', 'note', 'responsible', 'start_date', 'end_date']

    query = f'''
        INSERT INTO sessions (session_id, note, n_experiments, responsible, start_date, end_date)
        VALUES (?, ?, ?, ?, ?, ?);
        '''

    con = db_builder.get_db_connection(db_path)
    con.executemany(query, sessions.values.tolist())
    con.commit()
    con.close()

    return None


# Object queries
def put_object(object_id: str,
               polymer_type: str = None,
               length: float = None,
               texture: str = None,
               stiffness: str = None,
               color: str = None,
               contamination: str = None,
               form: str = None,
               note: str = None,
               reference_image: bool = None,
               db_path: str = db) -> None:
    """
    Add an object to the database.
    :param object_id: str, unique identifier of the object
    :param polymer_type: str (optional), polymer type of the object
    :param length: float (optional), length of the object
    :param texture: str (optional), texture of the object
    :param stiffness: str (optional), stiffness of the object
    :param color: str (optional), color of the object
    :param contamination: str (optional), level contamination of the object
    :param form: str (optional), class of the object
    :param note: str (optional), note about the object
    :param reference_image: bool (optional), whether the object has a reference image or not
    :param db_path: str (optional), name of the database
    :return: None
    """
    con = db_builder.get_db_connection(db_path)

    con.execute(
        f'''
        INSERT INTO objects (object_id, polymer_type, length, texture, stiffness, 
        color, contamination, form, note, reference_image)
        VALUES ('{object_id}', '{polymer_type}', {length}, '{texture}', '{stiffness}', '{color}', '{contamination}', 
        '{form}', '{note}', {reference_image});
        ''')

    con.commit()
    con.close()
    return None


def put_multiple_objects(objects: pd.DataFrame, db_path: str = db) -> None:
    """
    Add multiple objects to the database.
    :param objects: pd.DataFrame, columns: object_id, polymer_type, length, texture, stiffness, color, contamination,
    form, note, reference_image
    :param db_path: str (optional), name of the database
    :return: None
    """
    assert objects.columns.tolist() == ['object_id', 'polymer_type', 'length', 'texture', 'stiffness', 'color',
                                        'contamination', 'form', 'note', 'reference_image']

    query = f'''
        INSERT INTO objects (object_id, polymer_type, length, texture, stiffness,
        color, contamination, form, note, reference_image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        '''

    con = db_builder.get_db_connection(db_path)
    con.executemany(query, objects.values.tolist())
    con.commit()
    con.close()

    return None


# Container queries
def put_container(container_id: str, material_type: str = None, company: str = None, location: str = None,
                  note: str = None, date: str = None, db_path: str = db) -> None:
    """
    Add a container to the database.
    :param container_id: str, unique identifier of the container
    :param material_type: str (optional), material type of the container, either compost or digestive
    :param company: str (optional), company that owns the container
    :param location: str (optional), location of the container
    :param note: str (optional), note about the container
    :param date: str (optional), date of collection
    :param db_path: str (optional), name of the database
    :return: None
    """
    con = db_builder.get_db_connection(db_path)

    con.execute(
        f'''
        INSERT INTO containers (container_id, material_type, company, location, note, date)
        VALUES ('{container_id}', '{material_type}', '{company}', '{location}', '{note}', '{date}');
        ''')

    con.commit()
    con.close()
    return None


def put_multiple_containers(containers: pd.DataFrame, db_path: str = db) -> None:
    """
    Add multiple containers to the database.
    :param containers: pd.DataFrame, columns: container_id, material_type, company, location, note, date
    :param db_path: str (optional), name of the database
    :return: None
    """
    assert containers.columns.tolist() == ['container_id', 'material_type', 'company', 'location', 'note', 'date']

    query = f'''
        INSERT INTO containers (container_id, material_type, company, location, note, date)
        VALUES (?, ?, ?, ?, ?, ?);
        '''

    con = db_builder.get_db_connection(db_path)
    con.executemany(query, containers.values.tolist())
    con.commit()
    con.close()

    return None


# Experiment queries
def put_experiment(experiment_id: str = None,
                   session_id: str = None,
                   container_id: str = None,
                   n_objects: int = None,
                   db_path: str = db) -> None:
    """
    Add an experiment to the database. If no experiment_id is given, a new one is created.
    Note that this does not connect an experiment to the necessary objects.
    :param experiment_id: str (optional), if not given, a new one is created
    :param session_id: str (optional), session_id of the session the experiment belongs to
    :param container_id: str (optional), container_id of the container the experiment belongs to
    :param n_objects: int (optional), number of objects in the experiment
    :param db_path: str (optional), name of the database
    :return: None
    """
    con = db_builder.get_db_connection(db_path)
    if experiment_id is None:
        experiment_id = db_builder.get_next_experiment_id(db_path)

    con.execute(
        f'''
        INSERT INTO experiments (experiment_id, session_id, container_id, n_objects) 
        VALUES ('{experiment_id.strip()}', '{session_id.strip()}', '{container_id.strip()}', {n_objects});
        ''')

    con.commit()
    con.close()
    return None


def put_multiple_experiments(experiments: pd.DataFrame, db_path: str = db) -> None:
    """
    Add multiple experiments to the database.
    :param experiments: pd.DataFrame, columns: experiment_id, session_id, container_id, n_objects
    :param db_path: str (optional), name of the database
    :return: None
    """
    assert experiments.columns.tolist() == ['session_id', 'experiment_id', 'container_id', 'n_objects']

    query = f'''
        INSERT INTO experiments (session_id, experiment_id, container_id, n_objects)
        VALUES (?, ?, ?, ?);
        '''

    con = db_builder.get_db_connection(db_path)
    con.executemany(query, experiments.values.tolist())
    con.commit()
    con.close()

    return None


def link_experiment_objects(experiment_id: str, objects: List[str], db_path: str = db) -> None:
    """
    Link a list of object_ids to an experiment
    :param experiment_id: str, experiment_id of the experiment
    :param objects: List[str], list of object_ids
    :param db_path: str (optional), name of the database
    :return: None
    """

    query = f'''
            INSERT INTO experiment_objects (experiment_id, object_id)
            VALUES (?, ?);            
            '''

    con = db_builder.get_db_connection(db_path)
    con.executemany(query, [(experiment_id, object_id) for object_id in objects])
    con.commit()
    con.close()

    return None


# Fetch queries
def get_complete_session(session_id: str, db_path: str = db) -> List[tuple]:
    """
    Return all experiments to a session. Returns a list in the form
        [(session_id, experiment_id, container_id, [object_list]), ...]
    :param session_id: str, session_id of the session
    :param db_path: str (optional), name of the database
    :return: list, [(session_id, experiment_id, container_id, [object_list]), ...]
    """
    con = db_builder.get_db_connection(db_path)
    query = f'''
        SELECT sessions.session_id, 
                experiments.experiment_id, 
                experiments.container_id, 
                GROUP_CONCAT(experiment_objects.object_id) AS object_list
            FROM sessions
        JOIN experiments ON sessions.session_id = experiments.session_id
        JOIN experiment_objects ON experiments.experiment_id = experiment_objects.experiment_id
            WHERE sessions.session_id = '{session_id}'
            GROUP BY experiments.experiment_id;
        '''
    full_session = con.execute(query).fetchall()
    con.close()

    return full_session


def get_complete_experiment(experiment_id: str, db_path: str = db) -> dict:
    """
    Return all objects to an experiment. Returns a dictionary in the form {experiment_id: {object_id: {}}}
    :param experiment_id: str, experiment_id of the experiment
    :param db_path: str (optional), name of the database
    :return: dict, {experiment_id: {object_id: {}}}
    """
    con = db_builder.get_db_connection(db_path)
    query = f'''
        SELECT experiments.experiment_id, experiments.container_id, GROUP_CONCAT(experiment_objects.object_id) AS object_list
            FROM experiments
        JOIN experiment_objects ON experiments.experiment_id = experiment_objects.experiment_id
            WHERE experiments.experiment_id = '{experiment_id}'
           GROUP BY experiments.experiment_id;
        '''
    full_experiment = con.execute(query).fetchall()
    con.close()

    return full_experiment


def get_object(object_id: str, db_path: str = db) -> dict:
    """Return all information about an object. Returns a dictionary in the form {object_id: {}}"""
    con = db_builder.get_db_connection(db_path)
    query = f'''
        SELECT * FROM objects
            WHERE object_id = '{object_id}';
        '''
    full_object_description = con.execute(query).fetchall()
    con.close()

    return full_object_description


def get_container(container_id: str, db_path: str = db) -> dict:
    """Return all information about a container. Returns a dictionary in the form {container_id: {}}"""
    con = db_builder.get_db_connection(db_path)
    query = f'''
        SELECT * FROM containers
            WHERE container_id = '{container_id}';
        '''
    container_description = con.execute(query).fetchall()
    con.close()

    return container_description


def get_session(session_id: str, db_name: str = db) -> dict:
    """Return all information about a session. Returns a dictionary in the form {session_id: {}}"""
    con = db_builder.get_db_connection(db_name)
    query = f'''
        SELECT * FROM sessions
            WHERE session_id = '{session_id}';
        '''
    session_description = con.execute(query).fetchall()
    con.close()

    return session_description


def get_experiment(experiment_id: str, db_path: str = db) -> dict:
    """Return all information about an experiment. Returns a dictionary in the form {experiment_id: {}}"""
    con = db_builder.get_db_connection(db_path)
    query = f'''
        SELECT * FROM experiments
            WHERE experiment_id = '{experiment_id}';
        '''
    experiment_description = con.execute(query).fetchall()
    con.close()

    return experiment_description


def run_query(query: str, db_path: str = db):
    """
    Run an arbitrary query on the database
    :param query: str, a query in SQLite Format
    :param db_path: path to the database
    :return: result of the query
    """
    con = db_builder.get_db_connection(db_path)
    query_result = pd.read_sql_query(query, con)
    con.close()

    return query_result


if __name__ == '__main__':
    result = get_complete_session('S0000')
