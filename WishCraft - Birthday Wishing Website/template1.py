def template_two(name, date, wish, song_url, picture_url_list, first_img ):
	code1 = f"""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{name} Birthday Countdown</title>
    <!-- Import Google Fonts -->
    <link
      href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Poppins:wght@400;600&display=swap"
      rel="stylesheet"
    />
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Tailwind configuration for custom colors, fonts, and animations -->
 """
	code2 = """
    <script>
      tailwind.config = {
        theme: {
          extend: {
            fontFamily: {
              poppins: ['Poppins', 'sans-serif'],
              dancing: ['"Dancing Script"', 'cursive'],
            },
            colors: {
              primary: "#6b46c1", // Purple
              secondary: "#9f7aea", // Lighter purple
              accent: "#f6e05e", // Golden yellow
              celebrationBg: "#4fd1c5", // Teal
            },
            keyframes: {
              float: {
                "0%": { transform: "translateY(100vh) rotate(0deg)" },
                "100%": { transform: "translateY(-100vh) rotate(360deg)" },
              },
            },
            animation: {
              float: "float 4s infinite linear",
              "float-slow": "float 8s infinite ease-in",
            },
          },
        },
      };
    </script>
    """
	code3 = f"""
  </head>
  <body
    class="font-poppins text-center m-0 p-0 bg-gradient-to-br from-primary to-secondary text-white min-h-screen overflow-x-hidden transition-colors duration-500 ease-in-out"
  >
    <!-- Top Right Image (initially hidden) -->
    <img
      class="top-right-image hidden fixed top-5 right-5 w-[100px] h-[100px] rounded-full border-[3px] border-white shadow-[0_8px_15px_rgba(0,0,0,0.2)] transition-all duration-300 ease-in-out cursor-pointer z-[100] object-cover hover:rotate-[15deg] hover:scale-110 hover:shadow-[0_12px_20px_rgba(0,0,0,0.3)]"
      src="{first_img}"
      alt="image"
    />

    <!-- Page Title -->
    <h2 class="pt-20 font-dancing text-4xl md:text-5xl my-5 drop-shadow-md px-5">
      🎉 Countdown to {name} Magical Birthday 🎂
    </h2>
    <div
      class="text-[2.5rem] text-accent my-5 drop-shadow-[0_0_10px_rgba(246,224,94,0.5)]"
    >
      {date}
    </div>

    <!-- Countdown Container -->
    <div
      class="flex flex-col md:flex-row justify-center gap-5 my-8 p-5 bg-white/10 backdrop-blur-md rounded-xl shadow-md flex-wrap"
    >
      <!-- Countdown Item: Days -->
      <div
        class="relative text-2xl font-semibold p-4 min-w-[100px] bg-[rgba(255,255,255,0.15)] rounded-lg shadow-sm transition-all duration-300 text-center"
      >
        <div id="day">00</div>
        <div
          class="text-xs font-normal uppercase tracking-widest text-accent mt-2"
        >
          Days
        </div>
      </div>
      <!-- Countdown Item: Hours -->
      <div
        class="relative text-2xl font-semibold p-4 min-w-[100px] bg-[rgba(255,255,255,0.15)] rounded-lg shadow-sm transition-all duration-300 text-center"
      >
        <div id="hour">00</div>
        <div
          class="text-xs font-normal uppercase tracking-widest text-accent mt-2"
        >
          Hours
        </div>
      </div>
      <!-- Countdown Item: Minutes -->
      <div
        class="relative text-2xl font-semibold p-4 min-w-[100px] bg-[rgba(255,255,255,0.15)] rounded-lg shadow-sm transition-all duration-300 text-center"
      >
        <div id="minute">00</div>
        <div
          class="text-xs font-normal uppercase tracking-widest text-accent mt-2"
        >
          Minutes
        </div>
      </div>
      <!-- Countdown Item: Seconds -->
      <div
        class="relative text-2xl font-semibold p-4 min-w-[100px] bg-[rgba(255,255,255,0.15)] rounded-lg shadow-sm transition-all duration-300 text-center"
      >
        <div id="second">00</div>
        <div
          class="text-xs font-normal uppercase tracking-widest text-accent mt-2"
        >
          Seconds
        </div>
      </div>
    </div>

    <!-- Image Modal -->
    <div
      id="image-modal"
      class="fixed inset-0 bg-black bg-opacity-90 hidden z-[1000]"
    >
      <span
        class="close absolute top-5 right-7 text-white text-4xl cursor-pointer transition-all duration-300 hover:rotate-90"
        >&times;</span
      >
      <img
        class="modal-content hidden absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 max-w-[90%] max-h-[90%] rounded-xl shadow-[0_0_40px_rgba(255,255,255,0.2)] transition-transform duration-300 cursor-pointer"
        id="modal-image"
        alt="Enlarged Image"
      />
    </div>

    <!-- Audio Play/Pause Button (initially hidden) -->
    <button
      id="playPauseButton"
      class="fixed bottom-[30px] left-[30px] hidden bg-gradient-to-br from-primary to-secondary text-white py-3 px-6 rounded-full text-base cursor-pointer transition-all duration-300 shadow-lg flex items-center gap-2 hover:-translate-y-1"
    >
      <span>🎵</span>
      <span>Play Song</span>
    </button>

    <!-- Wish Button -->
    <button
      id="wish"
      class="fixed bottom-[30px] right-[30px] bg-gradient-to-br from-primary to-secondary text-white py-3 px-6 rounded-full text-base cursor-pointer transition-all duration-300 shadow-lg flex items-center gap-2 hover:-translate-y-1"
    >
      Wish 😊
    </button>

    <!-- Dialog Box -->
    <div
      id="dialogBox"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center hidden opacity-0 transition-opacity duration-300 z-[1000]"
    >
      <div
        class="dialog-content bg-celebrationBg text-gray-800 p-5 rounded-lg w-11/12 max-w-xl relative shadow-md"
      >
        <span
          id="closeDialogBtn"
          class="close-btn absolute top-2 right-4 text-2xl font-bold cursor-pointer"
          >&times;</span
        >
        <p>
          {wish}
        </p>
      </div>
    </div>

    <!-- Audio Player -->
    <audio id="audioPlayer">
      <source
        src="{song_url}"
        type="audio/mpeg"
      />
    </audio>

    <!-- JavaScript -->
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
      const profileImage = document.querySelector(".top-right-image");
      const modalImage = document.getElementById("modal-image");
      """
	code4="""

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
          dayEl.textContent = d.toString().padStart(2, "0");
          hourEl.textContent = h.toString().padStart(2, "0");
          minuteEl.textContent = m.toString().padStart(2, "0");
          secondEl.textContent = s.toString().padStart(2, "0");
        }

        updateBackground(gap);
        requestAnimationFrame(updateCountdown);
      }

      // Update background and handle wish button visibility
      function updateBackground(gap) {
        let background = "";
        if (gap <= 0) {
          background = "radial-gradient(circle, #4fd1c5, #319795)"; // Teal gradient
          songbutton.style.background = "#4fd1c5";
          wish.style.background = "#4fd1c5";
          wishButton.style.display = "flex";
          songbutton.style.display = "flex";
          profileImage.style.display = "flex";
          modalImage.style.display = "flex";
          addCelebration();
        } else if (gap <= 86400000) {
          background = "linear-gradient(135deg, #9f7aea, #6b46c1)";
          wishButton.style.display = "none";
        } else if (gap <= 604800000) {
          background = "linear-gradient(135deg, #805ad5, #6b46c1)";
          wishButton.style.display = "none";
        } else {
          background = "linear-gradient(135deg, #6b46c1, #9f7aea)";
          wishButton.style.display = "none";
        }
        body.style.background = background;
      }

      function addCelebration() {
        createParticles();
      }

      function createParticles() {
        for (let i = 0; i < 1; i++) {
          const particle = document.createElement("div");
          particle.className =
            "celebration-particle absolute pointer-events-none animate-float";
          particle.innerHTML =
            ["🎉", "🎂", "🎈", "✨", "🥳"][
              Math.floor(Math.random() * 5)
            ];
          particle.style.left = Math.random() * 100 + "%";
          particle.style.fontSize =
            Math.random() * 20 + 10 + "px";
          particle.style.animationDuration =
            Math.random() * 3 + 2 + "s";
          document.body.appendChild(particle);
          setTimeout(() => particle.remove(), 5000);
        }
      }

      function addBalloons() {
        const balloon = document.createElement("div");
        balloon.className =
          "balloon absolute w-10 h-[60px] bg-primary rounded-[80%_80%_120%_120%] animate-float-slow -bottom-[60px] z-10 opacity-80";
        balloon.style.left = Math.random() * 100 + "vw";
        balloon.style.animationDelay =
          Math.random() * 2 + "s";
        balloon.style.background = `hsl(${Math.random() * 360}, 70%, 60%)`;
        const string = document.createElement("span");
        string.className =
          "absolute -bottom-[10px] left-1/2 transform -translate-x-1/2 w-[2px] h-10 bg-white";
        balloon.appendChild(string);
        document.body.appendChild(balloon);
        setTimeout(() => balloon.remove(), 8000);
      }

      // Modal Controls for Image
      const modal = document.getElementById("image-modal");
      document.querySelector(".top-right-image").addEventListener("click", () => {
        modal.style.display = "block";
      });
      document.querySelector(".close").addEventListener("click", () => {
        modal.style.display = "none";
      });
      window.addEventListener("click", (e) => {
        if (e.target === modal) modal.style.display = "none";
      });

      // Audio Controls
      const audioPlayer = document.getElementById("audioPlayer");
      const playPauseButton = document.getElementById("playPauseButton");
      function togglePlayPause() {
        if (audioPlayer.paused) {
          audioPlayer.play();
          playPauseButton.innerHTML = '<span>🎵</span> Pause Song';
        } else {
          audioPlayer.pause();
          playPauseButton.innerHTML = '<span>🎵</span> Play Song';
        }
      }
      playPauseButton.addEventListener("click", togglePlayPause);

      // Dialog Box Controls
      const dialogBox = document.getElementById("dialogBox");
      const closeDialogBtn = document.getElementById("closeDialogBtn");

      wishButton.addEventListener("click", function () {
        dialogBox.classList.remove("hidden");
        dialogBox.classList.add("flex", "opacity-100");
      });

      closeDialogBtn.addEventListener("click", function () {
        dialogBox.classList.remove("flex", "opacity-100");
        dialogBox.classList.add("hidden");
      });

      window.addEventListener("click", function (event) {
        if (event.target === dialogBox) {
          dialogBox.classList.remove("flex", "opacity-100");
          dialogBox.classList.add("hidden");
        }
      });

      // Initialize Countdown and Effects
      updateCountdown();
      setInterval(createParticles, 6000);
      setInterval(addBalloons, 5000);

      document.addEventListener("click", () => {
        console.log("hello");
        try {
          if (document.documentElement.requestFullscreen) {
            document.documentElement.requestFullscreen();
          } else if (document.documentElement.mozRequestFullScreen) {
            document.documentElement.mozRequestFullScreen();
          } else if (document.documentElement.webkitRequestFullscreen) {
            document.documentElement.webkitRequestFullscreen();
          } else if (document.documentElement.msRequestFullscreen) {
            document.documentElement.msRequestFullscreen();
          }
        } catch (e) {
          console.error("Fullscreen request failed:", e);
        }
      });
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

# print(template_two("Abdullah", "12, 2, 2005", "hello", "https://", '["hh", "hh", "hh", "hh"]', "https://"))

