-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         12.0.2-MariaDB - mariadb.org binary distribution
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.11.0.7065
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Volcando datos para la tabla bdautogestion.assign_asignationinstructor: ~0 rows (aproximadamente)

-- Volcando datos para la tabla bdautogestion.assign_boss: ~1 rows (aproximadamente)
INSERT INTO `assign_boss` (`id`, `name_boss`, `phone_number`, `email_boss`, `position`, `active`, `delete_at`, `enterprise_id`) VALUES
	(1, 'zxfvdsav', 3102944906, 'vdvfds@empresa.com', 'master', 1, NULL, 1);

-- Volcando datos para la tabla bdautogestion.assign_enterprise: ~1 rows (aproximadamente)
INSERT INTO `assign_enterprise` (`id`, `name_enterprise`, `locate`, `nit_enterprise`, `active`, `email_enterprise`, `delete_at`) VALUES
	(1, 'ewferf', 'sdvdsv sdv', 122112121, 1, 'asdfas@sele.ecd', NULL);

-- Volcando datos para la tabla bdautogestion.assign_humantalent: ~1 rows (aproximadamente)
INSERT INTO `assign_humantalent` (`id`, `name`, `email`, `phone_number`, `active`, `delete_at`, `enterprise_id`) VALUES
	(1, 'dsdcsadvc sadf as asdf', 'sadfsv@osos.com', 3102944906, 1, NULL, 1);

-- Volcando datos para la tabla bdautogestion.assign_modalityproductivestage: ~0 rows (aproximadamente)
INSERT INTO `assign_modalityproductivestage` (`id`, `name_modality`, `description`, `active`, `delete_at`) VALUES
	(1, 'Contrato de aprendizaje', 'El aprendiz desarrolla su etapa practica con contrato de aprendizaje', 1, NULL);

-- Volcando datos para la tabla bdautogestion.assign_requestasignation: ~1 rows (aproximadamente)
INSERT INTO `assign_requestasignation` (`id`, `request_date`, `date_start_production_stage`, `date_end_production_stage`, `pdf_request`, `request_state`, `rejectionMessage`, `delete_at`, `aprendiz_id`, `enterprise_id`, `modality_productive_stage_id`) VALUES
	(1, '2025-09-29', '2025-09-29', '2026-03-31', 'requests/articulo.pdf', 'SIN_ASIGNAR', NULL, NULL, 1, 1, 1);

-- Volcando datos para la tabla bdautogestion.assign_visitfollowing: ~0 rows (aproximadamente)

-- Volcando datos para la tabla bdautogestion.auth_group: ~0 rows (aproximadamente)

-- Volcando datos para la tabla bdautogestion.auth_group_permissions: ~0 rows (aproximadamente)

