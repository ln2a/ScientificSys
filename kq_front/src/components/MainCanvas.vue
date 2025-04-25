<template>
    <div class="elmain" style="width: 100%;height: 96vh;">
        <div class="mainCanvasBox"></div>
    </div>
    <!-- <div class="container" id="mainContainer">
        <el-container>
            <el-header class="header" style="width: 100%;height: 10vh;">MainNetwork</el-header>
        </el-container>
        <div class="elmain" style="width: 100%;height: 90vh;">
            <div class="mainCanvasBox"></div>
        </div>
    </div> -->
</template>

<script>
import * as d3 from 'd3'
import { onMounted, ref } from "vue";
// import testGraph from '../../../data/d3TestData.json'
// import testGraph from '../../../output_data/sourceJson.json'
// import testGraph from '../../../output_data/sourceJsonTest.json'
// import testGraph from '../../../output_data/sourceJsonTest_cluster.json'
// import testGraph from '../../../output_data/jsonCluster_Draw.json'
// import testGraph from '../../../output_data/jsonCluster_Draw_Coop_Min.json'
// import testGraph from '../../../output_data/jsonCluster_Draw_Coop.json'
import testGraph from '../../../output_data/jsonCluster_Draw_Coop10.json'

export default {
    props: {
        topicMsg: Number
    },

    emits: ["sendNode", "sendControl"],

    setup(props, { emit }) {
        const GraphData = ref(testGraph)
        const nodeMsg = ref(null);
        const clusterType = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        onMounted(() => {
            console.log(GraphData.value);

            initGraph(GraphData.value)



        })

        function initGraph(data) {
            // Specify the dimensions of the chart.
            // const width = 680;
            // const height = 680;
            const element = document.querySelector(".elmain");
            const width = element.offsetWidth;
            const height = element.offsetHeight;
            // const bodyWidth = window.innerWidth;
            // const bodyHeight = window.innerHeight;
            // console.log(bodyWidth);
            // const width = bodyWidth * 0.5
            // const height = bodyHeight * 0.9;
            // Specify the color scale.
            // const color = d3.scaleOrdinal(d3.schemeCategory10);
            const color = d3.scaleOrdinal()
                .domain(clusterType)
                .range(d3.schemeCategory10);
            // .range(["black"]);


            // The force simulation mutates links and nodes, so create a copy
            // so that re-evaluating this cell produces the same result.
            const links = data.links.map(d => ({ ...d }));
            const nodes = data.nodes.map(d => ({ ...d }));
            emit("sendControl", nodes.length, links.length);
            // Create a simulation with several forces.
            const simulation = d3.forceSimulation(nodes)
                .force("link", d3.forceLink(links).id(d => d.id).distance(300)
                    .strength((link) => link.value / 10))
                // 设置最小边长
                .force("charge", d3.forceManyBody().strength(-300))
                // 离心力
                .force("collide", d3.forceCollide().radius(() => 120))
                // 节点间最小半径
                .force("x", d3.forceX())
                .force("y", d3.forceY());

            // Create the SVG container.
            const svg = d3.select(".mainCanvasBox").append("svg")
                .attr("width", width)
                .attr("height", height)
                .attr("viewBox", [-width / 2, -height / 2, width, height])
                // 视口坐上角是-width / 2，中心点为(0,0)
                .attr("style", "max-width: 100%; height: auto;");

            const g = svg.append("g")
                .attr("class", "content")
            const zoom = d3.zoom().on("zoom", function (event) {
                g.attr("transform", event.transform)
            })
            // 设置初始缩放比例——面对过多节点，让视图变小
            const initialTransform = d3.zoomIdentity.scale(0.05);
            // 为svg添加鼠标缩放功能
            svg.call(zoom)
            svg.call(zoom.transform, initialTransform)



            // Add a line for each link, and a circle for each node.
            const link = g.append("g")
                .attr("stroke", "#999")
                .attr("stroke-opacity", 0.4)
                .selectAll("line")
                .data(links)
                .join("line")
                .attr("stroke-width", d => Math.sqrt(d.value));

            const node = g.append("g")
                .selectAll("circle")
                .data(nodes)
                .join("circle")
                .attr("stroke-width", d => d.group == 1 ? 5 : 20)
                .attr("stroke", d => {
                    if (d.group == 1) return "#fff";
                    else { return "#000"; }
                })
                .attr("r", 50)
                .attr("class", d => `node node${d.cluster}`)
                // .attr("fill", d => color(d.group));
                .attr("fill", d => color(d.cluster))
                .on("click", selectNode)
                .on("mouseover", function (event, d) {
                    d3.selectAll(`.node${d.cluster}`) // 选中所有相同 class 的元素
                        .style("stroke-width", 20) // 还原边框
                        .style("r", 70); // 变粗
                })
                .on("mouseout", function (event, d) {
                    d3.selectAll(`.node${d.cluster}`) // 选中所有相同 class 的元素
                        .style("stroke-width", d => d.group == 1 ? 5 : 20) // 还原边框
                        .style("r", 50); // 还原边框
                });

            node.append("title")
                .text(d => d.id);

            // 拖动事件
            // Add a drag behavior.
            // node.call(d3.drag()
            //     .on("start", dragstarted)
            // .on("drag", dragged)
            // .on("end", dragended));

            // Set the position attributes of links and nodes each time the simulation ticks.
            simulation.on("tick", () => {
                link
                    .attr("x1", d => d.source.x)
                    .attr("y1", d => d.source.y)
                    .attr("x2", d => d.target.x)
                    .attr("y2", d => d.target.y);

                node
                    .attr("cx", d => d.x)
                    .attr("cy", d => d.y);
            });

            // Reheat the simulation when drag starts, and fix the subject position.
            function dragstarted(event) {
                if (!event.active) simulation.alphaTarget(0.3).restart();
                event.subject.fx = event.subject.x;
                event.subject.fy = event.subject.y;
            }

            // Update the subject (dragged node) position during drag.
            function dragged(event) {
                event.subject.fx = event.x;
                event.subject.fy = event.y;
            }

            // Restore the target alpha so the simulation cools after dragging ends.
            // Unfix the subject position now that it’s no longer being dragged.
            function dragended(event) {
                if (!event.active) simulation.alphaTarget(0);
                event.subject.fx = null;
                event.subject.fy = null;
            }
        }

        function selectNode(e, d) {
            console.log(d);
            let data = {}
            for (var i in d) {
                if (i == 'x' || i == 'y' || i == 'vx' || i == 'vy' || i == 'index' || i == "ab")
                    continue
                data[i] = d[i]
            }
            nodeMsg.value = data;
            console.log("send:", nodeMsg.value);
            emit("sendNode", nodeMsg.value);
        }

        return {
            nodeMsg
        }
    }
}
</script>

<style scoped>
.mainContainer {
    height: 100vh;
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
}

/* .mainCanvasBox {
    background: #2c3e50 repeating-linear-gradient(30deg,
            hsla(0, 0%, 100%, .1), hsla(0, 0%, 100%, .1) 15px,
            transparent 0, transparent 30px);


} */

.node {
    /* stroke: #fff; */
    /* stroke-width: 5; */
    cursor: pointer;
}
</style>