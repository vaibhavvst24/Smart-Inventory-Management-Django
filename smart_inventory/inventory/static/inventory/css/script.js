// Popup auto hide

setTimeout(() => {

let popup = document.getElementById("popup");

if(popup)
popup.style.display = "none";

}, 3000);



// Dark mode toggle

function toggleDarkMode(){

document.body.classList.toggle("dark");

}
