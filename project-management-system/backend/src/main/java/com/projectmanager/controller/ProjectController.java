package com.projectmanager.controller;

import com.projectmanager.entity.Project;
import com.projectmanager.service.ProjectService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Tag(name = "项目管理", description = "项目相关接口")
@RestController
@RequestMapping("/api/projects")
public class ProjectController {
    
    @Autowired
    private ProjectService projectService;
    
    @Operation(summary = "获取所有项目")
    @GetMapping
    public List<Project> list() {
        return projectService.list();
    }
    
    @Operation(summary = "获取项目详情")
    @GetMapping("/{id}")
    public Project get(@PathVariable Long id) {
        return projectService.getById(id);
    }
    
    @Operation(summary = "创建项目")
    @PostMapping
    public boolean create(@RequestBody Project project) {
        return projectService.save(project);
    }
    
    @Operation(summary = "更新项目")
    @PutMapping("/{id}")
    public boolean update(@PathVariable Long id, @RequestBody Project project) {
        project.setId(id);
        return projectService.updateById(project);
    }
    
    @Operation(summary = "删除项目")
    @DeleteMapping("/{id}")
    public boolean delete(@PathVariable Long id) {
        return projectService.removeById(id);
    }
}
