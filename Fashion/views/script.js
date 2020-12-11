window.onscroll = function() {
    stickHeader();
}

var container = document.querySelector(".header-container-2");
var logo = document.querySelector(".header-logo");
var registerLoginContainer = document.querySelector(".register-login-container");
var sticky = container.offsetTop;

var slideIdx = 0;
var slides = document.querySelectorAll(".info-slide-container");
incrementSlideIdx();

setInterval(checkIfWidthLessThan700, 500);

function stickHeader () {
    if (window.pageYOffset >= sticky) {
        container.classList.add("sticky");
        logo.setAttribute("src", "imgs/nwo4.png");
        logo.style.top = "3rem";
    } else {
        container.classList.remove("sticky");

        if (window.innerWidth > 700)
        {
            logo.setAttribute("src", "imgs/nwo2.png");
            logo.style.top = "-6rem";
            logo.style.left = "9rem";
        }
    }
}

function checkIfWidthLessThan700 () {
    if (window.innerWidth <= 700) {
        logo.setAttribute("src", "imgs/nwo4.png");
        logo.style.top = "3rem";

        if (window.innerWidth <= 515) {
            logo.style.left = "1rem";
            registerLoginContainer.style.right = "1rem";
            Array.from(registerLoginContainer.children).forEach(child => child.style.margin = "0.1rem");
        } else {
            logo.style.left = "3rem";
            registerLoginContainer.style.right = "2rem";
            Array.from(registerLoginContainer.children).forEach(child => child.style.margin = "0.1rem");
        }

        console.log("Lefted");
    } else
    {
        logo.style.left = "9rem";
        registerLoginContainer.style.right = "5rem";
        Array.from(registerLoginContainer.children).forEach(child => child.style.margin = "1rem");
    }
}

function incrementSlideIdx () {
    console.log("Again");
    slideIdx++;

    if (slideIdx == slides.length)
        slideIdx = 0;

    for (var i = 0; i < slides.length; i++)
    {
        slides[i].style.display = i == slideIdx ? "flex" : "none";
    }

    setTimeout(incrementSlideIdx, 3000);
}