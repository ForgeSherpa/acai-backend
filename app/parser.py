from .data import ModelResponse

class Parser:
    def __init__(self, query: ModelResponse):
        self.query = query

    def parse(self):
        for table in self.query.tables:
            pass
            # match table.name:
                # case 'lecturers':
