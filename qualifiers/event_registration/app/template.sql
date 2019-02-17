DROP TABLE users;
CREATE TABLE users (id INT AUTO_INCREMENT, name VARCHAR(55), username VARCHAR(55) UNIQUE, password VARCHAR(55), PRIMARY KEY (id));
INSERT INTO users (name, username, password) VALUES ('root', 'root', '{{env:ADMIN_PASSWORD}}');
