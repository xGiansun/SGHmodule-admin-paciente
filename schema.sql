-- ============================================================
-- SGH - Sistema de Gestión Hospitalaria
-- Módulo: Administración de Pacientes
-- Esquema de base de datos MySQL
-- Generado a partir de las migraciones de Django (0001 → 0006)
-- ============================================================

-- Crear la base de datos (ajustar el nombre según tu .env → DB_NAME)
CREATE DATABASE IF NOT EXISTS sgh_pacientes
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE sgh_pacientes;

-- ============================================================
-- Tabla de pacientes
-- ============================================================

CREATE TABLE IF NOT EXISTS `pacientes_paciente` (
    `id`                BIGINT          NOT NULL AUTO_INCREMENT,
    `tipo_documento`    VARCHAR(2)      NOT NULL DEFAULT 'CC'
                            COMMENT 'CC=Cédula Ciudadanía, TI=Tarjeta Identidad, CE=Cédula Extranjería, PP=Pasaporte',
    `numero_documento`  VARCHAR(20)     NOT NULL UNIQUE
                            COMMENT 'Número de documento, único por paciente',
    `nombres`           VARCHAR(100)    NOT NULL,
    `apellidos`         VARCHAR(100)    NOT NULL,
    `fecha_nacimiento`  DATE            NOT NULL,
    `telefono`          VARCHAR(20)     NOT NULL,
    `correo`            VARCHAR(254)    NOT NULL,
    `direccion`         VARCHAR(200)    NOT NULL,
    `fecha_registro`    DATETIME(6)     NOT NULL
                            COMMENT 'Se establece automáticamente al crear el registro',
    PRIMARY KEY (`id`),
    UNIQUE KEY `pacientes_paciente_numero_documento` (`numero_documento`)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Pacientes registrados en el sistema hospitalario';

-- ============================================================
-- Tablas de Django (autenticación y sesiones)
-- Generadas automáticamente por python manage.py migrate
-- Se listan aquí como referencia del esquema completo
-- ============================================================

-- Usuarios del sistema (gestión por Django)
CREATE TABLE IF NOT EXISTS `auth_user` (
    `id`            INT             NOT NULL AUTO_INCREMENT,
    `username`      VARCHAR(150)    NOT NULL UNIQUE,
    `password`      VARCHAR(128)    NOT NULL,
    `email`         VARCHAR(254)    NOT NULL DEFAULT '',
    `first_name`    VARCHAR(150)    NOT NULL DEFAULT '',
    `last_name`     VARCHAR(150)    NOT NULL DEFAULT '',
    `is_staff`      TINYINT(1)      NOT NULL DEFAULT 0,
    `is_active`     TINYINT(1)      NOT NULL DEFAULT 1,
    `is_superuser`  TINYINT(1)      NOT NULL DEFAULT 0,
    `last_login`    DATETIME(6)     NULL,
    `date_joined`   DATETIME(6)     NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Usuarios administradores del módulo';

-- Tokens de autenticación REST (Django REST Framework)
CREATE TABLE IF NOT EXISTS `authtoken_token` (
    `key`        VARCHAR(40)  NOT NULL,
    `created`    DATETIME(6)  NOT NULL,
    `user_id`    INT          NOT NULL UNIQUE,
    PRIMARY KEY (`key`),
    CONSTRAINT `fk_authtoken_user`
        FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Tokens de acceso para la API REST';

-- ============================================================
-- Datos de ejemplo (opcionales — para desarrollo y pruebas)
-- ============================================================

INSERT INTO `pacientes_paciente`
    (`tipo_documento`, `numero_documento`, `nombres`, `apellidos`,
     `fecha_nacimiento`, `telefono`, `correo`, `direccion`, `fecha_registro`)
VALUES
    ('CC', '1234567890', 'María', 'Gómez Torres',
     '1990-05-14', '3001234567', 'maria.gomez@example.com',
     'Calle 10 # 5-20, Armenia', NOW()),

    ('TI', '987654321', 'Carlos', 'Ramírez López',
     '2005-11-03', '3109876543', 'carlos.ramirez@example.com',
     'Carrera 15 # 8-45, Calarcá', NOW()),

    ('CC', '1122334455', 'Ana', 'Martínez Ríos',
     '1978-02-28', '3205551234', 'ana.martinez@example.com',
     'Avenida Bolívar # 12-30, Montenegro', NOW());
