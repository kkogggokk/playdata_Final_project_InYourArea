<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tutorial AnimeJS</title>
    <link rel="stylesheet" type="text/css" href="../static/css/home.css">
    <link rel="stylesheet" type="text/css" href="../static/css/style3.css">
</head>
<body>
    <section>
        <img src="../static/images/bg.jpg" id="bg">
        <img src="../static/images/bp_member.png" id="bp_member">
    </section>
    <div class="sec">
        <H2>BLACK PINK - lovesick girl</H2>
        <p>Blackpink released their debut full-length studio LP, The Album, at midnight on Thursday alongside dropping a new video for their new single, “Lovesick Girls.” The K-pop stars premiered the video during the debut of YouTube Originals 16-episode music series Released.</p>
    </div>
    <div class="video-container">
        <video id="a" preload="auto" controls>
            <source src="../static/videos/1080.mp4" type="video/mp4"></source>
        </video>
        <video id="b" autoplay="autoplay" loop muted>
            <source src="../static/videos/ad.mp4" type="video/mp4"></source>
            <source preload="auto" src="../static/videos/rose.mp4" type="video/mp4"></source>
            <source preload="auto" src="../static/videos/lisa.mp4" type="video/mp4"></source>
            <source preload="auto" src="../static/videos/jennie.mp4" type="video/mp4"></source>
            <source preload="auto" src="../static/videos/jisoo.mp4" type="video/mp4"></source>
        </video>
    </div>
    <div class="btn-container" style="text-align:center">
        <img src="../static/images/rose_logo.png" onclick="btnClick('../static/videos/rose.mp4')">
        <img src="../static/images/lisa_logo.png" onclick="btnClick('../static/videos/lisa.mp4')">
        <img src="../static/images/jennie_logo.png" onclick="btnClick('../static/videos/jennie.mp4')">
        <img src="../static/images/jisoo_logo.png" onclick="btnClick('../static/videos/jisoo.mp4')">
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.7.0/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.7.0/ScrollTrigger.min.js"></script>
    <script type="text/javascript"> // CSS 기능 
        gsap.to("#bg", {
            scrollTrigger : {
                scrub : 1
            },
            scale : 1.5
        });
        gsap.to("#bp_member", {
            scrollTrigger : {
                scrub : 1
            },
            scale : 0.5
        });
    </script>
    <script src="../static/js/Popcorn.js"></script>
    <script src="http://code.jquery.com/jquery-latest.js"></script>
    <script type="text/javascript"> //VIDEO 기능 
        var videos = {
            a: Popcorn(".video-container #a"),
            b: Popcorn(".video-container #b"),
        },
        scrub = $("#scrub"),
        loadCount = 0,
        events = "play pause timeupdate seeking".split(/\s+/g);
        Popcorn.forEach(videos, function(media, type) {
        media.on("canplayall", function() {
            this.emit("sync");
            scrub.attr("max", this.duration());   
        }).on("sync", function() {
            if (++loadCount == 2) {
            events.forEach(function(event) {
                videos.a.on(event, function() {
                if (event === "timeupdate") {
                    if (!this.media.paused) {
                    return;
                    }
                    videos.b.emit("timeupdate");
                    scrub.val(this.currentTime());
                    return;
                }
                if (event === "seeking") {
                    videos.b.currentTime(this.currentTime());
                }
                if (event === "play" || event === "pause") {
                    videos.b[event]();
                }
                });
            });
            }
        });
        });
        scrub.bind("change", function() {
        var val = this.value;
        videos.a.currentTime(val);
        videos.b.currentTime(val);
        });
        function sync() {
        if (videos.b.media.readyState === 4) { //TODO : ===readyState, === 확인 
            videos.b.currentTime(
            videos.a.currentTime()
            );
        }
        requestAnimationFrame(sync); //TODO : === requestAnimationFrame 확인 
        }
        function btnClick(srcVideo){
            let orinVideo = document.getElementById("a");
            let resultVideo = document.getElementById("b");
            let source = document.createElement("source");
            resultVideo.setAttribute('src',srcVideo)
            orinVideo.appendChild(source);
            sync();
        }
    </script>
</body>
</html>