---
# 页面元配置：开启统计功能 + 隐藏反馈按钮
statistics: true
hide:
  - feedback
---

# (´･ᴗ･` )

=== "<font size = 6>:fontawesome-solid-paw: </font><font size = 6 face = "微软雅黑" >关于我</font>"

    !!! note inline ""
        🍟 **个人简介**：一个用感性解剖理性的观察者
        
        ☺️ **姓名**：可以叫我'江屿'
        
        🏔️ **碎语**：我把自己从货架上取下，退回到只属于我的世界

    !!! note inline "" 
        📖  **兴趣爱好**：阅读、旅行、摄影

        💻 **技术栈**：偶尔用代码打发时间，擅长/接触 :material-language-python: | 【你的其他技术，如：:material-language-java:、:material-language-js:】

        🧩 **专注方向**：数据分析，机器学习

    !!! success inline ""
        🧸 **MBTI人格**：<font face = "American Typewriter" >INFP</font>[^2] 
        
        🎀 **生活状态**：时间的摄影师
          
        🔆 **星座**：♑️

    !!! success inline ""
        🌏 **所在地**：暂居 **【你的城市】**[^4]

        🐳 **性格特质**：【你的性格/风格，如：偏爱安静独处，也爱说走就走的旅行】

        ☘️ **近期目标**：【你的近期目标，如：完成10个实战项目、读完5本专业书籍】


=== "<font size = 6>:fontawesome-solid-book: </font><font size = 6 face = "微软雅黑" >关于此站</font>"

    ⛪ 总页面数：{{pages}} 页；
    
    🔠 总字数：{{words}} 字；
    
    🤖 代码行数：{{codes}} 行；

    🛩️ 上线时长：<span id="web-time"></span>；
    
    🦄 代码仓库：https://github.com/CiQuBeiJiang

    ??? abstract indexinline "站点里程碑"

        其实我有一个个人网站，但是最近在学习的时候刷到了相关github部署的网站，我觉得比之前的简单多了，于是就部署了一个

        - **2026.1.17** 🎉 站点首次部署
   

=== "<font size = 6>:fontawesome-solid-envelope: </font><font size = 6 face = "微软雅黑" >联系我</font>"

    - :fontawesome-solid-envelope:  <a href="mailto:1724961030@qq.com">个人邮箱</a>，:fontawesome-regular-envelope: <a href = "mailto:【你的工作/学习邮箱】">工作/学习邮箱</a>。

    - :fontawesome-brands-github: [【你的GitHub昵称】](【你的GitHub链接])，主要存放【你的项目方向，如：技术项目、代码笔记】相关内容。

    - :fontawesome-brands-csdn: [【你的博客昵称】](【你的博客链接])，分享技术笔记与实战经验。
    - :fontawesome-brands-weixin: 【你的微信号/公众号名称】（可选，可补充二维码图片）。



<!-- 设备导航提示 -->
<br>

- 💻 **桌面端**：通过顶部导航栏切换主题；左侧可查看目录结构。
- 📱 **移动端**：点击左上角图标展开菜单。
- 🔍 **搜索功能**：支持中英文关键词检索。


<!-- 网站运行时长JS：修改startDate为你的站点创建时间（格式：YYYY/MM/DD HH:MM:SS） -->
<script>
function updateTime() {
    var date = new Date();
    var now = date.getTime();
    var startDate = new Date("2026/1/16");
    var start = startDate.getTime();
    var diff = now - start;
    var y, d, h, m;
    y = Math.floor(diff / (365 * 24 * 3600 * 1000));
    diff -= y * 365 * 24 * 3600 * 1000;
    d = Math.floor(diff / (24 * 3600 * 1000));
    h = Math.floor(diff / (3600 * 1000) % 24);
    m = Math.floor(diff / (60 * 1000) % 60);
    if (y == 0) {
        document.getElementById("web-time").innerHTML = d + "<span class=\"heti-spacing\"> </span>天 <span class=\"heti-spacing\"> </span>" + h + "<span class=\"heti-spacing\"> </span>时 <span class=\"heti-spacing\"> </span>" + m + "<span class=\"heti-spacing\"> </span>分";
    } else {
        document.getElementById("web-time").innerHTML = y + "<span class=\"heti-spacing\"> </span>年 <span class=\"heti-spacing\"> </span>" + d + "<span class=\"heti-spacing\"> </span>天 <span class=\"heti-spacing\"> </span>" + h + "<span class=\"heti-spacing\"> </span>时 <span class=\"heti-spacing\"> </span>" + m + "<span class=\"heti-spacing\"> </span>分";
    }
    setTimeout(updateTime, 1000 * 60);
}
updateTime();
function toggle_statistics() {
    var statistics = document.getElementById("statistics");
    if (statistics.style.opacity == 0) {
        statistics.style.opacity = 1;
    } else {
        statistics.style.opacity = 0;
    }
}
</script>
