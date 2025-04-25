<template>
    <div class="detail">
        <div class="title">Control Panel</div>
        <el-descriptions :column="1">
            <el-descriptions-item label="总节点数">{{ controlMsg.x }}</el-descriptions-item>
            <el-descriptions-item label="总关系数">{{ controlMsg.y }}</el-descriptions-item>
            <el-descriptions-item label="总实体类型数">{{ entityNum }}</el-descriptions-item>
        </el-descriptions>
        <hr>
        <div class="selection">
            <span class="demonstration">Selection</span>
            <div class="btn">
                <el-button v-show="networkFlag" @click="netStart" type="primary">NetWork</el-button>
                <el-button v-show="topicFlag" @click="topicStart" type="success">Topic Info</el-button>
                <el-button v-show="backFlag" @click="backToPanel" type="warning">Back</el-button>
            </div>
        </div>
        <div class="title">Info Panel</div>
        <!-- 节点信息表示 -->
        <div style="margin-top: 5px;border-bottom: 1px solid #000;" v-show="cardFlag"
            v-if="typeof nodeMsg === 'object'">Node Info Tabel</div>
        <div style="margin-top: 5px;border-bottom: 1px solid #000;" v-show="cardFlag" v-else>Topic Info Tabel</div>
        <div class="demain" v-show="cardFlag">
            <div v-if="typeof nodeMsg === 'object'">
                <el-table :data="nodeInfo" stripe style="width: 100%">
                    <el-table-column prop="key" width="80" />
                    <el-table-column prop="value" />
                </el-table>
            </div>
            <div v-else style="width: 300px; font-size: 16px; white-space: pre-wrap;">
                {{ nodeMsg }}
            </div>
        </div>
        <!-- 词云 -->
        <div style="margin-top: 5px;border-bottom: 1px solid #000;" v-show="cardFlag">Keywords Tabel</div>
        <KeyWordsCloud :msg="msg" />
    </div>


    <!-- <div class="nodeCard">
        <el-container>
            <el-header class="header">DetailPanel</el-header>
            <div class="demain" v-show="cardFlag">
                <table>
                    <tbody>
                        <tr v-if="typeof nodeMsg === 'object'" v-for="(v, k) in nodeMsg">
                            <td>{{ k }}</td>
                            <td>{{ v }}</td>
                        </tr>
                        <tr v-else>
                            <td style="width: 300px; font-size: 14px; white-space: pre-wrap;">{{ nodeMsg }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="btnController">
                <div class="mb-4">
                    <el-button v-show="networkFlag" @click="netStart" type="primary">NetWork</el-button>
                    <el-button v-show="topicFlag" @click="topicStart" type="success">Topic Info</el-button>
                    <el-button v-show="backFlag" @click="backToPanel" type="warning">Back</el-button>
                </div>
            </div>
        </el-container>
    </div> -->

</template>
<script>
import KeyWordsCloud from "./KeyWordsCloud.vue";
import linkInfo from '../../../output_data/topicInfoJson.json'
import { ref, watch } from 'vue'
export default {
    components: {
        KeyWordsCloud
    },
    props: {
        msg: Object,
        control: Object,
    },
    emits: ["sendNet", "sendTopic", "backPanel"],
    setup(props, { emit }) {
        const nodeMsg = ref(props.msg)
        const controlMsg = ref(props.control)
        const networkFlag = ref(false)
        const topicFlag = ref(false)
        const cardFlag = ref(false)
        const backFlag = ref(false)
        const linkData = ref(linkInfo)
        const entityNum = ref(3)

        const value1 = ref(0)
        const nodeInfo = ref(null)

        function msgToObj(obj) {
            nodeInfo.value = Object.entries(obj).map(([key, value]) => ({
                key,
                value
            }));
            console.log(nodeInfo.value);

        }

        watch(
            () => props.msg,
            (newValue) => {
                if (newValue !== null) {
                    cardFlag.value = true
                    if (newValue.id !== "") {
                        nodeMsg.value = newValue;
                        msgToObj(nodeMsg.value)
                        if (newValue.group === 1) {
                            if (backFlag.value != true) {
                                if (newValue.cluster !== 0)
                                    topicFlag.value = true
                                else
                                    topicFlag.value = false
                                networkFlag.value = false
                            }
                        }
                        else if (newValue.group === 2 || newValue.group === 3) {
                            topicFlag.value = false
                            networkFlag.value = true
                        }
                        else {
                            // console.log("是link");
                            nodeMsg.value = linkData.value[newValue.cluster][newValue.topic]
                            // console.log(linkData.value[newValue.cluster][newValue.topic]);
                        }
                    }

                    // delete nodeMsg.value.group;
                    console.log("show:", nodeMsg.value);

                    // console.log(topicFlag.value);
                }
            },
            { immediate: true }
        );

        function netStart() {
            console.log(nodeMsg.value.cluster);
            emit("sendNet", nodeMsg.value.group, nodeMsg.value.cluster)
        }

        function topicStart() {
            entityNum.value = 1
            console.log(nodeMsg.value.cluster);

            emit("sendTopic", nodeMsg.value.cluster)
            topicFlag.value = false
            backFlag.value = true
        }

        function backToPanel() {
            entityNum.value = 3
            topicFlag.value = true
            backFlag.value = false
            emit("backPanel");
        }

        return {
            nodeMsg,
            networkFlag,
            topicFlag,
            netStart,
            cardFlag,
            topicStart,
            backFlag,
            backToPanel,
            linkData,
            value1,
            nodeInfo,
            controlMsg,
            entityNum
        }
    }

}
</script>

<style scoped>
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

/* .slider-demo-block {
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
    flex: 0 0 70%;
} */

.selection {
    max-width: 500px;
    display: flex;
    align-items: center;
}

.selection .demonstration {
    flex: 1;
    font-size: 14px;
    line-height: 44px;
    margin-bottom: 0;
}

.selection .demonstration+.btn {
    flex: 0 0 70%;
}

.demain {
    width: 100%;
    height: 20vh;
    overflow-y: scroll;
}

/* 分隔 */

/* .nodeCard {
    height: 50vh;
    width: 100%;
    border: 2px solid #000;
    text-align: center;
    font-size: 18px;
} */

/* .header {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 10vh;
    background-color: rgba(128, 128, 128, 0.6);
} */

/* .elmain {
    height: 40vh;

} */

/* .demain {
    width: 100%;
    height: 30vh;
    overflow-y: scroll;
} */

/* td {
    font-size: 12px;
    text-align: left;
    border-bottom: 1px solid #aaa;
    width: 200px;
    word-break: break-word;
} */

/* .btnController {
    height: 10vh;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
} */
</style>