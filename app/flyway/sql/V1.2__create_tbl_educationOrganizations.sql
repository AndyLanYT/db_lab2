CREATE TABLE IF NOT EXISTS tbl_educationOrganizations (
    EOName VARCHAR (255) PRIMARY KEY,
    EOTypeName VARCHAR (255),
    EORegName VARCHAR (255),
    EOTerName VARCHAR (255),
    FOREIGN KEY (EORegName, EOTerName) REFERENCES tbl_regions (regName, terName) ON DELETE CASCADE
);
