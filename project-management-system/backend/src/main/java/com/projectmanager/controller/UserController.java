package com.projectmanager.controller;

import com.projectmanager.entity.User;
import com.projectmanager.service.UserService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Tag(name = "用户管理", description = "用户相关接口")
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    @Autowired
    private UserService userService;
    
    @Operation(summary = "获取所有用户")
    @GetMapping
    public List<User> list() {
        return userService.list();
    }
    
    @Operation(summary = "获取用户详情")
    @GetMapping("/{id}")
    public User get(@PathVariable Long id) {
        return userService.getById(id);
    }
    
    @Operation(summary = "创建用户")
    @PostMapping
    public boolean create(@RequestBody User user) {
        return userService.save(user);
    }
    
    @Operation(summary = "更新用户")
    @PutMapping("/{id}")
    public boolean update(@PathVariable Long id, @RequestBody User user) {
        user.setId(id);
        return userService.updateById(user);
    }
    
    @Operation(summary = "删除用户")
    @DeleteMapping("/{id}")
    public boolean delete(@PathVariable Long id) {
        return userService.removeById(id);
    }
}
