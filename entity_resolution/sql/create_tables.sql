CREATE TABLE IF NOT EXISTS grants (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  application_id VARCHAR(20) NOT NULL,
  start_at DATE,
  grant_type VARCHAR(10),
  total_cost INTEGER
);

CREATE TABLE IF NOT EXISTS grantees (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  surname VARCHAR(250) NOT NULL,
  forename VARCHAR(250),
  initials VARCHAR(10),
  affiliation VARCHAR(250),
  application_id VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS articles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pmid VARCHAR(20) NOT NULL,
  title VARCHAR(250) NOT NULL
);

CREATE TABLE IF NOT EXISTS authors (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  surname VARCHAR(250) NOT NULL,
  forename VARCHAR(250),
  initials VARCHAR(10),
  affiliation VARCHAR(250),
  pmid VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS grantees_authors (
  grantee_id INTEGER NOT NULL,
  author_id INTEGER NOT NULL,
  FOREIGN KEY (grantee_id) REFERENCES grantees (id),
  FOREIGN KEY (author_id) REFERENCES authors (id)
);