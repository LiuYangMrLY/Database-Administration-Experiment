<template>
    <div>
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>课程表</el-breadcrumb-item>
        </el-breadcrumb>

        <el-row :gutter="20" class="searchRow">
            <el-col :span="12">
                <el-input placeholder="请输入内容" v-model="searchContent" class="input-with-select">
                    <el-select v-model="select" slot="prepend" placeholder="请选择">
                        <el-option label="课程号" value="1"></el-option>
                        <el-option label="课程名" value="2"></el-option>
                    </el-select>
                    <el-button slot="append" icon="el-icon-search" @click="searchCourse"></el-button>

                </el-input>
            </el-col>
            <el-col :span="6">
                <el-button type="primary" @click="showAddDialog">添加信息</el-button>
            </el-col>
        </el-row>

        <el-table :data="tableData" style="width: 100%">
            <el-table-column
                    prop="cno"
                    label="课程号"
                    width="150px">
            </el-table-column>
            <el-table-column
                    prop="name"
                    label="课程名"
                    width="">
            </el-table-column>
            <el-table-column
                    prop="cpno_name"
                    label="先修课"
                    width="">
            </el-table-column>
            <el-table-column
                    prop="credit"
                    label="学分"
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

        <el-dialog title="添加课程信息" :visible.sync="addDialogVisible" width="50%">
            <el-form :model="tempDialogForm" ref="editFormRef" label-width="70px">
                <el-form-item label="课程号">
                    <el-input v-model="tempDialogForm.cno"></el-input>
                </el-form-item>
                <el-form-item label="课程名">
                    <el-input v-model="tempDialogForm.name"></el-input>
                </el-form-item>
                <el-form-item label="先修课">
                    <el-select v-model="tempDialogForm.cpno" placeholder="请选择">
                        <el-option
                                v-for="item in courseOptions"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="学分">
                    <el-input v-model="tempDialogForm.credit"></el-input>
                </el-form-item>
            </el-form>

            <span slot="footer" class="dialog-footer">
                <el-button @click="addDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="addCourseInfo">确 定</el-button>
            </span>
        </el-dialog>

        <el-dialog title="修改课程信息" :visible.sync="editDialogVisible" width="50%">
            <el-form :model="tempDialogForm" ref="editFormRef" label-width="70px">
                <el-form-item label="课程号">
                    <el-input v-model="tempDialogForm.cno" disabled></el-input>
                </el-form-item>
                <el-form-item label="课程名">
                    <el-input v-model="tempDialogForm.name"></el-input>
                </el-form-item>
                <el-form-item label="先修课">
                    <el-select v-model="tempDialogForm.cpno" placeholder="请选择">
                        <el-option
                                v-for="item in courseOptions"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                                :disabled="item.value === tempDialogForm.cno">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="学分">
                    <el-input v-model="tempDialogForm.credit"></el-input>
                </el-form-item>
            </el-form>

            <span slot="footer" class="dialog-footer">
                <el-button @click="editDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="editCourseInfo">确 定</el-button>
            </span>
        </el-dialog>

        <el-dialog title="删除课程信息" :visible.sync="deleteDialogVisible" width="50%" class="deleteDialog">
            <el-row>
                <el-col :span="2" class="deleteDialogLabel">课程号</el-col>
                <el-col :span="4" class="deleteDialogContent">{{tempDialogForm.cno}}</el-col>
            </el-row>
            <el-row>
                <el-col :span="2" class="deleteDialogLabel">课程名</el-col>
                <el-col :span="4" class="deleteDialogContent">{{tempDialogForm.name}}</el-col>
            </el-row>
            <el-row>
                <el-col :span="2" class="deleteDialogLabel">先修课</el-col>
                <el-col :span="4" class="deleteDialogContent">{{tempDialogForm.cpno_name}}</el-col>
            </el-row>
            <el-row>
                <el-col :span="2" class="deleteDialogLabel">学分</el-col>
                <el-col :span="4" class="deleteDialogContent">{{tempDialogForm.credit}}</el-col>
            </el-row>

            <span slot="footer" class="dialog-footer">
                <el-button @click="deleteDialogVisible = false">取 消</el-button>
                <el-button type="danger" @click="deleteCourseInfo">删 除</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                searchContent: '',
                select: '1',

                tableData: [],
                courseOptions: [],
                tempDialogForm: {
                    index: null,
                    cno: null,
                    name: null,
                    cpno_name: null,
                    credit: null,
                    cpno: null,
                },

                addDialogVisible: false,
                editDialogVisible: false,
                deleteDialogVisible: false,
            }
        },
        methods: {
            showAddDialog() {
                this.tempDialogForm.index = null
                this.tempDialogForm.cno = null
                this.tempDialogForm.name = null
                this.tempDialogForm.cpno_name = null
                this.tempDialogForm.credit = null
                this.tempDialogForm.cpno = null

                this.addDialogVisible = true
            },
            showEditDialog(index, row) {
                this.tempDialogForm.index = index
                this.tempDialogForm.cno = row.cno
                this.tempDialogForm.name = row.name
                this.tempDialogForm.cpno_name = row.cpno_name
                this.tempDialogForm.credit = row.credit
                this.tempDialogForm.cpno = row.cpno

                this.editDialogVisible = true
            },
            showDeleteDialog(index, row) {
                this.tempDialogForm.index = index
                this.tempDialogForm.cno = row.cno
                this.tempDialogForm.name = row.name
                this.tempDialogForm.cpno_name = row.cpno_name
                this.tempDialogForm.credit = row.credit
                this.tempDialogForm.cpno = row.cpno

                this.deleteDialogVisible = true
            },

            refresh() {
                this.tableData = []
                this.$http.get('administration/get_courses')
                    .then(res => {
                        this.tableData = res.data['data']['courses']

                        for (let course of this.tableData) {
                            this.courseOptions.push({
                                'label': course.name,
                                'value': course.cno
                            })
                        }
                    })
            },

            addCourseInfo() {
                this.$http.post('administration/add_course',
                    JSON.stringify({
                        'cno': this.tempDialogForm.cno,
                        'name': this.tempDialogForm.name,
                        'cpno': this.tempDialogForm.cpno,
                        'credit': this.tempDialogForm.credit
                    }))
                    .then(res => {
                        if (res.data['code'] === undefined) {
                            this.$message.error('error')
                        } else if (res.data['code'] !== 200) {
                            this.$message.error(res.data['message'])
                        } else {
                            this.$message.success(res.data['message'])
                            this.addDialogVisible = false
                            this.refresh()
                        }
                    })
            },
            deleteCourseInfo() {
                this.$http.post('administration/delete_course',
                    JSON.stringify({'cno': this.tempDialogForm.cno}))
                    .then(res => {
                        if (res.data['code'] === undefined) {
                            this.$message.error('error')
                        } else if (res.data['code'] !== 200) {
                            this.$message.error(res.data['message'])
                        } else {
                            this.$message.success(res.data['message'])
                            this.deleteDialogVisible = false
                            this.refresh()
                        }
                    })
            },
            editCourseInfo() {
                let oldInfo = this.tableData[this.tempDialogForm.index]
                let newInfo = this.tempDialogForm

                if (oldInfo.cno === newInfo.cno
                    && oldInfo.name === newInfo.name
                    && oldInfo.cpno === newInfo.cpno
                    && oldInfo.credit === newInfo.credit) {

                    return this.editDialogVisible = false
                }


                this.$http.post('administration/edit_course',
                    JSON.stringify({
                        'cno': this.tempDialogForm.cno,
                        'name': this.tempDialogForm.name,
                        'cpno': this.tempDialogForm.cpno,
                        'credit': this.tempDialogForm.credit
                    }))
                    .then(res => {
                        if (res.data['code'] === undefined) {
                            this.$message.error('error')
                        } else if (res.data['code'] !== 200) {
                            this.$message.error(res.data['message'])
                        } else {
                            this.$message.success(res.data['message'])
                            this.editDialogVisible = false
                            this.refresh()
                        }
                    })
            },

            searchCourse() {
                if (this.searchContent === null || this.searchContent === '') {
                    this.$message.error('请输入搜索内容')
                    return
                }

                this.$http.get('administration/search_course', {
                    params: {
                        't': this.select,
                        'c': this.searchContent
                    }
                })
                    .then(res => {
                        this.tableData = res.data['data']['courses']
                    })
            },
        },
        created() {
            this.refresh()
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

    .deleteDialog .el-row {
        padding-left: 50px;
        height: 40px;
        line-height: 40px;
        border-bottom: 1px solid #e6e6e6;

        .deleteDialogContent {
            padding-left: 10px;
            height: 40px;
            width: 300px;
            text-align: center;
        }
    }
</style>
