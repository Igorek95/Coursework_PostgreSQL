CREATE TABLE company (
	id_company serial PRIMARY KEY,
	company_name varchar(30)NOT NULL,
	count_vacancy int
)

CREATE TABLE vacancies (
	id_vacancy serial PRIMARY KEY,
	company_id REFERENCES company(id_company) NOT NULL,
	name_job varchar(50) NOT NULL,
	avr_salary int ,
	link_vacancy varchar(30),
	adress varchar(100),

)