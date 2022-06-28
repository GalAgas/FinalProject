import sqlite3
from pathlib import Path
from ddi import SeleniumSearch

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
        """
        connect to database
        """
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
        """
        get the record from database of specific antibiotic
        :param antibiotic_name: string
        :return: list
        """
        sql_query ='''SELECT * FROM Antibiotics WHERE Name=?'''
        info = self.select_from_db(sql_query, antibiotic_name)
        return info

    def get_all_antibiotics(self):
        """
        get the records from database of all antibiotics
        :return: list
        """
        sql_query = '''SELECT * FROM Antibiotics'''
        res = self.select_from_db(sql_query)
        return res
    
    def get_all_DDI(self):
        """
        get the records from database of all DDI
        :return: list
        """
        sql_query = '''SELECT * FROM DDI'''
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
        """
        create 2 tables, antibiotics and DDI.
        """
        anti_query = '''CREATE TABLE Antibiotics(
            ID INTEGER PRIMARY KEY,
            Name VARCHAR(100) Unique Not Null,
            Coverage VARCHAR(20),
            CrclThreshold INTEGER,
            pregnancyCategory VARCHAR(20)
            );'''
            
        ddi_query = '''CREATE TABLE DDI(
            ID INTEGER PRIMARY KEY,
            Antibiotic VARCHAR(100) Not Null,
            Drug VARCHAR(100) Not Null,
            Major INTEGER Not Null,
            Moderate INTEGER Not Null,
            Minor INTEGER Not Null
            );'''
            
        self.cur.execute(anti_query)
        self.commit()
        self.cur.execute(ddi_query)
        self.commit()
        
    def build_db(self):
        """
        main function of class.
        create the database and insert all data into.
        """
        self.create_table_func()
        antibiotics = {
            "ampicillin_sulbactam": ['Broad', -1, 'B'],
            "ceftazidime": ['Narrow', -1, 'B'],
            "ceftriaxone": ['Broad', -1, 'B'],
            "ciprofloxacin": ['Broad', -1, 'C'],
            'imipenem': ['Broad', -1, 'B'],
            "gentamicin": ['Narrow', 30, 'D'],
            "levofloxacin": ['Broad', -1, 'C'],
            "tetracycline": ['Broad', -1, 'D'],
            "tobramycin": ['Narrow', 30, 'D'],
            "trimethoprim_sulfamethoxazole": ['Narrow', -1, 'C']
        }
        sql_query = '''INSERT INTO Antibiotics(Name,Coverage,CrclThreshold,pregnancyCategory)
        VALUES (?,?,?,?)
        '''
        for ab in antibiotics:
            ab_val = antibiotics[ab]
            self.insert_or_update_to_db(sql_query, ab, ab_val[0], ab_val[1], ab_val[2])
        self.commit()
        
        antis = ['ampicillin/sulbactam',
                 'ceftazidime',
                 'ceftriaxone',
                 'ciprofloxacin',
                 'gentamicin',
                 'cilastatin/imipenem',
                 'levofloxacin',
                 'tetracycline',
                 'tobramycin',
                 'sulfamethoxazole/trimethoprim',
                 ]
        
        change = {'ampicillin/sulbactam': 'ampicillin_sulbactam',
                  'cilastatin/imipenem': 'imipenem',
                  'sulfamethoxazole/trimethoprim': 'trimethoprim_sulfamethoxazole'
                  }
        
        p1 = set(['Abilify', 'Ativan', 'Advil', 'Lasix', 'Aspirin'])
        p2 = set(open("server\interactions drugs texts\interacted.txt","r").read().splitlines())
        p3 = set(open("server\interactions drugs texts\common_drugs.txt","r").read().splitlines())
        prev = list(p1.union(p2).union(p3))

        sel = SeleniumSearch()
        interactions = sel.search_drugs(antibiotics=antis, prev_drugs=prev)
        
        for anti, drug in interactions.copy():
            if anti in change:
                interactions[(change[anti], drug)] = interactions.pop((anti, drug))
        
        sql_query = '''INSERT INTO DDI(Antibiotic,Drug,Major,Moderate,Minor)
        VALUES (?,?,?,?,?)
        '''
        for inter in interactions:
            major, moderate, minor = interactions[inter]
            self.insert_or_update_to_db(sql_query, inter[0], inter[1], major, moderate, minor)
        self.commit()
        
        


