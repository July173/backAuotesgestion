USE `bdautogestion`;

INSERT INTO `support_contact` (`id`, `type`, `label`, `value`, `extra_info`, `active`, `delete_at`) VALUES
  (1, 'Email', 'Soporte por correo electrónico', 'servicio@sena.edu.co', 'Respuesta en 24-48 horas', 1, NULL),
  (2, 'Teléfono', 'Línea gratuita nacional', '01 8000 910 270', 'Lunes a viernes: 7:00 AM - 7:00 PM', 1, NULL),
  (3, 'Enlaces útiles', 'Sofia Plus - Oferta Educativa', 'https://betowa.sena.edu.co/', 'enlace', 1, NULL);

INSERT INTO `support_schedule` (`id`, `day_range`, `hours`, `is_closed`, `notes`, `active`, `delete_at`) VALUES
  (1, 'Lunes a Viernes', '7:00 AM - 7:00 PM', 0, NULL, 1, NULL),
  (2, 'Sábados', '8:00 AM - 4:00 PM', 0, NULL, 1, NULL),
  (3, 'Domingos y festivos', 'Ninguna', 1, NULL, 1, NULL);

INSERT INTO `type_contract` (`id`, `name`, `description`, `active`, `delete_at`) VALUES
  (1, 'Planta', 'Contrato estable y permanente, con todos los beneficios de ley.', 1, NULL),
  (2, 'Contrato', 'Acuerdo laboral que puede ser por tiempo definido o indefinido.', 1, NULL),
  (3, 'OPS', 'Orden de Prestación de Servicios. Sin relación laboral.', 1, NULL),
  (4, 'Provisional', 'Vinculación temporal mientras se realiza selección definitiva.', 1, NULL),
  (5, 'Temporal', 'Vinculación por periodo limitado para necesidad específica.', 1, NULL),
  (6, 'Prestación de Servicios', 'Contrato civil/comercial por actividad determinada.', 1, NULL);

INSERT INTO `type_of_queries` (`id`, `name`, `description`, `active`, `delete_at`) VALUES
  (1, 'Soporte Técnico', 'Para consultas técnicas del sistema', 1, NULL),
  (2, 'Consulta Académica', 'Para consultas académicas del sistema', 1, NULL),
  (3, 'Problemas con la plataforma', 'Para consulta sobre problemas con el sistema', 1, NULL),
  (4, 'Otros', 'Para consulta sobre el sistema', 1, NULL);

INSERT INTO `document_type` (`id`, `name`, `acronyms`, `active`, `delete_at`) VALUES
  (1, 'Cédula de Ciudadanía', 'CC', 1, NULL),
  (2, 'Tarjeta de Identidad', 'TI', 1, NULL),
  (3, 'Cédula de Extranjería', 'CE', 1, NULL),
  (4, 'Pasaporte', 'PASSPORT', 1, NULL),
  (5, 'Número ciego - SENA', 'NUMERO_CIEGO_SENA', 1, NULL),
  (6, 'Documento Nacional de Identificación', 'DNI', 1, NULL),
  (7, 'Número de Identificación Tributaria', 'NIT', 1, NULL),
  (8, 'Permiso por Protección Temporal', 'PERMISO_TEMPORAL', 1, NULL);

INSERT INTO `knowledge_area` (`id`, `name`, `description`, `active`, `delete_at`) VALUES
  (1, 'Diseño', 'Pertenece al área de diseño', 1, NULL);

INSERT INTO `regional` (`id`, `name`, `code_regional`, `description`, `address`, `active`, `delete_at`) VALUES
(1, 'Distrito Capital', '001', 'Regional que atiende Bogotá D.C. con formación técnica y tecnológica especializada', 'Calle 57 No. 8-69, Bogotá D.C.', true, NULL),
(2, 'Antioquia', '002', 'Regional de Antioquia enfocada en industria, servicios y desarrollo empresarial', 'Calle 52 No. 48-30, Medellín, Antioquia', true, NULL),
(3, 'Valle del Cauca', '003', 'Regional del Valle especializada en agroindustria y servicios portuarios', 'Carrera 15 No. 14-50, Cali, Valle del Cauca', true, NULL),
(4, 'Atlántico', '004', 'Regional del Atlántico con énfasis en logística portuaria y comercio exterior', 'Carrera 46 No. 85-35, Barranquilla, Atlántico', true, NULL),
(5, 'Santander', '005', 'Regional de Santander especializada en petróleo, gas y energías renovables', 'Carrera 21 No. 37-52, Bucaramanga, Santander', true, NULL),
(6, 'Cundinamarca', '006', 'Regional de Cundinamarca con programas agropecuarios y turísticos', 'Calle 8 No. 4-19, Fusagasugá, Cundinamarca', true, NULL),
(7, 'Huila', '007', 'Regional del Huila con programas en café, turismo y energías renovables', 'Carrera 5 No. 8-45, Neiva, Huila', true, NULL),
(8, 'Norte de Santander', '008', 'Regional Norte de Santander con programas fronterizos y comercio internacional', 'Avenida 4 No. 12-52, Cúcuta, Norte de Santander', true, NULL),
(9, 'Bolívar', '009', 'Regional de Bolívar con énfasis en turismo, logística y servicios portuarios', 'Calle 30 No. 17-25, Cartagena, Bolívar', true, NULL),
(10, 'Meta', '010', 'Regional del Meta enfocada en ganadería, agricultura y petróleo', 'Calle 32 No. 28-15, Villavicencio, Meta', true, NULL);

