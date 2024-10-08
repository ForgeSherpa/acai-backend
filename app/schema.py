from .data import Tables, TableDefinition, Column


class Schema:
    table_data = Tables(
        tables=[
            TableDefinition(
                name="lecturers",
                columns=[
                    Column(name="id", type="int"),
                    Column(name="nidn", type="int"),
                    Column(name="name", type="str"),
                ],
                relations=["researches"],
            ),
            TableDefinition(
                name="lecturer_researches",
                columns=[
                    Column(name="id", type="int"),
                    Column(name="nidn", type="int"),
                    Column(name="title", type="str"),
                    Column(name="publication_date", type="date"),
                    Column(name="publication_type", type="str"),
                    Column(name="publication_detail", type="str"),
                ],
                relations=["lecturer"],
            ),
            TableDefinition(
                name="students",
                columns=[
                    Column(name="id", type="int"),
                    Column(name="name", type="str"),
                    Column(name="faculty", type="str"),
                    Column(name="generation", type="int"),
                    Column(name="gpa", type="float"),
                    Column(name="status", type="str"),
                    Column(name="graduation_year", type="int"),
                    Column(name="graduation_semester", type="int"),
                ],
                relations=["activities"],
            ),
            TableDefinition(
                name="student_activities",
                columns=[
                    Column(name="id", type="int"),
                    Column(name="student_id", type="int"),
                    Column(name="bank_id", type="int"),
                    Column(name="name", type="str"),
                    Column(name="type", type="str"),
                    Column(name="date", type="date"),
                ],
                relations=["student"],
            ),
        ]
    )

    def tables(self):
        return [table.name for table in self.table_data.tables]

    def columns(self, table_name):
        for table in self.table_data.tables:
            if table.name == table_name:
                return table.columns

    def columns_name(self, table_name):
        return [column.name for column in self.columns(table_name)]

    def relations(self, table_name):
        for table in self.table_data.tables:
            if table.name == table_name:
                return table.relations
            
    