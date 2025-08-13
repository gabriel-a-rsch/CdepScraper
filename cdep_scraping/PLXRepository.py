from datetime import datetime

from cdep_scraping import cdepParsing
from cdep_scraping.LegislativeProcedureStageInstance import LegislativeProcedureStageInstance
from cdep_scraping.PLXBasicData import PLXBasicData
from cdep_scraping.PLXFullDataWrapper import PLXFullDataWrapper
import json
import sqlite3
from typing import Optional


class PLXRepository:
    @staticmethod
    def plx_serializer(obj):
        if isinstance(obj,PLXFullDataWrapper):
            return {"basic_data":obj.basicData, "procedural_stages":obj.ProceduralStages } #incomplete serialization TODO: Add complete serialization
        elif isinstance(obj,PLXBasicData):
            return {"plx_number":obj.PLXNumber,
                    "bill_name":obj.BillName,
                    "bpi_number":obj.BPINumber,
                    "senate_number":obj.SenateNumber,
                    "gov_number":obj.GovNumber,
                    "decisional_chamber":obj.DecisionalChamber,
                    "is_emergency_procedure":obj.IsUrgentProcedure,
                    "initiator":obj.Initiator,
                    "character":obj.Character,
                    "initiative_type":obj.InitiativeType,
                    "current_stage":obj.CurrentStage,
                    "legislative_procedure":obj.LegislativeProcedure,
                    }
        elif isinstance(obj,LegislativeProcedureStageInstance):
            return {
                "date":obj.date,
                "identifier":obj.identifier,
                "content":obj.content
            }
        else:
            raise TypeError(f'Cannot serialize object of {type(obj)}')
    def __init__(self, dbPath:str='data.db'):
        self.plxList: list[PLXFullDataWrapper] = []
        self.db_path: str = dbPath  # SQLite3 db path

    def addPLXFromHTMLString(self,htmlString:str):
        myBasicData:PLXBasicData = cdepParsing.plxMainTextToBasicData(htmlString)
        fullWrapperToAdd:PLXFullDataWrapper = PLXFullDataWrapper(myBasicData,[],[])
        self.plxList.append(fullWrapperToAdd)

    def exportToJSONStrFlat(self)->str:
        raise NotImplementedError
    def exportToJSONFileFlat(self)->str:
        raise NotImplementedError
        pass
    def exportToJSONStr(self)->str:
        return json.dumps(self.plxList, default=self.plx_serializer)
        pass
    def exportToJSONFile(self,filePath:str="")->str:
        now = datetime.now()
        currentFilePath=filePath
        if filePath=="":
            currentFilePath="CDEPJSONExport"+now.strftime("%m-%d-%Y-%H-%M-%S")+".json"
        jsonStr:str = self.exportToJSONStr()
        with open(currentFilePath,"w") as f:
            f.write(jsonStr)
    def init_sqlite_db(self) -> None:
        """Initialize SQLite database with proper schema for PLXFullDataWrapper data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Main table for PLXBasicData
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS plx_basic_data
                           (
                               id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               bill_name
                               TEXT
                               NOT
                               NULL,
                               plx_number
                               TEXT
                               NOT
                               NULL
                               UNIQUE,
                               bpi_number
                               TEXT,
                               senate_number
                               TEXT,
                               gov_number
                               TEXT,
                               legislative_procedure
                               TEXT,
                               initiative_type
                               TEXT,
                               character
                               TEXT,
                               current_stage
                               TEXT,
                               initiator
                               TEXT,
                               decisional_chamber
                               TEXT,
                               is_urgent_procedure
                               TEXT,
                               created_at
                               TIMESTAMP
                               DEFAULT
                               CURRENT_TIMESTAMP
                           )
                           ''')

            # Table for PLX Attachments (Consultations)
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS plx_consultations
                           (
                               id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               plx_number
                               TEXT
                               NOT
                               NULL,
                               name
                               TEXT
                               NOT
                               NULL,
                               url_path
                               TEXT
                               NOT
                               NULL,
                               FOREIGN
                               KEY
                           (
                               plx_number
                           ) REFERENCES plx_basic_data
                           (
                               plx_number
                           )
                               ON DELETE CASCADE
                               )
                           ''')

            # Table for Legislative Procedure Stage Instances
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS procedural_stages
                           (
                               id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               plx_number
                               TEXT
                               NOT
                               NULL,
                               stage_date
                               TEXT
                               NOT
                               NULL,
                               content
                               TEXT
                               NOT
                               NULL,
                               stage_order
                               INTEGER,
                               FOREIGN
                               KEY
                           (
                               plx_number
                           ) REFERENCES plx_basic_data
                           (
                               plx_number
                           )
                               ON DELETE CASCADE
                               )
                           ''')

            # Table for Stage Attachments
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS stage_attachments
                           (
                               id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               stage_id
                               INTEGER
                               NOT
                               NULL,
                               name
                               TEXT
                               NOT
                               NULL,
                               url_path
                               TEXT
                               NOT
                               NULL,
                               FOREIGN
                               KEY
                           (
                               stage_id
                           ) REFERENCES procedural_stages
                           (
                               id
                           )
                               ON DELETE CASCADE
                               )
                           ''')

            # Create indexes for better search performance
            self._create_indexes(cursor)

            conn.commit()
            print("Database initialized successfully with all required tables")

        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")
            conn.rollback()
        finally:
            conn.close()

    def _create_indexes(self, cursor: sqlite3.Cursor) -> None:
        """Create indexes for common search operations"""
        indexes = [
            # Basic data indexes
            'CREATE INDEX IF NOT EXISTS idx_plx_number ON plx_basic_data(plx_number)',
            'CREATE INDEX IF NOT EXISTS idx_bill_name ON plx_basic_data(bill_name)',
            'CREATE INDEX IF NOT EXISTS idx_current_stage ON plx_basic_data(current_stage)',
            'CREATE INDEX IF NOT EXISTS idx_initiator ON plx_basic_data(initiator)',
            'CREATE INDEX IF NOT EXISTS idx_initiative_type ON plx_basic_data(initiative_type)',
            'CREATE INDEX IF NOT EXISTS idx_character ON plx_basic_data(character)',
            'CREATE INDEX IF NOT EXISTS idx_created_at ON plx_basic_data(created_at)',

            # Consultation indexes
            'CREATE INDEX IF NOT EXISTS idx_consult_plx_number ON plx_consultations(plx_number)',

            # Procedural stage indexes
            'CREATE INDEX IF NOT EXISTS idx_stage_plx_number ON procedural_stages(plx_number)',
            'CREATE INDEX IF NOT EXISTS idx_stage_date ON procedural_stages(stage_date)',
            'CREATE INDEX IF NOT EXISTS idx_stage_order ON procedural_stages(stage_order)',

            # Stage attachment indexes
            'CREATE INDEX IF NOT EXISTS idx_attachment_stage_id ON stage_attachments(stage_id)'
        ]

        for index_sql in indexes:
            try:
                cursor.execute(index_sql)
            except sqlite3.Error as e:
                print(f"Warning: Could not create index: {e}")

    def check_database_status(self) -> dict:
        """Check if database exists and return table information"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]

            # Get row counts for each table
            table_counts = {}
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                table_counts[table] = cursor.fetchone()[0]

            conn.close()

            return {
                'database_exists': True,
                'tables': tables,
                'table_counts': table_counts
            }

        except sqlite3.Error as e:
            return {
                'database_exists': False,
                'error': str(e)
            }

    def drop_all_tables(self) -> None:
        """Drop all tables - use with caution!"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Drop tables in reverse dependency order
            tables_to_drop = [
                'stage_attachments',
                'procedural_stages',
                'plx_consultations',
                'plx_basic_data'
            ]

            for table in tables_to_drop:
                cursor.execute(f'DROP TABLE IF EXISTS {table}')

            conn.commit()
            print("All tables dropped successfully")

        except sqlite3.Error as e:
            print(f"Error dropping tables: {e}")
            conn.rollback()
        finally:
            conn.close()


# Usage example:
#if __name__ == "__main__":
    # Initialize repository
#    repo = PLXRepository()

    # Check current database status
#    status = repo.check_database_status()
#    print("Database status:", status)

    # Initialize/create database
#    repo.init_sqlite_db()

    # Check status after initialization
#    status = repo.check_database_status()
#    print("Database status after init:", status)