INSERT INTO `center` (`id`, `name`, `code_center`, `address`, `active`, `delete_at`, `regional_id`) VALUES
(1, 'Centro de Biotecnología Agropecuaria', '001001', 'Calle 166 No. 52-05, Bogotá D.C.', true, NULL, 1),
(2, 'Centro de Diseño y Metrología', '001002', 'Calle 52 No. 13-65, Bogotá D.C.', true, NULL, 1),
(3, 'Centro de Electricidad y Automatización Industrial', '001003', 'Calle 57 No. 8-69, Bogotá D.C.', true, NULL, 1),
(4, 'Centro de Gestión de Mercados, Logística y TIC', '001004', 'Carrera 30 No. 17-52, Bogotá D.C.', true, NULL, 1),
(5, 'Centro de Servicios y Gestión Empresarial', '002001', 'Calle 52 No. 48-30, Medellín, Antioquia', true, NULL, 2),
(6, 'Centro de Tecnología de la Manufactura Avanzada', '002002', 'Carrera 75 No. 42-169, Medellín, Antioquia', true, NULL, 2),
(7, 'Centro Minero', '002003', 'Carrera 80 No. 65-223, Medellín, Antioquia', true, NULL, 2),
(8, 'Centro de Gestión Tecnológica de Servicios', '003001', 'Carrera 15 No. 14-50, Cali, Valle del Cauca', true, NULL, 3),
(9, 'Centro de Biotecnología Industrial', '003002', 'Carrera 52 No. 2 Bis-15, Cali, Valle del Cauca', true, NULL, 3),
(10, 'Centro Agropecuario de Buga', '003003', 'Carrera 18 No. 2-24, Buga, Valle del Cauca', true, NULL, 3),
(11, 'Centro Industrial y de Aviación', '004001', 'Carrera 46 No. 85-35, Barranquilla, Atlántico', true, NULL, 4),
(12, 'Centro de Comercio y Servicios', '004002', 'Calle 30 No. 15-20, Barranquilla, Atlántico', true, NULL, 4),
(13, 'Centro de Tecnologías del Gas y Petróleo', '005001', 'Carrera 21 No. 37-52, Bucaramanga, Santander', true, NULL, 5),
(14, 'Centro de Gestión Industrial', '005002', 'Calle 35 No. 8-43, Bucaramanga, Santander', true, NULL, 5),
(15, 'Centro Agropecuario y de Biotecnología El Porvenir', '005003', 'Km 13 Vía Rionegro, Rionegro, Santander', true, NULL, 5),
(16, 'Centro de Desarrollo Agroempresarial', '006001', 'Calle 8 No. 4-19, Fusagasugá, Cundinamarca', true, NULL, 6),
(17, 'Centro de Gestión y Fortalecimiento Socioempresarial', '006002', 'Carrera 7 No. 12-45, Fusagasugá, Cundinamarca', true, NULL, 6),
(18, 'Centro de la Industria, la Empresa y los Servicios', '007001', 'Carrera 5 No. 8-45, Neiva, Huila', true, NULL, 7),
(19, 'Centro Agropecuario La Granja', '007002', 'Km 7 Vía Neiva-Espinal, Neiva, Huila', true, NULL, 7),
(20, 'Centro de Desarrollo Agroindustrial y Empresarial', '007003', 'Carrera 4 No. 8-15, Pitalito, Huila', true, NULL, 7),
(21, 'Centro de la Industria Petrolera', '008001', 'Avenida 4 No. 12-52, Cúcuta, Norte de Santander', true, NULL, 8),
(22, 'Centro Agropecuario La Granja', '008002', 'Carrera 11 No. 10-45, Ocaña, Norte de Santander', true, NULL, 8),
(23, 'Centro Náutico Pesquero', '009001', 'Calle 30 No. 17-25, Cartagena, Bolívar', true, NULL, 9),
(24, 'Centro de Industria y Construcción', '009002', 'Zona Industrial Mamonal, Cartagena, Bolívar', true, NULL, 9),
(25, 'Centro de la Macarena', '010001', 'Calle 32 No. 28-15, Villavicencio, Meta', true, NULL, 10),
(26, 'Centro Agropecuario La Macarena', '010002', 'Carrera 11 No. 15-30, Villavicencio, Meta', true, NULL, 10);

