package com.projectmanager.service;

import com.projectmanager.dto.LoginRequest;
import com.projectmanager.dto.LoginResponse;
import com.projectmanager.dto.Result;
import com.projectmanager.entity.User;
import com.projectmanager.repository.UserMapper;
import com.projectmanager.security.JwtUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class AuthService {
    
    @Autowired
    private AuthenticationManager authenticationManager;
    
    @Autowired
    private JwtUtil jwtUtil;
    
    @Autowired
    private UserMapper userMapper;
    
    @Autowired
    private PasswordEncoder passwordEncoder;
    
    public Result<LoginResponse> login(LoginRequest request) {
        try {
            Authentication authentication = authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(request.getUsername(), request.getPassword())
            );
            
            User user = userMapper.selectOne(
                    new com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper<User>()
                            .eq(User::getUsername, request.getUsername())
            );
            
            String token = jwtUtil.generateToken(user.getUsername(), user.getRole());
            
            LoginResponse response = new LoginResponse();
            response.setToken(token);
            response.setUsername(user.getUsername());
            response.setRole(user.getRole());
            
            return Result.success(response);
        } catch (Exception e) {
            return Result.error("用户名或密码错误");
        }
    }
    
    public Result<Void> register(User user) {
        if (userMapper.selectCount(
                new com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper<User>()
                        .eq(User::getUsername, user.getUsername())
        ) > 0) {
            return Result.error("用户名已存在");
        }
        
        user.setPassword(passwordEncoder.encode(user.getPassword()));
        user.setRole("DEVELOPER");
        userMapper.insert(user);
        
        return Result.success();
    }
}
