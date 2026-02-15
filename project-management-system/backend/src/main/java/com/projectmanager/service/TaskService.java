package com.projectmanager.service;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.projectmanager.entity.Task;
import com.projectmanager.repository.TaskMapper;
import org.springframework.stereotype.Service;

@Service
public class TaskService extends ServiceImpl<TaskMapper, Task> {
    
    // 任务服务逻辑
}