INSERT INTO `sede` (`id`, `name`, `code_sede`, `address`, `phone_sede`, `email_contact`, `active`, `delete_at`, `center_id`) VALUES
(1, 'Sede Principal Biotecnología', '001001001', 'Calle 166 No. 52-05, Bogotá D.C.', '6015461500', 'biotecnologia@sena.edu.co', true, NULL, 1),
(2, 'Sede Ricaurte', '001001002', 'Carrera 13 No. 65-10, Bogotá D.C.', '6015461501', 'ricaurte@sena.edu.co', true, NULL, 1),
(3, 'Sede Principal Diseño', '001002001', 'Calle 52 No. 13-65, Bogotá D.C.', '6015461500', 'diseno@sena.edu.co', true, NULL, 2),
(4, 'Sede Restrepo', '001002002', 'Calle 20 Sur No. 12-30, Bogotá D.C.', '6015461502', 'restrepo@sena.edu.co', true, NULL, 2),
(5, 'Sede Principal Electricidad', '001003001', 'Calle 57 No. 8-69, Bogotá D.C.', '6015461500', 'electricidad@sena.edu.co', true, NULL, 3),
(6, 'Sede Salitre', '001003002', 'Avenida El Dorado No. 68D-51, Bogotá D.C.', '6015461503', 'salitre@sena.edu.co', true, NULL, 3),
(7, 'Sede Principal Mercados', '001004001', 'Carrera 30 No. 17-52, Bogotá D.C.', '6015461500', 'mercados@sena.edu.co', true, NULL, 4),
(8, 'Sede Sur', '001004002', 'Carrera 10 No. 15-20 Sur, Bogotá D.C.', '6015461504', 'mercados.sur@sena.edu.co', true, NULL, 4),
(9, 'Sede Principal Empresarial', '002001001', 'Calle 52 No. 48-30, Medellín, Antioquia', '6045190600', 'empresarial.medellin@sena.edu.co', true, NULL, 5),
(10, 'Sede Itagüí', '002001002', 'Carrera 51 No. 50-20, Itagüí, Antioquia', '6045190601', 'itagui@sena.edu.co', true, NULL, 5),
(11, 'Sede Principal Manufactura', '002002001', 'Carrera 75 No. 42-169, Medellín, Antioquia', '6045190600', 'manufactura.medellin@sena.edu.co', true, NULL, 6),
(12, 'Sede Copacabana', '002002002', 'Carrera 47 No. 70-85, Copacabana, Antioquia', '6045190602', 'copacabana@sena.edu.co', true, NULL, 6),
(13, 'Sede Principal Minero', '002003001', 'Carrera 80 No. 65-223, Medellín, Antioquia', '6045190600', 'minero.antioquia@sena.edu.co', true, NULL, 7),
(14, 'Sede Amalfi', '002003002', 'Calle 12 No. 8-45, Amalfi, Antioquia', '6045190603', 'amalfi@sena.edu.co', true, NULL, 7),
(15, 'Sede Principal Servicios Cali', '003001001', 'Carrera 15 No. 14-50, Cali, Valle del Cauca', '6024315800', 'servicios.cali@sena.edu.co', true, NULL, 8),
(16, 'Sede Norte Cali', '003001002', 'Calle 70 No. 11-50, Cali, Valle del Cauca', '6024315801', 'norte.cali@sena.edu.co', true, NULL, 8),
(17, 'Sede Principal Industrial', '003002001', 'Carrera 52 No. 2 Bis-15, Cali, Valle del Cauca', '6024315800', 'industrial.cali@sena.edu.co', true, NULL, 9),
(18, 'Sede Yumbo', '003002002', 'Carrera 8 No. 15-30, Yumbo, Valle del Cauca', '6024315802', 'yumbo@sena.edu.co', true, NULL, 9),
(19, 'Sede Principal Buga', '003003001', 'Carrera 18 No. 2-24, Buga, Valle del Cauca', '6024315800', 'buga@sena.edu.co', true, NULL, 10),
(20, 'Sede Tuluá', '003003002', 'Calle 26 No. 23-12, Tuluá, Valle del Cauca', '6024315803', 'tulua@sena.edu.co', true, NULL, 10),
(21, 'Sede Principal Aviación', '004001001', 'Carrera 46 No. 85-35, Barranquilla, Atlántico', '6053304400', 'aviacion.atlantico@sena.edu.co', true, NULL, 11),
(22, 'Sede Soledad', '004001002', 'Carrera 21 No. 45-30, Soledad, Atlántico', '6053304401', 'soledad@sena.edu.co', true, NULL, 11),
(23, 'Sede Principal Comercio', '004002001', 'Calle 30 No. 15-20, Barranquilla, Atlántico', '6053304400', 'comercio.atlantico@sena.edu.co', true, NULL, 12),
(24, 'Sede Malambo', '004002002', 'Carrera 12 No. 8-25, Malambo, Atlántico', '6053304402', 'malambo@sena.edu.co', true, NULL, 12),
(25, 'Sede Principal Gas y Petróleo', '005001001', 'Carrera 21 No. 37-52, Bucaramanga, Santander', '6076910800', 'gas.santander@sena.edu.co', true, NULL, 13),
(26, 'Sede Barrancabermeja', '005001002', 'Carrera 28 No. 45-15, Barrancabermeja, Santander', '6076910801', 'barrancabermeja@sena.edu.co', true, NULL, 13),
(27, 'Sede Principal Industrial', '005002001', 'Calle 35 No. 8-43, Bucaramanga, Santander', '6076910800', 'industrial.santander@sena.edu.co', true, NULL, 14),
(28, 'Sede Girón', '005002002', 'Calle 33 No. 25-10, Girón, Santander', '6076910802', 'giron@sena.edu.co', true, NULL, 14),
(29, 'Sede Principal El Porvenir', '005003001', 'Km 13 Vía Rionegro, Rionegro, Santander', '6076910800', 'elporvenir@sena.edu.co', true, NULL, 15),
(30, 'Sede Principal Agroempresarial', '006001001', 'Calle 8 No. 4-19, Fusagasugá, Cundinamarca', '6018821200', 'agroempresarial.cundinamarca@sena.edu.co', true, NULL, 16),
(31, 'Sede Soacha', '006001002', 'Carrera 9 No. 15-21, Soacha, Cundinamarca', '6018821201', 'soacha@sena.edu.co', true, NULL, 16),
(32, 'Sede Principal Socioempresarial', '006002001', 'Carrera 7 No. 12-45, Fusagasugá, Cundinamarca', '6018821200', 'socioempresarial@sena.edu.co', true, NULL, 17),
(33, 'Sede Girardot', '006002002', 'Calle 17 No. 5-22, Girardot, Cundinamarca', '6018821202', 'girardot@sena.edu.co', true, NULL, 17),
(34, 'Sede Principal Neiva', '007001001', 'Carrera 5 No. 8-45, Neiva, Huila', '6088750400', 'neiva@sena.edu.co', true, NULL, 18),
(35, 'Sede Centro', '007001002', 'Calle 12 No. 5-30, Neiva, Huila', '6088750401', 'neiva.centro@sena.edu.co', true, NULL, 18),
(36, 'Sede La Granja', '007002001', 'Km 7 Vía Neiva-Espinal, Neiva, Huila', '6088750400', 'lagranja.huila@sena.edu.co', true, NULL, 19),
(37, 'Sede Campoalegre', '007002002', 'Calle 8 No. 6-15, Campoalegre, Huila', '6088750402', 'campoalegre@sena.edu.co', true, NULL, 19),
(38, 'Sede Principal Pitalito', '007003001', 'Carrera 4 No. 8-15, Pitalito, Huila', '6088750400', 'pitalito@sena.edu.co', true, NULL, 20),
(39, 'Sede Garzón', '007003002', 'Carrera 6 No. 7-45, Garzón, Huila', '6088750403', 'garzon@sena.edu.co', true, NULL, 20),
(40, 'Sede Principal Cúcuta', '008001001', 'Avenida 4 No. 12-52, Cúcuta, Norte de Santander', '6075820400', 'cucuta@sena.edu.co', true, NULL, 21),
(41, 'Sede Villa del Rosario', '008001002', 'Carrera 5 No. 8-20, Villa del Rosario, Norte de Santander', '6075820401', 'villadelrosario@sena.edu.co', true, NULL, 21),
(42, 'Sede Principal Ocaña', '008002001', 'Carrera 11 No. 10-45, Ocaña, Norte de Santander', '6075820400', 'ocana@sena.edu.co', true, NULL, 22),
(43, 'Sede Convención', '008002002', 'Calle 7 No. 9-25, Convención, Norte de Santander', '6075820402', 'convencion@sena.edu.co', true, NULL, 22),
(44, 'Sede Principal Náutico', '009001001', 'Calle 30 No. 17-25, Cartagena, Bolívar', '6056640600', 'nautico.bolivar@sena.edu.co', true, NULL, 23),
(45, 'Sede Bazurto', '009001002', 'Barrio Bazurto, Cartagena, Bolívar', '6056640601', 'bazurto@sena.edu.co', true, NULL, 23),
(46, 'Sede Principal Industrial', '009002001', 'Zona Industrial Mamonal, Cartagena, Bolívar', '6056640600', 'industrial.bolivar@sena.edu.co', true, NULL, 24),
(47, 'Sede Magangué', '009002002', 'Calle 15 No. 8-30, Magangué, Bolívar', '6056640602', 'magangue@sena.edu.co', true, NULL, 24),
(48, 'Sede Principal Villavicencio', '010001001', 'Calle 32 No. 28-15, Villavicencio, Meta', '6086620400', 'villavicencio@sena.edu.co', true, NULL, 25),
(49, 'Sede Kirpas', '010001002', 'Carrera 35 No. 25-40, Villavicencio, Meta', '6086620401', 'kirpas@sena.edu.co', true, NULL, 25),
(50, 'Sede Agropecuario Macarena', '010002001', 'Carrera 11 No. 15-30, Villavicencio, Meta', '6086620400', 'agropecuario.meta@sena.edu.co', true, NULL, 26),
(51, 'Sede Granada', '010002002', 'Carrera 9 No. 10-15, Granada, Meta', '6086620402', 'granada@sena.edu.co', true, NULL, 26);

