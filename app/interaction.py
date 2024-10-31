from .data import ModelResponse, TableLookup, FilterLookup


def query_model(q: str) -> ModelResponse:
    # WIP: Implement the query model function based on AI model response.
    return ModelResponse(
        tables=[
            TableLookup(
                name="table1",
                columns=["field1"],
                filters=[
                    FilterLookup(
                        column="field1",  # must match with columns above
                        operator="=",
                        value="value1",
                    ),
                ],
                relations=["table2"],
            ),
        ]
    )
