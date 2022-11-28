Unsupported Features:
=====================
  Constraints:
  ------------
    NOT NULL [forced on all columns]
    UNIQUE
    PRIMARY KEY
    FOREIGN KEY
    CHECK
    DEFAULT [constructed from type]
  Indexes:
  --------
    CREATE
    DROP
  Increment:
  ----------
    AUTO INCREMENT
    Starting Value
    Increment by X
      ["ROW_ID" starts at and increments by 1 but is not accessible]
  Dates:
  ------
    NOW()
    CURDATE()
    CURTIME()
    EXTRACT()
    DATE_ADD()
    DATE_SUB()
    DATEDIFF()
    DATE_FORMAT()
    GETDATE()
    CONVERT()
      ["DatePart" and "date" are supported and may
       be supplemented with the "datetime" module]
  Nulls:
  ------
    ISNULL()
    NVL()
    IFNULL()
    COALESCE()
      [the NOT NULL constraint is forced on all columns]
  Data Types:
  -----------
    Data types that cannot be initialized with a
    parameterless call are not directly supported.
  Functions:
  ----------
    max() [use "table.max_(column)" instead]
    min() [use "table.min_(column)" instead]
    sum() [use "table.sum_(column)" instead]
    Having Statement
    ucase() or upper() [use "(str.upper, 'column')" instead]
    lcase() or lower() [use "(str.lower, 'column')" instead)
    Virtual Columns [Function Based]
    Materialized Views [Cached Functions]
  Transactions:
  -------------
    Table Level Transactions
      [database level transactions are supported;
       table locks are supported in the same way]