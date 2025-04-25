<template>
    <div class="wordCloudmain" style="width: 100%;height: 36vh">
        <div class="keyWordCloud"></div>
    </div>
    <!-- <div class="container">
        <el-container>
            <el-header class="header" style="width: 100%;height: 10vh;">KeyWordCloud</el-header>
        </el-container>
        <div class="wordCloudmain" style="width: 100%;height: 40vh;">
            <div class="keyWordCloud"></div>
        </div>
    </div> -->
</template>

<script>
import * as d3 from 'd3'
// import * as cloud from "../../../data/d3.layout.cloud.js";
import cloud from "d3-cloud";
import allGraph from '../../../output_data/jsonCluster_Draw_Coop10.json'
import paperGraph from '../../../output_data/papersCoop10.json'

import {
    ref,
    watch
} from 'vue'

export default {
    props: {
        msg: Object
    },
    setup(props) {
        const clusterData = ref(allGraph)
        const topicData = ref(paperGraph)
        const clusterNum = ref('');
        const topicNum = ref('');
        // clusterNum.value = 5
        const clusterType = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        watch(
            () => props.msg,
            (newValue) => {
                if (newValue !== null) {
                    if ("topic" in newValue) {
                        topicNum.value = newValue.topic;
                        clusterNum.value = -1;
                    }
                    else {
                        clusterNum.value = newValue.cluster;
                        topicNum.value = -1;
                    }
                    drawWordsCloud(clusterNum.value, topicNum.value);

                }
            },
            { immediate: true }
        )


        // onMounted(() => {
        //     // console.log(clusterData.value.nodes);



        //     // drawWordsCloud(clusterNum.value);


        // })

        function drawWordsCloud(c, t) {
            const words = []
            if (c !== -1)
                clusterData.value.nodes.filter(d => d.group === 1 && d.cluster === c)
                    .forEach(d => d.keywords.split(",").forEach(d => words.push(d.trim().toLowerCase())));
            // nodeswords.map(d=>{words.push(d.trim())})
            // console.log(words);
            else
                topicData.value.nodes.filter(d => d.group === 1 && d.topic === t)
                    .forEach(d => d.keywords.split(",").forEach(d => words.push(d.trim().toLowerCase())));
            const data = d3.rollups(words, size => size.length, w => w)
                .sort(([, a], [, b]) => d3.descending(a, b))
                .slice(0, 30)
                .map(([key, size]) => ({ text: key, size }));
            // console.log(data);

            const minSize = data[data.length - 1].size;
            const maxSize = data[0].size;
            const sizeScale = d3.scaleLinear()
                .domain([minSize, maxSize])
                .range([10, 100]);
            const color = d3.scaleOrdinal()
                .domain(clusterType)
                .range(d3.schemeCategory10);


            const element = document.querySelector(".wordCloudmain");
            const width = element.offsetWidth;
            const height = element.offsetHeight;

            var layout = cloud()
                .size([width, height])
                .words(data)
                .padding(5)
                // .rotate(function () { return ~~(Math.random() * 2) * 90; })
                .rotate(0)
                .font("Arial")
                .fontSize(d => sizeScale(d.size))
                // .fontSize(d => d.size)
                .on("end", draw);

            layout.start();

            function draw(words) {
                d3.select('.keyWordCloud').selectAll("svg").remove();

                const svg = d3.select(".keyWordCloud").append("svg")
                    .attr("width", layout.size()[0])
                    .attr("height", layout.size()[1])
                // .attr("transform", `translate(${element.offsetWidth * 0.05},${element.offsetHeight * 0.05})`)
                const g = svg.append("g")
                    .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
                g.selectAll("text")
                    .data(words)
                    .enter().append("text")
                    .style("font-size", function (d) { return d.size + "px"; })
                    .style("font-family", "Impact")
                    .style("fill", c === -1 ? color(t) : color(c))
                    .attr("text-anchor", "middle")
                    .attr("transform", function (d) {
                        return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                    })
                    .text(function (d) { return d.text; });
                // console.log(color(t), "words");

            }
        }



        return {

        }
    }
}
</script>

<style scoped>
/* .container {
    height: 50vh;
    width: 100%;
    border: 2px solid #000;
    text-align: center;
    font-size: 18px;
}

.header {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: rgba(128, 128, 128, 0.6);
} */
</style>
