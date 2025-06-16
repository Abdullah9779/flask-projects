def template_one(name, date, wish, song_url, picture_url_list, first_img ):
  code1 = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{name} Birthday Countdown</title>
  <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Poppins:wght@400;600&display=swap" rel="stylesheet">
  """
  code2 = """
  <style>
    :root {
      --primary-color: #ff6b6b;
      --secondary-color: #ff9e9e;
      --accent-color: #ffe66d;
    }

    body {
      font-family: 'Poppins', sans-serif;
      text-align: center;
      margin: 0;
      padding: 0;
      background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
      color: white;
      min-height: 100vh;
      overflow-x: hidden;
      transition: background 0.5s ease;
    }

    .top-right-image {
      display: none;
      position: fixed;
      top: 20px;
      right: 20px;
      width: 100px;
      height: 100px;
      border-radius: 50%;
      border: 3px solid white;
      box-shadow: 0 8px 15px rgba(0,0,0,0.2);
      transition: all 0.3s ease;
      cursor: pointer;
      z-index: 100;
      object-fit: cover;
    }

    .top-right-image:hover {
      transform: rotate(15deg) scale(1.1);
      box-shadow: 0 12px 20px rgba(0,0,0,0.3);
    }

    h2 {
      font-family: 'Dancing Script', cursive;
      font-size: 2.5rem;
      margin: 20px 0;
      text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
      padding: 0 20px;
    }

    .year {
      font-size: 2.5rem;
      color: var(--accent-color);
      text-shadow: 0 0 10px rgba(255,230,109,0.5);
      margin: 20px 0;
    }

    .title {
      padding-top: 80px;
    }

    .countdown {
      display: flex;
      justify-content: center;
      gap: 20px;
      margin: 30px 0;
      padding: 20px;
      background: rgba(255,255,255,0.1);
      backdrop-filter: blur(10px);
      border-radius: 15px;
      box-shadow: 0 6px 25px rgba(0,0,0,0.1);
      flex-wrap: wrap;
    }

    .countdown div {
      font-size: 2rem;
      font-weight: 600;
      position: relative;
      padding: 15px;
      min-width: 100px;
      background: rgba(255,255,255,0.15);
      border-radius: 10px;
      box-shadow: 0 3px 10px rgba(0,0,0,0.1);
      transition: all 0.3s ease;
      text-align: center;
    }

    .countdown div::before {
      content: attr(data-label);
      position: absolute;
      bottom: -25px;
      left: 50%;
      transform: translateX(-50%);
      font-size: 0.8rem;
      font-weight: 400;
      color: var(--accent-color);
      text-transform: uppercase;
      letter-spacing: 1px;
      padding: 5px;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
      .countdown {
        flex-direction: column;
        gap: 20px;
        padding: 20px;
      }

      h2 {
        font-size: 2rem;
      }

      .year {
        font-size: 2rem;
      }

      .countdown div {
        font-size: 2rem;
        min-width: 100px;
      }
    }

    @media (max-width: 480px) {
      .countdown div {
        font-size: 1.2rem;
        padding: 8px;
        min-width: 60px;
      }
    }

    #playPauseButton, #wish {
      position: fixed;
      background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
      color: white;
      padding: 12px 25px;
      border: none;
      border-radius: 30px;
      font-size: 1rem;
      cursor: pointer;
      transition: all 0.3s ease;
      box-shadow: 0 4px 15px rgba(0,0,0,0.2);
      display: flex;
      align-items: center;
      gap: 10px;
      z-index: 100;
    }

    #playPauseButton {
      display: none;
      bottom: 30px;
      left: 30px;
    }

    #playPauseButton:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }

    #wish {
      bottom: 30px;
      right: 30px;
    }

    #wish:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }

    .modal {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0,0,0,0.9);
      z-index: 1000;
    }

    .modal-content {
      display: none;
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      max-width: 90%;
      max-height: 90%;
      border-radius: 15px;
      box-shadow: 0 0 40px rgba(255,255,255,0.2);
      transition: transform 0.3s ease;
      cursor: zoom-in;
    }

    .close {
      position: absolute;
      top: 20px;
      right: 30px;
      color: white;
      font-size: 40px;
      cursor: pointer;
      transition: all 0.3s ease;
    }

    .close:hover {
      color: var(--accent-color);
      transform: rotate(90deg);
    }

    .celebration-particle {
      position: absolute;
      pointer-events: none;
      animation: float 4s infinite linear;
    }

    @keyframes float {
      0% { transform: translateY(100vh) rotate(0deg); }
      100% { transform: translateY(-100vh) rotate(360deg); }
    }

    .balloon {
      position: absolute;
      width: 40px;
      height: 60px;
      background: #ff6b6b;
      border-radius: 80% 80% 120% 120%;
      animation: float 8s infinite ease-in;
      bottom: -60px;
      z-index: 10;
      opacity: 0.8;
    }

    .balloon::after {
      content: "";
      position: absolute;
      bottom: -10px;
      left: 50%;
      width: 2px;
      height: 40px;
      background: white;
    }

    @keyframes float {
      0% {
        transform: translateY(0) rotate(0deg);
        bottom: -60px;
      }
      100% {
        transform: translateY(-100vh) rotate(360deg);
        bottom: 100vh;
      }
    }

    /* --- Updated Dialog Box Styles --- */
    .dialog {
      display: none; /* Hidden by default */
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.5); /* Semi-transparent background */
      align-items: center;
      justify-content: center;
      z-index: 1000;
      opacity: 0;
      transition: opacity 0.3s ease;
    }

    .dialog.show {
      display: flex;
      opacity: 1;
    }

    .dialog-content {
      background: #00d2ff;
      color: #333;
      padding: 20px;
      border-radius: 8px;
      width: 90%;
      max-width: 600px;
      position: relative;
      box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }

    .close-btn {
      position: absolute;
      top: 10px;
      right: 15px;
      font-size: 24px;
      font-weight: bold;
      cursor: pointer;
    }
  </style>
    """
  code3 = f"""
