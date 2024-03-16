<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { Select, Loading } from '@element-plus/icons-vue'

const form = reactive({
  sep: ',',
  encoding: 'utf-8'
})
const data = reactive({
  entity: '被审计单位',
  entitySelect: 'column',
  entityLanguage: 'EN',
  company: '',
  companySelect: '',
  journalNumber: '凭证编号',
  journalType: '',
  numberMdate: 'single',
  dateEntered: '',
  dateEffective: '记账时间',
  dateSelect: 'equal',
  userEnterd: '',
  userUpdated: '',
  userSelect: 'EN',
  ami: 'Manual',
  lineDesciption: '业务说明',
  currency: 'CNY',
  currencySelect: 'input',
  amount: '借方发生额|贷方发生额',
  amountSelect: 'dc',
  accountNumber: '科目编号',
  accountDescription: '科目名称',
  columns: '',
  oldChar: '',
  newChar: '',
  switchValue: false
})
const tableData = ref([])
const columns = ref([])
const isLoading = ref(false)
const isFinish = ref(false)
const isRuntime = ref(false)
const runtime = ref(0.0)

// 打开文件
function openFile() {
  isLoading.value = false
  isFinish.value = false
  isRuntime.value = false
  tableData.value = null
  columns.value = null
  window.pywebview.api.system_open_file(form.encoding, form.sep).then((res) => {
    const jsData = JSON.parse(res)
    tableData.value = jsData
    columns.value = Object.keys(jsData[0])
  })
}

// 生成模板
async function process() {
  ElMessage.info('开始运行')
  isLoading.value = true
  isFinish.value = false
  isRuntime.value = false
  console.log(data.switchValue)
  await window.pywebview.api.system_process(data.entity, data.entitySelect, data.entityLanguage, data.company, data.companySelect, data.journalNumber, data.journalType, data.numberMdate, data.dateEntered, data.dateEffective, data.dateSelect, data.userEnterd, data.userUpdated, data.userSelect, data.ami, data.lineDesciption, data.currency, data.currencySelect, data.amount, data.amountSelect, data.accountNumber, data.accountDescription, data.switchValue).then((err) => {
    if (err != null) {
      isLoading.value = false
      isFinish.value = true
      isRuntime.value = true
      runtime.value = err
      ElMessage.error(err)
    } else {
      isLoading.value = false
      isFinish.value = true
      isRuntime.value = true
      ElMessage.success('模板已生成')
    }
  })
}

// 生成指定列模板
async function processF() {
  ElMessage.info('开始运行')
  isLoading.value = true
  isFinish.value = false
  isRuntime.value = false
  console.log(data.switchValue)
  await window.pywebview.api.system_process_specific(data.entity, data.entitySelect, data.entityLanguage, data.company, data.companySelect, data.journalNumber, data.journalType, data.numberMdate, data.dateEntered, data.dateEffective, data.dateSelect, data.userEnterd, data.userUpdated, data.userSelect, data.lineDesciption, data.currency, data.currencySelect, data.amount, data.amountSelect, data.accountNumber, data.accountDescription, data.switchValue).then((err) => {
    if (err != null) {
      isLoading.value = false
      isFinish.value = true
      isRuntime.value = true
      runtime.value = err
      ElMessage.error(err)
    } else {
      isLoading.value = false
      isFinish.value = true
      isRuntime.value = true
      ElMessage.success('模板已生成')
    }
  })
}

// 中文转拼音
async function cn2pinyin() {
  ElMessage.info('开始运行')
  isLoading.value = true
  isFinish.value = false
  isRuntime.value = false
  await window.pywebview.api.system_cn2pinyin(data.columns).then((res) => {
    if (res != null) {
      isLoading.value = false
      isFinish.value = true
      isRuntime.value = true
      runtime.value = res
      ElMessage.error(res)
    } else {
      isLoading.value = false
      isFinish.value = true
      isRuntime.value = true
      ElMessage.success('运行结束')
    }
  })
}

// 替换特殊符号
async function replChar() {
  ElMessage.info('开始运行')
  isLoading.value = true
  isFinish.value = false
  isRuntime.value = false
  await window.pywebview.api.system_repl_char(data.columns).then((res) => {
    if (res != null) {
      isLoading.value = false
      isFinish.value = true
      isRuntime.value = true
      runtime.value = res
      ElMessage.error(res)
    } else {
      isLoading.value = false
      isFinish.value = true
      isRuntime.value = true
      ElMessage.success('运行结束')
    }
  })
}