INSERT INTO `program` (`id`, `name`, `code_program`, `description`, `active`, `delete_at`) VALUES
  (1, 'Análisis y Desarrollo de Software', 1001, 'Programa de desarrollo', 1, NULL),
  (2, 'Diseño Gráfico', 1002, 'Programa de diseño', 1, NULL);

INSERT INTO `ficha` (`id`, `file_number`, `type_modality`, `active`, `delete_at`, `program_id`) VALUES
  (1, 2901817, 'Presencial', 1, NULL, 1),
  (2, 2901885, 'Virtual', 1, NULL, 2);

INSERT INTO `modality_productive_stage` (`id`, `name_modality`, `description`, `active`, `delete_at`) VALUES
  (1, 'Contrato de aprendizaje', 'El aprendiz desarrolla su etapa práctica con contrato de aprendizaje', 1, NULL),
  (2, 'Vínculo Laboral', 'El aprendiz desarrolla su etapa práctica con vinculo laboral', 1, NULL),
  (3, 'Vínculo Formativo', 'El aprendiz desarrolla su etapa práctica con vinculo formativo', 1, NULL),
  (4, 'Proyecto Productivo', 'El aprendiz desarrolla su etapa práctica con proyecto productivo', 1, NULL),
  (5, 'Unidad Productiva Familiar', 'El aprendiz desarrolla su etapa práctica con unidad productiva familiar', 1, NULL),
  (6, 'Monitoria', 'El aprendiz desarrolla su etapa práctica con monitoria', 1, NULL);

INSERT INTO `legal_document` (`id`, `type`, `title`, `effective_date`, `last_update`, `active`, `delete_at`) VALUES
  (1, 'terms', 'Términos y condiciones', '2025-10-01', '2025-10-01', 1, NULL);

