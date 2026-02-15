-- ============================================
-- 项目管理系统数据库初始化脚本
-- OceanBase MySQL 兼容模式
-- ============================================

-- 创建数据库
CREATE DATABASE IF NOT EXISTS project_manager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE project_manager;

-- ============================================
-- 用户表
-- ============================================
DROP TABLE IF EXISTS pm_user;
CREATE TABLE pm_user (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    password VARCHAR(100) NOT NULL COMMENT '密码',
    email VARCHAR(100) COMMENT '邮箱',
    role VARCHAR(20) DEFAULT 'DEVELOPER' COMMENT '角色: ADMIN, MANAGER, DEVELOPER',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT DEFAULT 0 COMMENT '删除标识'
) COMMENT = '用户表';

-- 插入默认管理员用户 (密码: 123456)
INSERT INTO pm_user (username, password, email, role) VALUES 
('admin', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iKTVKIUi', 'admin@example.com', 'ADMIN'),
('test', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iKTVKIUi', 'test@example.com', 'DEVELOPER');

-- ============================================
-- 项目表
-- ============================================
DROP TABLE IF EXISTS pm_project;
CREATE TABLE pm_project (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '项目ID',
    name VARCHAR(100) NOT NULL COMMENT '项目名称',
    description TEXT COMMENT '项目描述',
    status VARCHAR(20) DEFAULT 'ACTIVE' COMMENT '状态: ACTIVE, COMPLETED, ARCHIVED',
    leader_id BIGINT COMMENT '负责人ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT DEFAULT 0 COMMENT '删除标识',
    INDEX idx_leader (leader_id)
) COMMENT = '项目表';

-- 插入示例数据
INSERT INTO pm_project (name, description, status, leader_id) VALUES 
('项目管理系统', '企业内部项目管理系统', 'ACTIVE', 1),
('电商平台', 'B2C 电商平台', 'ACTIVE', 1);

-- ============================================
-- 任务表
-- ============================================
DROP TABLE IF EXISTS pm_task;
CREATE TABLE pm_task (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '任务ID',
    title VARCHAR(100) NOT NULL COMMENT '任务标题',
    description TEXT COMMENT '任务描述',
    status VARCHAR(20) DEFAULT 'TODO' COMMENT '状态: TODO, IN_PROGRESS, DONE',
    priority VARCHAR(20) DEFAULT 'MEDIUM' COMMENT '优先级: LOW, MEDIUM, HIGH',
    project_id BIGINT COMMENT '所属项目ID',
    assignee_id BIGINT COMMENT '负责人ID',
    deadline DATETIME COMMENT '截止时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT DEFAULT 0 COMMENT '删除标识',
    INDEX idx_project (project_id),
    INDEX idx_assignee (assignee_id)
) COMMENT = '任务表';

-- 插入示例数据
INSERT INTO pm_task (title, description, status, priority, project_id, assignee_id) VALUES 
('设计数据库表结构', '完成项目管理系统的数据库设计', 'DONE', 'HIGH', 1, 2),
('开发用户认证模块', '实现 JWT 用户认证功能', 'IN_PROGRESS', 'HIGH', 1, 2),
('前端页面开发', '完成 Vue 前端页面', 'TODO', 'MEDIUM', 1, 2);

-- ============================================
-- 初始化完成
-- ============================================
SELECT '数据库初始化完成!' AS status;

-- 验证数据
SELECT '用户表:' AS table_name, COUNT(*) AS count FROM pm_user;
SELECT '项目表:' AS table_name, COUNT(*) AS count FROM pm_project;
SELECT '任务表:' AS table_name, COUNT(*) AS count FROM pm_task;