-- Volcando datos para la tabla bdautogestion.auth_permission: ~88 rows (aproximadamente)
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
	(1, 'Can add log entry', 1, 'add_logentry'),
	(2, 'Can change log entry', 1, 'change_logentry'),
	(3, 'Can delete log entry', 1, 'delete_logentry'),
	(4, 'Can view log entry', 1, 'view_logentry'),
	(5, 'Can add permission', 2, 'add_permission'),
	(6, 'Can change permission', 2, 'change_permission'),
	(7, 'Can delete permission', 2, 'delete_permission'),
	(8, 'Can view permission', 2, 'view_permission'),
	(9, 'Can add group', 3, 'add_group'),
	(10, 'Can change group', 3, 'change_group'),
	(11, 'Can delete group', 3, 'delete_group'),
	(12, 'Can view group', 3, 'view_group'),
	(13, 'Can add content type', 4, 'add_contenttype'),
	(14, 'Can change content type', 4, 'change_contenttype'),
	(15, 'Can delete content type', 4, 'delete_contenttype'),
	(16, 'Can view content type', 4, 'view_contenttype'),
	(17, 'Can add session', 5, 'add_session'),
	(18, 'Can change session', 5, 'change_session'),
	(19, 'Can delete session', 5, 'delete_session'),
	(20, 'Can view session', 5, 'view_session'),
	(21, 'Can add form', 6, 'add_form'),
	(22, 'Can change form', 6, 'change_form'),
	(23, 'Can delete form', 6, 'delete_form'),
	(24, 'Can view form', 6, 'view_form'),
	(25, 'Can add module', 7, 'add_module'),
	(26, 'Can change module', 7, 'change_module'),
	(27, 'Can delete module', 7, 'delete_module'),
	(28, 'Can view module', 7, 'view_module'),
	(29, 'Can add permission', 8, 'add_permission'),
	(30, 'Can change permission', 8, 'change_permission'),
	(31, 'Can delete permission', 8, 'delete_permission'),
	(32, 'Can view permission', 8, 'view_permission'),
	(33, 'Can add person', 9, 'add_person'),
	(34, 'Can change person', 9, 'change_person'),
	(35, 'Can delete person', 9, 'delete_person'),
	(36, 'Can view person', 9, 'view_person'),
	(37, 'Can add role', 10, 'add_role'),
	(38, 'Can change role', 10, 'change_role'),
	(39, 'Can delete role', 10, 'delete_role'),
	(40, 'Can view role', 10, 'view_role'),
	(41, 'Can add form module', 11, 'add_formmodule'),
	(42, 'Can change form module', 11, 'change_formmodule'),
	(43, 'Can delete form module', 11, 'delete_formmodule'),
	(44, 'Can view form module', 11, 'view_formmodule'),
	(45, 'Can add Usuario', 12, 'add_user'),
	(46, 'Can change Usuario', 12, 'change_user'),
	(47, 'Can delete Usuario', 12, 'delete_user'),
	(48, 'Can view Usuario', 12, 'view_user'),
	(49, 'Can add rol form permission', 13, 'add_rolformpermission'),
	(50, 'Can change rol form permission', 13, 'change_rolformpermission'),
	(51, 'Can delete rol form permission', 13, 'delete_rolformpermission'),
	(52, 'Can view rol form permission', 13, 'view_rolformpermission'),
	(53, 'Can add aprendiz', 14, 'add_aprendiz'),
	(54, 'Can change aprendiz', 14, 'change_aprendiz'),
	(55, 'Can delete aprendiz', 14, 'delete_aprendiz'),
	(56, 'Can view aprendiz', 14, 'view_aprendiz'),
	(57, 'Can add center', 15, 'add_center'),
	(58, 'Can change center', 15, 'change_center'),
	(59, 'Can delete center', 15, 'delete_center'),
	(60, 'Can view center', 15, 'view_center'),
	(61, 'Can add ficha', 16, 'add_ficha'),
	(62, 'Can change ficha', 16, 'change_ficha'),
	(63, 'Can delete ficha', 16, 'delete_ficha'),
	(64, 'Can view ficha', 16, 'view_ficha'),
	(65, 'Can add instructor', 17, 'add_instructor'),
	(66, 'Can change instructor', 17, 'change_instructor'),
	(67, 'Can delete instructor', 17, 'delete_instructor'),
	(68, 'Can view instructor', 17, 'view_instructor'),
	(69, 'Can add knowledge area', 18, 'add_knowledgearea'),
	(70, 'Can change knowledge area', 18, 'change_knowledgearea'),
	(71, 'Can delete knowledge area', 18, 'delete_knowledgearea'),
	(72, 'Can view knowledge area', 18, 'view_knowledgearea'),
	(73, 'Can add Person Sede', 19, 'add_personsede'),
	(74, 'Can change Person Sede', 19, 'change_personsede'),
	(75, 'Can delete Person Sede', 19, 'delete_personsede'),
	(76, 'Can view Person Sede', 19, 'view_personsede'),
	(77, 'Can add program', 20, 'add_program'),
	(78, 'Can change program', 20, 'change_program'),
	(79, 'Can delete program', 20, 'delete_program'),
	(80, 'Can view program', 20, 'view_program'),
	(81, 'Can add regional', 21, 'add_regional'),
	(82, 'Can change regional', 21, 'change_regional'),
	(83, 'Can delete regional', 21, 'delete_regional'),
	(84, 'Can view regional', 21, 'view_regional'),
	(85, 'Can add sede', 22, 'add_sede'),
	(86, 'Can change sede', 22, 'change_sede'),
	(87, 'Can delete sede', 22, 'delete_sede'),
	(88, 'Can view sede', 22, 'view_sede');

-- Volcando datos para la tabla bdautogestion.django_admin_log: ~0 rows (aproximadamente)

-- Volcando datos para la tabla bdautogestion.django_content_type: ~22 rows (aproximadamente)
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
	(1, 'admin', 'logentry'),
	(2, 'auth', 'permission'),
	(3, 'auth', 'group'),
	(4, 'contenttypes', 'contenttype'),
	(5, 'sessions', 'session'),
	(6, 'security', 'form'),
	(7, 'security', 'module'),
	(8, 'security', 'permission'),
	(9, 'security', 'person'),
	(10, 'security', 'role'),
	(11, 'security', 'formmodule'),
	(12, 'security', 'user'),
	(13, 'security', 'rolformpermission'),
	(14, 'general', 'aprendiz'),
	(15, 'general', 'center'),
	(16, 'general', 'ficha'),
	(17, 'general', 'instructor'),
	(18, 'general', 'knowledgearea'),
	(19, 'general', 'personsede'),
	(20, 'general', 'program'),
	(21, 'general', 'regional'),
	(22, 'general', 'sede');

