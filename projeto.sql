create database db_projeto;

use db_projeto;

create table tb_usuarios(
usr_id int primary key auto_increment not null,
usr_nome varchar(50),
usr_email text,
usr_senha varchar(50));

create table tb_tarefas(
tar_id int primary key auto_increment not null,
tar_nome varchar(50),
tar_descricao text,
tar_data date,
tar_data_limite date,
tar_usr_id int not null,
tar_status text,
foreign key (tar_usr_id) references tb_usuarios(usr_id));


