package com.projectmanager.repository;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.projectmanager.entity.Project;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface ProjectMapper extends BaseMapper<Project> {
}