INSERT INTO `legal_section` (`id`, `order`, `code`, `title`, `content`, `active`, `delete_at`, `document_id`, `parent_id`) VALUES
  (1, 1, '1', 'Aceptación de los términos', 'Al acceder y utilizar los servicios del SENA (Servicio Nacional de Aprendizaje), usted acepta estar sujeto a estos términos y condiciones de uso. Si no está de acuerdo con alguno de estos términos, no debe utilizar nuestros servicios. El SENA se reserva el derecho de modificar estos términos en cualquier momento. Las modificaciones entrarán en vigor inmediatamente después de su publicación en este sitio web.', 1, NULL, 1, NULL),
  (2, 2, '2', 'Descripción de los servicios', 'El SENA ofrece formación profesional integral gratuita en los siguientes servicios:\n - Programas de formación técnica y tecnológica\n - Cursos complementarios virtuales y presenciales\n - Servicios de empleabilidad y emprendimiento\n - Plataformas educativas digitales (Sofia Plus, LMS SENA)\n - Servicios de bienestar al aprendiz\n - Certificación de competencias laborales', 1, NULL, 1, NULL),
  (3, 3, '3', 'Obligaciones del usuario', NULL, 1, NULL, 1, NULL),
  (4, 4, '4', 'Derechos de propiedad intelectual', 'Todo el contenido disponible en las plataformas del SENA, incluyendo pero no limitado a textos, gráficos, logotipos, iconos, imágenes, clips de audio, descargas digitales y compilaciones de datos, es propiedad del SENA o de sus proveedores de contenido y está protegido por las leyes de derechos de autor de Colombia e internacionales. Los usuarios pueden utilizar el contenido únicamente para fines educativos personales y no comerciales, respetando siempre los créditos correspondientes.', 1, NULL, 1, NULL),
  (5, 5, '5', 'Protección de datos personales', 'El SENA se compromete a proteger la privacidad de los usuarios conforme a la Ley 1581 de 2012 y el Decreto 1377 de 2013 sobre Protección de Datos Personales en Colombia. Para más información sobre cómo recopilamos, utilizamos y protegemos sus datos personales, consulte nuestra Política de Privacidad.', 1, NULL, 1, NULL),
  (6, 6, '6', 'Limitación de responsabilidad', 'El SENA no será responsable por daños directos, indirectos, incidentales, especiales o consecuenciales que resulten del uso o la imposibilidad de uso de nuestros servicios. Nos esforzamos por mantener la disponibilidad continua de nuestros servicios, pero no garantizamos que estén libres de interrupciones, errores o virus.', 1, NULL, 1, NULL),
  (7, 7, '7', 'Terminación del servicio', 'El SENA se reserva el derecho de suspender o terminar el acceso a sus servicios a cualquier usuario que viole estos términos y condiciones, sin previo aviso. Los usuarios pueden solicitar la terminación de su cuenta en cualquier momento contactando a nuestro servicio de soporte.', 1, NULL, 1, NULL),
  (8, 8, '8', 'Ley Aplicable y jurisdicción', 'Estos términos y condiciones se rigen por las leyes de la República de Colombia. Cualquier disputa que surja en relación con estos términos será sometida a la jurisdicción exclusiva de los tribunales competentes de Bogotá D.C., Colombia.', 1, NULL, 1, NULL),
  (9, 1, '3.1', 'Requisitos de registro', '- Proporcionar información verdadera, precisa y completa\n - Mantener actualizada su información personal\n - Ser responsables de la confidencialidad de sus credenciales\n - Cumplir con los requisitos académicos establecidos', 1, NULL, 1, 3),
  (10, 2, '3.2', 'Conducta del usuario', '- Respetar las normas de convivencia institucional\n - No utilizar los servicios para fines ilegales o no autorizados\n - Mantener un comportamiento ético y profesional\n - Respetar los derechos de propiedad intelectual\n - No compartir contenido inapropiado o ofensivo', 1, NULL, 1, 3);

INSERT INTO `legal_document` (`id`, `type`, `title`, `effective_date`, `last_update`, `active`, `delete_at`) VALUES
  (2, 'privacy', 'Política de privacidad', '2025-10-01', '2025-10-01', 1, NULL);