-- Volcando datos para la tabla bdautogestion.django_migrations: ~23 rows (aproximadamente)
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
	(1, 'contenttypes', '0001_initial', '2025-09-24 23:52:22.741642'),
	(2, 'contenttypes', '0002_remove_content_type_name', '2025-09-24 23:52:22.799694'),
	(3, 'auth', '0001_initial', '2025-09-24 23:52:23.010963'),
	(4, 'auth', '0002_alter_permission_name_max_length', '2025-09-24 23:52:23.049474'),
	(5, 'auth', '0003_alter_user_email_max_length', '2025-09-24 23:52:23.064584'),
	(6, 'auth', '0004_alter_user_username_opts', '2025-09-24 23:52:23.102569'),
	(7, 'auth', '0005_alter_user_last_login_null', '2025-09-24 23:52:23.124493'),
	(8, 'auth', '0006_require_contenttypes_0002', '2025-09-24 23:52:23.146291'),
	(9, 'auth', '0007_alter_validators_add_error_messages', '2025-09-24 23:52:23.181790'),
	(10, 'auth', '0008_alter_user_username_max_length', '2025-09-24 23:52:23.210421'),
	(11, 'auth', '0009_alter_user_last_name_max_length', '2025-09-24 23:52:23.226116'),
	(12, 'auth', '0010_alter_group_name_max_length', '2025-09-24 23:52:23.315634'),
	(13, 'auth', '0011_update_proxy_permissions', '2025-09-24 23:52:23.338072'),
	(14, 'auth', '0012_alter_user_first_name_max_length', '2025-09-24 23:52:23.351201'),
	(15, 'security', '0001_initial', '2025-09-24 23:52:24.042727'),
	(16, 'admin', '0001_initial', '2025-09-24 23:52:24.235002'),
	(17, 'admin', '0002_logentry_remove_auto_add', '2025-09-24 23:52:24.263915'),
	(18, 'admin', '0003_logentry_add_action_flag_choices', '2025-09-24 23:52:24.361677'),
	(19, 'general', '0001_initial', '2025-09-24 23:52:24.604616'),
	(20, 'assign', '0001_initial', '2025-09-24 23:52:24.749958'),
	(21, 'assign', '0002_initial', '2025-09-24 23:52:25.095555'),
	(22, 'general', '0002_initial', '2025-09-24 23:52:25.615353'),
	(23, 'sessions', '0001_initial', '2025-09-24 23:52:25.668534');

-- Volcando datos para la tabla bdautogestion.django_session: ~0 rows (aproximadamente)

-- Volcando datos para la tabla bdautogestion.general_aprendiz: ~2 rows (aproximadamente)
INSERT INTO `general_aprendiz` (`id`, `active`, `delete_at`, `person_id`, `ficha_id`) VALUES
	(1, 1, NULL, 2, 2),
	(2, 1, NULL, 4, NULL);

-- Volcando datos para la tabla bdautogestion.general_center: ~26 rows (aproximadamente)
INSERT INTO `general_center` (`id`, `name`, `codeCenter`, `address`, `active`, `delete_at`, `regional_id`) VALUES
	(1, 'Centro de Biotecnología Agropecuaria', 1001, 'Calle 166 No. 52-05, Bogotá D.C.', 1, NULL, 1),
	(2, 'Centro de Diseño y Metrología', 1002, 'Calle 52 No. 13-65, Bogotá D.C.', 1, NULL, 1),
	(3, 'Centro de Electricidad y Automatización Industrial', 1003, 'Calle 57 No. 8-69, Bogotá D.C.', 1, NULL, 1),
	(4, 'Centro de Gestión de Mercados, Logística y TIC', 1004, 'Carrera 30 No. 17-52, Bogotá D.C.', 1, NULL, 1),
	(5, 'Centro de Servicios y Gestión Empresarial', 2001, 'Calle 52 No. 48-30, Medellín, Antioquia', 1, NULL, 2),
	(6, 'Centro de Tecnología de la Manufactura Avanzada', 2002, 'Carrera 75 No. 42-169, Medellín, Antioquia', 1, NULL, 2),
	(7, 'Centro Minero', 2003, 'Carrera 80 No. 65-223, Medellín, Antioquia', 1, NULL, 2),
	(8, 'Centro de Gestión Tecnológica de Servicios', 3001, 'Carrera 15 No. 14-50, Cali, Valle del Cauca', 1, NULL, 3),
	(9, 'Centro de Biotecnología Industrial', 3002, 'Carrera 52 No. 2 Bis-15, Cali, Valle del Cauca', 1, NULL, 3),
	(10, 'Centro Agropecuario de Buga', 3003, 'Carrera 18 No. 2-24, Buga, Valle del Cauca', 1, NULL, 3),
	(11, 'Centro Industrial y de Aviación', 4001, 'Carrera 46 No. 85-35, Barranquilla, Atlántico', 1, NULL, 4),
	(12, 'Centro de Comercio y Servicios', 4002, 'Calle 30 No. 15-20, Barranquilla, Atlántico', 1, NULL, 4),
	(13, 'Centro de Tecnologías del Gas y Petróleo', 5001, 'Carrera 21 No. 37-52, Bucaramanga, Santander', 1, NULL, 5),
	(14, 'Centro de Gestión Industrial', 5002, 'Calle 35 No. 8-43, Bucaramanga, Santander', 1, NULL, 5),
	(15, 'Centro Agropecuario y de Biotecnología El Porvenir', 5003, 'Km 13 Vía Rionegro, Rionegro, Santander', 1, NULL, 5),
	(16, 'Centro de Desarrollo Agroempresarial', 6001, 'Calle 8 No. 4-19, Fusagasugá, Cundinamarca', 1, NULL, 6),
	(17, 'Centro de Gestión y Fortalecimiento Socioempresarial', 6002, 'Carrera 7 No. 12-45, Fusagasugá, Cundinamarca', 1, NULL, 6),
	(18, 'Centro de la Industria, la Empresa y los Servicios', 7001, 'Carrera 5 No. 8-45, Neiva, Huila', 1, NULL, 7),
	(19, 'Centro Agropecuario La Granja', 7002, 'Km 7 Vía Neiva-Espinal, Neiva, Huila', 1, NULL, 7),
	(20, 'Centro de Desarrollo Agroindustrial y Empresarial', 7003, 'Carrera 4 No. 8-15, Pitalito, Huila', 1, NULL, 7),
	(21, 'Centro de la Industria Petrolera', 8001, 'Avenida 4 No. 12-52, Cúcuta, Norte de Santander', 1, NULL, 8),
	(22, 'Centro Agropecuario La Granja', 8002, 'Carrera 11 No. 10-45, Ocaña, Norte de Santander', 1, NULL, 8),
	(23, 'Centro Náutico Pesquero', 9001, 'Calle 30 No. 17-25, Cartagena, Bolívar', 1, NULL, 9),
	(24, 'Centro de Industria y Construcción', 9002, 'Zona Industrial Mamonal, Cartagena, Bolívar', 1, NULL, 9),
	(25, 'Centro de la Macarena', 10001, 'Calle 32 No. 28-15, Villavicencio, Meta', 1, NULL, 10),
	(26, 'Centro Agropecuario La Macarena', 10002, 'Carrera 11 No. 15-30, Villavicencio, Meta', 1, NULL, 10);

