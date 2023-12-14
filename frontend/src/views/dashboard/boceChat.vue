<template>
  <el-card class="box-card">
    <div slot="header" class="clearfix">
      <span class="card-span-title">拨测任务报表</span>
      <el-button style="float: right; padding: 3px 0" type="text">
        <el-date-picker
          v-model="selectdata"
          type="daterange"
          align="right"
          unlink-panels
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          :picker-options="pickerOptions"
          value-format="yyyy-MM-dd HH:mm:ss"
          @change="changeDate"
        ></el-date-picker>
      </el-button>
    </div>
    <el-row :gutter="32" v-loading="xxljob_loading">
      <el-col :xs="24" :sm="24" :lg="16">
        <div class="chart-wrapper">
          <bar-chart ref="bar" :optionData="baroptionData" />
        </div>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="8">
        <div class="chart-wrapper">
          <pie-chart ref="pie" :optionData="pieoptionData" />
        </div>
      </el-col>
    </el-row>
  </el-card>
</template>

<script>
import PieChart from "./components/PieChart";
import BarChart from "./components/BarChart";
import { c_xxljob } from "../../api/all";
import { FormatTime } from "@/utils/index";

export default {
  name: "bocechat",
  components: {
    PieChart,
    BarChart
  },
  data() {
    return {
      xxljob_loading: false,
      selectdata: ["", ""],
      pickerOptions: {
        shortcuts: [
          {
            text: "最近一周",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit("pick", [start, end]);
            }
          },
          {
            text: "最近一个月",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
              picker.$emit("pick", [start, end]);
            }
          },
          {
            text: "最近三个月",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
              picker.$emit("pick", [start, end]);
            }
          }
        ]
      },
      listQuery: {
        startDate: undefined,
        endDate: undefined
      },
      baroptionData: {
        title: {
          text: "日期分布图",
          left: "left"
        },
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "cross",
            label: {
              backgroundColor: "#6a7985"
            }
          }
        },
        legend: {
          data: ["成功", "失败", "进行中"]
        },
        toolbox: {
          feature: {
            saveAsImage: {}
          }
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true
        },
        xAxis: [
          {
            type: "category",
            boundaryGap: false,
            data: ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
          }
        ],
        yAxis: [
          {
            type: "value"
          }
        ],
        series: [
          {
            name: "成功",
            type: "line",
            stack: "总量",
            areaStyle: {},
            data: [120, 132, 101, 134, 90, 230, 210]
          },
          {
            name: "失败",
            type: "line",
            stack: "总量",
            areaStyle: {},
            data: [220, 182, 191, 234, 290, 330, 310]
          },
          {
            name: "进行中",
            type: "line",
            stack: "总量",
            areaStyle: {},
            data: [150, 232, 201, 154, 190, 330, 410]
          }
        ]
      },
      pieoptionData: {
        title: {
          text: "成败分布图",
          left: "left"
        },
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
          left: "center",
          top: "bottom",
          data: ["成功", "失败", "进行中"]
        },
        toolbox: {
          feature: {
            saveAsImage: {}
          }
        },
        calculable: true,
        series: [
          {
            name: "成败比例图",
            type: "pie",
            roseType: "radius",
            radius: [10, 80],
            center: ["50%", "50%"],
            data: [1, 2, 3],
            animationEasing: "cubicInOut",
            animationDuration: 1600
          }
        ]
      }
    };
  },
  computed: {},
  created() {
    const end = new Date();
    const start = new Date();
    start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
    this.listQuery.startDate = this.selectdata[0] = FormatTime(start);
    this.listQuery.endDate = this.selectdata[1] = FormatTime(end);
    this.fetchChat();
  },
  methods: {
    changeDate(val) {
      this.listQuery.startDate = val[0];
      this.listQuery.endDate = val[1];
      this.fetchChat();
    },
    fetchChat() {
      this.xxljob_loading = true;
      c_xxljob.chatinfo(this.listQuery).then(response => {
        this.xxljob_loading = false;
        const data = response.results.content;
        // bar
        this.baroptionData.xAxis[0].data = data.triggerDayList;
        this.baroptionData.series[0].data = data.triggerDayCountSucList;
        this.baroptionData.series[1].data = data.triggerDayCountFailList;
        this.baroptionData.series[2].data = data.triggerDayCountRunningList;
        this.$refs.bar.initChart();
        // pie
        this.pieoptionData.series[0].data = [
          { value: data.triggerCountSucTotal, name: "成功" },
          { value: data.triggerCountFailTotal, name: "失败" },
          { value: data.triggerCountRunningTotal, name: "进行中" }
        ];
        this.$refs.pie.initChart();
      });
    }
  }
};
</script>

<style lang="scss" scoped>
.box-card {
  background: linear-gradient(
      rgba(251, 252, 253, 0.9),
      rgba(251, 252, 253, 0.9)
    ),
    url("https://pbs.twimg.com/media/D1DLizJVsAAMgGX?format=jpg") no-repeat 0%
      20% / cover;
}
</style>
