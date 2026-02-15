package com.projectmanager.controller;

import com.projectmanager.entity.Task;
import com.projectmanager.service.TaskService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Tag(name = "任务管理", description = "任务相关接口")
@RestController
@RequestMapping("/api/tasks")
public class TaskController {
    
    @Autowired
    private TaskService taskService;
    
    @Operation(summary = "获取所有任务")
    @GetMapping
    public List<Task> list() {
        return taskService.list();
    }
    
    @Operation(summary = "获取任务详情")
    @GetMapping("/{id}")
    public Task get(@PathVariable Long id) {
        return taskService.getById(id);
    }
    
    @Operation(summary = "创建任务")
    @PostMapping
    public boolean create(@RequestBody Task task) {
        return taskService.save(task);
    }
    
    @Operation(summary = "更新任务")
    @PutMapping("/{id}")
    public boolean update(@PathVariable Long id, @RequestBody Task task) {
        task.setId(id);
        return taskService.updateById(task);
    }
    
    @Operation(summary = "删除任务")
    @DeleteMapping("/{id}")
    public boolean delete(@PathVariable Long id) {
        return taskService.removeById(id);
    }
}