-- Volcando datos para la tabla bdautogestion.general_ficha: ~2 rows (aproximadamente)
INSERT INTO `general_ficha` (`id`, `file_number`, `active`, `delete_at`, `program_id`) VALUES
	(1, 2901817, 1, NULL, 1),
	(2, 2901885, 1, NULL, 2);

-- Volcando datos para la tabla bdautogestion.general_instructor: ~1 rows (aproximadamente)
INSERT INTO `general_instructor` (`id`, `contractType`, `contractStartDate`, `contractEndDate`, `active`, `delete_at`, `person_id`, `knowledgeArea_id`) VALUES
	(1, 'Planta', '2024-01-15', '2024-12-31', 1, NULL, 3, 1);

-- Volcando datos para la tabla bdautogestion.general_knowledgearea: ~0 rows (aproximadamente)
INSERT INTO `general_knowledgearea` (`id`, `name`, `description`, `active`, `delete_at`) VALUES
	(1, 'Diseño', 'Pertence al area de diseño', 1, NULL);

-- Volcando datos para la tabla bdautogestion.general_personsede: ~1 rows (aproximadamente)
INSERT INTO `general_personsede` (`id`, `DeleteAt`, `PersonId_id`, `SedeId_id`) VALUES
	(1, NULL, 2, 6);

-- Volcando datos para la tabla bdautogestion.general_program: ~2 rows (aproximadamente)
INSERT INTO `general_program` (`id`, `codeProgram`, `name`, `typeProgram`, `description`, `active`, `delete_at`) VALUES
	(1, 1001, 'Análisis y Desarrollo de Software', 'Tecnologo', 'Programa de desarrollo', 1, NULL),
	(2, 1002, 'Diseño Gráfico', 'Tecnico', 'Programa de diseño', 1, NULL);

-- Volcando datos para la tabla bdautogestion.general_regional: ~10 rows (aproximadamente)
INSERT INTO `general_regional` (`id`, `name`, `codeRegional`, `description`, `active`, `address`, `delete_at`) VALUES
	(1, 'Distrito Capital', 1, 'Regional que atiende Bogotá D.C. con formación técnica y tecnológica especializada', 1, 'Calle 57 No. 8-69, Bogotá D.C.', NULL),
	(2, 'Antioquia', 2, 'Regional de Antioquia enfocada en industria, servicios y desarrollo empresarial', 1, 'Calle 52 No. 48-30, Medellín, Antioquia', NULL),
	(3, 'Valle del Cauca', 3, 'Regional del Valle especializada en agroindustria y servicios portuarios', 1, 'Carrera 15 No. 14-50, Cali, Valle del Cauca', NULL),
	(4, 'Atlántico', 4, 'Regional del Atlántico con énfasis en logística portuaria y comercio exterior', 1, 'Carrera 46 No. 85-35, Barranquilla, Atlántico', NULL),
	(5, 'Santander', 5, 'Regional de Santander especializada en petróleo, gas y energías renovables', 1, 'Carrera 21 No. 37-52, Bucaramanga, Santander', NULL),
	(6, 'Cundinamarca', 6, 'Regional de Cundinamarca con programas agropecuarios y turísticos', 1, 'Calle 8 No. 4-19, Fusagasugá, Cundinamarca', NULL),
	(7, 'Huila', 7, 'Regional del Huila con programas en café, turismo y energías renovables', 1, 'Carrera 5 No. 8-45, Neiva, Huila', NULL),
	(8, 'Norte de Santander', 8, 'Regional Norte de Santander con programas fronterizos y comercio internacional', 1, 'Avenida 4 No. 12-52, Cúcuta, Norte de Santander', NULL),
	(9, 'Bolívar', 9, 'Regional de Bolívar con énfasis en turismo, logística y servicios portuarios', 1, 'Calle 30 No. 17-25, Cartagena, Bolívar', NULL),
	(10, 'Meta', 10, 'Regional del Meta enfocada en ganadería, agricultura y petróleo', 1, 'Calle 32 No. 28-15, Villavicencio, Meta', NULL);

