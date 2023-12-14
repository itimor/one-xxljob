<template>
  <el-row :gutter="40" class="panel-group">
    <el-col v-loading="domain_loading" :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel">
        <div class="card-panel-icon-wrapper icon-people">
          <svg-icon icon-class="peoples" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">总域名数</div>
          <count-to :start-val="0" :end-val="domain_total" :duration="2600" class="card-panel-num" />
        </div>
      </div>
    </el-col>
    <el-col v-loading="boce_loading" :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel">
        <div class="card-panel-icon-wrapper icon-message">
          <svg-icon icon-class="message" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">总拨测任务</div>
          <count-to :start-val="0" :end-val="boce_total" :duration="3000" class="card-panel-num" />
        </div>
      </div>
    </el-col>
    <el-col v-loading="group_loading" :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel">
        <div class="card-panel-icon-wrapper icon-money">
          <svg-icon icon-class="money" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">拨测执行器</div>
          <count-to :start-val="0" :end-val="group_total" :duration="3200" class="card-panel-num" />
        </div>
      </div>
    </el-col>
    <el-col v-loading="log_loading" :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel">
        <div class="card-panel-icon-wrapper icon-shopping">
          <svg-icon icon-class="shopping" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">本周执行任务数</div>
          <count-to :start-val="0" :end-val="log_total" :duration="3600" class="card-panel-num" />
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script>
import CountTo from "vue-count-to";
import { domain, xxljob, c_xxljob } from "@/api/all";

export default {
  components: {
    CountTo
  },
  data() {
    return {
      domain_total: 0,
      domain_loading: false,
      boce_total: 0,
      boce_loading: false,
      group_total: 0,
      group_loading: false,
      log_total: 0,
      log_loading: false,
      listQuery: {}
    };
  },
  created() {
    this.getDomainList();
    this.getBoceList();
    this.getBoceGroupList();
    this.getLogCountList();
  },
  methods: {
    getDomainList() {
      this.domain_loading = true;
      domain.requestGet().then(response => {
        this.domain_loading = false;
        this.domain_total = response.results.length;
      });
    },
    getBoceList() {
      this.boce_loading = true;
      xxljob.requestGet().then(response => {
        this.boce_loading = false;
        this.boce_total = response.results.length;
      });
    },
    getBoceGroupList() {
      this.group_loading = true;
      c_xxljob.get_group().then(response => {
        this.group_loading = false;
        this.group_total = response.results.length;
      });
    },
    getLogCountList() {
      this.log_loading = true;
      c_xxljob.get_log_count().then(response => {
        this.log_loading = false;
        this.log_total = response.results;
      });
    }
  }
};
</script>

<style lang="scss" scoped>
.panel-group {
  margin-top: 18px;
  .card-panel-col {
    margin-bottom: 32px;
  }
  .card-panel {
    height: 108px;
    cursor: pointer;
    font-size: 12px;
    position: relative;
    overflow: hidden;
    color: #666;
    background: #fff;
    box-shadow: 4px 4px 40px rgba(0, 0, 0, 0.05);
    border-color: rgba(0, 0, 0, 0.05);
    &:hover {
      .card-panel-icon-wrapper {
        color: #fff;
      }
      .icon-people {
        background: #40c9c6;
      }
      .icon-message {
        background: #36a3f7;
      }
      .icon-money {
        background: #f4516c;
      }
      .icon-shopping {
        background: #34bfa3;
      }
    }
    .icon-people {
      color: #40c9c6;
    }
    .icon-message {
      color: #36a3f7;
    }
    .icon-money {
      color: #f4516c;
    }
    .icon-shopping {
      color: #34bfa3;
    }
    .card-panel-icon-wrapper {
      float: left;
      margin: 14px 0 0 14px;
      padding: 16px;
      transition: all 0.38s ease-out;
      border-radius: 6px;
    }
    .card-panel-icon {
      float: left;
      font-size: 48px;
    }
    .card-panel-description {
      float: right;
      font-weight: bold;
      margin: 26px;
      margin-left: 0px;
      .card-panel-text {
        line-height: 18px;
        color: rgba(0, 0, 0, 0.45);
        font-size: 16px;
        margin-bottom: 12px;
      }
      .card-panel-num {
        font-size: 20px;
      }
    }
  }
}
</style>
