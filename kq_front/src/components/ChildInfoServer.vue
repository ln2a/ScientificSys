<template>
    <div class="server"></div>
    <!-- <h3>消息接收</h3> -->
    <!-- <p>{{ nodeMsg }}</p> -->
    <button @click="yyy">go</button>
</template>

<script setup>
import { ref, watch } from "vue";

const props = defineProps({
    msg: Object
});
const nodeMsg = ref(props.msg);

const emit = defineEmits(["msgShow"]);


watch(
    () => props.msg,
    (newVal) => {
        nodeMsg.value = newVal;
        console.log("newMsg：", nodeMsg.value);
        emit("msgShow", "yyy");
        yyy();
        // emit("msgShow", nodeMsg.value);
    },
    { immediate: true }
);

function yyy() {
    console.log("yes");
    emit("msgShow", "yyy");
}
</script>