



document.getElementById("startDorking").addEventListener("click", () => {
     const targetDomain = document.getElementById("domainInput").value.trim();

     if (!targetDomain) {
          alert("Please enter a target domain.");
          return;
     }

     // List of Google dork queries
     const queries = [
          `site:${targetDomain} filetype:txt`,
          `site:${targetDomain} filetype:log`,
          `site:${targetDomain} filetype:env`,
          `site:${targetDomain} filetype:sql`,
          `site:${targetDomain} filetype:bak`,
          `site:${targetDomain} filetype:json`,
          `site:${targetDomain} filetype:xml`,
          `site:${targetDomain} filetype:yml`,
          `site:${targetDomain} filetype:db`,
          `site:${targetDomain} filetype:jsp`,
          `site:${targetDomain} filetype:js`,
          `site:${targetDomain} filetype:map`,
          `site:${targetDomain} filetype:pdf`,
          `site:${targetDomain} filetype:docx`,
          `site:${targetDomain} filetype:csv`,
          `site:${targetDomain} filetype:doc`,
          `site:${targetDomain} filetype:xls`,
          `site:${targetDomain} filetype:xlsx`,
          `site:${targetDomain} filetype:ppt`,
          `site:${targetDomain} filetype:pptx`,
          `site:${targetDomain} filetype:php`,
          `site:${targetDomain} filetype:pl`,
          `site:${targetDomain} filetype:py`,
          `site:${targetDomain} filetype:rb`,
          `site:${targetDomain} filetype:sh`,
          `site:${targetDomain} filetype:txt`,
          `site:${targetDomain} filetype:rtf`,
          `site:${targetDomain} filetype:md`,
          `site:${targetDomain} filetype:yaml`,
          `site:${targetDomain} filetype:ini`,
          `site:${targetDomain} filetype:log`,
          `site:${targetDomain} filetype:csv`,
          `site:${targetDomain} filetype:xml`,
          `site:${targetDomain} filetype:properties`,
          `site:${targetDomain} filetype:class`,
          `site:${targetDomain} filetype:jar`,
          `site:${targetDomain} filetype:war`,
          `site:${targetDomain} filetype:apk`,
          `site:${targetDomain} filetype:bin`,
          `site:${targetDomain} filetype:lock`,
          `site:${targetDomain} filetype:sql`,
          `site:${targetDomain} filetype:swp`,
          `site:${targetDomain} filetype:htaccess`,
          `site:${targetDomain} filetype:json`,
          `site:${targetDomain} filetype:svg`,
          `site:${targetDomain} filetype:css`,
          `site:${targetDomain} filetype:less`,
          `site:${targetDomain} filetype:sass`,

          `site:${targetDomain} inurl:db_backup`,
          `site:${targetDomain} inurl:admin`,
          `site:${targetDomain} inurl:login`,
          `site:${targetDomain} inurl:etc`,
          `site:${targetDomain} inurl:uploads`,
          `site:${targetDomain} inurl:"id="`,
          `site:${targetDomain} inurl:"redirect="`,
          `site:${targetDomain} inurl:"cmd="`,
          `site:${targetDomain} inurl:"lang="`,
          `site:${targetDomain} inurl:"/api/"`,
          `site:${targetDomain} inurl:"test"`,
          `site:${targetDomain} inurl:"/staging"`,

          `site:${targetDomain} intitle:"index of" "admin"`,
          `site:${targetDomain} intitle:"index of"`,
          `site:${targetDomain} intitle:"index of" backup`,

          `site:${targetDomain} intext:"password"`,
          `site:${targetDomain} intext:"API_KEY"`,
          `site:${targetDomain} intext:"Authorization: Bearer"`,

          `cache:${targetDomain}`,
     ];

     // Open each query in a new tab
     queries.forEach(query => {
          const url = `https://www.google.com/search?q=${encodeURIComponent(query)}`;
          chrome.tabs.create({ url });
     });
});

document.getElementById("startBrowsing").addEventListener("click", () => {
     const targetDomains = document.getElementById("domainsInput").
          value.
          split('\n').
          map(domain => domain.trim()).
          filter(domain => domain); // Creates a new array

     targetDomains.forEach(domain => {
          chrome.tabs.create({ domain });
     })
});

document.getElementById("spinnerExtractDepth").addEventListener("change", async () => {
     const spinnerValue = document.getElementById("spinnerExtractDepth").value;
     chrome.runtime.sendMessage({ type: "changeDepthValueForExtraction", depth: spinnerValue });
});


document.getElementById("startExtracting").addEventListener("click", async () => {
     const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
     chrome.runtime.sendMessage({ type: "extractMetadataByMessage", tab: tab, depth: 1 });
})


document.getElementById("downloadExtensionFiles").addEventListener("click", async () => {
     var input = document.getElementById("fileExtensionInput").value.trim()
     const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
     chrome.scripting.executeScript({
          target: { tabId: tab.id },
          func: downloadFilesWithExtension,
          args: [input]
     }).then(
          () => console.log("Script Executed")
     );
})


document.getElementById("resumeDownloadsButton").addEventListener("click", async () => {
     chrome.runtime.sendMessage({ type: "resumeAllDownloads" });
});


document.getElementById("resetEverything").addEventListener("click", async () => {
     chrome.runtime.sendMessage({ type: "resetEverything" });
});

document.getElementById("copyLogsToClipboard").addEventListener("click", async () => {
     const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
     chrome.runtime.sendMessage({ type: "copyLogsToClipboard", tab: tab });
});

document.getElementById("saveLogsToFile").addEventListener("click", async () => {
     chrome.runtime.sendMessage({ type: "saveLogsToFile" });
});


const proxyInput = document.getElementById("proxy-address");
const schemeSelect = document.getElementById("scheme");

window.addEventListener("DOMContentLoaded", () => {
     const savedProxy = localStorage.getItem("proxyAddress");
     const savedScheme = localStorage.getItem("scheme");

     if (savedProxy) proxyInput.value = savedProxy;
     if (savedScheme) schemeSelect.value = savedScheme;
});

document.getElementById("configureProxyButton").addEventListener("click", () => {
     const proxyAddress = proxyInput.value;
     const scheme = schemeSelect.value
     localStorage.setItem("proxyAddress", proxyAddress);
     localStorage.setItem("scheme", scheme);
     chrome.runtime.sendMessage({ type: "setProxy", address: proxyAddress, scheme: scheme })
});

document.getElementById("resetProxyButton").addEventListener("click", () => {
     chrome.runtime.sendMessage({ type: "resetProxy" });
});