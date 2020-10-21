Feature: Step given request headers
    Validates the functionality of the given step "request headers"


    Scenario: Sets the specified headers in the context
        Given request headers
            | header | value |
            | foo    | bar   |
            | baz    | fizz  |
        Then the context contains header foo with value set to bar
        And the context contains header baz with value set to fizz




    Scenario: Resolves request parameter values
        Given request parameters
            | param | value            |
            | id    | ${OBJECT_ID}     |
            | name  | ${RESOURCE_NAME} |
        Then the context contains param id with value set to 3
        And the context contains param name with value set to resolved name




    Scenario: Resolves request parameter names
        Given request parameters
            | param         | value |
            | ${PARAM_ID}   | 13    |
            | ${PARAM_NAME} | greg  |
        Then the context contains param id_number with value set to 13
        And the context contains param first_name with value set to greg