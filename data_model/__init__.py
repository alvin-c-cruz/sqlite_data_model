from dataclasses import dataclass, field

@dataclass
class SimpleModel:
	table_name: str = field(repr=False,default=None)

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
				if field.default == 'primary_key': 
					_dict["primary_key"] = True
				else:
					_dict["default"] = field.default
				
				_list.append(_dict)

		return _list


	def __post_init__(self):
		class_name = str(self.__class__)
		loc = class_name.rfind('.') + 1
		length = len(class_name) - 2
		self.class_name = class_name[class_name.rfind('.') + 1: length].lower()

		if not self.table_name: self.table_name = 'tbl_' + self.class_name 

	@property
	def sql(self):
		return {
			'create': self._create(),
		}

	def _create(self):
		fields = []
		for field in self._fields():
			name = field.get('name')
			datatype = field.get('datatype')
			primary_key = field.get('primary_key')
			default = field.get('default')

			if primary_key:
				fields.append(f'{name} {datatype} PRIMARY KEY')
			else:
				fields.append(f'{name} {datatype}')

		return f'CREATE TABLE {self.table_name} ({", ".join(fields)});'
