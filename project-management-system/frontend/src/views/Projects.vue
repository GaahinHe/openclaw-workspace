<template>
  <div class="projects">
    <div class="header">
      <h1>项目管理</h1>
      <el-button type="primary" @click="showDialog = true">新建项目</el-button>
    </div>
    
    <el-table :data="projects" style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="项目名称" />
      <el-table-column prop="description" label="描述" show-overflow-tooltip />
      <el-table-column prop="status" label="状态" width="120">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150">
        <template #default="{ row }">
          <el-button type="primary" link size="small">编辑</el-button>
          <el-button type="danger" link size="small">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <el-dialog v-model="showDialog" title="新建项目" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="名称">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="createProject">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import api from '@/api'
import { ElMessage } from 'element-plus'

const projects = ref([])
const showDialog = ref(false)
const form = reactive({
  name: '',
  description: ''
})

const getStatusType = (status) => {
  const map = { ACTIVE: 'success', COMPLETED: 'info', ARCHIVED: 'warning' }
  return map[status] || 'info'
}

const fetchProjects = async () => {
  try {
    projects.value = await api.get('/projects')
  } catch (error) {
    console.error('获取项目列表失败:', error)
  }
}

const createProject = async () => {
  try {
    await api.post('/projects', form)
    ElMessage.success('创建成功')
    showDialog.value = false
    fetchProjects()
  } catch (error) {
    ElMessage.error('创建失败')
  }
}

onMounted(fetchProjects)
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style>
