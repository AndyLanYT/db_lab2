CREATE TABLE IF NOT EXISTS tbl_students (
    outID VARCHAR (36) PRIMARY KEY,
    birth INT NOT NULL,
    sexTypeName VARCHAR (255) NOT NULL,
    EOName VARCHAR (255),
    FOREIGN KEY (EOName) REFERENCES tbl_educationOrganizations (EOName) ON DELETE CASCADE
);
