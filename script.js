document.addEventListener("DOMContentLoaded", function () {
    let bgMusic = document.getElementById('bg-music');
    let currentMusicSrc = "";

    // 垂直滑动切换文件夹
    let verticalSwiper = new Swiper('.swiper-container', {
        direction: 'vertical',
        loop: false,
        on: {
            slideChange: updateMusic // 触发背景音乐更新
        }
    });

    // 水平滑动切换文件夹内的内容
    let horizontalSwipers = document.querySelectorAll('.swiper-horizontal');
    horizontalSwipers.forEach(container => {
        new Swiper(container, {
            direction: 'horizontal',
            loop: false
        });
    });

    function updateMusic() {
        let newFolder = document.querySelector('.swiper-slide-active'); // 获取当前激活的文件夹
        let newMusicSrc = newFolder.dataset.music; // 获取该文件夹的背景音乐

        if (newMusicSrc && newMusicSrc !== currentMusicSrc) {
            currentMusicSrc = newMusicSrc;
            bgMusic.src = newMusicSrc;
            bgMusic.play().catch(error => console.log("音乐播放失败:", error));
        }
    }

    // 监听上下滑动切换文件夹，保证音乐切换
    verticalSwiper.on('slideChangeTransitionEnd', updateMusic);

    // 图片自动播放（3秒切换）
    function autoSlideImages() {
        let activeFolder = document.querySelector('.swiper-slide-active .swiper-horizontal .swiper-wrapper');
        if (!activeFolder) return;

        let imageSlides = activeFolder.querySelectorAll('.image-slide');
        if (imageSlides.length === 0) return;

        let currentIndex = 0;
        function nextImage() {
            imageSlides[currentIndex].classList.remove('active');
            currentIndex = (currentIndex + 1) % imageSlides.length;
            activeFolder.style.transform = `translateX(-${currentIndex * 100}%)`;
            imageSlides[currentIndex].classList.add('active');
        }
        setInterval(nextImage, 3000);
    }
    autoSlideImages();

    // 点击暂停/播放所有内容
    document.querySelectorAll('.folder').forEach(folder => {
        folder.addEventListener('click', function () {
            if (bgMusic.paused) {
                bgMusic.play();
                document.querySelectorAll('.video-slide').forEach(video => video.play());
                autoSlideImages();
            } else {
                bgMusic.pause();
                document.querySelectorAll('.video-slide').forEach(video => video.pause());
            }
        });
    });
});