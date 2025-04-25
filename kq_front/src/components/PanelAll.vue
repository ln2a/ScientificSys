<template>
    <!-- <h3>全局面板</h3> -->
    <div class="Panel">
        <div class="leftBox">
            <div class="cardPanel">
                <DetailPanel :msg="nodeMsg" :control="controlMsg" @sendNet="netShow" @send-topic="topicShow"
                    @back-panel="backPanel" />
            </div>
            <!-- <div class="cloudpanel"> -->
            <!-- <KeyWordsCloud :msg="nodeMsg" /> -->
            <!-- </div> -->
        </div>
        <div class="mainBox">
            <KeepAlive>
                <component :is="currentComponent" @send-node="nodeShow" :topicMsg="topicInfo"
                    @send-control="controlShow" />
            </KeepAlive>
            <!-- <MainCanvas @send-node="nodeShow" /> -->
            <!-- <PaperCoopNetwork /> -->
        </div>
        <div class="rightBox">
            <KeepAlive>
                <component :is="curRightComponent" :auClusterMsg="auNetInfo" :instClusterMsg="instNetInfo"
                    :topicMsg="topicInfo" @nodeShowToTop="nodeShow" />
            </KeepAlive>
            <!-- <KeepAlive>
                <TimeTrend v-if="toggle === 1" />
            </KeepAlive>
            <KeepAlive>
                <div v-if="toggle === 0">
                    <div class="auPanel">
                        <AuCoopNetwork @send-node="nodeShow" :clusterMsg="auNetInfo" />
                    </div>
                    <div class="instPanel">
                        <InstCoopNetwork @send-node="nodeShow" :clusterMsg="instNetInfo" />
                    </div>
                </div>
            </KeepAlive> -->

        </div>
    </div>
</template>

<script>
import MainCanvas from './MainCanvas.vue';
import AuCoopNetwork from './AuCoopNetwork.vue'
import InstCoopNetwork from './InstCoopNetwork.vue'
import DetailPanel from './DetailPanel.vue'
import PaperCoopNetwork from "./PaperCoopNetwork.vue";
import KeyWordsCloud from "./KeyWordsCloud.vue";
import TimeTrend from "./TimeTrend.vue"
import AuInstAll from "./AuInstAll.vue"

import { ref } from 'vue'
export default {
    components: {
        MainCanvas,
        DetailPanel,
        AuCoopNetwork,
        InstCoopNetwork,
        PaperCoopNetwork,
        KeyWordsCloud,
        TimeTrend,
        AuInstAll,
    },
    setup() {
        const nodeMsg = ref(null);
        const topicInfo = ref(null);
        const auNetInfo = ref(null);
        const instNetInfo = ref(null);
        // const netInfo = ref({});
        const currentComponent = ref("MainCanvas");
        const curRightComponent = ref("AuInstAll");
        const controlMsg = ref({});

        const nodeShow = (msg) => {
            nodeMsg.value = msg
            console.log("get:", nodeMsg.value);
        }

        const controlShow = (x, y) => {
            console.log(x, y);
            controlMsg.value.x = x;
            controlMsg.value.y = y;
        }

        const netShow = (group, cluster) => {
            console.log(group);
            console.log(cluster);
            // netInfo.value.group = group
            // netInfo.value.cluster = cluster
            // console.log(netInfo.value);

            if (group == 2)
                auNetInfo.value = cluster
            if (group == 3)
                instNetInfo.value = cluster
            console.log(instNetInfo.value);
            console.log(auNetInfo.value);
            // console.log(typeof (auNetInfo.value));
        }

        const topicShow = (cluster) => {
            // 切换组件
            console.log("get", cluster);
            currentComponent.value = (currentComponent.value != "MainCanvas") ?
                "MainCanvas" : "PaperCoopNetwork";
            curRightComponent.value = (curRightComponent.value != "AuInstAll") ?
                "AuInstAll" : "TimeTrend";
            topicInfo.value = cluster;
        }

        const backPanel = () => {
            currentComponent.value = (currentComponent.value != "MainCanvas") ?
                "MainCanvas" : "PaperCoopNetwork";
            curRightComponent.value = (curRightComponent.value != "AuInstAll") ?
                "AuInstAll" : "TimeTrend";
        }

        return {
            nodeMsg,
            nodeShow,
            netShow,
            topicShow,
            auNetInfo,
            instNetInfo,
            currentComponent,
            curRightComponent,
            topicInfo,
            backPanel,
            controlShow,
            controlMsg
        }
    }
}
</script>

<style scoped>
.Panel {
    display: flex;
    overflow: hidden;
    /* border: 0.5px solid #333; */
    /* border-radius: 5px; */
    /* padding: 10px; */
}

.leftBox {
    width: 20%;
    height: 96vh;
    border: 0.5px solid #333;
    border-radius: 5px;
    padding: 10px;
    margin: 5px;
}

.mainBox {
    width: 50%;
    height: 96vh;
    border: 0.5px solid #333;
    border-radius: 5px;
    padding: 10px;
    margin: 5px;
    background: #323232 repeating-linear-gradient(30deg,
            hsla(0, 0%, 100%, .1), hsla(0, 0%, 100%, .1) 15px,
            transparent 0, transparent 30px);
}

.rightBox {
    width: 30%;
    height: 96vh;
    border: 0.5px solid #333;
    border-radius: 5px;
    padding: 10px;
    margin: 5px;
}
</style>