# SQL Validation

Conditions for validation:
- Each table has a primary key
- TO DO: Create\modified date columns have a default value of getdate()
- TO DO: Each primary key that is a unique identifier should have the default value of newid()
- TO DO: Each primary key that is an int needs to have identity specification turned on

## SQL Validation Steps

1.  If schemas are provided
1.1 Validate all tables in the schema
1.2  Validate that all tables have a primary key

2.  Else, if schemas aren't provided and tables are
2.1 Validate that all tables exist
2.2 Validate that all tables have a primary key