INSERT INTO `legal_section` (`id`, `order`, `code`, `title`, `content`, `active`, `delete_at`, `document_id`, `parent_id`) VALUES
  (11, 1, '1', 'Información que recopilamos', NULL, 1, NULL, 2, NULL),
  (12, 1, '1.1', 'Información personal', 'Nombres y apellidos completos\nNúmero de identificación\nFecha de nacimiento\nDirección de residencia\nCorreo electrónico\nNúmero de teléfono\nInformación académica y profesional\nEstado socioeconómico (cuando aplique)', 1, NULL, 2, 11),
  (13, 2, '1.2', 'Información técnica', 'Dirección IP\nTipo de navegador y versión\nSistema operativo\nPáginas visitadas y tiempo de permanencia\nCookies y tecnologías similares', 1, NULL, 2, 11),
  (14, 2, '2', 'Uso de la información', NULL, 1, NULL, 2, NULL),
  (15, 1, '2.1', 'Servicios educativos', 'Gestión de inscripciones y matrículas\nSeguimiento académico y evaluación\nEmisión de certificados y títulos\nComunicación sobre programas y cursos', 1, NULL, 2, 14),
  (16, 2, '2.2', 'Servicios administrativos', 'Verificación de identidad\nGestión de pagos (cuando aplique)\nSoporte técnico y atención al usuario\nCumplimiento de obligaciones legales', 1, NULL, 2, 14),
  (17, 3, '2.3', 'Mejora de servicios', 'Análisis estadístico y de rendimiento\nPersonalización de la experiencia educativa\nDesarrollo de nuevos programas formativos\nInvestigación educativa institucional', 1, NULL, 2, 14),
  (18, 3, '3', 'Protección de datos', NULL, 1, NULL, 2, NULL),
  (19, 1, '3.1', 'Medidas técnicas', 'Cifrado de datos en tránsito y en reposo\nFirewalls y sistemas de detección de intrusiones\nCopias de seguridad regulares\nActualizaciones de seguridad constantes\nControl de acceso basado en roles', 1, NULL, 2, 18),
  (20, 2, '3.2', 'Medidas organizativas', 'Políticas internas de manejo de datos\nCapacitación del personal en protección de datos\nProcedimientos de respuesta a incidentes\nAuditorías regulares de seguridad\nAcuerdos de confidencialidad con terceros', 1, NULL, 2, 18),
  (21, 4, '4', 'Derechos sobre los datos', 'Acceso: Conocer qué datos tenemos sobre usted\nRectificación: Corregir datos inexactos o incompletos\nActualización: Mantener sus datos actualizados\nSupresión: Solicitar la eliminación de sus datos (cuando sea posible)\nOposición: Oponerse al tratamiento de sus datos en ciertos casos\nPortabilidad: Obtener una copia de sus datos en formato estructurado\n\nPara ejercer estos derechos, puede contactarnos a través de los canales indicados al final de esta política.', 1, NULL, 2, NULL),
  (22, 5, '5', 'Compartir información', NULL, 1, NULL, 2, NULL),
  (23, 1, '5.1', 'Entidades Gubernamentales', 'Con entidades del gobierno colombiano cuando sea requerido por ley o para cumplir con obligaciones regulatorias.', 1, NULL, 2, 22),
  (24, 2, '5.2', 'Proveedores de Servicios', 'Con proveedores de servicios tecnológicos bajo estrictos acuerdos de confidencialidad.', 1, NULL, 2, 22),
  (25, 3, '5.3', 'Instituciones Educativas', 'Con otras instituciones educativas para fines de articulación académica y reconocimiento de estudios.', 1, NULL, 2, 22),
  (26, 6, '6', 'Retención de datos', 'Datos académicos: permanentes para efectos de certificación\nDatos de contacto: mientras mantenga relación activa con el SENA\nDatos técnicos: máximo 2 años\nDatos financieros: según legislación contable y tributaria', 1, NULL, 2, NULL),
  (27, 7, '7', 'Menores de edad', 'Los menores de edad pueden utilizar nuestros servicios con el consentimiento de sus padres o tutores legales. \nMedidas adicionales:\n- Verificación del consentimiento parental\n- Limitación en la recopilación de datos personales\n- Supervisión adicional en el procesamiento de datos\n- Derechos especiales de eliminación de datos', 1, NULL, 2, NULL);

INSERT INTO `module` (`id`, `name`, `description`, `active`, `delete_at`) VALUES
  (1, 'Inicio', 'Parte inicial del sistema', 1, NULL),
  (2, 'Seguridad', 'Administra el sistema', 1, NULL),
  (3, 'Asignar seguimientos', 'Proceso de asignación y seguimiento de etapa práctica', 1, NULL);

INSERT INTO `form` (`id`, `name`, `description`, `path`, `active`, `delete_at`) VALUES
  (1, 'Administración', 'Sección de control de administración del sistema (módulo seguridad)', '/admin', 1, NULL),
  (2, 'Registro Masivo', 'Registro de usuarios masivamente mediante plantillas de excel', '/mass-registration', 1, NULL),
  (3, 'Inicio', 'Inicio del sistema', '/home', 1, NULL),
  (4, 'Solicitud', 'Solicitud de aprendiz para asignación de instructor', '/request-registration', 1, NULL),
  (5, 'Reasignar', 'El coordinador reasigna instructor a aprendiz', '/reassign', 1, NULL),
  (6, 'Seguimiento', 'El instructor hace seguimiento a los aprendices', '/following', 1, NULL),
  (7, 'Historial de seguimiento', 'Historial de todos los seguimientos', '/following-history', 1, NULL),
  (8, 'Evaluar visita final', 'El coordinador evalúa la visita final', '/evaluate-final-visit', 1, NULL),
  (9, 'Asignar', 'El coordinador asigna instructor a aprendiz', '/assign', 1, NULL),
  (10, 'Registrar EP', 'Operador sofia plus deja su mensaje', '/register-ep', 1, NULL),
	(11, 'Valoración solicitud', 'Instructor valora previamente una solictud', '/application-evaluation', 1, NULL);


INSERT INTO `permission` (`id`, `type_permission`, `description`, `delete_at`, `active`) VALUES
  (1, 'Ver', 'Visualizar los datos', NULL, 1),
  (2, 'Editar', 'Editar los datos', NULL, 1),
  (3, 'Registrar', 'Ingresar datos nuevos', NULL, 1),
  (4, 'Eliminar', 'Eliminar permanentemente datos', NULL, 1),
  (5, 'Activar', 'Activar datos', NULL, 1);

