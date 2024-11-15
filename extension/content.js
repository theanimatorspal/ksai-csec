let global_data = { should_highlight: false };
let clickedElements = [];

function addHighlight(element) {
     if (element.style) {
          element.style.outline = "2px solid red";
     }
}

function removeHighlight(element) {
     if (element.style) {
          element.style.outline = "";
     }
}

document.addEventListener("mouseover", (event) => {
     if (global_data.should_highlight) {
          addHighlight(event.target);
     }
});

document.addEventListener("mouseout", (event) => {
     removeHighlight(event.target);
});

document.addEventListener("click", (event) => {
     const target = event.target;
     if ((target.tagName === "INPUT" || target.tagName === "BUTTON") && !clickedElements.includes(target)) {
          clickedElements.push(target);
     }
});

chrome.runtime.onMessage.addListener(
     function (arg, sender, sendResponse) {
          if (arg.type == "startRecording") {
               console.log("should hightlight changed")
               global_data.should_highlight = true;
               clickedElements = [];
          } else if (arg.type == "endRecording") {
               console.log("should hightlight changed")
               global_data.should_highlight = false;
               clickedElements = [];
          }
     }
);