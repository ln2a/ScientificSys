<template>
    <div class="elmain" style="width: 100%;height: 96vh;">
        <div class="paperNetBox"></div>
    </div>

    <!-- <div class="container" id="mainContainer">
        <el-container>
            <el-header class="header" style="width: 100%;height: 10vh;">TopicNetwork</el-header>
        </el-container>
        <div class="elmain" style="width: 100%;height: 90vh;">
            <div class="paperNetBox"></div>
        </div>
    </div> -->
</template>

<script>
import * as d3 from 'd3'
import { onMounted, ref, watch } from 'vue'
// import testGraph from '../../../data/d3TestData2.json'
import testGraph from '../../../output_data/papersCoop10.json'


export default {
    props: {
        topicMsg: Number
    },
    emits: ["sendNode", "sendControl"],
    setup(props, { emit }) {
        const GraphData = ref(testGraph)
        const nodeMsg = ref(null);
        const clusterType = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        const clusterNum = ref(null)
        // clusterNum.value = 6

        watch(
            () => props.topicMsg,
            (newValue, oldValue) => {
                // console.log(newValue); 
                if (newValue !== null) {
                    console.log(newValue);
                    clusterNum.value = newValue;
                    if (oldValue !== undefined)
                        initGraph(GraphData.value, clusterNum.value)

                }
            },
            { immediate: true }
        );

        onMounted(() => {
            console.log(GraphData.value);
            if (clusterNum.value != null)
                initGraph(GraphData.value, clusterNum.value)
        })

        function initGraph(data, n) {
            // Specify the dimensions of the chart.
            // const width = 928;
            // const height = 600;

            const element = document.querySelector(".elmain");
            const width = element.offsetWidth;
            const height = element.offsetHeight;
            const alpgaScale = d3.scaleLinear()
                .domain([1, 10])
                .range([0.01, 1]);
            // const widthScale = d3.scaleLinear()
            //     .domain([1, 10])
            //     .range([1, 1]);
            // Specify the color scale.
            // const color = d3.scaleOrdinal(d3.schemeCategory10);
            const color = d3.scaleOrdinal()
                .domain(clusterType)
                .range(d3.schemeCategory10);


            // The force simulation mutates links and nodes, so create a copy
            // so that re-evaluating this cell produces the same result.
            const links = data.links.filter(d => d.cluster === n).map(d => ({ ...d }));
            const nodes = data.nodes.filter(d => d.cluster === n).map(d => ({ ...d }));
            console.log(links);
            console.log(links.length);

            console.log(nodes);
            emit("sendControl", nodes.length, links.length);
            const svgScale = d3.scaleLinear()
                .domain([links.length > 500 ? links.length : 500, 50])
                .range([0.4, 0.6]);

            // const links = data.links.map(d => ({ ...d }));
            // const nodes = data.nodes.map(d => ({ ...d }));

            // Create a simulation with several forces.
            const simulation = d3.forceSimulation(nodes)
                .force("link", d3.forceLink(links).id(d => d.id).distance(100)
                    .strength((link) => alpgaScale(link.value)))
                .force("charge", d3.forceManyBody().strength(-200))
                // .force("collide", d3.forceCollide().radius(() => 10))
                // .force("center", d3.forceCenter(width / 2, height / 2))
                .force("x", d3.forceX())
                .force("y", d3.forceY())
                .on("tick", ticked);

            // Create the SVG container.
            d3.select('.paperNetBox').selectAll("svg").remove();
            const svg = d3.select(".paperNetBox")
                .append("svg")
                .attr("width", width)
                .attr("height", height)
                // .attr("viewBox", [0, 0, width, height])
                .attr("viewBox", [-width / 2, -height / 2, width, height])
                .attr("style", "max-width: 100%; height: auto;");

            const g = svg.append('g')
            const zoom = d3.zoom().on("zoom", function (event) {
                g.attr("transform", event.transform)
            })
            // 设置初始缩放比例——面对过多节点，让视图变小
            const initialTransform = d3.zoomIdentity
                // .translate(width / 2, height / 2)
                .scale(svgScale(links.length))
            // .translate(-width / 2, -height / 2);

            // 为svg添加鼠标缩放功能
            svg.call(zoom)
            svg.call(zoom.transform, initialTransform)

            // Add a line for each link, and a circle for each node.
            const link = g.append("g")
                .selectAll()
                .data(links)
                .join("line")
                .attr("stroke", d => "topic" in d ? color(d.topic) : "#999")
                .attr("stroke-opacity", d => d.value / 10)
                .attr("stroke-width", d => d.value * 1.5)
                // .filter(d => d.topic)
                .on("click", selectLink)
                .on("mouseover", function (event, d) {
                    if ("topic" in d) {
                        d3.selectAll(`.node${d.topic}`) // 选中所有相同 class 的元素
                            .style("stroke-width", 10) // 变粗
                            .style("r", 15); // 变粗
                    }
                })
                .on("mouseout", function (event, d) {
                    if ("topic" in d) {
                        d3.selectAll(`.node${d.topic}`) // 选中所有相同 class 的元素
                            .style("stroke-width", 1.5) // 还原边框
                            .style("r", 10); // 还原边框
                    }
                });
            // console.log(color(t), "links");

            const node = g.append("g")
                .attr("stroke", "#fff")
                .attr("stroke-width", 1.5)
                .selectAll()
                .data(nodes)
                .join("circle")
                .attr("r", 10)
                .attr("fill", d => color(d.cluster))
                .attr("class", d => `node node${d.topic}`)
                .on("click", selectNode)

            node.append("title")
                .text(d => d.id);

            // Add a drag behavior.
            node.call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

            // Set the position attributes of links and nodes each time the simulation ticks.
            function ticked() {
                link
                    .attr("x1", d => d.source.x)
                    .attr("y1", d => d.source.y)
                    .attr("x2", d => d.target.x)
                    .attr("y2", d => d.target.y);

                node
                    .attr("cx", d => d.x)
                    .attr("cy", d => d.y);
            }

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
                if (i == 'x' || i == 'y' || i == 'vx' || i == 'vy' || i == 'index' || i == "ab" || i == "fx" || i == "fy")
                    continue
                data[i] = d[i]
            }
            nodeMsg.value = data;
            console.log("send:", nodeMsg.value);
            emit("sendNode", nodeMsg.value);
        }

        function selectLink(e, d) {
            console.log(d);
            nodeMsg.value = d;
            if ("topic" in d)
                emit("sendNode", nodeMsg.value);
        }

        return {
            nodeMsg
        }
    }
}

</script>


<style scoped>
/* .container {
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
} */
</style>