INSERT INTO `role` (`id`, `type_role`, `description`, `active`, `delete_at`) VALUES
  (1, 'Administrador', 'Administra y tiene acceso absoluto al sistema', 1, NULL),
  (2, 'Aprendiz', 'Accede a sus secciones permitidas en el sistema', 1, NULL),
  (3, 'Instructor', 'Accede a sus secciones permitidas en el sistema', 1, NULL),
  (4, 'Coordinador', 'Evalúa y sigue los procesos', 1, NULL),
  (5, 'Operador de Sofia Plus', 'Revisa las asignaciones y hace el proceso en sofia plus', 1, NULL);


INSERT INTO `form_module` (`id`, `active`, `deleted_at`, `form_id`, `module_id`) VALUES
	(1, 1, NULL, 1, 2),
	(2, 1, NULL, 2, 2),
	(3, 1, NULL, 3, 1),
	(4, 1, NULL, 4, 3),
	(5, 1, NULL, 6, 3),
	(6, 1, NULL, 5, 3),
	(7, 1, NULL, 7, 3),
	(8, 1, NULL, 8, 3),
	(9, 1, NULL, 9, 3),
	(10, 1, NULL, 10, 3),
	(11, 1, NULL, 11, 3);

INSERT INTO `role_form_permission` (`id`, `role_id`, `form_id`, `permission_id`, `delete_at`, `active`) VALUES
(1, 2, 3, 1, NULL, true),
(2, 3, 3, 1, NULL, true),
(3, 2, 4, 1, NULL, true),
(4, 2, 4, 4, NULL, true),
(5, 4, 2, 1, NULL, true),
(6, 4, 2, 2, NULL, true),
(7, 4, 2, 3, NULL, true),
(8, 4, 2, 4, NULL, true),
(9, 4, 2, 5, NULL, true),
(10, 4, 3, 1, NULL, true),
(11, 4, 3, 2, NULL, true),
(12, 4, 3, 3, NULL, true),
(13, 4, 3, 4, NULL, true),
(14, 4, 3, 5, NULL, true),
(15, 4, 5, 1, NULL, true),
(16, 4, 5, 2, NULL, true),
(17, 4, 5, 3, NULL, true),
(18, 4, 5, 4, NULL, true),
(19, 4, 5, 5, NULL, true),
(20, 4, 7, 1, NULL, true),
(21, 4, 7, 2, NULL, true),
(22, 4, 7, 3, NULL, true),
(23, 4, 7, 4, NULL, true),
(24, 4, 7, 5, NULL, true),
(25, 4, 8, 1, NULL, true),
(26, 4, 8, 2, NULL, true),
(27, 4, 8, 3, NULL, true),
(28, 4, 8, 4, NULL, true),
(29, 4, 8, 5, NULL, true),
(30, 4, 9, 1, NULL, true),
(31, 4, 9, 2, NULL, true),
(32, 4, 9, 3, NULL, true),
(33, 4, 9, 4, NULL, true),
(34, 4, 9, 5, NULL, true),
(35, 3, 3, 1, NULL, true),
(36, 3, 6, 1, NULL, true),
(37, 3, 6, 2, NULL, true),
(38, 3, 6, 3, NULL, true),
(39, 3, 6, 4, NULL, true),
(40, 3, 6, 5, NULL, true),
(41, 3, 7, 1, NULL, true),
(42, 3, 7, 2, NULL, true),
(43, 3, 7, 3, NULL, true),
(44, 3, 7, 4, NULL, true),
(45, 3, 7, 5, NULL, true),
(46, 1, 1, 1, NULL, true),
(47, 1, 1, 2, NULL, true),
(48, 1, 1, 3, NULL, true),
(49, 1, 1, 4, NULL, true),
(50, 1, 1, 5, NULL, true),
(51, 1, 1, 1, NULL, true),
(52, 1, 1, 2, NULL, true),
(53, 1, 1, 3, NULL, true),
(54, 1, 1, 4, NULL, true),
(55, 1, 1, 5, NULL, true),
(56, 1, 2, 1, NULL, true),
(57, 1, 2, 2, NULL, true),
(58, 1, 2, 3, NULL, true),
(59, 1, 2, 4, NULL, true),
(60, 1, 2, 5, NULL, true),
(61, 1, 2, 1, NULL, true),
(62, 1, 2, 2, NULL, true),
(63, 1, 2, 3, NULL, true),
(64, 1, 2, 4, NULL, true),
(65, 1, 2, 5, NULL, true),
(66, 1, 3, 1, NULL, true),
(67, 1, 3, 2, NULL, true),
(68, 1, 3, 3, NULL, true),
(69, 1, 3, 4, NULL, true),
(70, 1, 3, 5, NULL, true),
(71, 1, 3, 1, NULL, true),
(72, 1, 3, 2, NULL, true),
(73, 1, 3, 3, NULL, true),
(74, 1, 3, 4, NULL, true),
(75, 1, 3, 5, NULL, true),
(76, 1, 5, 1, NULL, true),
(77, 1, 5, 2, NULL, true),
(78, 1, 5, 3, NULL, true),
(79, 1, 5, 4, NULL, true),
(80, 1, 5, 5, NULL, true),
(81, 1, 7, 1, NULL, true),
(82, 1, 7, 2, NULL, true),
(83, 1, 7, 3, NULL, true),
(84, 1, 7, 4, NULL, true),
(85, 1, 7, 5, NULL, true),
(86, 1, 8, 1, NULL, true),
(87, 1, 8, 2, NULL, true),
(88, 1, 8, 3, NULL, true),
(89, 1, 8, 4, NULL, true),
(90, 1, 8, 5, NULL, true),
(91, 1, 9, 1, NULL, true),
(92, 1, 9, 2, NULL, true),
(93, 1, 9, 3, NULL, true),
(94, 1, 9, 4, NULL, true),
(95, 1, 9, 5, NULL, true),
(101, 5, 10, 1, NULL, true),
(102, 5, 10, 2, NULL, true),
(103, 5, 10, 3, NULL, true),
(104, 5, 10, 4, NULL, true),
(105, 5, 10, 5, NULL, true),
(106, 5, 3, 1, NULL, true),
(107, 5, 3, 2, NULL, true),
(108, 5, 3, 3, NULL, true),
(109, 5, 3, 4, NULL, true),
(110, 5, 3, 5, NULL, true),
(111, 3, 11, 1, NULL, true),
(112, 3, 11, 2, NULL, true),
(113, 3, 11, 3, NULL, true),
(114, 3, 11, 4, NULL, true),
(115, 3, 11, 5, NULL, true);




