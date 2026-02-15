<template>
  <div class="home">
    <h1>欢迎使用项目管理系统</h1>
    <el-row :gutter="20" style="margin-top: 30px;">
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>项目统计</template>
          <div class="stat-value">{{ projectCount }}</div>
          <div class="stat-label">总项目数</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>任务统计</template>
          <div class="stat-value">{{ taskCount }}</div>
          <div class="stat-label">总任务数</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>用户统计</template>
          <div class="stat-value">{{ userCount }}</div>
          <div class="stat-label">总用户数</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'

const projectCount = ref(0)
const taskCount = ref(0)
const userCount = ref(0)

onMounted(async () => {
  // 统计数据
})
</script>

<style scoped>
.home h1 {
  color: #303133;
  margin-bottom: 20px;
}

.stat-value {
  font-size: 48px;
  font-weight: bold;
  color: #409EFF;
  text-align: center;
  padding: 20px 0;
}

.stat-label {
  text-align: center;
  color: #909399;
}
</style>
