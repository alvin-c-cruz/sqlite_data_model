from dataclasses import dataclass, field
from datetime import date

@dataclass
class sqliteDataModel:
	db: any = field(repr=False)
	table_name: str = field(repr=False,default=None)

	def __post_init__(self):
		class_name = str(self.__class__)
		loc = class_name.rfind('.') + 1
		length = len(class_name) - 2
		self.class_name = class_name[class_name.rfind('.') + 1: length].lower()

		if not self.table_name: self.table_name = 'tbl_' + self.class_name 


	def _fields(self):
		_list = []
		def d_type(name, field_type):
			if field_type == int: return 'INTEGER'
			if field_type == float: return 'FLOAT'
			if field_type == str: return 'TEXT'
			if field_type == bool: return 'BOOLEAN'
			if field_type == date: return 'TIMESTAMP'


		data_fields = self.__dataclass_fields__

		for key in data_fields:
			if key[0] != '_': 
				field = data_fields[key]

				name = field.name

				if name in ('db', 'table_name'): continue
				_dict = {'name': name}
				_dict["datatype"] = d_type(name, field.type)
				if field.default == 'primary_key': _dict["primary_key"] = True
				
				_list.append(_dict)

		return _list


	@property
	def create_table(self):
		fields = []
		for field in self._fields():
			name = field.get('name')
			datatype = field.get('datatype')
			primary_key = field.get('primary_key')

			if primary_key:
				fields.append(f'{name} {datatype} PRIMARY KEY')
			else:
				fields.append(f'{name} {datatype}')

		self.db.execute(f'CREATE TABLE {self.table_name} ({", ".join(fields)});')


	@property
	def delete_table(self):
		self.db.execute(f'DROP TABLE IF EXISTS {self.table_name};')


	@property
	def delete(self):
		if self.is_related():
			return f"{self.name} has related information and cannot be deleted."
		else:
			self.db.execute(f'DELETE FROM {self.table_name} WHERE id={self.id};')
			self.db.commit()


	@property
	def save(self):
		if self.id:
			fields = [f'{field["name"]}=?' for field in self.fields()]
			values = [getattr(self, field['name']) for field in self.fields()]

			self.db.execute(f"UPDATE {self.table_name} set {', '.join(fields)} WHERE id={self.id};", values)

		else:
			fields = [field['name'] for field in self.fields() if field['name'] != 'id']
			field_values = ["?" for field in self.fields() if field['name'] != 'id']
			values = []
			for field in self.fields():
				if field['name'] == 'id': continue
				values.append(getattr(self, field['name']))	

			sql = f"INSERT INTO {self.table_name} ({', '.join(fields)}) VALUES ({', '.join(field_values)});"
			self.db.execute(sql, values)
			self.id = self.db.execute("SELECT last_insert_rowid();").fetchone()[0]

		self.db.commit()


	def get(self, **filter): 
		clause = [f'{key}=?' for key in filter]
		record = self.db.execute(f'SELECT * FROM {self.table_name} WHERE {", ".join(clause)};', tuple(filter.values())).fetchone()

		for field in self.fields():
			setattr(self, field['name'], record[field['name']])


	def all(self, **filter):
		if filter:
			clause = [f'{key}=?' for key in filter]
			return self.db.execute(f'SELECT * FROM {self.table_name} WHERE {", ".join(clause)};', tuple(filter.values())).fetchall()
		else:
			return self.db.execute(f'SELECT * FROM {self.table_name};').fetchall()


	def is_related(self):
		return False

