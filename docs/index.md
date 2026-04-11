---
statistics: true
hide:
  - feedback
---

# 首页

##(´･ᴗ･` )


=== "<font size = 6>:fontawesome-solid-camera-retro: </font><font size = 6>关于我</font>"

    !!! note inline ""
        🍟 简介：一个用感性解剖理性的观察者

        ☺️ 姓名：可以叫我'江屿'

        🏔️ 碎语：退回到只属于我的世界

    !!! note inline "" 
        📖 兴趣：阅读、旅行、摄影
        
        💻 技术栈 :material-language-python: | :material-language-java: 。

        🧩 专注方向：数据分析，机器学习

    !!! success inline ""
        🧸 MBTI人格：<font face = "American Typewriter" >INFP</font>

        🎀 生活状态：时间的摄影师
          
        > 我以为按下快门就是囚禁了时间

    !!! success inline ""
        🌏 所在地：人间一隅，步履不停

        🐳 性格特质：偏爱安静独处，喜赴山海

        > 当时年少掷春光，花马踏蹄酒溅香

=== "<font size = 6>:fontawesome-solid-book: </font><font size = 6 face = '文泉驿正黑' >关于此站</font>"

    ⛪ 总页面数：{{pages}} 页；
    
    🔠 总字数：{{words}} 字；
    
    🤖 代码行数：{{codes}} 行；

    🛩️ 上线时长：<span id="web-time"></span>；
    
    🦄 代码仓库：<a href="https://github.com/CiQuBeiJiang" target="_blank">CiQuBeiJiang</a>

    ??? abstract indexinline "站点里程碑"
        其实我有一个个人网站，但是最近在学习的时候刷到了相关github部署的网站，我觉得比之前的简单多了，于是就部署了一个

        - **2026.1.17** 🎉 站点首次部署

=== "<font size = 6>:fontawesome-solid-envelope: </font><font size = 6 face = '文泉驿正黑' >联系我</font>"

    - :fontawesome-solid-envelope:  <a href="mailto:1724961030@qq.com">个人邮箱</a>
    - :fontawesome-brands-github: <a href="https://github.com/CiQuBeiJiang" target="_blank">GitHub</a> ｜ 存放我的项目代码与学习笔记

<br>

- 💻 **桌面端**：通过顶部导航栏切换主题；左侧可查看目录结构。
- 📱 **移动端**：点击左上角图标展开菜单。
- 🔍 **搜索功能**：支持中英文关键词检索。

<script>
function updateTime() {
    var date = new Date();
    var now = date.getTime();
    var startDate = new Date("2026/01/16 00:00:00");
    var start = startDate.getTime();
    var diff = now - start;
    var y, d, h, m;
    y = Math.floor(diff / (365 * 24 * 3600 * 1000));
    diff -= y * 365 * 24 * 3600 * 1000;
    d = Math.floor(diff / (24 * 3600 * 1000));
    h = Math.floor(diff / (3600 * 1000) % 24);
    m = Math.floor(diff / (60 * 1000) % 60);
    if (y == 0) {
        document.getElementById("web-time").innerHTML = d + " 天 " + h + " 时 " + m + " 分";
    } else {
        document.getElementById("web-time").innerHTML = y + " 年 " + d + " 天 " + h + " 时 " + m + " 分";
    }
    setTimeout(updateTime, 60000);
}
updateTime();
</script>
