document.addEventListener("DOMContentLoaded", function () {
    let verticalSwiper = new Swiper('.swiper-container', {
        direction: 'vertical',
        loop: false,
        on: {
            slideChange: updateMusic
        }
    });

    let horizontalSwipers = document.querySelectorAll('.swiper-horizontal');
    horizontalSwipers.forEach(container => {
        new Swiper(container, {
            direction: 'horizontal',
            loop: false
        });
    });

    let bgMusic = document.getElementById('bg-music');
    let currentFolder = document.querySelector('.swiper-slide-active');
    updateMusic();

    function updateMusic() {
        let newFolder = document.querySelector('.swiper-slide-active');
        if (newFolder && newFolder.dataset.music) {
            let newMusicSrc = newFolder.dataset.music;
            if (bgMusic.src.includes(newMusicSrc)) return;
            bgMusic.src = newMusicSrc;
            bgMusic.play();
        }
    }

    // 图片自动播放（3秒切换）
    let images = document.querySelectorAll('.image-slide');
    let currentIndex = 0;

    function autoSlideImages() {
        let activeFolder = document.querySelector('.swiper-slide-active .swiper-horizontal .swiper-wrapper');
        if (!activeFolder) return;

        let imageSlides = activeFolder.querySelectorAll('.image-slide');
        if (imageSlides.length === 0) return;

        imageSlides[currentIndex].classList.remove('active');
        currentIndex = (currentIndex + 1) % imageSlides.length;
        activeFolder.style.transform = `translateX(-${currentIndex * 100}%)`;
        imageSlides[currentIndex].classList.add('active');

        setTimeout(autoSlideImages, 3000);
    }
    autoSlideImages();

    // 点击暂停/播放所有内容
    document.querySelectorAll('.folder').forEach(folder => {
        folder.addEventListener('click', function () {
            let isPaused = bgMusic.paused;
            if (isPaused) {
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