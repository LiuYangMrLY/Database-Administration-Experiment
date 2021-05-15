<template>
    <div>
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>学生表</el-breadcrumb-item>
        </el-breadcrumb>

        <el-row :gutter="20" class="searchRow">
            <el-col :span="12">
                <el-input placeholder="请输入内容" v-model="searchContent" class="input-with-select">
                    <el-select v-model="select" slot="prepend" placeholder="请选择">
                        <el-option label="学号" value="1"></el-option>
                        <el-option label="姓名" value="2"></el-option>
                        <el-option label="系" value="3"></el-option>
                    </el-select>
                    <el-button slot="append" icon="el-icon-search" @click="searchStudent"></el-button>

                </el-input>
            </el-col>
            <el-col :span="6">
                <el-button type="primary" @click="showAddDialog">添加信息</el-button>
            </el-col>
        </el-row>

        <el-table :data="tableData" style="width: 100%">
            <el-table-column
                    prop="no"
                    label="学号"
                    width="">
            </el-table-column>
            <el-table-column
                    prop="name"
                    label="姓名"
                    width="">
            </el-table-column>
            <el-table-column
                    prop="gender"
                    label="性别"
                    width="">
            </el-table-column>
            <el-table-column
                    prop="age"
                    label="年龄"
                    width="">
            </el-table-column>
            <el-table-column
                    prop="department"
                    label="系"
                    width="">
            </el-table-column>

            <el-table-column label="操作">
                <template slot-scope="scope">
                    <el-button
                            size="mini"
                            @click="showEditDialog(scope.$index, scope.row)">编辑
                    </el-button>
                    <el-button
                            size="mini"
                            type="danger"
                            @click="showDeleteDialog(scope.$index, scope.row)">删除
                    </el-button>
                </template>
            </el-table-column>
        </el-table>

        <el-pagination
                @current-change="handleCurrentChange"
                :current-page.sync="currentPage"
                :page-count="totalPage"
                layout="prev, pager, next, jumper"
                :hide-on-single-page="hideOnSingle">
        </el-pagination>

        <el-dialog title="添加学生信息" :visible.sync="addDialogVisible" width="50%">
            <el-form :model="tempDialogForm" ref="editFormRef" label-width="50px">
                <el-form-item label="学号">
                    <el-input v-model="tempDialogForm.no"></el-input>
                </el-form-item>
                <el-form-item label="姓名">
                    <el-input v-model="tempDialogForm.name"></el-input>
                </el-form-item>
                <el-form-item label="性别">
                    <el-select v-model="tempDialogForm.gender" placeholder="请选择">
                        <el-option
                                v-for="item in genderOptions"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="年龄">
                    <el-input v-model="tempDialogForm.age"></el-input>
                </el-form-item>
                <el-form-item label="系">
                    <el-input v-model="tempDialogForm.department"></el-input>
                </el-form-item>
            </el-form>

            <span slot="footer" class="dialog-footer">
                <el-button @click="addDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="addStudentInfo">确 定</el-button>
            </span>
        </el-dialog>

        <el-dialog title="修改学生信息" :visible.sync="editDialogVisible" width="50%">
            <el-form :model="tempDialogForm" ref="editFormRef" label-width="50px">
                <el-form-item label="学号">
                    <el-input v-model="tempDialogForm.no" disabled></el-input>
                </el-form-item>
                <el-form-item label="姓名">
                    <el-input v-model="tempDialogForm.name"></el-input>
                </el-form-item>
                <el-form-item label="性别">
                    <el-select v-model="tempDialogForm.gender" placeholder="请选择">
                        <el-option
                                v-for="item in genderOptions"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="年龄">
                    <el-input v-model="tempDialogForm.age"></el-input>
                </el-form-item>
                <el-form-item label="系">
                    <el-input v-model="tempDialogForm.department"></el-input>
                </el-form-item>
            </el-form>

            <span slot="footer" class="dialog-footer">
                <el-button @click="editDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="editStudentInfo">确 定</el-button>
            </span>
        </el-dialog>

        <el-dialog title="删除学生信息" :visible.sync="deleteDialogVisible" width="50%" class="deleteDialog">
            <el-row>
                <el-col :span="2" class="deleteDialogLabel">学号</el-col>
                <el-col :span="4" class="deleteDialogContent">{{tempDialogForm.no}}</el-col>
            </el-row>
            <el-row>
                <el-col :span="2" class="deleteDialogLabel">姓名</el-col>
                <el-col :span="4" class="deleteDialogContent">{{tempDialogForm.name}}</el-col>
            </el-row>
            <el-row>
                <el-col :span="2" class="deleteDialogLabel">性别</el-col>
                <el-col :span="4" class="deleteDialogContent">{{tempDialogForm.gender}}</el-col>
            </el-row>
            <el-row>
                <el-col :span="2" class="deleteDialogLabel">年龄</el-col>
                <el-col :span="4" class="deleteDialogContent">{{tempDialogForm.age}}</el-col>
            </el-row>
            <el-row>
                <el-col :span="2" class="deleteDialogLabel">系</el-col>
                <el-col :span="4" class="deleteDialogContent">{{tempDialogForm.department}}</el-col>
            </el-row>

            <span slot="footer" class="dialog-footer">
                <el-button @click="deleteDialogVisible = false">取 消</el-button>
                <el-button type="danger" @click="deleteStudentInfo">删 除</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                tableData: [],
                genderOptions: [
                    {
                        value: '男',
                        label: '男'
                    }, {
                        value: '女',
                        label: '女'
                    }
                ],

                searchContent: '',
                select: '1',

                // pagination
                currentPage: 1,
                totalPage: 1,
                hideOnSingle: false,

                // dialog
                addDialogVisible: false,
                editDialogVisible: false,
                deleteDialogVisible: false,
                tempDialogForm: {
                    index: null,
                    no: null,
                    name: null,
                    gender: null,
                    age: null,
                    department: null
                }
            }
        },
        methods: {
            handleCurrentChange(currentPage) {
                this.$http.get('administration/get_students', {
                    params: {'current_page': currentPage}
                })
                    .then(res => {
                        this.tableData = res.data['data']['students']
                        this.currentPage = res.data['data']['current_page']
                        this.totalPage = res.data['data']['total_page']
                    })
            },
            searchStudent() {
                if (this.searchContent === null || this.searchContent === '') {
                    this.$message.error('请输入搜索内容')
                    return
                }

                this.$http.get('administration/search_student', {
                    params: {
                        't': this.select,
                        'c': this.searchContent
                    }
                })
                    .then(res => {
                        this.tableData = res.data['data']['students']
                        this.currentPage = 1
                        this.totalPage = 1
                        this.hideOnSingle = true
                    })
            },

            showAddDialog() {
                this.tempDialogForm.index = null
                this.tempDialogForm.no = null
                this.tempDialogForm.name = null
                this.tempDialogForm.gender = null
                this.tempDialogForm.age = null
                this.tempDialogForm.department = null

                this.addDialogVisible = true;
            },
            showEditDialog(index, row) {
                this.tempDialogForm.index = index
                this.tempDialogForm.no = row.no
                this.tempDialogForm.name = row.name
                this.tempDialogForm.gender = row.gender
                this.tempDialogForm.age = row.age
                this.tempDialogForm.department = row.department

                this.editDialogVisible = true
            },
            showDeleteDialog(index, row) {
                this.tempDialogForm.index = index
                this.tempDialogForm.no = row.no
                this.tempDialogForm.name = row.name
                this.tempDialogForm.gender = row.gender
                this.tempDialogForm.age = row.age
                this.tempDialogForm.department = row.department

                this.deleteDialogVisible = true
            },

            addStudentInfo() {
                this.$http.post('administration/add_student',
                    JSON.stringify({
                        'sno': this.tempDialogForm.no,
                        'name': this.tempDialogForm.name,
                        'gender': this.tempDialogForm.gender,
                        'age': this.tempDialogForm.age,
                        'department': this.tempDialogForm.department
                    }))
                    .then(res => {
                        if (res.data['code'] === undefined) {
                            this.$message.error('error')
                        } else if (res.data['code'] !== 200) {
                            this.$message.error(res.data['message'])
                        } else {
                            this.$message.success(res.data['message'])
                            this.handleCurrentChange(this.currentPage)
                            this.addDialogVisible = false
                        }
                    })
            },
            deleteStudentInfo() {
                this.$http.post('administration/delete_student',
                    JSON.stringify({'sno': this.tempDialogForm.no}))
                    .then(res => {
                        if (res.data['code'] === undefined) {
                            this.$message.error('error')
                        } else if (res.data['code'] !== 200) {
                            this.$message.error(res.data['message'])
                        } else {
                            this.$message.success(res.data['message'])
                            this.handleCurrentChange(this.currentPage)
                            this.deleteDialogVisible = false
                        }
                    })
            },
            editStudentInfo() {
                let oldInfo = this.tableData[this.tempDialogForm.index]
                let newInfo = this.tempDialogForm

                if (oldInfo.name === newInfo.name
                    && oldInfo.gender === newInfo.gender
                    && oldInfo.age === newInfo.age
                    && oldInfo.department === newInfo.department) {
                    return this.editDialogVisible = false
                }

                this.$http.post('administration/edit_student',
                    JSON.stringify({
                        "sno": this.tempDialogForm.no,
                        "name": this.tempDialogForm.name,
                        "gender": this.tempDialogForm.gender,
                        "age": this.tempDialogForm.age,
                        "department": this.tempDialogForm.department
                    }))
                    .then(res => {
                        if (res.data['code'] === undefined) {
                            this.$message.error('error')
                        } else if (res.data['code'] !== 200) {
                            this.$message.error(res.data['message'])
                        } else {
                            this.$message.success(res.data['message'])
                            this.handleCurrentChange(this.currentPage)
                            this.editDialogVisible = false
                        }
                    })
            },
        },
        created() {
            // 默认请求 第一页数据
            this.$http.get('administration/get_students')
                .then(res => {
                    this.tableData = res.data['data']['students']
                    this.currentPage = res.data['data']['current_page']
                    this.totalPage = res.data['data']['total_page']
                })
        }
    }
</script>

<style lang="less" scoped>
    .el-breadcrumb {
        padding-bottom: 15px;
    }

    .el-select {
        width: 130px;
    }

    .searchRow {
        padding-top: 5px;
        padding-bottom: 5px;
    }

    .input-with-select .el-input-group__prepend {
        background-color: #fff;
    }

    .deleteDialog .el-row {
        padding-left: 50px;
        height: 40px;
        line-height: 40px;
        border-bottom: 1px solid #e6e6e6;

        .deleteDialogLabel {
            padding-left: 20px;
            padding-right: 20px;
            width: 70px;
            height: 40px;
            text-align: center;
        }

        .deleteDialogContent {
            padding-left: 10px;
            height: 40px;
            width: 300px;
            text-align: center;

        }
    }

    .el-pagination {
        position: absolute;
        bottom: 20px;
    }

</style>
