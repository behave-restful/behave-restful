Feature: Step given request parameters
    Validates the functionality of the given step "request parameters"


    Scenario: Sets the specified parameters in the context
        Given request parameters
            | param | value |
            | foo   | bar   |
            | baz   | fizz  |
        Then the context contains param foo with value set to bar
            And the context contains param baz with value set to fizz




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