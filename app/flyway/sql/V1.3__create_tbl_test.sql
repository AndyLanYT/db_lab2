CREATE TABLE IF NOT EXISTS tbl_test ( 
    testID SERIAL PRIMARY KEY,
    testName VARCHAR(255),
    testMark100 REAL,
    testMark12 INT,
    testStatus VARCHAR (255),
    EOName VARCHAR (255),
    FOREIGN KEY (EOName) REFERENCES tbl_educationOrganizations (EOName)
);
