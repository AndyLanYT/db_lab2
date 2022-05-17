CREATE TABLE IF NOT EXISTS tbl_educationOrganizations (
    EOName VARCHAR (255) PRIMARY KEY,
    EOTypeName VARCHAR (255),
    EORegName VARCHAR (255),
    EOAreaName VARCHAR (255),
    FOREIGN KEY (EORegName, EOAreaName) REFERENCES tbl_regions (regName, areaName) ON DELETE CASCADE
);
