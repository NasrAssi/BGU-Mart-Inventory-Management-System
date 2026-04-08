import inspect

_ALLOWED_TABLES = {'employees', 'suppliers', 'products', 'branches', 'activities'}


def _validate_table(name):
    if name not in _ALLOWED_TABLES:
        raise ValueError(f"Invalid table name: {name!r}")


def orm(cursor, dto_type):
    args = list(inspect.signature(dto_type.__init__).parameters.keys())[1:]
    col_names = [column[0] for column in cursor.description]
    col_mapping = [col_names.index(arg) for arg in args]
    return [row_map(row, col_mapping, dto_type) for row in cursor.fetchall()]


def row_map(row, col_mapping, dto_type):
    ctor_args = [row[idx] for idx in col_mapping]
    return dto_type(*ctor_args)


class Dao(object):
    def __init__(self, dto_type, conn):
        self._conn = conn
        self._dto_type = dto_type

        if hasattr(dto_type, '_table_name'):
            self._table_name = dto_type._table_name
        else:
            self._table_name = dto_type.__name__.lower() + 's'

        _validate_table(self._table_name)

        # Build the set of valid column names from the DTO constructor parameters
        self._columns = set(
            list(inspect.signature(dto_type.__init__).parameters.keys())[1:]
        )

    def _validate_columns(self, column_names):
        for col in column_names:
            if col not in self._columns:
                raise ValueError(f"Invalid column name: {col!r} for table {self._table_name!r}")

    def insert(self, dto_instance):
        ins_dict = vars(dto_instance)
        column_names = ','.join(ins_dict.keys())
        params = list(ins_dict.values())
        qmarks = ','.join(['?'] * len(ins_dict))
        stmt = 'INSERT INTO {} ({}) VALUES ({})'.format(self._table_name, column_names, qmarks)
        self._conn.execute(stmt, params)

    def find_all(self):
        c = self._conn.cursor()
        c.execute('SELECT * FROM {}'.format(self._table_name))
        return orm(c, self._dto_type)

    def find(self, **keyvals):
        if not keyvals:
            return self.find_all()
        column_names = list(keyvals.keys())
        self._validate_columns(column_names)
        params = list(keyvals.values())
        stmt = 'SELECT * FROM {} WHERE {}'.format(
            self._table_name,
            ' AND '.join([col + '=?' for col in column_names])
        )
        c = self._conn.cursor()
        c.execute(stmt, params)
        return orm(c, self._dto_type)

    def delete(self, **keyvals):
        if not keyvals:
            raise ValueError("delete() requires at least one filter condition")
        column_names = list(keyvals.keys())
        self._validate_columns(column_names)
        params = list(keyvals.values())
        stmt = 'DELETE FROM {} WHERE {}'.format(
            self._table_name,
            ' AND '.join([col + '=?' for col in column_names])
        )
        self._conn.cursor().execute(stmt, params)
