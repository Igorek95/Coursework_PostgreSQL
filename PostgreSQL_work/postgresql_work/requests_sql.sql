-- Удаление и создание базы данных
DROP DATABASE IF EXISTS coursework_postgresql;
CREATE DATABASE coursework_postgresql;


-- Создание таблицы "company"
CREATE TABLE company (
   id_company serial PRIMARY KEY,
   company_name varchar(70) NOT NULL,
   count_vacancy int
);

-- Добавление ограничения на уникальность поля "company_name"
ALTER TABLE company
ADD CONSTRAINT company_name_unique UNIQUE (company_name);

-- Создание таблицы "vacancies"
CREATE TABLE vacancies (
   id_vacancy serial PRIMARY KEY,
   name_job varchar(100) NOT NULL,
   avr_salary int,
   link_vacancy varchar(50),
   address varchar(100),
   company_id integer REFERENCES company(id_company) NOT NULL
);

-- Вставка данных в таблицу "company"
INSERT INTO company (company_name, count_vacancy) VALUES ('Company Name', 1) RETURNING id_company;

-- Вставка данных в таблицу "vacancies"
INSERT INTO vacancies (company_id, name_job, avr_salary, link_vacancy, address) VALUES (1, 'Job Name', 50000, 'http://example.com', 'Address');

-- SQL-запрос для получения данных о вакансиях
SELECT company_name, name_job, avr_salary, link_vacancy FROM company INNER JOIN vacancies ON company.id_company = vacancies.company_id;

-- SQL-запрос для получения средней зарплаты по вакансиям
SELECT AVG(avr_salary) FROM vacancies;

-- SQL-запрос для получения вакансий с зарплатой выше средней
SELECT company_name, name_job, avr_salary, link_vacancy FROM vacancies INNER JOIN company ON vacancies.company_id = company.id_company WHERE avr_salary > (SELECT AVG(avr_salary) FROM vacancies);

-- SQL-запрос для получения вакансий с ключевым словом в названии
SELECT company_name, name_job, avr_salary, link_vacancy FROM vacancies INNER JOIN company ON vacancies.company_id = company.id_company WHERE name_job ILIKE '%keyword%';
