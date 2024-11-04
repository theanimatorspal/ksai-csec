

function downloadFilesWithExtension(extension) {
     // Get all anchor elements on the page
     const links = document.querySelectorAll("a");

     // Filter links that end with the specified extension and are absolute URLs
     const filesToDownload = Array.from(links).filter(link => {
          const url = link.href;
          return url && url.endsWith(`.${extension}`);
     });

     console.log("Links:", links);
     console.log("FilesToDownload:", filesToDownload);

     filesToDownload.forEach(file => {
          const downloadLink = file.href;
          const filename = downloadLink.substring(downloadLink.lastIndexOf('/') + 1);

          console.log("To Download:", filename)
          var param = { type: "downloadFile", downloadLink: downloadLink, filename: filename };
          chrome.runtime.sendMessage(param);

     });

     console.log(`${filesToDownload.length} .${extension} files queued for download.`);
}