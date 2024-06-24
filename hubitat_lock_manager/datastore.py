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
