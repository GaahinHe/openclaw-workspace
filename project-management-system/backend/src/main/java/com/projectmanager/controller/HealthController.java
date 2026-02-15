package com.projectmanager.controller;

import org.springframework.web.bind.annotation.*;
import io.swagger.v3.oas.annotations.tags.Tag;

@Tag(name = "健康检查", description = "API 健康检查")
@RestController
@RequestMapping("/api")
public class HealthController {
    
    @GetMapping("/health")
    public String health() {
        return "OK";
    }
}
