CREATE SCHEMA `mydbScrap` DEFAULT CHARACTER SET utf8;
USE `mydbScrap`;


create table `mydbScrap`.`Casa` (   
  `id` int auto_increment not null, /* select * from Casa use sys; drop database mydbScrap */
  `imagen` varchar(200), 
  `titulo` varchar(150), 
  `precio` varchar(20),
  `tipo` varchar(40),
  `venta` varchar(40),
  `externas` varchar(500),
  `superficie` varchar(40),
  `tamano` varchar(20),
  `camas` int,
  `banos` int,
  `mascotas` varchar(55),
  `fechaConstruccion` varchar(50),
  `ubicacion` varchar(700),
  `tipoEdificio` varchar(50),
  `visto` int,
  `fechaVisto` varchar(25), 
	primary key (`id`))
ENGINE = InnoDB; 
