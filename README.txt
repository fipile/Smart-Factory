Projeto de um sistema de delivery de bebidas chamado Licor Express, com capacidade para registros, logins, 
recuperação de senha e também seguro contra SQL Injection, inicie colocando suas credenciais do seu banco de dados, 
e usando esse trigger criado para integração entre os bancos de dados users e userpj e o allusers


DELIMITER //

-- Trigger para inserir em allUsers após inserção em users
CREATE TRIGGER after_insert_users
AFTER INSERT ON users
FOR EACH ROW
BEGIN
    INSERT INTO allUsers (username, email, userType)
    VALUES (NEW.usernames, NEW.email, NEW.userType);
END//

-- Trigger para inserir em allUsers após inserção em userPJ
CREATE TRIGGER after_insert_userPJ
AFTER INSERT ON userPJ
FOR EACH ROW
BEGIN
    INSERT INTO allUsers (username, email, userType)
    VALUES (NEW.username, NEW.email, NEW.userType);
END//

-- Trigger para deletar de allUsers após deleção em users
CREATE TRIGGER after_delete_users
AFTER DELETE ON users
FOR EACH ROW
BEGIN
    DELETE FROM allUsers 
    WHERE username = OLD.usernames AND userType = OLD.userType;
END//

-- Trigger para deletar de allUsers após deleção em userPJ
CREATE TRIGGER after_delete_userPJ
AFTER DELETE ON userPJ
FOR EACH ROW
BEGIN
    DELETE FROM allUsers 
    WHERE username = OLD.username AND userType = OLD.userType;
END//

DELIMITER ;