-- Volcando datos para la tabla bdautogestion.general_sede: ~51 rows (aproximadamente)
INSERT INTO `general_sede` (`id`, `name`, `codeSede`, `address`, `phoneSede`, `emailContact`, `active`, `delete_at`, `center_id`) VALUES
	(1, 'Sede Principal Biotecnología', 1001001, 'Calle 166 No. 52-05, Bogotá D.C.', '601-5461500', 'biotecnologia@sena.edu.co', 1, NULL, 1),
	(2, 'Sede Ricaurte', 1001002, 'Carrera 13 No. 65-10, Bogotá D.C.', '601-5461501', 'ricaurte@sena.edu.co', 1, NULL, 1),
	(3, 'Sede Principal Diseño', 1002001, 'Calle 52 No. 13-65, Bogotá D.C.', '601-5461500', 'diseno@sena.edu.co', 1, NULL, 2),
	(4, 'Sede Restrepo', 1002002, 'Calle 20 Sur No. 12-30, Bogotá D.C.', '601-5461502', 'restrepo@sena.edu.co', 1, NULL, 2),
	(5, 'Sede Principal Electricidad', 1003001, 'Calle 57 No. 8-69, Bogotá D.C.', '601-5461500', 'electricidad@sena.edu.co', 1, NULL, 3),
	(6, 'Sede Salitre', 1003002, 'Avenida El Dorado No. 68D-51, Bogotá D.C.', '601-5461503', 'salitre@sena.edu.co', 1, NULL, 3),
	(7, 'Sede Principal Mercados', 1004001, 'Carrera 30 No. 17-52, Bogotá D.C.', '601-5461500', 'mercados@sena.edu.co', 1, NULL, 4),
	(8, 'Sede Sur', 1004002, 'Carrera 10 No. 15-20 Sur, Bogotá D.C.', '601-5461504', 'mercados.sur@sena.edu.co', 1, NULL, 4),
	(9, 'Sede Principal Empresarial', 2001001, 'Calle 52 No. 48-30, Medellín, Antioquia', '604-5190600', 'empresarial.medellin@sena.edu.co', 1, NULL, 5),
	(10, 'Sede Itagüí', 2001002, 'Carrera 51 No. 50-20, Itagüí, Antioquia', '604-5190601', 'itagui@sena.edu.co', 1, NULL, 5),
	(11, 'Sede Principal Manufactura', 2002001, 'Carrera 75 No. 42-169, Medellín, Antioquia', '604-5190600', 'manufactura.medellin@sena.edu.co', 1, NULL, 6),
	(12, 'Sede Copacabana', 2002002, 'Carrera 47 No. 70-85, Copacabana, Antioquia', '604-5190602', 'copacabana@sena.edu.co', 1, NULL, 6),
	(13, 'Sede Principal Minero', 2003001, 'Carrera 80 No. 65-223, Medellín, Antioquia', '604-5190600', 'minero.antioquia@sena.edu.co', 1, NULL, 7),
	(14, 'Sede Amalfi', 2003002, 'Calle 12 No. 8-45, Amalfi, Antioquia', '604-5190603', 'amalfi@sena.edu.co', 1, NULL, 7),
	(15, 'Sede Principal Servicios Cali', 3001001, 'Carrera 15 No. 14-50, Cali, Valle del Cauca', '602-4315800', 'servicios.cali@sena.edu.co', 1, NULL, 8),
	(16, 'Sede Norte Cali', 3001002, 'Calle 70 No. 11-50, Cali, Valle del Cauca', '602-4315801', 'norte.cali@sena.edu.co', 1, NULL, 8),
	(17, 'Sede Principal Industrial', 3002001, 'Carrera 52 No. 2 Bis-15, Cali, Valle del Cauca', '602-4315800', 'industrial.cali@sena.edu.co', 1, NULL, 9),
	(18, 'Sede Yumbo', 3002002, 'Carrera 8 No. 15-30, Yumbo, Valle del Cauca', '602-4315802', 'yumbo@sena.edu.co', 1, NULL, 9),
	(19, 'Sede Principal Buga', 3003001, 'Carrera 18 No. 2-24, Buga, Valle del Cauca', '602-4315800', 'buga@sena.edu.co', 1, NULL, 10),
	(20, 'Sede Tuluá', 3003002, 'Calle 26 No. 23-12, Tuluá, Valle del Cauca', '602-4315803', 'tulua@sena.edu.co', 1, NULL, 10),
	(21, 'Sede Principal Aviación', 4001001, 'Carrera 46 No. 85-35, Barranquilla, Atlántico', '605-3304400', 'aviacion.atlantico@sena.edu.co', 1, NULL, 11),
	(22, 'Sede Soledad', 4001002, 'Carrera 21 No. 45-30, Soledad, Atlántico', '605-3304401', 'soledad@sena.edu.co', 1, NULL, 11),
	(23, 'Sede Principal Comercio', 4002001, 'Calle 30 No. 15-20, Barranquilla, Atlántico', '605-3304400', 'comercio.atlantico@sena.edu.co', 1, NULL, 12),
	(24, 'Sede Malambo', 4002002, 'Carrera 12 No. 8-25, Malambo, Atlántico', '605-3304402', 'malambo@sena.edu.co', 1, NULL, 12),
	(25, 'Sede Principal Gas y Petróleo', 5001001, 'Carrera 21 No. 37-52, Bucaramanga, Santander', '607-6910800', 'gas.santander@sena.edu.co', 1, NULL, 13),
	(26, 'Sede Barrancabermeja', 5001002, 'Carrera 28 No. 45-15, Barrancabermeja, Santander', '607-6910801', 'barrancabermeja@sena.edu.co', 1, NULL, 13),
	(27, 'Sede Principal Industrial', 5002001, 'Calle 35 No. 8-43, Bucaramanga, Santander', '607-6910800', 'industrial.santander@sena.edu.co', 1, NULL, 14),
	(28, 'Sede Girón', 5002002, 'Calle 33 No. 25-10, Girón, Santander', '607-6910802', 'giron@sena.edu.co', 1, NULL, 14),
	(29, 'Sede Principal El Porvenir', 5003001, 'Km 13 Vía Rionegro, Rionegro, Santander', '607-6910800', 'elporvenir@sena.edu.co', 1, NULL, 15),
	(30, 'Sede Principal Agroempresarial', 6001001, 'Calle 8 No. 4-19, Fusagasugá, Cundinamarca', '601-8821200', 'agroempresarial.cundinamarca@sena.edu.co', 1, NULL, 16),
	(31, 'Sede Soacha', 6001002, 'Carrera 9 No. 15-21, Soacha, Cundinamarca', '601-8821201', 'soacha@sena.edu.co', 1, NULL, 16),
	(32, 'Sede Principal Socioempresarial', 6002001, 'Carrera 7 No. 12-45, Fusagasugá, Cundinamarca', '601-8821200', 'socioempresarial@sena.edu.co', 1, NULL, 17),
	(33, 'Sede Girardot', 6002002, 'Calle 17 No. 5-22, Girardot, Cundinamarca', '601-8821202', 'girardot@sena.edu.co', 1, NULL, 17),
	(34, 'Sede Principal Neiva', 7001001, 'Carrera 5 No. 8-45, Neiva, Huila', '608-8750400', 'neiva@sena.edu.co', 1, NULL, 18),
	(35, 'Sede Centro', 7001002, 'Calle 12 No. 5-30, Neiva, Huila', '608-8750401', 'neiva.centro@sena.edu.co', 1, NULL, 18),
	(36, 'Sede La Granja', 7002001, 'Km 7 Vía Neiva-Espinal, Neiva, Huila', '608-8750400', 'lagranja.huila@sena.edu.co', 1, NULL, 19),
	(37, 'Sede Campoalegre', 7002002, 'Calle 8 No. 6-15, Campoalegre, Huila', '608-8750402', 'campoalegre@sena.edu.co', 1, NULL, 19),
	(38, 'Sede Principal Pitalito', 7003001, 'Carrera 4 No. 8-15, Pitalito, Huila', '608-8750400', 'pitalito@sena.edu.co', 1, NULL, 20),
	(39, 'Sede Garzón', 7003002, 'Carrera 6 No. 7-45, Garzón, Huila', '608-8750403', 'garzon@sena.edu.co', 1, NULL, 20),
	(40, 'Sede Principal Cúcuta', 8001001, 'Avenida 4 No. 12-52, Cúcuta, Norte de Santander', '607-5820400', 'cucuta@sena.edu.co', 1, NULL, 21),
	(41, 'Sede Villa del Rosario', 8001002, 'Carrera 5 No. 8-20, Villa del Rosario, Norte de Santander', '607-5820401', 'villadelrosario@sena.edu.co', 1, NULL, 21),
	(42, 'Sede Principal Ocaña', 8002001, 'Carrera 11 No. 10-45, Ocaña, Norte de Santander', '607-5820400', 'ocana@sena.edu.co', 1, NULL, 22),
	(43, 'Sede Convención', 8002002, 'Calle 7 No. 9-25, Convención, Norte de Santander', '607-5820402', 'convencion@sena.edu.co', 1, NULL, 22),
	(44, 'Sede Principal Náutico', 9001001, 'Calle 30 No. 17-25, Cartagena, Bolívar', '605-6640600', 'nautico.bolivar@sena.edu.co', 1, NULL, 23),
	(45, 'Sede Bazurto', 9001002, 'Barrio Bazurto, Cartagena, Bolívar', '605-6640601', 'bazurto@sena.edu.co', 1, NULL, 23),
	(46, 'Sede Principal Industrial', 9002001, 'Zona Industrial Mamonal, Cartagena, Bolívar', '605-6640600', 'industrial.bolivar@sena.edu.co', 1, NULL, 24),
	(47, 'Sede Magangué', 9002002, 'Calle 15 No. 8-30, Magangué, Bolívar', '605-6640602', 'magangue@sena.edu.co', 1, NULL, 24),
	(48, 'Sede Principal Villavicencio', 10001001, 'Calle 32 No. 28-15, Villavicencio, Meta', '608-6620400', 'villavicencio@sena.edu.co', 1, NULL, 25),
	(49, 'Sede Kirpas', 10001002, 'Carrera 35 No. 25-40, Villavicencio, Meta', '608-6620401', 'kirpas@sena.edu.co', 1, NULL, 25),
	(50, 'Sede Agropecuario Macarena', 10002001, 'Carrera 11 No. 15-30, Villavicencio, Meta', '608-6620400', 'agropecuario.meta@sena.edu.co', 1, NULL, 26),
	(51, 'Sede Granada', 10002002, 'Carrera 9 No. 10-15, Granada, Meta', '608-6620402', 'granada@sena.edu.co', 1, NULL, 26);

