const MAX_DEPTH = 2;
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
     const dataUrl = `data:text/plain;base64,${btoa(content)}`;
     chrome.downloads.download({
          url: dataUrl,
          filename: filename,
          saveAs: true
     }, () => {
          console.log("File saved successfully");
     });
}


function extractMetadataAndLinks(depth) {
     function extractMetadata() {
          const metadata = [];

          // Get DOCTYPE
          if (document.doctype) {
               metadata.push(`DOCTYPE: ${document.doctype.name}`);
          }

          // Extract meta tags
          document.querySelectorAll("meta").forEach(meta => {
               const name = meta.getAttribute("name");
               const content = meta.getAttribute("content");
               if (name && content) {
                    metadata.push(`Meta name: ${name}, content: ${content}`);
               }
          });

          // Extract link tags
          document.querySelectorAll("link[rel]").forEach(link => {
               const rel = link.getAttribute("rel");
               const href = link.getAttribute("href");
               if (rel && href) {
                    metadata.push(`Link rel: ${rel}, href: ${href}`);
               }
          });

          // Extract comments
          const walker = document.createTreeWalker(document, NodeFilter.SHOW_COMMENT, null, false);
          while (walker.nextNode()) {
               const comment = walker.currentNode.nodeValue.trim();
               if (comment) {
                    metadata.push(`Comment: ${comment}`);
               }
          }

          // Extract scripts (both inline and external)
          document.querySelectorAll("script").forEach(script => {
               const src = script.getAttribute("src");
               if (src) {
                    metadata.push(`External Script src: ${src}`);
               } else {
                    metadata.push(`Inline Script: ${script.innerHTML.slice(0, 100)}...`);
               }
          });

          var vLogs = ""
          // Return metadata as a single formatted string
          console.log(metadata.join("\n"));
          vLogs = vLogs + metadata.join("\n");
          vLogs = vLogs + "\n";
          return vLogs;
     }

     var vLogs = ""
     vLogs = vLogs + `METADATA OF LINK (Depth ${depth}): ${window.location.href}\n`;
     console.log("MetaData SHIT============");
     vLogs = vLogs + extractMetadata(vLogs);
     const links = [...new Set([...document.querySelectorAll('a[href]')].map(link => link.href))];
     links.forEach(link => {
          chrome.runtime.sendMessage({ type: "extractMetadata", url: link, depth: depth + 1 });
     });
     return vLogs
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
          } else if (arg.type == "extractMetadata") {
               const { url, depth } = arg;

               if (depth <= MAX_DEPTH) {
                    chrome.tabs.create({ url: url, active: false }, (tab) => {
                         Logs = Logs + "Tab: " + toString(tab.id) + "\n";
                         console.log("Adding Listener to tab", tab.id);
                         chrome.tabs.onUpdated.addListener(async function listener(tabId, info) {
                              if (tabId === tab.id && info.status === 'complete') {
                                   const [{ result }] = await chrome.scripting.executeScript({
                                        target: { tabId: tab.id },
                                        func: extractMetadataAndLinks,
                                        args: [depth]
                                   });
                                   Logs = Logs + result + "\n";
                                   chrome.tabs.remove(tab.id);
                                   chrome.tabs.onUpdated.removeListener(listener);
                              }
                         });
                    });
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
               alert(Logs)
          }
          else if (arg.type == "saveLogsToFile") {
               Logs = Logs + "========= LOGS END =========";
               saveToFile("file.txt", Logs)
          }
          else if (arg.type == "resetEverything") {
               Logs = " ========= LOGS BEGIN ========= \n";
          }
     }
);