import bz2
import contextlib
import sqlite3
from pathlib import Path
from tempfile import TemporaryDirectory


@contextlib.contextmanager
def postcodes():
    with TemporaryDirectory() as dirname:
        yield Postcodes(filename=Path(dirname) / "postcodes.db")


class Postcodes:
    @staticmethod
    def __dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def __init__(self, filename=None):
        zip_filename = Path(__file__).parent / "postcodes.db.bz2"
        if filename is None:
            self.tempdir = TemporaryDirectory()
            filename = self.tempdir.name

        database_file = Path(filename) / "postcodes.db"
        with bz2.open(zip_filename, 'rb') as bz_file:
            with open(database_file, 'wb') as output_file:
                while True:
                    data = bz_file.read(1024)
                    if not data:
                        break
                    output_file.write(data)

        self.conn = sqlite3.connect(database_file)
        self.conn.row_factory = self.__dict_factory

    def get_postcode(self, pc, *args, fields=None):
        if args:
            postcodes = [pc, *args]
        else:
            postcodes = [pc]

        cur = self.conn.cursor()
        cur.execute("SELECT * FROM postcode WHERE pcd IN (%s)" %
                    ','.join('?'*len(postcodes)), postcodes)

        rows = cur.fetchall()
        for row in rows:
            yield row
