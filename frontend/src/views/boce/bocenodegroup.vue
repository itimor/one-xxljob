<template>
  <div class="app-container">
    <div class="filter-container">
      <el-button-group>
        <el-button
          class="filter-item"
          type="primary"
          icon="el-icon-search"
          @click="handleFilter"
        >
          {{ "搜索" }}
        </el-button>
        <el-button
          v-if="permissionList.add"
          class="filter-item"
          type="success"
          icon="el-icon-edit"
          @click="handleCreate"
        >
          {{ "添加" }}
        </el-button>
      </el-button-group>
    </div>

    <el-table :data="list" v-loading="listLoading" border style="width: 100%" highlight-current-row>
      <el-table-column label="排序" prop="order"></el-table-column>
      <el-table-column label="AppName" prop="app_name"></el-table-column>
      <el-table-column label="名称" prop="title"></el-table-column>
      <el-table-column label="注册方式" prop="address_type">
        <template slot-scope="scope">
          <el-tag v-if="scope.row.address_type===0" type="info">自动注册</el-tag>
          <el-tag v-else>手动录入</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="OnLine机器地址" prop="address_list">
        <template slot-scope="scope">
          <el-tag v-for="item in scope.row.address_list" effect="dark" type="success" size="mini">{{item}}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="260" class-name="small-padding fixed-width">
        <template slot-scope="{ row }">
          <el-button-group>
            <el-button
              v-if="permissionList.update"
              size="small"
              type="primary"
              @click="handleUpdate(row)"
            >
              {{ "编辑" }}
            </el-button>
            <el-button
              v-if="permissionList.del"
              size="small"
              type="danger"
              @click="handleDelete(row)"
            >
              {{ "删除" }}
            </el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible" :close-on-click-modal="false">
      <el-form
        ref="dataForm"
        :rules="rules"
        :model="temp"
        label-position="left"
        label-width="120px"
        style="width: 400px; margin-left:50px;"
      >
        <el-form-item label="名称" prop="title">
          <el-input v-model="temp.title"/>
        </el-form-item>
        <el-form-item label="AppName" prop="app_name">
          <el-input v-model="temp.app_name"/>
        </el-form-item>
        <el-form-item label="排序" prop="order">
          <el-input v-model="temp.order"/>
        </el-form-item>
        <el-form-item label="注册方式" prop="address_type">
          <el-radio-group v-model="temp.address_type">
            <el-radio :label="0">自动注册</el-radio>
            <el-radio :label="1">手动录入</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="机器地址" prop="address_list">
          <el-input v-model="temp.address_list" type="textarea" placeholder="多地址以逗号分离" :autosize="{ minRows: 3, maxRows: 5}"/>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          {{ "取消" }}
        </el-button>
        <el-button type="primary" @click="dialogStatus === 'create' ? createData() : updateData()">
          {{ "确定" }}
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
  import {auth, c_xxljob} from '@/api/all'
  import Pagination from '@/components/Pagination'
  import {checkAuthAdd, checkAuthDel, checkAuthView, checkAuthUpdate} from '@/utils/permission'

  export default {
    name: 'bocenodegroup',

    components: {Pagination},
    data() {
      return {
        operationList: [],
        permissionList: {
          add: false,
          del: false,
          view: false,
          update: false
        },
        list: [],
        total: 0,
        listLoading: true,
        loading: true,
        temp: {},
        dialogFormVisible: false,
        dialogStatus: '',
        dialogFormManyVisible: false,
        textMap: {
          update: '编辑',
          create: '添加',
        },
        rules: {
          app_name: [{required: true, message: '请输入名称', trigger: 'blur'}],
          title: [{required: true, message: '请输入名称', trigger: 'blur'}],
          order: [{required: true, message: '请输入名称', trigger: 'blur'}],
          address_list: [{required: true, message: '请输入名称', trigger: 'blur'}],
        },
        multipleSelection: [],
        nodes: []
      }
    },
    computed: {},
    created() {
      this.getMenuButton()
      this.getList()
    },
    methods: {
      checkPermission() {
        this.permissionList.add = checkAuthAdd(this.operationList)
        this.permissionList.del = checkAuthDel(this.operationList)
        this.permissionList.view = checkAuthView(this.operationList)
        this.permissionList.update = checkAuthUpdate(this.operationList)
      },
      getMenuButton() {
        auth.requestMenuButton('bocenodegroup').then(response => {
          this.operationList = response.results
        }).then(() => {
          this.checkPermission()
        })
      },
      getList() {
        this.listLoading = true
        c_xxljob.get_group().then(response => {
          this.list = response.results
          this.total = response.results.length
          this.listLoading = false
        })
      },
      handleFilter() {
        this.getList()
      },
      resetTemp() {
        this.temp = {
          id: '',
          app_name: '',
          title: '',
          order: '',
          address_type: 1,
          address_list: ''
        }
      },
      handleCreate() {
        this.resetTemp()
        this.dialogStatus = 'create'
        this.dialogFormVisible = true
        this.loading = false
        this.$nextTick(() => {
          this.$refs['dataForm'].clearValidate()
        })
      },
      createData() {
        this.$refs['dataForm'].validate((valid) => {
          if (valid) {
            this.loading = true
            c_xxljob.create_group(this.temp).then(response => {
              this.dialogFormVisible = false
              this.$notify({
                title: '成功',
                message: '创建成功',
                type: 'success',
                duration: 2000
              })
              this.getList()
            }).catch(() => {
              this.loading = false
            })
          }
        })
      },
      handleUpdate(row) {
        this.temp = row
        this.dialogStatus = 'update'
        this.dialogFormVisible = true
        this.$nextTick(() => {
          this.$refs['dataForm'].clearValidate()
        })
      },
      updateData() {
        this.$refs['dataForm'].validate((valid) => {
          if (valid) {
            this.loading = true
            c_xxljob.update_group(this.temp).then(() => {
              this.dialogFormVisible = false
              this.$notify({
                title: '成功',
                message: '更新成功',
                type: 'success',
                duration: 2000
              })
              this.getList()
            }).catch(() => {
              this.loading = false
            })
          }
        })
      },
      handleDelete(row) {
        this.$confirm('是否确定删除?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.temp.id = row.id
          c_xxljob.delete_group(this.temp).then(() => {
            this.$message({
              message: '删除成功',
              type: 'success'
            })
            this.getList()
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
      }
    }
  }
</script>
