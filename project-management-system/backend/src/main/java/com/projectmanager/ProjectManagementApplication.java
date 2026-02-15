package com.projectmanager;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@MapperScan("com.projectmanager.repository")
public class ProjectManagementApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(ProjectManagementApplication.class, args);
    }
}
