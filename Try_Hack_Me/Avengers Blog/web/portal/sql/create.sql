create database avengers;


CREATE TABLE users (
  id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(30) NOT NULL,
  password VARCHAR(30) NOT NULL,
  notes VARCHAR(250),
  reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO users (username, password, notes) VALUES ("spiderman", "w3bs", "Suit needs upgrading");
INSERT INTO users (username, password, notes) VALUES ("thanos", "ihave3stones", "flag4:sanitize_queries_mr_stark");