INSERT INTO `person` (`id`, `first_name`, `second_name`, `first_last_name`, `second_last_name`, `phone_number`, `number_identification`, `image`, `active`, `delete_at`, `type_identification_id`) VALUES
	(1, 'July', '', 'Ramos', '', 3125647896, 1032679504, '', 1, NULL, 1),
  (2, 'Daniela', '', 'Ramos', '', 3125647896, 1032679503, '', 1, NULL, 1),
  (3, 'Ramos', '', 'Sena', '', 3125647897, 1098765431, '', 1, NULL, 1),
  (4, 'Paola', '', 'Sena', '', 3125647897, 1098765432, '', 1, NULL, 1),
  (5, 'Mario', '', 'Sena', '', 3125647897, 1098765400, '', 1, NULL, 1);


INSERT INTO `apprentice` (`id`, `active`, `delete_at`, `ficha_id`, `person_id`) VALUES
	(1, 1, NULL, NULL, 1);

INSERT INTO `instructor` ( `id`, `contract_start_date`,  `contract_end_date`,  `assigned_learners`,  `max_assigned_learners`,  `is_followup_instructor`,  `active`,  `delete_at`,  `contract_type_id`,  `knowledge_area_id`, `person_id`
) VALUES
(1, '2024-01-15', '2025-01-15', 0, 0, 0, 1, NULL, 2, 1, 2),
(2, '2023-08-01', '2024-08-01', 0, 80, 1, 1, NULL, 1, 1, 3),
(3, '2023-08-01', '2024-08-01', 0, 0, 0, 1, NULL, 1, 1, 4),
(4, '2023-08-01', '2024-08-01', 0, 0, 0, 1, NULL, 1, 1, 5);


INSERT INTO `person_sede` (`id`, `active`, `delete_at`, `person_id`, `sede_id`) VALUES
	(1, 1, NULL, 1, 32),
  (2, 1, NULL, 2, 32),
  (3, 1, NULL, 3, 32),
  (4, 1, NULL, 4, 32),
  (5, 1, NULL, 5, 32);



INSERT INTO `security_user` (`id`, `password`, `last_login`, `is_superuser`, `registered`, `email`, `is_active`, `is_staff`, `deleted_at`, `created_at`, `updated_at`, `reset_code`, `reset_code_expiration`, `person_id`, `role_id`) VALUES
	(1, 'pbkdf2_sha256$600000$c27VSLoHl7gXHmV3Ii5pOK$FuYQpuI1rTwjdwCt3X9nYZiftEoIlOpQGkzT6+6cIEE=', NULL, 0, 0, 'daniela_ramos@soy.sena.edu.co', 1, 0, NULL, '2025-11-06 19:31:52.609196', '2025-11-06 19:32:53.972992', NULL, NULL, 1, 2),
  (2, 'pbkdf2_sha256$600000$c27VSLoHl7gXHmV3Ii5pOK$FuYQpuI1rTwjdwCt3X9nYZiftEoIlOpQGkzT6+6cIEE=', NULL, 0, 0, 'july@sena.edu.co', 1, 0, NULL, '2025-11-06 19:31:52.609196', '2025-11-06 19:32:53.972992', NULL, NULL, 2, 1),
  (3, 'pbkdf2_sha256$600000$c27VSLoHl7gXHmV3Ii5pOK$FuYQpuI1rTwjdwCt3X9nYZiftEoIlOpQGkzT6+6cIEE=', NULL, 0, 0, 'ramos@sena.edu.co', 1, 0, NULL, '2025-11-06 19:31:52.609196', '2025-11-06 19:32:53.972992', NULL, NULL, 3, 3),
  (4, 'pbkdf2_sha256$600000$c27VSLoHl7gXHmV3Ii5pOK$FuYQpuI1rTwjdwCt3X9nYZiftEoIlOpQGkzT6+6cIEE=', NULL, 0, 0, 'paola@sena.edu.co', 1, 0, NULL, '2025-11-06 19:31:52.609196', '2025-11-06 19:32:53.972992', NULL, NULL, 4, 5),
  (5, 'pbkdf2_sha256$600000$c27VSLoHl7gXHmV3Ii5pOK$FuYQpuI1rTwjdwCt3X9nYZiftEoIlOpQGkzT6+6cIEE=', NULL, 0, 0, 'mario@sena.edu.co', 1, 0, NULL, '2025-11-06 19:31:52.609196', '2025-11-06 19:32:53.972992', NULL, NULL, 5, 4);



SELECT 'Estructura e inserts cargados correctamente en bdautogestion (alineado a bd_sena.sql)' AS mensaje;
