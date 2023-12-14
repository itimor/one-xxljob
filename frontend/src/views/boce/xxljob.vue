<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model="listQuery.search"
        placeholder="请输入内容"
        clearable
        prefix-icon="el-icon-search"
        style="width: 200px;"
        class="filter-item"
        @keyup.enter.native="handleFilter"
        @clear="handleFilter"
      />
      <el-select class="filter-item" v-model="listQuery.group" filterable placeholder="请选择执行器" @change="handleFilter">
         <el-option
           v-for="item in groups"
           :key="item.id"
           :label="item.title"
           :value="item.id">
         </el-option>
      </el-select>
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

    <el-table :data="list" v-loading="listLoading" border style="width: 100%" highlight-current-row
              @sort-change="handleSortChange"
              @cell-click="updateStatus">
      <el-table-column label="任务ID" prop="task_id"></el-table-column>
      <el-table-column label="执行器id" prop="group"></el-table-column>
      <el-table-column label="名称" prop="name"></el-table-column>
      <el-table-column label="运行模式" prop="type"></el-table-column>
      <el-table-column label="Cron" prop="jobCron"></el-table-column>
      <el-table-column label="负责人" prop="author"></el-table-column>
      <el-table-column label="状态" prop="status">
        <template slot-scope="scope">
          <el-switch
            v-model="scope.row.status"
            active-color="#13ce66"
            inactive-color="#ff4949">
          </el-switch>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="300" class-name="small-padding fixed-width">
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
            <el-button
              v-if="permissionList.update"
              size="small"
              type="warning"
              @click="handleCodeUpdate(row)"
            >
              {{ "code" }}
            </el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>
    <div class="table-pagination">
      <pagination
        v-show="total > 0"
        :total="total"
        :page.sync="listQuery.offset"
        :limit.sync="listQuery.limit"
        @pagination="getList"
      />
    </div>
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible" :close-on-click-modal="false">
      <el-form
        ref="dataForm"
        :rules="rules"
        :model="temp"
        label-position="right"
        label-width="100px"
        style="width: 400px; margin-left:50px;"
      >
        <el-form-item v-if="dialogStatus === 'update_taskid'" label="任务ID" prop="task_id">
          <el-input v-model="temp.task_id"/>
        </el-form-item>
        <div v-if="dialogStatus !== 'update_taskid'">
          <el-form-item label="执行器" prop="group">
            <el-select v-model="temp.group" filterable placeholder="请选择执行器">
              <el-option
                v-for="item in groups"
                :key="item.id"
                :label="item.title"
                :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="名称" prop="name">
            <el-input v-model="temp.name"/>
          </el-form-item>
          <el-form-item label="路由策略" prop="router">
            <el-select v-model="temp.router" filterable placeholder="请选择执行器">
              <el-option
                v-for="(label, value) in route_type"
                :key="value"
                :label="label"
                :value="value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="cron表达式" prop="jobCron">
            <el-popover v-model="cronPopover">
                <vue-cron @change="changeCron" @close="cronPopover=false" i18n="cn"></vue-cron>
                <el-input slot="reference" @click="cronPopover=true" v-model="temp.jobCron" placeholder="请输入定时策略"></el-input>
            </el-popover>
          </el-form-item>
          <el-form-item label="GLUE类型" prop="type">
            <el-select v-model="temp.type" filterable placeholder="请选择GLUE脚本类型">
              <el-option
                v-for="(label, value) in glue_type"
                :key="value"
                :label="label"
                :value="value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="阻塞策略" prop="block">
            <el-select v-model="temp.block" filterable placeholder="请选择阻塞策略">
              <el-option
                v-for="(label, value) in block_type"
                :key="value"
                :label="label"
                :value="value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="负责人" prop="author">
            <el-input v-model="temp.author"/>
          </el-form-item>
          <el-form-item label="参数" prop="param">
            <el-input v-model="temp.param" type="textarea" :autosize="{ minRows: 3, maxRows: 5}"/>
          </el-form-item>
        </div>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          {{ "取消" }}
        </el-button>
        <el-button type="primary" @click="dialogStatus === 'create' ? createData() : updateData()">
          {{ "保存" }}
        </el-button>
      </div>
    </el-dialog>

    <el-dialog class="showcode" :visible.sync="dialogCodeVisible" :close-on-click-modal="false" :fullscreen="true" :show-close="false"
               @before-close="updateData()">
      <el-card class="box-card">
        <div slot="header" class="clearfix">
          <span class="card-span-title">编写code</span>
          <div style="float: right;" >
            <el-select class="filter-item" v-model="listQuery.group" filterable placeholder="历史版本" @change="handleCodeFilter">
              <el-option
                v-for="item in code_historys"
                :key="item.id"
                :label="item.glue_remark"
                :value="item.id">
              </el-option>
            </el-select>

            <el-button type="danger" @click="dialogCodeVisible = false">
            {{ "取消" }}
            </el-button>
            <el-button type="primary" @click="updateData()">
              {{ "保存" }}
            </el-button>
          </div>
        </div>
      <el-form ref="dataForm" :model="temp">
        <codemirror :value="temp.code" @input="onCmCodeChange"></codemirror>
      </el-form>
      </el-card>
      <div slot="footer" class="dialog-footer">
      </div>
    </el-dialog>
  </div>
</template>

