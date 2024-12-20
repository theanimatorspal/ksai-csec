let MAX_DEPTH = 1;
var Logs = ""
Logs = Logs + "========= LOGS BEGIN =========\n";

function copyToClipboard(text) {
     navigator.clipboard.writeText(text).then(() => {
          console.log("Text copied to clipboard");
     }).catch(err => {
          console.error("Failed to copy text: ", err);
     });
}

function resumeAllFailedDownloads() {
     chrome.downloads.search({ state: 'interrupted' }, (downloads) => {
          downloads.forEach((download) => {
               chrome.downloads.resume(download.id).then(() => {
                    if (chrome.runtime.lastError) {
                         console.log(`Failed to resume download ${download.id}: ${chrome.runtime.lastError.message}`);
                         // Optional: retry by re-downloading if resuming fails
                         chrome.downloads.download({ url: download.url });
                    } else {
                         console.log(`Resumed download ${download.id}`);
                    }
               });
          });
     });
}

function saveToFile(filename, content) {
     // Convert content to UTF-8 and then to Base64
     const utf8Content = new TextEncoder().encode(content);
     const base64Content = btoa(String.fromCharCode(...utf8Content));
     const dataUrl = `data:text/plain;base64,${base64Content}`;

     chrome.downloads.download({
          url: dataUrl,
          filename: filename,
          saveAs: true
     }, () => {
          console.log("File saved successfully.");
     });
}


function extractMetadataAndLinks(depth) {
     function extractMetadata() {
          const metadata = [];
          const warnings = [];

          // Capture DOCTYPE
          if (document.doctype) {
               metadata.push(`\tDOCTYPE: ${document.doctype.name}`);
          } else {
               warnings.push("\tWarning: Missing DOCTYPE");
          }

          // Extract meta tags with additional checks for security-relevant headers
          document.querySelectorAll("meta").forEach(meta => {
               const name = meta.getAttribute("name") || meta.getAttribute("property");
               const content = meta.getAttribute("content");
               if (name && content) {
                    metadata.push(`\tMeta - Name/Property: ${name}, Content: ${content}`);
                    if (name.toLowerCase() === "description" && content.toLowerCase().includes("password")) {
                         warnings.push("\tPotentially sensitive information in meta description.");
                    }
               }
          });

          // Extract link tags with security-relevant attributes
          document.querySelectorAll("link[rel]").forEach(link => {
               const rel = link.getAttribute("rel");
               const href = link.getAttribute("href");
               const integrity = link.getAttribute("integrity");
               const crossorigin = link.getAttribute("crossorigin");
               if (rel && href) {
                    let linkInfo = `\tLink - Rel: ${rel}, Href: ${href}`;
                    if (integrity) linkInfo += `, Integrity: ${integrity}`;
                    if (crossorigin) linkInfo += `, Crossorigin: ${crossorigin}`;
                    metadata.push(linkInfo);
               }
          });

          // Extract comments and flag any suspicious content
          const walker = document.createTreeWalker(document, NodeFilter.SHOW_COMMENT, null, false);
          while (walker.nextNode()) {
               const comment = walker.currentNode.nodeValue.trim();
               if (comment) {
                    metadata.push(`\tComment: ${comment}`);
                    if (/TODO|FIXME|HACK/i.test(comment)) {
                         warnings.push(`\tSuspicious comment found: "${comment}"`);
                    }
               }
          }

          // Extract scripts with enhanced inspection
          document.querySelectorAll("script").forEach(script => {
               const src = script.getAttribute("src");
               const integrity = script.getAttribute("integrity");
               const crossorigin = script.getAttribute("crossorigin");

               if (src) {
                    let scriptInfo = `\tExternal Script - Src: ${src}`;
                    if (integrity) scriptInfo += `, Integrity: ${integrity}`;
                    if (crossorigin) scriptInfo += `, Crossorigin: ${crossorigin}`;
                    metadata.push(scriptInfo);

                    // Potential issue with untrusted src
                    if (!integrity) warnings.push(`\tExternal script without integrity attribute: ${src}`);
               } else {
                    const inlineContent = script.innerHTML.trim();
                    metadata.push(`\tInline Script: ${inlineContent}`);

                    // Flag risky JavaScript patterns
                    if (/eval|innerHTML|document\.write|setTimeout|setInterval/i.test(inlineContent)) {
                         warnings.push("\tRisky inline JavaScript detected (e.g., eval, document.write, etc.).");
                    }
               }
          });

          // Log the metadata and warnings
          console.log("===== Metadata Extracted =====\n" + metadata.join("\n"));
          if (warnings.length > 0) {
               console.log("\n===== Potential Issues Detected =====\n" + warnings.join("\n"));
          }

          // Return combined log
          return metadata.concat(warnings).join("\n");
     }

     var vLogs = ""
     vLogs = vLogs + `(Depth ${depth}): ${window.location.href}\n`;
     vLogs = vLogs + extractMetadata(vLogs);
     const links = [...new Set([...document.querySelectorAll('a[href]')].map(link => link.href))];
     links.forEach(link => {
          chrome.runtime.sendMessage({ type: "extractMetadata", url: link, depth: depth + 1 });
     });
     return vLogs
}