</head>
<body>
  <img class="top-right-image" src="{first_img}" alt="image" />

  <h2 class="title">🎉 Countdown to {name} Magical Birthday 🎂</h2>
  <div class="year">{date}</div>
  
  <div class="countdown">
    <div data-label="Days" id="day">00</div>
    <div data-label="Hours" id="hour">00</div>
    <div data-label="Minutes" id="minute">00</div>
    <div data-label="Seconds" id="second">00</div>
  </div>


  <div id="image-modal" class="modal">
    <span class="close">&times;</span>
    <img class="modal-content" id="modal-image" alt="Enlarged Image">
  </div>

  <button id="playPauseButton">
    <span>🎵</span>
    <span>Play Song</span>
  </button>

  <button id="wish">
    Wish 😊
  </button>

  <!-- Dialog Box -->
  <div id="dialogBox" class="dialog">
    <div class="dialog-content">
      <span id="closeDialogBtn" class="close-btn">&times;</span>
      <p>
        {wish}
      </p>
    </div>
  </div>

  <audio id="audioPlayer">
    <source src="{song_url}">
  </audio>

  <script>
    document.documentElement.webkitRequestFullscreen();
    // Countdown Timer Elements
    const dayEl = document.getElementById("day");
    const hourEl = document.getElementById("hour");
    const minuteEl = document.getElementById("minute");
    const secondEl = document.getElementById("second");
    const birthdayTime = new Date("{date} 00:00:00").getTime();
    const body = document.body;
    const songbutton = document.getElementById("playPauseButton");
    const wishButton = document.getElementById("wish");

    // Image cycling elements
    const imageUrls = {picture_url_list};
    let currentImageIndex = 0;
    const profileImage = document.querySelector('.top-right-image');
    const modalImage = document.getElementById('modal-image');
