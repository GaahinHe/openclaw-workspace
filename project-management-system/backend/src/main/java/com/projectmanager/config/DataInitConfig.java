package com.projectmanager.config;

import com.projectmanager.entity.Project;
import com.projectmanager.entity.Task;
import com.projectmanager.entity.User;
import com.projectmanager.repository.ProjectMapper;
import com.projectmanager.repository.TaskMapper;
import com.projectmanager.repository.UserMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.context.event.ApplicationReadyEvent;
import org.springframework.context.event.EventListener;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

/**
 * 数据初始化（应用启动后执行）
 */
@Component
public class DataInitConfig {
    
    @Autowired
    private JdbcTemplate jdbcTemplate;
    
    @Autowired
    private PasswordEncoder passwordEncoder;
    
    @EventListener(ApplicationReadyEvent.class)
    public void initData() {
        // 创建表（如果不存在）
        createTables();
        
        // 检查是否已有数据
        Integer count = jdbcTemplate.queryForObject("SELECT COUNT(*) FROM pm_user", Integer.class);
        if (count != null && count > 0) {
            System.out.println("数据已存在，跳过初始化");
            return;
        }
        
        System.out.println("========== 初始化示例数据 ==========");
        
        // 创建用户表数据
        jdbcTemplate.update("INSERT INTO pm_user (username, password, email, role, created_at, updated_at, deleted) VALUES (?, ?, ?, ?, NOW(), NOW(), 0)",
                "admin", passwordEncoder.encode("123456"), "admin@example.com", "ADMIN");
        jdbcTemplate.update("INSERT INTO pm_user (username, password, email, role, created_at, updated_at, deleted) VALUES (?, ?, ?, ?, NOW(), NOW(), 0)",
                "test", passwordEncoder.encode("123456"), "test@example.com", "DEVELOPER");
        
        // 创建项目表数据
        jdbcTemplate.update("INSERT INTO pm_project (name, description, status, leader_id, created_at, updated_at, deleted) VALUES (?, ?, ?, ?, NOW(), NOW(), 0)",
                "项目管理系统", "企业内部项目管理系统", "ACTIVE", 1L);
        jdbcTemplate.update("INSERT INTO pm_project (name, description, status, leader_id, created_at, updated_at, deleted) VALUES (?, ?, ?, ?, NOW(), NOW(), 0)",
                "电商平台", "B2C 电商平台", "ACTIVE", 1L);
        
        // 创建任务表数据
        jdbcTemplate.update("INSERT INTO pm_task (title, description, status, priority, project_id, assignee_id, created_at, updated_at, deleted) VALUES (?, ?, ?, ?, ?, ?, NOW(), NOW(), 0)",
                "设计数据库表结构", "完成项目管理系统的数据库设计", "DONE", "HIGH", 1L, 2L);
        jdbcTemplate.update("INSERT INTO pm_task (title, description, status, priority, project_id, assignee_id, created_at, updated_at, deleted) VALUES (?, ?, ?, ?, ?, ?, NOW(), NOW(), 0)",
                "开发用户认证模块", "实现 JWT 用户认证功能", "IN_PROGRESS", "HIGH", 1L, 2L);
        jdbcTemplate.update("INSERT INTO pm_task (title, description, status, priority, project_id, assignee_id, created_at, updated_at, deleted) VALUES (?, ?, ?, ?, ?, ?, NOW(), NOW(), 0)",
                "前端页面开发", "完成 Vue 前端页面", "TODO", "MEDIUM", 1L, 2L);
        
        System.out.println("✅ 示例数据初始化完成!");
        System.out.println("  - 用户: admin/123456, test/123456");
        System.out.println("  - 项目: 2 个");
        System.out.println("  - 任务: 3 个");
        System.out.println("=====================================");
    }
    
    private void createTables() {
        // 创建用户表
        jdbcTemplate.execute("CREATE TABLE IF NOT EXISTS pm_user (" +
                "id BIGINT PRIMARY KEY AUTO_INCREMENT, " +
                "username VARCHAR(50) NOT NULL UNIQUE, " +
                "password VARCHAR(100) NOT NULL, " +
                "email VARCHAR(100), " +
                "role VARCHAR(20) DEFAULT 'DEVELOPER', " +
                "created_at DATETIME, " +
                "updated_at DATETIME, " +
                "deleted TINYINT DEFAULT 0)");
        
        // 创建项目表
        jdbcTemplate.execute("CREATE TABLE IF NOT EXISTS pm_project (" +
                "id BIGINT PRIMARY KEY AUTO_INCREMENT, " +
                "name VARCHAR(100) NOT NULL, " +
                "description TEXT, " +
                "status VARCHAR(20) DEFAULT 'ACTIVE', " +
                "leader_id BIGINT, " +
                "created_at DATETIME, " +
                "updated_at DATETIME, " +
                "deleted TINYINT DEFAULT 0)");
        
        // 创建任务表
        jdbcTemplate.execute("CREATE TABLE IF NOT EXISTS pm_task (" +
                "id BIGINT PRIMARY KEY AUTO_INCREMENT, " +
                "title VARCHAR(100) NOT NULL, " +
                "description TEXT, " +
                "status VARCHAR(20) DEFAULT 'TODO', " +
                "priority VARCHAR(20) DEFAULT 'MEDIUM', " +
                "project_id BIGINT, " +
                "assignee_id BIGINT, " +
                "deadline DATETIME, " +
                "created_at DATETIME, " +
                "updated_at DATETIME, " +
                "deleted TINYINT DEFAULT 0)");
        
        System.out.println("✅ 数据库表创建完成");
    }
}