async function waitForTabsAndExecute(url, depth) {
     const allTabs = await chrome.tabs.query({});
     const tabCount = allTabs.length;

     if (tabCount < 4) {
          const tab = await chrome.tabs.create({ url: url, active: false });
          Logs += "Tab: " + tab.id.toString() + "\n";

          chrome.tabs.onUpdated.addListener(async function listener(tabId, info) {
               if (tabId === tab.id && info.status === 'complete') {
                    const tabInfo = await chrome.tabs.get(tab.id);

                    // Check if the URL is allowed for scripting
                    if (!tabInfo.url.startsWith("chrome://") && !tabInfo.url.startsWith("about:")) {
                         const [{ result }] = await chrome.scripting.executeScript({
                              target: { tabId: tab.id },
                              func: extractMetadataAndLinks,
                              args: [depth]
                         });
                         Logs += result + "\n";
                    } else {
                         Logs += `Skipped restricted URL: ${tabInfo.url}\n`;
                    }

                    // Close the tab and remove the listener
                    chrome.tabs.remove(tab.id);
                    chrome.tabs.onUpdated.removeListener(listener);
               }
          });
     }
}


chrome.runtime.onMessage.addListener(
     async function (arg, sender, sendResponse) {
          if (arg.type == "downloadFile") {
               chrome.downloads.download({
                    url: arg.downloadLink,
                    filename: arg.filename,
                    conflictAction: 'uniquify'
               }, (downloadId) => {
                    if (chrome.runtime.lastError) {
                         console.error("Download failed:", chrome.runtime.lastError.message);
                         sendResponse({ success: false, error: chrome.runtime.lastError.message });
                    } else if (downloadId === undefined) {
                         console.error("Download ID is undefined.");
                         sendResponse({ success: false, error: "Download ID is undefined." });
                    } else {
                         console.log("Download started with ID:", downloadId);
                         sendResponse({ success: true, downloadId: downloadId });
                    }
               });
          }
          else if (arg.type == "changeDepthValueForExtraction") {
               MAX_DEPTH = arg.depth;
          } else if (arg.type == "extractMetadata") {
               const { url, depth } = arg;
               if (depth <= MAX_DEPTH) {
                    await waitForTabsAndExecute(url, depth)
               }
          }
          else if (arg.type == "extractMetadataByMessage") {
               Logs = Logs + "Tab: " + toString(arg.tab.id) + "\n";
               const [{ result }] = await chrome.scripting.executeScript({
                    target: { tabId: arg.tab.id },
                    func: extractMetadataAndLinks,
                    args: [arg.depth]
               });
               Logs = Logs + result + "\n";
          } else if (arg.type == "resumeAllDownloads") {
               resumeAllFailedDownloads();
          }
          else if (arg.type == "copyLogsToClipboard") {
               chrome.scripting.executeScript({
                    target: { tabId: arg.tab.id },
                    func: async (logs) => {
                         await navigator.clipboard.writeText(logs);
                    },
                    args: [Logs]
               });
          }
          else if (arg.type == "saveLogsToFile") {
               Logs = Logs + "========= LOGS END ========= \n";
               saveToFile("file.txt", Logs)
          }
          else if (arg.type == "resetEverything") {
               Logs = " ========= LOGS BEGIN ========= \n";
          }
          else if (arg.type == "setProxy") {
               const [address, port] = arg.address.split(":");
               const config = {
                    mode: "fixed_servers",
                    rules: {
                         singleProxy: {
                              scheme: arg.scheme,
                              host: address,
                              port: parseInt(port, 10)
                         },
                         bypassList: ["<local>"]
                    }
               };
               chrome.proxy.settings.set(
                    { value: config, scope: "regular" },
                    () => {
                         console.log("Proxy settings applied");
                    }
               )
          } else if (arg.type == "resetProxy") {
               chrome.proxy.settings.clear({ scope: "regular" }, () => {
                    console.log("Proxy settings cleared");
               });
          }
     }
);

chrome.runtime.onMessage.addListener(
     function (arg, sender, sendResponse) {
          if (arg.type == "getTabsData") {
               chrome.tabs.query({}, async (tabs) => {
                    try {
                         const tabData = [];
                         for (const tab of tabs) {
                              const tabContent = await chrome.scripting.executeScript({
                                   target: { tabId: tab.id },
                                   func: () => document.body.innerText
                              });
                              tabData.push({ url: tab.url, content: tabContent[0].result });
                         }
                         sendResponse(tabData);
                         if (chrome.runtime.lastError) {
                              console.error("Runtime error after sending response: ", chrome.runtime.lastError);
                         }
                    } catch (error) {
                         console.error("ERROR gathering the table data ", error);
                    }
               });
               return true;
          }
     }
)

chrome.runtime.onInstalled.addListener(() => {
     chrome.contextMenus.create({
          id: "open-multiple-links",
          title: "Open Multiple Links in New Tabs",
          contexts: ["selection"]
     });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
     if (info.menuItemId === "open-multiple-links") {
          chrome.scripting.executeScript({
               target: { tabId: tab.id },
               function: extractAndOpenLinks
          });
     }
});

// This function runs in the context of the webpage
function extractAndOpenLinks() {
     const selection = window.getSelection();
     if (!selection.rangeCount) return;

     const range = selection.getRangeAt(0);
     const container = range.commonAncestorContainer;
     const parentElement = container.nodeType === 3 ? container.parentElement : container;

     // Find all <a> elements within the selection
     const links = Array.from(parentElement.querySelectorAll('a'));
     const hrefs = links.map(link => link.href).filter(href => href); // Filter out empty hrefs

     if (hrefs.length > 0) {
          hrefs.forEach(href => window.open(href, '_blank'));
     } else {
          alert("No links found in the selected text or its parent container.");
     }
}



////
////
////
////
////
////
////
////
////
////
////
////
////
////
////
////
////
////
chrome.runtime.onInstalled.addListener(() => {
     chrome.contextMenus.create({
          id: "scanJSFiles",
          title: "Scan JavaScript Files",
          contexts: ["page"]
     });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
     if (info.menuItemId === "scanJSFiles" && tab.id) {
          chrome.scripting.executeScript({
               target: { tabId: tab.id },
               files: ["scan.js"]
          });
     }
});
