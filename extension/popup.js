
async function Popup(inmessage) {
     function showPopup(message) {
          const popup = document.createElement("div");
          popup.textContent = message;
          Object.assign(popup.style, {
               position: "fixed",
               bottom: "20px",
               right: "50px",
               padding: "10px",
               backgroundColor: "rgba(1, 0, 0, 0.8)",
               color: "white",
               borderRadius: "5px",
               zIndex: "10000",
          });

          document.body.appendChild(popup);

          // Remove the popup after 5 seconds
          setTimeout(() => {
               popup.remove();
          }, 5000);
     }
     const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
     chrome.scripting.executeScript({
          target: { tabId: tab.id },
          func: showPopup,
          args: [inmessage]
     }).then(
          () => console.log("Script Executed")
     );
}



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
          `site:${targetDomain} inurl: "/view.shtml" inurl: "axis-cgi"`,
          `site:${targetDomain} inurl: "amazonaws.com" inurl: "/bucket/" -site: aws.amazon.com`,

          `cache:${targetDomain}`,
     ];

     // Open each query in a new tab
     queries.forEach(query => {
          const url = `https://www.google.com/search?q=${encodeURIComponent(query)}`;
          chrome.tabs.create({ url });
     });
});

document.getElementById("startGithubDorking").addEventListener("click", () => {

     // Define categories with associated dork queries
     const categories = {
          general: [
               "Jenkins", "OTP", "oauth", "authorization", "password", "pwd", "ftp", "dotfiles", "JDBC", "key-keys",
               "send_key-keys", "send,key-keys", "token", "user", "login-singin", "passkey-passkeys", "pass", "secret",
               "SecretAccessKey", "app_AWS_SECRET_ACCESS_KEY AWS_SECRET_ACCESS_KEY", "credentials", "config",
               "security_credentials", "connectionstring", "ssh2_auth_password", "DB_PASSWORD"
          ],
          bash: [
               "language:bash Jenkins", "language:bash OTP", "language:bash oauth", "language:bash authorization",
               "language:bash password", "language:bash pwd", "language:bash ftp", "language:bash dotfiles",
               "language:bash JDBC", "language:bash key-keys", "language:bash send_key-keys", "language:bash send,key-keys",
               "language:bash token", "language:bash user", "language:bash login-singin", "language:bash passkey-passkeys",
               "language:bash pass", "language:bash secret", "language:bash SecretAccessKey",
               "language:bash app_AWS_SECRET_ACCESS_KEY AWS_SECRET_ACCESS_KEY", "language:bash credentials",
               "language:bash config", "language:bash security_credentials", "language:bash connectionstring",
               "language:bash ssh2_auth_password", "language:bash DB_PASSWORD"
          ],
          python: [
               "language:python Jenkins", "language:python OTP", "language:python oauth", "language:python authorization",
               "language:python password", "language:python pwd", "language:python ftp", "language:python dotfiles",
               "language:python JDBC", "language:python key-keys", "language:python send_key-keys", "language:python send,key-keys",
               "language:python token", "language:python user", "language:python login-singin", "language:python passkey-passkeys",
               "language:python pass", "language:python secret", "language:python SecretAccessKey",
               "language:python app_AWS_SECRET_ACCESS_KEY AWS_SECRET_ACCESS_KEY", "language:python credentials",
               "language:python config", "language:python security_credentials", "language:python connectionstring",
               "language:python ssh2_auth_password", "language:python DB_PASSWORD"
          ]
     };

     // Sequentially process URLs for a single category
     const processUrlsSequentially = (urls, windowId, index = 0) => {
          if (index >= urls.length) return; // End of URLs

          // Open the next URL in a new tab
          chrome.tabs.create({ windowId, url: urls[index] }, () => {
               // Process the next URL after a short delay to prevent overloading
               setTimeout(() => {
                    processUrlsSequentially(urls, windowId, index + 1);
               }, 2500);
          });
     };

     // Function to execute searches with controlled concurrency
     const executeDorks = (domain) => {
          if (!domain) {
               alert("Please enter a target domain.");
               return;
          }

          // Loop through each category
          Object.entries(categories).forEach(([category, dorks]) => {
               const urls = dorks.map(dork => {
                    const query = `${domain} ${dork}`;
                    return `https://www.github.com/search?q=${encodeURIComponent(query)}&type=code`;
               });

               // Create a new Chrome window for the category
               chrome.windows.create({ url: [], type: "normal" }, (newWindow) => {
                    // Process URLs sequentially in the new window
                    processUrlsSequentially(urls, newWindow.id);
               });
          });
     };

     const targetDork = document.getElementById("domainInput").value.trim();
     executeDorks(targetDork);

});



document.getElementById("startBrowsing").addEventListener("click", () => {
     const targetDomains = document.getElementById("domainsInput")
          .value
          .trim()
          .split('\n')
          .map(domain => {
               domain = domain.trim();
               return domain.startsWith('http') ? domain : `https://${domain}`;
          })
          .filter(domain => domain);

     targetDomains.forEach(url => {
          chrome.tabs.create({ url });
     });

});

document.getElementById("getTabsDataButton").addEventListener("click", () => {
     chrome.runtime.sendMessage({ type: "getTabsData" }, (tabsData) => {
          if (!tabsData) {
               console.error("Error retrieving tabs data:", chrome.runtime.lastError);
               return;
          }

          const csvContent = "data:text/csv;charset=utf-8," +
               tabsData.map(tab => `"${tab.url}","${tab.content.replace(/"/g, '""')}"`).join("\n");
          const encodedUri = encodeURI(csvContent);
          const link = document.createElement("a");
          link.setAttribute("href", encodedUri);
          link.setAttribute("download", "tabs_data.csv");
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
     });
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

document.getElementById("testInputValidation").addEventListener("click", (event) => {
});

document.getElementById("testInputValidationStartRecording").addEventListener("click", (event) => {
     Popup("Recording Started");
     chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
          chrome.tabs.sendMessage(tabs[0].id, { type: "startRecording" });
     });
});

document.getElementById("testInputValidationEndRecording").addEventListener("click", (event) => {
     Popup("Recording Ended");
     chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
          chrome.tabs.sendMessage(tabs[0].id, { type: "endRecording" });
     });
});