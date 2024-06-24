from dataclasses import dataclass
import mysql.connector
from mysql.connector import MySQLConnection
from hubitat_lock_manager.models import CreateKeyCodeParams, UpdateKeyCodeParams, DeleteKeyCodeParams, ReadKeyCodeResult

@dataclass(frozen=True)
class DataStore:
    connection: MySQLConnection

    def create(self, params: CreateKeyCodeParams):
        cursor = self.connection.cursor()
        # SQL logic to create key code
        cursor.close()
        return True

    def read(self, params: ReadKeyCodeParams) -> ReadKeyCodeResult:
        cursor = self.connection.cursor()
        # SQL logic to read key code
        cursor.close()
        return ReadKeyCodeResult(code="1234", name="Test Code")

    def update(self, params: UpdateKeyCodeParams):
        cursor = self.connection.cursor()
        # SQL logic to update key code
        cursor.close()
        return True

    def delete(self, params: DeleteKeyCodeParams):
        cursor = self.connection.cursor()
        # SQL logic to delete key code
        cursor.close()
        return True

    def get_pending_key_codes(self):
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM key_codes WHERE status = 'pending' ORDER BY timestamp"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results

    def is_request_processed(self, request_hash: str) -> bool:
        cursor = self.connection.cursor()
        query = "SELECT COUNT(*) FROM key_code_results WHERE request_hash = %s"
        cursor.execute(query, (request_hash,))
        result = cursor.fetchone()
        cursor.close()
        return result[0] > 0

    def record_key_code_result(self, lock_id: str, code: str, name: str, success: bool, message: str, request_hash: str):
        cursor = self.connection.cursor()
        query = """
            INSERT INTO key_code_results (lock_id, code, name, success, message, request_hash, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
        """
        cursor.execute(query, (lock_id, code, name, success, message, request_hash))
        self.connection.commit()
        cursor.close()