// 替换指定符号
async function replSfChar() {
  ElMessage.info('开始运行')
  isLoading.value = true
  isFinish.value = false
  isRuntime.value = false
  await window.pywebview.api.system_repl_sf_char(data.columns, data.oldChar, data.newChar).then((res) => {
    if (res != null) {
      isLoading.value = false
      isFinish.value = true
      isRuntime.value = true
      runtime.value = res
      ElMessage.error(res)
    } else {
      isLoading.value = false
      isFinish.value = true
      isRuntime.value = true
      ElMessage.success('运行结束')
    }
  })
}
</script>

<template>
  <el-row :gutter="24">
    <el-col :span="8">
      <el-form-item label="Entity">
        <el-input v-model="data.entity" placeholder="Entity" clearable>
          <template #prepend>
            <el-select v-model="data.entitySelect" style="width: 100px">
              <el-option label="column" value="column" />
              <el-option label="input" value="input" />
            </el-select>
          </template>
        </el-input>
      </el-form-item>
    </el-col>
    <el-col :span="8">
      <el-form-item label="Company">
        <el-input v-model="data.company" placeholder="Company" clearable>
          <template #prepend>
            <el-select v-model="data.companySelect" style="width: 100px">
              <el-option label="column" value="column" />
              <el-option label="input" value="input" />
            </el-select>
          </template>
        </el-input>
      </el-form-item>
    </el-col>
    <el-col :span="8">
      <el-form-item label="EntityLanguage">
        <el-select v-model="data.entityLanguage" style="width: 100px">
          <el-option label="EN" value="EN" />
          <el-option label="CN" value="CN" />
        </el-select>
      </el-form-item>
    </el-col>
  </el-row>
  <el-row :gutter="24">
    <el-col :span="8">
      <el-form-item label="Journal Number">
        <el-input v-model="data.journalNumber" placeholder="Journal Number" clearable>
          <template #prepend>
            <el-select v-model="data.numberMdate" style="width: 100px">
              <el-option label="single" value="single" />
              <el-option label="multi" value="multi" />
            </el-select>
          </template>
        </el-input>
      </el-form-item>
    </el-col>
    <el-col :span="8">
      <el-form-item label="Date Entered">
        <el-input v-model="data.dateEntered" placeholder="Date Entered" clearable>
          <template #prepend>
            <el-select v-model="data.dateSelect" style="width: 100px">
              <el-option label="equal" value="equal" />
              <el-option label="not equal" value="nequal" />
            </el-select>
          </template>
        </el-input>
      </el-form-item>
    </el-col>
    <el-col :span="8">
      <el-form-item label="Date Effective">
        <el-input v-model="data.dateEffective" placeholder="Date Effective" clearable>
          <template #prepend>
            <el-select v-model="data.dateSelect" style="width: 100px">
              <el-option label="equal" value="equal" />
              <el-option label="not equal" value="nequal" />
            </el-select>
          </template>
        </el-input>
      </el-form-item>
    </el-col>
  </el-row>
  <el-row :gutter="24">
    <el-col :span="8">
      <el-form-item label="Journal Type">
        <el-input v-model="data.journalType" placeholder="Journal Type" clearable> </el-input>
      </el-form-item>
    </el-col>
    <el-col :span="8">
      <el-form-item label="UserID Entered">
        <el-input v-model="data.userEnterd" placeholder="UserID Entered" clearable>
          <template #prepend>
            <el-select v-model="data.userSelect" style="width: 100px">
              <el-option label="CN" value="CN" />
              <el-option label="EN" value="EN" />
            </el-select>
          </template>
        </el-input>
      </el-form-item>
    </el-col>
    <el-col :span="8">
      <el-form-item label="UserID Updated">
        <el-input v-model="data.userUpdated" placeholder="UserID Updated" clearable>
          <template #prepend>
            <el-select v-model="data.userSelect" style="width: 100px">
              <el-option label="CN" value="CN" />
              <el-option label="EN" value="EN" />
            </el-select>
          </template>
        </el-input>
      </el-form-item>
    </el-col>
  </el-row>
  <el-row :gutter="24">
    <el-col :span="8">
      <el-form-item label="Auto Manual Interface">
        <el-input v-model="data.ami" placeholder="Auto Manual Interface" clearable />
      </el-form-item>
    </el-col>
    <el-col :span="8">
      <el-form-item label="Line Description">
        <el-input v-model="data.lineDesciption" placeholder="Line Description" clearable />
      </el-form-item>
    </el-col>
    <el-col :span="8">
      <el-form-item label="Currency">
        <el-input v-model="data.currency" placeholder="Currency" clearable>
          <template #prepend>
            <el-select v-model="data.currencySelect" style="width: 100px">
              <el-option label="column" value="column" />
              <el-option label="input" value="input" />
            </el-select>
          </template>
        </el-input>
      </el-form-item>
    </el-col>
  </el-row>
  <el-row :gutter="24">
    <el-col :span="8">
      <el-form-item label="Amount">
        <el-input v-model="data.amount" placeholder="Signed Amount EC" clearable>
          <template #prepend>
            <el-select v-model="data.amountSelect" style="width: 100px">
              <el-option label="amount" value="amount" />
              <el-option label="d|c" value="dc" />
            </el-select>
          </template>
        </el-input>
      </el-form-item>
    </el-col>
    <el-col :span="8">
      <el-form-item label="Account Number">
        <el-input v-model="data.accountNumber" placeholder="Account Number" clearable />
      </el-form-item>
    </el-col>
    <el-col :span="8">
      <el-form-item label="Account Description">
        <el-input v-model="data.accountDescription" placeholder="Account Description" clearable />
      </el-form-item>
    </el-col>
  </el-row>
  <el-row :gutter="24" class="custom-sep-enc">
    <el-col :span="8">
      <el-form-item label="Entity">
        <el-switch v-model="data.switchValue" class="mb-2" active-text="multi" inactive-text="single" />
      </el-form-item>
    </el-col>
    <el-col :span="8">
      <el-form-item label="Separator" style="width: 180px;">
        <el-select v-model="form.sep">
          <el-option label="," value="," />
          <el-option label="|" value="|" />
          <el-option label="\t" value="\\t" />
          <el-option label=";" value=";" />
        </el-select>
      </el-form-item>
    </el-col>
    <el-col :span="8">
      <el-form-item label="Encoding" style="width: 180px;">
        <el-select v-model="form.encoding">
          <el-option label="utf-8" value="utf-8" />
          <el-option label="utf_8_sig" value="utf_8_sig" />
          <el-option label="gbk" value="gbk" />
          <el-option label="utf-16le" value="utf-16le" />
        </el-select>
      </el-form-item>
    </el-col>
  </el-row>
  <!-- 操作按钮 -->
  <el-row :gutter="24">
    <el-col :span="24">
      <el-button type="primary" @click="openFile">open file</el-button>
      <el-button type="success" @click="process">process</el-button>
      <el-button type="success" @click="processF">procespf</el-button>
      <div class="icon-group">
        <el-icon v-if="isLoading" color="#FF4500" class="is-loading">
          <Loading />
        </el-icon>
        <el-icon v-if="isFinish" color="#32CD32">
          <Select />
        </el-icon>
        <el-text v-if="isRuntime" :style="{ color: '#32CD32', fontSize: '20px' }">{{ runtime }}</el-text>
      </div>
    </el-col>
  </el-row>
  <el-table :data="tableData" height="400" style="width: 100%">
    <el-table-column v-for="column in columns" :key="column" :prop="column" :label="column"></el-table-column>
  </el-table>
  <el-row :gutter="28">
    <el-col :span="12">
      <el-form-item label="columns" class="custom-columns">
        <el-input v-model="data.columns" placeholder="A|B|C" clearable />
      </el-form-item>
    </el-col>
    <el-col :span="12">
      <el-button type="primary" @click="cn2pinyin">CN2Pinyin</el-button>
      <el-button type="primary" @click="replChar">ReplChar</el-button>
    </el-col>
  </el-row>
  <el-row :gutter="20">
    <el-col :span="8">
      <el-form-item label="old char" class="custom-char">
        <el-input v-model="data.oldChar" placeholder=" -  " clearable />
      </el-form-item>
    </el-col>
    <el-col :span="8">
      <el-form-item label="new char" class="custom-char">
        <el-input v-model="data.newChar" placeholder="0" clearable />
      </el-form-item>
    </el-col>
    <el-col :span="8">
      <el-button type="primary" @click="replSfChar">ReplSfChar</el-button>
    </el-col>
  </el-row>
</template>

<style>
.custom-sep-enc {
  width: 550px !important;
}
.custom-columns {
  width: 250px !important;
}
.custom-char {
  width: 150px !important;
}
</style>
