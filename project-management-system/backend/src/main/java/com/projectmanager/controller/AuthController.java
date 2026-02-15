package com.projectmanager.controller;

import com.projectmanager.dto.LoginRequest;
import com.projectmanager.dto.LoginResponse;
import com.projectmanager.dto.Result;
import com.projectmanager.entity.User;
import com.projectmanager.service.AuthService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@Tag(name = "认证管理", description = "用户登录注册接口")
@RestController
@RequestMapping("/api/auth")
public class AuthController {
    
    @Autowired
    private AuthService authService;
    
    @Operation(summary = "用户登录")
    @PostMapping("/login")
    public Result<LoginResponse> login(@RequestBody LoginRequest request) {
        return authService.login(request);
    }
    
    @Operation(summary = "用户注册")
    @PostMapping("/register")
    public Result<Void> register(@RequestBody User user) {
        return authService.register(user);
    }
}