"""
  code4 = """

    function cycleImages() {
      profileImage.style.opacity = 0;
      setTimeout(() => {
        currentImageIndex = (currentImageIndex + 1) % imageUrls.length;
        profileImage.src = imageUrls[currentImageIndex];
        modalImage.src = imageUrls[currentImageIndex];
        profileImage.style.opacity = 1;
      }, 500);
    }
    setInterval(cycleImages, 5000);

    // Countdown Timer Function
    function updateCountdown() {
      const now = new Date().getTime();
      const gap = birthdayTime - now;

      const second = 1000;
      const minute = second * 60;
      const hour = minute * 60;
      const day = hour * 24;

      const d = Math.floor(gap / day);
      const h = Math.floor((gap % day) / hour);
      const m = Math.floor((gap % hour) / minute);
      const s = Math.floor((gap % minute) / second);

      if (gap >= 0) {
        dayEl.textContent = d.toString().padStart(2, '0');
        hourEl.textContent = h.toString().padStart(2, '0');
        minuteEl.textContent = m.toString().padStart(2, '0');
        secondEl.textContent = s.toString().padStart(2, '0');
      }
      
      updateBackground(gap);
      requestAnimationFrame(updateCountdown);
    }

    // Update background and handle wish button visibility
    function updateBackground(gap) {
      let background = '';
      if (gap <= 0) {
        background = 'radial-gradient(circle, #00d2ff, #3a7bd5)';
        songbutton.style.background = "#00d2ff";
        wish.style.background = "#00d2ff"
        wishButton.style.display = "flex";
        songbutton.style.display = "flex";
        profileImage.style.display = "flex";
        modalImage.style.display = "flex";
        addCelebration();
      } else if (gap <= 86400000) {
        background = 'linear-gradient(135deg, #ff9e9e, #ff6b6b)';
        wishButton.style.display = "none";
      } else if (gap <= 604800000) {
        background = 'linear-gradient(135deg, #ffb347, #ff6b6b)';
        wishButton.style.display = "none";
      } else {
        background = 'linear-gradient(135deg, var(--primary-color), var(--secondary-color))';
        wishButton.style.display = "none";
      }
      body.style.background = background;
    }

    function addCelebration() {
      createParticles();
    }

    function createParticles() {
      for (let i = 0; i < 1; i++) {
        const particle = document.createElement('div');
        particle.className = 'celebration-particle';
        particle.innerHTML = ['🎉', '🎂', '🎈', '✨', '🥳'][Math.floor(Math.random() * 5)];
        particle.style.left = Math.random() * 100 + '%';
        particle.style.fontSize = Math.random() * 20 + 10 + 'px';
        particle.style.animationDuration = Math.random() * 3 + 2 + 's';
        document.body.appendChild(particle);
        setTimeout(() => particle.remove(), 5000);
      }
    }

    function addBalloons() {
      const balloon = document.createElement('div');
      balloon.className = 'balloon';
      balloon.style.left = Math.random() * 100 + 'vw';
      balloon.style.animationDelay = Math.random() * 2 + 's';
      balloon.style.background = `hsl(${Math.random() * 360}, 70%, 60%)`;
      document.body.appendChild(balloon);
      setTimeout(() => balloon.remove(), 8000);
    }

    // Modal Controls for Image
    const modal = document.getElementById('image-modal');
    document.querySelector('.top-right-image').addEventListener('click', () => {
      modal.style.display = 'block';
    });
    document.querySelector('.close').addEventListener('click', () => {
      modal.style.display = 'none';
    });
    window.addEventListener('click', (e) => {
      if (e.target === modal) modal.style.display = 'none';
    });

    // Audio Controls
    const audioPlayer = document.getElementById('audioPlayer');
    const playPauseButton = document.getElementById('playPauseButton');
    function togglePlayPause() {
      if (audioPlayer.paused) {
        audioPlayer.play();
        playPauseButton.innerHTML = '<span>🎵</span> Pause Song';
      } else {
        audioPlayer.pause();
        playPauseButton.innerHTML = '<span>🎵</span> Play Song';
      }
    }
    playPauseButton.addEventListener('click', togglePlayPause);

    // Dialog Box Controls
    const dialogBox = document.getElementById('dialogBox');
    const closeDialogBtn = document.getElementById('closeDialogBtn');

    wishButton.addEventListener('click', function() {
      dialogBox.classList.add('show');
    });

    closeDialogBtn.addEventListener('click', function() {
      dialogBox.classList.remove('show');
    });

    window.addEventListener('click', function(event) {
      if (event.target === dialogBox) {
        dialogBox.classList.remove('show');
      }
    });

    // Initialize Countdown and Effects
    updateCountdown();
    setInterval(createParticles, 6000);
    setInterval(addBalloons, 5000);


    document.addEventListener("click", () => {
            // Log "hello" to the console when the page is clicked
            console.log("hello");

            // Attempt to enter fullscreen
            try {
                if (document.documentElement.requestFullscreen) {
                    document.documentElement.requestFullscreen();
                } else if (document.documentElement.mozRequestFullScreen) {
                    document.documentElement.mozRequestFullScreen(); // Firefox
                } else if (document.documentElement.webkitRequestFullscreen) {
                    document.documentElement.webkitRequestFullscreen(); // Chrome, Safari, Edge
                } else if (document.documentElement.msRequestFullscreen) {
                    document.documentElement.msRequestFullscreen(); // IE/Edge
                }
            } catch (e) {
                console.error("Fullscreen request failed:", e);
            }
        })
    
  </script>
</body>
</html>


"""

  return f"""
{code1}
{code2}
{code3}
{code4}
"""