-- Volcando datos para la tabla bdautogestion.security_form: ~9 rows (aproximadamente)
INSERT INTO `security_form` (`id`, `name`, `description`, `path`, `active`, `delete_at`) VALUES
	(1, 'Administración', 'Toda la seccion de control de administración del sistema, del modulo de seguridad', '/admin', 1, NULL),
	(2, 'Registro Masivo', 'Toda la seccion de registro de usuarios masivamente mediante plantillas de excel', '/mass-registration', 1, NULL),
	(3, 'Inicio', 'El inicio del sistema', '/home', 1, NULL),
	(4, 'Solicitud', 'solicitud de aprendiz para asignacion de instructor', '/request-registration', 1, NULL),
	(5, 'Reasignar', 'El coordinador reasigna instructor a algun aprendiz', '/reassign', 1, NULL),
	(6, 'Seguimiento', 'El instructor hace seguimiento a los aprendices en su etapa practica', '/following', 1, NULL),
	(7, 'Historial de seguimiento', 'Historial de todos los seguimientos de todos los aprendices', '/following-history', 1, NULL),
	(8, 'Evaluar visita final', 'El coordinador evalua la visita final que suben los instructores', '/evaluate-final-visit', 1, NULL),
	(9, 'Asignar', 'El coordinaro asigna instructor a aprendiz', '/assign', 1, NULL);

