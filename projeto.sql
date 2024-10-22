create database db_projeto;

use db_projeto;

create table tb_usuarios(
usr_id int primary key auto_increment not null,
usr_nome varchar(255),
usr_email text,
usr_senha varchar(255));

create table tb_tarefas(
tar_id int primary key auto_increment not null,
tar_nome varchar(255),
tar_categoria varchar(255),
tar_descricao varchar(255),
tar_data date,
tar_data_limite date,
tar_usr_id int not null,
tar_status varchar(255),
tar_prioridade varchar(255),
foreign key (tar_usr_id) references tb_usuarios(usr_id)); 