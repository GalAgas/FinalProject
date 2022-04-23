import sqlite3
from pathlib import Path

class Database:
    """
    this class will be the only one that communicate with our DataBase
    """
    def __init__(self):
        current_path = Path(__file__).parent.absolute()
        self.file_exists = Path(str(current_path)+'\\database.db').exists()
        self.conn = sqlite3.connect(str(current_path)+'\\database.db', check_same_thread=False)
        self.cur = self.conn.cursor()
        if not self.file_exists:  # the file was not exist
            self.build_db()
            
    def commit(self):
        """
        commit all the queries
        :return:
        """
        self.conn.commit()

    def open_connection(self):
        current_path = Path(__file__).parent.absolute()
        self.conn = sqlite3.connect(str(current_path)+'\\database.db', check_same_thread=False)

    def close_connection(self):
        """
        close the connection
        :return:
        """
        self.conn.close()

    def select_from_db(self, sql_query, *params):
        """
        execute the select query
        :param sql_query: string
        :param params: tuple
        :return: list
        """
        if len(params) == 0:  # without params
            self.cur.execute(sql_query)
        else:
            self.cur.execute(sql_query, params)
        return self.cur.fetchall()

    def get_antibiotic_info(self, antibiotic_name):
        sql_query ='''SELECT * FROM Antibiotics WHERE Name=?'''
        info = self.select_from_db(sql_query, antibiotic_name)
        return info

    def get_all_antibiotics(self):
        sql_query = '''SELECT * FROM Antibiotics'''
        res = self.select_from_db(sql_query)
        return res

    def insert_or_update_to_db(self, sql_query, *params):
        """
        execute the insert query or the update query
        :param sql_query: string
        :param params: tuple
        :return:
        """
        self.cur.execute(sql_query, params)

    def create_table_func(self):
        sql_query = '''CREATE TABLE Antibiotics(
            ID INTEGER PRIMARY KEY,
            Name VARCHAR(100) Unique Not Null,
            Coverage VARCHAR(20),
            CrclThreshold INTEGER
            );'''
        self.cur.execute(sql_query)
        self.commit()
        
    def build_db(self):
        self.create_table_func()
        antibiotics = {
            "Amikacin": ['Narrow', -1],
            "Ampicillin": ['Narrow', -1],
            "Ampicillin-sulbactam": ['Broad', -1],
            "Aztreonam": ['Narrow', -1],
            "Cefazolin": ['Narrow', -1],
            "Cefepime": ['Broad', -1],
            "Ceftaxime": ['Broad', -1],
            "Ceftazidime": ['Narrow', -1],
            "Ceftriaxone": ['Broad', -1],
            "Ciprofloxacin": ['Broad', -1],
            "Colistin": ['Narrow', -1],
            "Doripenem": ['Broad', -1],
            "Gentamicin": ['Narrow', 30],
            "Levofloxacin": ['Broad', -1],
            "Meropenem": ['Broad', -1],
            "Minocyclin": ['Broad', -1],
            "Moxifloxacin": ['Broad', -1],
            "Nitrofurantoin": ['Narrow', -1],
            "Pipracillin - tazobactam": ['Broad', -1],
            "Tetracycline": ['Broad', -1],
            "Tobramycin": ['Narrow', 30],
            "TMP - SMX": ['Broad', -1],
        }
        sql_query = '''INSERT INTO Antibiotics(Name,Coverage,CrclThreshold)
        VALUES (?,?,?)
        '''
        for ab in antibiotics:
            ab_val = antibiotics[ab]
            self.insert_or_update_to_db(sql_query, ab, ab_val[0], ab_val[1])
        self.commit()