-- Volcando datos para la tabla bdautogestion.security_formmodule: ~10 rows (aproximadamente)
INSERT INTO `security_formmodule` (`id`, `form_id`, `module_id`) VALUES
	(1, 1, 2),
	(2, 2, 2),
	(3, 3, 1),
	(10, 4, 3),
	(11, 6, 3),
	(12, 5, 3),
	(13, 7, 3),
	(14, 8, 3),
	(15, 9, 3),
	(21, 3, 4);

-- Volcando datos para la tabla bdautogestion.security_module: ~4 rows (aproximadamente)
INSERT INTO `security_module` (`id`, `name`, `description`, `active`, `delete_at`) VALUES
	(1, 'Inicio', 'Parte inicial del sistema', 1, NULL),
	(2, 'Seguridad', 'Administra el sistema', 1, NULL),
	(3, 'Asignar seguimientos', 'Todo lo del proceso de asignar un instructor a un aprendiz para el seguimiento de su etapa practica', 1, NULL),
	(4, 'prubeas', 'pruebas', 1, NULL);

-- Volcando datos para la tabla bdautogestion.security_permission: ~5 rows (aproximadamente)
INSERT INTO `security_permission` (`id`, `type_permission`, `description`) VALUES
	(1, 'Ver', 'Visualizar los datos'),
	(2, 'Editar', 'Editar los datos'),
	(3, 'Registrar', 'ingresar datos nuevos'),
	(4, 'Eliminar', 'Eliminar permanentemente datos'),
	(5, 'Activar', 'Activar datos');

-- Volcando datos para la tabla bdautogestion.security_person: ~3 rows (aproximadamente)
INSERT INTO `security_person` (`id`, `first_name`, `second_name`, `first_last_name`, `second_last_name`, `phone_number`, `type_identification`, `number_identification`, `delete_at`, `active`, `image`) VALUES
	(2, 'Brayan', 'Stid', 'Cortes', 'Lombana', 3102944906, 'CC', '1129844804', NULL, 1, ''),
	(3, 'Juan', 'Carlos', 'Pérez', 'Gómez', 3004567890, 'CC', '1023456789', NULL, 1, ''),
	(4, 'María', 'José', 'García', 'López', 3007654321, 'CC', '87654321', NULL, 1, '');

-- Volcando datos para la tabla bdautogestion.security_role: ~5 rows (aproximadamente)
INSERT INTO `security_role` (`id`, `type_role`, `description`, `active`, `delete_at`) VALUES
	(1, 'Administrador', 'Administra y tiene acceso absoluto al sistema', 1, NULL),
	(2, 'Aprendiz', 'Accede a sus secciones permitidas en el sistema', 1, NULL),
	(3, 'Instructor', 'Accede a sus secciones permitidas en el sistema', 1, NULL),
	(4, 'Coordinador', 'El coordinador evalua y sigue los procesos', 1, NULL),
	(5, 'hola', 'cyfdhgd hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh', 1, NULL);

