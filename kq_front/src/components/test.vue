<template>

    <div class="box">
        <div class="title">Control Panel</div>

        <el-descriptions :column="1">
            <el-descriptions-item label="总节点数">kooriookami</el-descriptions-item>
            <el-descriptions-item label="总关系数">18100000000</el-descriptions-item>
            <el-descriptions-item label="总社区数">Suzhou</el-descriptions-item>
            <el-descriptions-item label="总实体数">
                No.1188, Wuzhong Avenue, Wuzhong District, Suzhou, Jiangsu Province
            </el-descriptions-item>
        </el-descriptions>
        <hr>
        <div class="slider-demo-block">
            <span class="demonstration">Scale</span>
            <el-slider v-model="value1" :step="10" />
        </div>


        <!-- 滑块 -->
        <div class="slider-demo-block">
            <span class="demonstration">Scale</span>
            <el-slider v-model="value1" :step="10" />
        </div>
        <!-- 节点信息表示 -->
        <el-table :data="tableData" stripe style="width: 100%">
            <el-table-column prop="date" label="Date" width="180" />
            <el-table-column prop="name" label="Name" width="180" />
            <el-table-column prop="address" label="Address" />
        </el-table>



    </div>



</template>

<script>
import { column } from 'element-plus/es/components/table-v2/src/common'
import { ref, watch } from 'vue'




export default {
    setup() {
        const value1 = ref(0)
        const tableData = [
            {
                date: '2016-05-03',
                name: 'Tom',
                address: 'No. 189, Grove St, Los Angeles',
            },
            {
                date: '2016-05-02',
                name: 'Tom',
                address: 'No. 189, Grove St, Los Angeles',
            },
            {
                date: '2016-05-04',
                name: 'Tom',
                address: 'No. 189, Grove St, Los Angeles',
            },
            {
                date: '2016-05-01',
                name: 'Tom',
                address: 'No. 189, Grove St, Los Angeles',
            },
        ]


        watch(
            () => value1.value,
            (newValue) => {
                console.log(newValue);

            },
            { immediate: true }
        )

        return {
            value1,
            tableData
        }
    }
}
</script>

<style scoped>
.box {
    width: max-content;
    height: 90vh;
    /* background-color: #f0f0f0; */
    border: 0.5px solid #333;
    border-radius: 5px;
    /* 圆角的大小 */
    padding: 10px;
}

.title {
    font-size: 16px;
    font-weight: bold;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #cbccce;
    width: max-content*0.8;

}

.el-descriptions {
    margin-top: 20px;
}

.slider-demo-block {
    max-width: 300px;
    display: flex;
    align-items: center;
}

.slider-demo-block .el-slider {
    margin-top: 0;
    margin-left: 8px;
}

.slider-demo-block .demonstration {
    font-size: 14px;
    line-height: 44px;
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    margin-bottom: 0;
}

.slider-demo-block .demonstration+.el-slider {
    flex: 0 0 80%;
}
</style>