<template>

    <div class="timeTrendmain" style="width: 100%;height: 96vh;">
        <div class="title">Statistical Characteristics</div>
        <div class="paperCounts"></div>
        <div class="closeness"></div>
        <div class="betweenness"></div>

    </div>

</template>

<script>
import * as d3 from 'd3'
import { ref, watch, onMounted } from 'vue'
import testGraph from '../../../output_Data/centrality_forecast.json'
export default {
    props: {
        auClusterMsg: Number,
        instClusterMsg: Number,
        topicMsg: Number,
    },
    setup(props) {
        const GraphData = ref(testGraph)
        const clusterType = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        const clusterNum = ref(null)
        // clusterNum.value = 1

        watch(
            () => props.topicMsg,
            (newValue, oldValue) => {
                console.log(newValue);
                if (newValue !== null) {
                    console.log(newValue);
                    clusterNum.value = newValue;
                    if (oldValue !== undefined)
                        drawAll();
                }
            },
            { immediate: true }
        );

        function drawAll() {
            drawGraph(GraphData.value, clusterNum.value, 'paperCounts');
            drawGraph(GraphData.value, clusterNum.value, 'closeness');
            drawGraph(GraphData.value, clusterNum.value, 'betweenness');
        }

        onMounted(() => {
            // console.log(GraphData.value);

            // deal(GraphData.value);
            // console.log(GraphData.value[0]);
            if (clusterNum.value != null)
                drawAll();
            // drawGraph(GraphData.value, clusterNum.value, 'paperCounts');
            // drawGraph(GraphData.value, clusterNum.value, 'closeness');
            // drawGraph(GraphData.value, clusterNum.value, 'betweenness');
        })

        function drawGraph(data, cluster, label) {
            const element = document.querySelector(".timeTrendmain");
            const width = element.offsetWidth;
            const height = element.offsetHeight / 3 * 0.9;
            const margin = ({ top: 25, right: 30, bottom: 30, left: 40 })
            const color = d3.scaleOrdinal()
                .domain(clusterType)
                .range(d3.schemeCategory10);
            const curLabel = label;

            data = data[curLabel].filter(d => d.cluster === cluster).map(d => ({
                topic: d.topic,
                year: d.year,
                date: new Date(d.year, 0, 1),
                value: d.value
            }))

            console.log(data);

            d3.select(`.${label}`).selectAll("svg").remove();
            const svg = d3.select(`.${label}`)
                .append('svg')
                .attr('width', width)
                .attr('height', height)
            const g = svg.append('g')

            const x = d3.scaleTime()
                .domain(d3.extent(data, d => d.date))
                .range([margin.left, width - margin.right])
            const y = d3.scaleLinear()
                .domain([0, d3.max(data, d => d.value)]).nice()
                .range([height - margin.bottom, margin.top])
            const xAxis = (g) =>
                g.attr("transform", `translate(0,${height - margin.bottom})`).call(
                    d3
                        .axisBottom(x)
                        .ticks(width / 80)
                        .tickSizeOuter(0)
                )
            const yAxis = g => g
                .attr("transform", `translate(${margin.left},0)`)
                .call(d3.axisLeft(y))
                .call(g => g.select(".domain").remove())
                .call(g => g.select(".tick:last-of-type text").clone()
                    .attr("class", "yaxis_label")
                    .attr("x", 3)
                    .attr("text-anchor", "start")
                    .attr("font-weight", "bold")
                    .attr("font-size", "12")
                    .text(""))
                .call(g => g.select(".tick:last-of-type text").clone()
                    // .attr("x", 3)
                    .attr("y", -16)
                    .attr("text-anchor", "start")
                    .attr("font-weight", "bold")
                    .attr("font-size", "16")
                    .text(curLabel === "paperCounts" ?
                        curLabel.toUpperCase() : curLabel.toUpperCase() + "(*1e4)"))

            g.append('g').call(xAxis);
            g.append('g').call(yAxis);

            // 将数据按照topic分组
            const groups = d3.rollup(data.filter(d => d.year !== 2025),
                v => Object.assign(v, { z: v[0].topic }),
                d => d.topic);
            // 预测组数据
            const groups_forecast = d3.rollup(data.filter(d => d.year === 2024 || d.year === 2025),
                v => Object.assign(v, { z: v[0].topic }),
                d => d.topic);
            console.log(groups);
            console.log(groups_forecast);


            // 线的绘制函数
            const line = d3.line()
                .defined(d => !isNaN(d.value))
                .x(d => x(d.date))
                .y(d => y(d.value))

            // 绘制历史趋势线
            const path = g.append("g")
                .attr("fill", "none")
                .attr("stroke-width", 1.5)
                .attr("stroke-linejoin", "round")
                .attr("stroke-linecap", "round")
                .selectAll("path")
                .data(groups.values())
                .join("path")
                .attr("stroke", d => color(d[0].topic))
                .style("mix-blend-mode", "multiply")
                .attr("d", line);
            // 绘制预测线
            const path_forecast = g.append("g")
                .attr("fill", "none")
                .attr("stroke-width", 1.5)
                .selectAll("path")
                .data(groups_forecast.values())
                .join("path")
                .attr("stroke", d => color(d[0].topic))
                .style("mix-blend-mode", "multiply")
                .attr("d", line)
                .attr("stroke-dasharray", "5,5")
                .attr("opacity", 0);

            // 路径绘制动画
            function transition(path) {
                path.transition()
                    .duration(3000)
                    .attrTween("stroke-dasharray", tweenDash)
                    .on("end", () => { d3.select(this).call(transition); });
            }
            function tweenDash() {
                const l = this.getTotalLength(),
                    i = d3.interpolateString("0," + l, l + "," + l);
                return function (t) { return i(t) };
            }
            path.call(transition);

            // 为每个数据点添加圆点
            const dot = g.append("g")
                .selectAll('circle')
                .data(data)
                .join('circle')
                .attr('cx', d => x(d.date)) // x 位置
                .attr('cy', d => y(d.value)) // y 位置
                .attr('r', 3) // 圆的半径
                .attr('fill', d => color(d.topic)) // 圆的颜色（你可以改成其他颜色）
                .style("mix-blend-mode", "multiply") // 重合时叠加颜色
                .attr("opacity", 0);

            dot.append('title').text(d => d.value)
            // 绘制数据点
            const dot_text = g.append('g')
                .append('text')
                .attr("text-anchor", "middle")
                .attr("y", -8)
                .attr("font-size", 10)
                .attr('display', "none");


            //增加线的选中效果
            const points = data.map((d) => [x(d.date), y(d.value), d.topic, d.value]);
            console.log(points);

            setTimeout(() => {
                dot.transition().duration(1000).attr("opacity", 1);
                path_forecast.transition().duration(1000).attr("opacity", 1);
            }, 3000);
            setTimeout(() => {
                svg
                    .on("pointerenter", pointerentered)
                    .on("pointermove", pointermoved)
                    .on("pointerleave", pointerleft)

            }, 4500);

            // 鼠标移入
            function pointerentered() {
                path.style("mix-blend-mode", null).style("stroke", "#ddd");
                path_forecast.style("mix-blend-mode", null).style("stroke", "#ddd");
                dot.style("mix-blend-mode", null).style("fill", "#ddd");
                dot_text.attr("display", null);
            }
            // 鼠标移动
            function pointermoved(event) {
                const [xm, ym] = d3.pointer(event);
                const i = d3.leastIndex(points, ([x, y]) => Math.hypot(x - xm, y - ym));
                const [x, y, t, v] = points[i];
                // console.log(t);
                path.style("stroke", d => d[0].topic === t ? color(t) : "#ddd")
                    .filter(d => d[0].topic === t).raise();
                path_forecast.style("stroke", d => d[0].topic === t ? color(t) : "#ddd")
                    .filter(d => d[0].topic === t).raise();
                dot.style("fill", ({ topic }) => topic === t ? color(t) : "#ddd")
                    .filter(({ topic }) => topic === t).raise();
                g.select(".yaxis_label").text(`Topic ${t}`);
                dot_text.attr("transform", `translate(${x},${y})`).text(v);

            }
            // 鼠标移出
            function pointerleft() {
                path.style("mix-blend-mode", "multiply").style("stroke", d => color(d[0].topic));
                path_forecast.style("mix-blend-mode", "multiply").style("stroke", d => color(d[0].topic));
                dot.style("mix-blend-mode", "multiply").style("fill", d => color(d.topic));
                g.select(".yaxis_label").text("");
                dot_text.attr("display", "none");
            }

        }



        return {

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

.paperCounts {
    margin-top: 25px;
    border-bottom: 1px solid #000;
}

.closeness {
    margin-top: 10px;
    border-bottom: 1px solid #000;
}

.betweenness {
    margin-top: 10px;
}
</style>