-- Volcando datos para la tabla bdautogestion.security_rolformpermission: ~105 rows (aproximadamente)
INSERT INTO `security_rolformpermission` (`id`, `form_id`, `permission_id`, `role_id`) VALUES
	(16, 3, 1, 2),
	(17, 3, 1, 3),
	(18, 4, 1, 2),
	(19, 4, 4, 2),
	(20, 2, 1, 4),
	(21, 2, 2, 4),
	(22, 2, 3, 4),
	(23, 2, 4, 4),
	(24, 2, 5, 4),
	(25, 3, 1, 4),
	(26, 3, 2, 4),
	(27, 3, 3, 4),
	(28, 3, 4, 4),
	(29, 3, 5, 4),
	(30, 5, 1, 4),
	(31, 5, 2, 4),
	(32, 5, 3, 4),
	(33, 5, 4, 4),
	(34, 5, 5, 4),
	(35, 7, 1, 4),
	(36, 7, 2, 4),
	(37, 7, 3, 4),
	(38, 7, 4, 4),
	(39, 7, 5, 4),
	(40, 8, 1, 4),
	(41, 8, 2, 4),
	(42, 8, 3, 4),
	(43, 8, 4, 4),
	(44, 8, 5, 4),
	(45, 9, 1, 4),
	(46, 9, 2, 4),
	(47, 9, 3, 4),
	(48, 9, 4, 4),
	(49, 9, 5, 4),
	(50, 3, 1, 3),
	(51, 6, 1, 3),
	(52, 6, 2, 3),
	(53, 6, 3, 3),
	(54, 6, 4, 3),
	(55, 6, 5, 3),
	(56, 7, 1, 3),
	(57, 7, 2, 3),
	(58, 7, 3, 3),
	(59, 7, 4, 3),
	(60, 7, 5, 3),
	(156, 1, 1, 1),
	(157, 1, 2, 1),
	(158, 1, 3, 1),
	(159, 1, 4, 1),
	(160, 1, 5, 1),
	(161, 1, 1, 1),
	(162, 1, 2, 1),
	(163, 1, 3, 1),
	(164, 1, 4, 1),
	(165, 1, 5, 1),
	(166, 2, 1, 1),
	(167, 2, 2, 1),
	(168, 2, 3, 1),
	(169, 2, 4, 1),
	(170, 2, 5, 1),
	(171, 2, 1, 1),
	(172, 2, 2, 1),
	(173, 2, 3, 1),
	(174, 2, 4, 1),
	(175, 2, 5, 1),
	(176, 3, 1, 1),
	(177, 3, 2, 1),
	(178, 3, 3, 1),
	(179, 3, 4, 1),
	(180, 3, 5, 1),
	(181, 3, 1, 1),
	(182, 3, 2, 1),
	(183, 3, 3, 1),
	(184, 3, 4, 1),
	(185, 3, 5, 1),
	(186, 4, 1, 1),
	(187, 4, 2, 1),
	(188, 4, 3, 1),
	(189, 4, 4, 1),
	(190, 4, 5, 1),
	(191, 5, 1, 1),
	(192, 5, 2, 1),
	(193, 5, 3, 1),
	(194, 5, 4, 1),
	(195, 5, 5, 1),
	(196, 6, 1, 1),
	(197, 6, 2, 1),
	(198, 6, 3, 1),
	(199, 6, 4, 1),
	(200, 6, 5, 1),
	(201, 7, 1, 1),
	(202, 7, 2, 1),
	(203, 7, 3, 1),
	(204, 7, 4, 1),
	(205, 7, 5, 1),
	(206, 8, 1, 1),
	(207, 8, 2, 1),
	(208, 8, 3, 1),
	(209, 8, 4, 1),
	(210, 8, 5, 1),
	(211, 9, 1, 1),
	(212, 9, 2, 1),
	(213, 9, 3, 1),
	(214, 9, 4, 1),
	(215, 9, 5, 1),
	(221, 3, 1, 5),
	(222, 3, 2, 5),
	(223, 3, 3, 5),
	(224, 3, 4, 5),
	(225, 3, 5, 5);

-- Volcando datos para la tabla bdautogestion.security_user: ~3 rows (aproximadamente)
INSERT INTO `security_user` (`id`, `password`, `last_login`, `is_superuser`, `registered`, `email`, `is_active`, `is_staff`, `deleted_at`, `created_at`, `updated_at`, `reset_code`, `reset_code_expiration`, `person_id`, `role_id`) VALUES
	(1, 'pbkdf2_sha256$1000000$azI6KB5t6LQF3yA8sJtx41$954WnaqmxDAvCmYcSGUkS7qEbT4q0Wd/VdGwyYGrHo8=', NULL, 0, 0, 'bscortes40@soy.sena.edu.co', 1, 0, NULL, '2025-09-24 23:57:53.136568', '2025-09-29 20:17:26.654222', NULL, NULL, 2, 1),
	(2, 'pbkdf2_sha256$1000000$inBLrdQUHtdaxIVUZODkX3$Z85F5UXctexz/tcb2/dsSm6DvPSSk9h8OwW7LAV09Q8=', NULL, 0, 1, 'juan.perez@sena.edu.co', 1, 0, NULL, '2025-09-24 23:59:54.317019', '2025-09-24 23:59:54.317059', NULL, NULL, 3, 3),
	(3, 'pbkdf2_sha256$1000000$ZyK0Dspb25B9z1RO7bSFKN$4pfXuI5+9tPSyqDJyypbioN8tVHEvoVgHvGhFA+dwtY=', NULL, 0, 0, 'maria.garcia@soy.sena.edu.co', 1, 0, NULL, '2025-09-25 00:00:05.660185', '2025-09-25 20:10:30.116149', NULL, NULL, 4, 2);

-- Volcando datos para la tabla bdautogestion.security_user_groups: ~0 rows (aproximadamente)

-- Volcando datos para la tabla bdautogestion.security_user_user_permissions: ~0 rows (aproximadamente)

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
