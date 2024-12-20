let InfoText = ""
const hud = document.createElement("div");
hud.id = "floatingHUD";
// hud.style.position = "fixed";
hud.style.top = "10px";
hud.style.right = "10px";
hud.style.width = "200px";
hud.style.padding = "15px";
hud.style.backgroundColor = "#333";
hud.style.color = "#fff";
hud.style.zIndex = "10000";
hud.style.borderRadius = "8px";
hud.style.boxShadow = "0 4px 8px rgba(0, 0, 0, 0.2)";
hud.style.cursor = "move";
hud.style.userSelect = "none";


hud.innerHTML = `
    <h4 style="margin: 0 0 10px; font-size: 16px;">Extension HUD</h4>
    <div id="multiLineLabel" style="white-space: pre-wrap; font-size: 14px; line-height: 1.5; margin-bottom: 10px;"></div>
    <button id="actionButton">Run Action</button>
`;

let isDragging = false;

hud.onmousedown = function (event) {
     isDragging = true;
     document.body.style.userSelect = "none"; // Disable background selection

     let shiftX = event.clientX - hud.getBoundingClientRect().left;
     let shiftY = event.clientY - hud.getBoundingClientRect().top;

     function moveAt(pageX, pageY) {
          hud.style.left = pageX - shiftX + 'px';
          hud.style.top = pageY - shiftY + 'px';
     }

     function onMouseMove(event) {
          if (isDragging) moveAt(event.pageX, event.pageY);
     }

     document.addEventListener('mousemove', onMouseMove);

     hud.onmouseup = function () {
          isDragging = false;
          document.removeEventListener('mousemove', onMouseMove);
          document.body.style.userSelect = ""; // Re-enable background selection
          hud.onmouseup = null;
     };
};

hud.ondragstart = function () {
     return false; // Prevent default drag behavior
};

chrome.runtime.onMessage.addListener(
     function (arg, sender, sendResponse) {
          if (arg.type == "startRecording") {
               document.body.appendChild(hud);
          } else if (arg.type == "endRecording") {
               document.body.removeChild(hud);
          } else if (arg.type == "setInfoText") {

          }
     }
);