<script>
  import {xxljob, auth, c_xxljob} from '@/api/all'
  import Pagination from '@/components/Pagination'
  import Codemirror from '@/components/Codemirror'
  import {checkAuthAdd, checkAuthDel, checkAuthView, checkAuthUpdate} from '@/utils/permission'

  export default {
    name: 'xxxjob',

    components: {Pagination, Codemirror},
    data() {
      return {
        cronPopover: false,
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
        listQuery: {
          offset: 1,
          limit: 20,
          search: undefined,
          ordering: undefined,
          group: undefined
        },
        temp: {},
        dialogFormVisible: false,
        dialogCodeVisible: false,
        dialogStatus: '',
        textMap: {
          update: '编辑',
          create: '添加',
        },
        rules: {
          name: [{required: true, message: '请输入名称', trigger: 'blur'}],
          jobCron: [{required: true, message: '请输入 0 */4 * * * ?', trigger: 'blur'}]
        },
        groups: [],
        route_type: {
          'FIRST': '第一个',
          'LAST': '最后一个',
          'ROUND': '轮询',
          'RANDOM': '随机',
          'SHARDING_BROADCAST': '分片广播',
        },
        glue_type: {
          'GLUE_GROOVY': 'java',
          'GLUE_SHELL': 'shell',
          'GLUE_PYTHON': 'python',
          'GLUE_PHP': 'php',
          'GLUE_NODEJS': 'nodejs',
        },
        block_type: {
          'SERIAL_EXECUTION': '单机串行',
          'DISCARD_LATER': '丢弃后续调度',
          'COVER_EARLY': '覆盖之前调度',
        },
        code_historys: []
      }
    },
    created() {
      this.getMenuButton()
      this.getList()
      this.getGroupList()
    },
    methods: {
      checkPermission() {
        this.permissionList.add = checkAuthAdd(this.operationList)
        this.permissionList.del = checkAuthDel(this.operationList)
        this.permissionList.view = checkAuthView(this.operationList)
        this.permissionList.update = checkAuthUpdate(this.operationList)
      },
      getMenuButton() {
        auth.requestMenuButton('xxljob').then(response => {
          this.operationList = response.results
        }).then(() => {
          this.checkPermission()
        })
      },
      getList() {
        this.listLoading = true
        xxljob.requestGet(this.listQuery).then(response => {
          this.list = response.results
          this.total = response.count
          this.listLoading = false
        })
      },
      getGroupList() {
        c_xxljob.get_group().then(response => {
          this.groups = response.results
        })
      },
      handleFilter() {
        this.getList()
      },
      handleCodeFilter(val) {
        for(var i of this.code_historys) {
          if (i.id===val){
            this.temp.code = i.glue_source
          }
        }
      },
      handleSortChange(val) {
        if (val.order === 'ascending') {
          this.listQuery.ordering = val.prop
        } else if (val.order === 'descending') {
          this.listQuery.ordering = '-' + val.prop
        } else {
          this.listQuery.ordering = ''
        }
        this.getList()
      },
      resetTemp() {
        this.temp = {
          task_id: '',
          status: false,
          group: '',
          name: 'xxl域名拨测',
          router: 'FIRST',
          jobCron: '0 */1 * * * ?',
          type: 'GLUE_PYTHON',
          block: 'SERIAL_EXECUTION',
          author: 'xman',
          dbrand: '',
          code: '',
          memo: '',
          param: ''
        }
      },
      changeCron(val){
         this.temp.jobCron=val
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
            xxljob.requestPost(this.temp).then(response => {
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
      handleCodeUpdate(row) {
        this.temp = row
        this.dialogCodeVisible = true
        c_xxljob.get_code_by_id(this.temp).then(response => {
          this.temp.code = response.results
        })
        c_xxljob.get_code_history_by_id(this.temp).then(response => {
          this.code_historys = response.results
        })
        this.$nextTick(() => {
          this.$refs['dataForm'].clearValidate()
        })
      },
      onCmCodeChange(val) {
        this.temp.code = val
      },
      updateData() {
        this.$refs['dataForm'].validate((valid) => {
          if (valid) {
            this.loading = true
            xxljob.requestPut(this.temp.id, this.temp).then(() => {
              this.dialogFormVisible = false
              this.$notify({
                title: '成功',
                message: '更新成功',
                type: 'success',
                duration: 2000
              })
              const payload = {
                code: this.temp.code,
                task_id: this.temp.task_id
              }
              c_xxljob.save_code(payload).then(() => {
                this.dialogCodeVisible = false
              })
            }).catch(() => {
              this.loading = false
            })
          }
        })
      },
      updateStatus(row, column) {
        if (column.property === 'status') {
          let action
          if (row.status) {
            action = 'start'
          } else {
            action = 'stop'
          }
          this.temp = row
          xxljob.requestPut(this.temp.id, this.temp).then(() => {
            const payload = {
              action: action,
              task_id: row.task_id
            }
            c_xxljob.action_task(payload)
          }).catch(() => {
            this.loading = false
          })
        }
      },
      handleDelete(row) {
        this.$confirm('是否确定删除?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          xxljob.requestDelete(row.id).then(() => {
            this.$message({
              message: '删除成功',
              type: 'success'
            })
            this.getList()
          })
          const payload = {
            action: 'remove',
            task_id: row.task_id
          }
          c_xxljob.action_task(payload)
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
      },
      handleshowOpera(val) {
        if (val === 3) {
          this.showOpera = true
        } else {
          this.showOpera = false
          this.temp.operate = 'none'
        }
      },
      getSelectTreeValue(value, type) {
        if (type === 1) {
          this.valueIdSelectTree = value
          this.handleFilter()
        } else {
          this.valueIdSelectTree2 = value
        }
      }
    }
  }
</script>

<style>
.cron-button-group {
    display: block;
    width: 150px!important;
    margin: 0 auto;
}
.showcode .el-dialog__header,.el-dialog__body {
    padding: 0 10px 0 0!important;
}
</style>
