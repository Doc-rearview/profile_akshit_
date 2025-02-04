// Loader
window.addEventListener('load', () => {
  const loader = document.getElementById('loader');
  
  // Set a timeout to make the loader disappear after 5 seconds
  setTimeout(() => {
    // Add fade-out class to apply the fade effect
    loader.classList.add('fade-out');
    
    // Add 'loaded' class to show the page content
    document.body.classList.add('loaded');
    
    // Remove the loader from the DOM after the fade-out transition is complete
    setTimeout(() => {
      loader.style.display = 'none';
    }, 1000); // Timeout for the fade-out duration
  }, 500); // 5 seconds
});



// Theme Toggle Functionality
const toggleSwitch = document.querySelector('#check-5');
const currentTheme = localStorage.getItem('theme');

if (currentTheme) {
  document.documentElement.setAttribute('data-theme', currentTheme);
  if (currentTheme === 'dark') {
    toggleSwitch.checked = true;
  }
}

function switchTheme(e) {
  if (e.target.checked) {
    document.documentElement.setAttribute('data-theme', 'dark');
    localStorage.setItem('theme', 'dark');
  } else {
    document.documentElement.setAttribute('data-theme', 'light');
    localStorage.setItem('theme', 'light');
  }
}

toggleSwitch.addEventListener('change', switchTheme);

// Hamburger Menu
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('nav-links');

hamburger.addEventListener('click', () => {
  navLinks.classList.toggle('active');
});

// Login Modal
function openLoginModal() {
  document.getElementById('loginModal').style.display = 'block';
}

function closeLoginModal() {
  document.getElementById('loginModal').style.display = 'none';
}

// Close modal when clicking outside of it
window.onclick = function (event) {
  const modal = document.getElementById('loginModal');
  if (event.target === modal) {
    modal.style.display = 'none';
  }
};

// // Handle CV Download
function downloadCV() {
  window.location.href = "/download-cv"; // Link to your backend route for CV download
}

const textLines = [
  "Building intelligent solutions,"," 1 algorithm at a time.",
  "Turning data into decisions, and",
  "Turning ideas into apps.",
  "AI-driven innovation meets",
  "Seamless app experiences. with us!!"
];

const typingElement = document.querySelector(".typing-effect");
let lineIndex = 0;

function typeText(line) {
  typingElement.style.opacity = "1"; // Ensure opacity is visible
  typingElement.textContent = "";
  let charIndex = 0;

  let typingInterval = setInterval(() => {
    if (charIndex < line.length) {
      typingElement.textContent += line.charAt(charIndex);
      charIndex++;
    } else {
      clearInterval(typingInterval);
      setTimeout(() => {
        // Smooth fade out before switching text
        typingElement.style.transition = "opacity 0.5s";
        typingElement.style.opacity = "0"; 

        setTimeout(() => {
          lineIndex = (lineIndex + 1) % textLines.length;
          typeText(textLines[lineIndex]);
        }, 500); // Wait for fade-out before changing text
      }, 2000);
    }
  }, 50);
}

// Start the typing effect
typeText(textLines[lineIndex]);




function submitLoginForm(event) {
  event.preventDefault(); // Prevent the form from submitting normally

  const form = event.target;
  const formData = new FormData(form);

  fetch('/login', {
      method: 'POST',
      body: formData
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
          // Redirect to the profile page on successful login
          window.location.href = data.redirect_url;
      } else {
          // Display the error message in the modal
          const errorElement = document.getElementById('loginError');
          errorElement.textContent = data.error;
          errorElement.style.display = 'block';
      }
  })
  .catch(error => {
      console.error('Error:', error);
  });
}

function closeLoginModal() {
  document.getElementById('loginModal').style.display = 'none';
}


let originalTitle = document.title;

        document.addEventListener("visibilitychange", function() {
            if (document.hidden) {
                document.title = "😊 Please visit again!";
            } else {
                document.title = originalTitle;
            }
        });

        document.addEventListener("DOMContentLoaded", function () {
          const elements = document.querySelectorAll(".fade-in");
        
          const scrollAnimation = () => {
            elements.forEach((el) => {
              const rect = el.getBoundingClientRect();
              if (rect.top < window.innerHeight * 0.85) {
                el.classList.add("show");
              }
            });
          };
        
          window.addEventListener("scroll", scrollAnimation);
          scrollAnimation(); // Run once on page load
        });
        


        const form = document.getElementById('contactForm');
        const responseMessage = document.getElementById('formResponse');
      
        form.addEventListener('submit', (e) => {
          e.preventDefault(); // Prevent default form submission
      
          const formData = new FormData(form);
      
          fetch(form.action, {
            method: form.method,
            body: formData,
          })
            .then((response) => {
              if (response.ok) {
                responseMessage.style.display = 'block';
                responseMessage.textContent = 'Thank you for your message! We will get back to you soon.';
                responseMessage.style.color = 'green';
              } else {
                responseMessage.style.display = 'block';
                responseMessage.textContent = 'Something went wrong. Please try again.';
                responseMessage.style.color = 'red';
              }
            })
            .catch(() => {
              responseMessage.style.display = 'block';
              responseMessage.textContent = 'An error occurred. Please try again later.';
              responseMessage.style.color = 'red';
            });
        });

        