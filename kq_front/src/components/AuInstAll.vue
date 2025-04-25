<template>
    <div class="auinstall">
        <div class="auPanel">
            <div class="title">Author Net</div>
            <AuCoopNetwork @send-node="nodeShowMid" :clusterMsg="auClusterMsg" />
        </div>
        <div class="instPanel">
            <div class="title">Instition Net</div>
            <InstCoopNetwork @send-node="nodeShowMid" :clusterMsg="instClusterMsg" />
        </div>
    </div>

</template>

<script>
import AuCoopNetwork from './AuCoopNetwork.vue'
import InstCoopNetwork from './InstCoopNetwork.vue'
import { ref, watch } from 'vue'

export default {
    components: {
        AuCoopNetwork,
        InstCoopNetwork,
    },
    props: {
        auClusterMsg: Number,
        instClusterMsg: Number,
        topicMsg: Number,
    },
    emits: ["nodeShowToTop"],
    setup(props, { emit }) {
        const nodeShowMid = (msg) => {
            emit("nodeShowToTop", msg);
        }
        return {
            nodeShowMid
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

.auinstall {
    height: 96vh;
}

.instPanel {
    margin-top: 10px;
}
</style>