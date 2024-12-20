(async function () {
     const scripts = [...document.scripts]
          .map(script => script.src)
          .filter(src => src);
     function beautifyCode(code) {
          const indentSize = 4;
          let indentLevel = 0;
          let inString = false;
          let currentStringChar = '';
          let result = '';
          let i = 0;

          while (i < code.length) {
               const char = code[i];
               const nextChar = i + 1 < code.length ? code[i + 1] : '';

               // Handle string boundaries
               if ((char === '"' || char === "'" || char === '`') && !inString) {
                    inString = true;
                    currentStringChar = char;
               } else if (char === currentStringChar && inString) {
                    inString = false;
               }

               // Add line breaks for block delimiters outside of strings
               if (!inString) {
                    if (char === '{' || char === '[') {
                         result += char + '\n' + ' '.repeat(++indentLevel * indentSize);
                    } else if (char === '}' || char === ']') {
                         result = result.trimEnd() + '\n' + ' '.repeat(--indentLevel * indentSize) + char;
                    } else if (char === ';') {
                         result += char + '\n' + ' '.repeat(indentLevel * indentSize);
                    } else if (char === '\n') {
                         // Normalize line breaks
                         result = result.trimEnd() + '\n' + ' '.repeat(indentLevel * indentSize);
                    } else if (char === ',') {
                         result += char + (nextChar.trim() === '' ? ' ' : '\n' + ' '.repeat(indentLevel * indentSize));
                    } else {
                         result += char;
                    }
               } else {
                    // Preserve everything inside strings
                    result += char;
               }

               i++;
          }

          // Ensure a single trailing newline
          return result.trimEnd() + '\n';
     }

     //add an ajax check
     const regexChecks = [
          {
               name: "ksaiJSAPIEndpoint",
               pattern: /https?:\/\/[\w.-]+\/api\/[\w./?=&-]*|(?<=(["'`]))\/[a-zA-Z0-9_?&=\/\-#\.]*(?=(["'`]))/gi,
               description: "Potential API endpoint or relative path detected within JavaScript files."
          },

     ];

     const Extensive = [
          { name: "ksaiMergeFunction", pattern: /\b_\.(merge|mergeWith|defaultsDeep)\s*\(/g, description: "Potential use of Lodash merge functions that may lead to prototype pollution." },
          { name: "ksaiProtoManipulation", pattern: /\b(__proto__|constructor\.prototype)\b/g, description: "Direct manipulation of __proto__ or constructor.prototype detected, which can lead to prototype pollution." },
          { name: "ksaiDeepClone", pattern: /\b_\.(cloneDeep|cloneDeepWith)\s*\(/g, description: "Potential use of Lodash cloneDeep functions, which might copy prototype-polluted objects." },
          { name: "ksaiAnyLink", pattern: /https?:\/\/[\w.-]+(?:\/[\w./?=&-]*)?/gi, description: "Potential link detected." },
          { name: "ksaiPotentialKey", pattern: /[\w-]{32,}/g, description: "Potential API key or token detected." },
          { name: "ksaiSensitiveData", pattern: /(password|secret|access[_\-]key|private[_\-]key|authorization|bearer\s[\w-]+)/gi, description: "Sensitive data detected in the JavaScript file." },
          { name: "ksaiJWTWeakness", pattern: /\beyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.?[a-zA-Z0-9_-]*\b/gi, description: "JWT token detected; check for weak algorithms or improper implementation." },
          { name: "ksaiInsecureHTTP", pattern: /http:\/\/[\w.-]+/gi, description: "Insecure HTTP endpoint detected." },
          { name: "ksaiEmailAddresses", pattern: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b/gi, description: "Email address found in JavaScript file." },
          { name: "ksaiAWSKey", pattern: /AKIA[0-9A-Z]{16}/g, description: "Potential AWS key detected." },
          { name: "ksaiDangerousFunction", pattern: /\b(eval|document\.write|setTimeout|setInterval|innerHTML)\b/gi, description: "Dangerous JavaScript function detected." },
          { name: "ksaiHardcodedCredentials", pattern: /\b(username|password)[\s=:]+["']?\w+["']?/gi, description: "Hardcoded credentials detected." },
          { name: "ksaiErrorPatterns", pattern: /(exception|stack trace|traceback|error|referenceerror|uncaughtexception)/gi, description: "Error patterns found in the JavaScript file." },
          { name: "ksaiPrivateIP", pattern: /\b(10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b/g, description: "Private IP address found; check for potential internal exposure." },
          { name: "ksaiHardcodedToken", pattern: /\b[A-Za-z0-9_-]{30,}\b/g, description: "Potential hardcoded token detected; check for sensitive data exposure." },
          { name: "ksaiWeakCrypto", pattern: /\b(md5|sha1|rot13)\b/g, description: "Usage of weak cryptographic algorithms found; consider stronger alternatives like SHA-256 or AES." },
          { name: "ksaiPrivateBucket", pattern: /https?:\/\/s3\.(.*)\.amazonaws\.com\/[^\s]+/g, description: "S3 bucket URL found; ensure it is properly secured." },
          { name: "ksaiQueryInjection", pattern: /\bSELECT .* FROM\b|\bUPDATE .* SET\b|\bDELETE FROM\b/g, description: "SQL keywords detected; verify the backend's, input sanitization and prepared statements." },
          { name: "ksaiOpenRedirect", pattern: /\b(location\.href|window\.location) *= *["']?https?:\/\/[^\s'"]+/g, description: "Potential open redirect vulnerability found; ensure validation of redirect URLs." },
          { name: "ksaiCrossDomainAccess", pattern: /\bwindow\.postMessage\(/g, description: "Cross-origin communication detected; ensure messages are sent to trusted domains only." },
          { name: "ksaiSensitiveEnv", pattern: /\b(process\.env|env\.)/g, description: "Environment variable access detected; verify it does not expose sensitive data." },
          { name: "ksaiCommandInjection", pattern: /\b(require|child_process)\.exec\(.+\)/g, description: "Command execution function detected; check for potential command injection risks." },
          { name: "ksaiExcessiveError", pattern: /\bconsole\.(error|log|warn)\(.+\)/g, description: "Excessive debugging information found; verify no sensitive information is logged." },
          { name: "ksaiSuperGlobalUsage", pattern: /\b(window|global|document)\.\w+/g, description: "Direct manipulation of global objects found; ensure no critical objects are being overridden." },
          { name: "ksaiUnsafeRegex", pattern: /(.*)\((.*)\)\1\2/g, description: "Potential unsafe regular expression found; check for ReDoS (Regular Expression Denial of Service)." }
     ];

     const results = await Promise.all(
          scripts.map(async (url) => {
               try {
                    const response = await fetch(url);
                    const text = await response.text();

                    const findings = regexChecks
                         .map(({ name, pattern }) => {
                              const matches = [...text.matchAll(pattern)];
                              return matches.length > 0
                                   ? matches.map((match) => ({
                                        name,
                                        match: match[0],
                                        context: extractContext(text, match.index),
                                   }))
                                   : [];
                         })
                         .flat();

                    return { url, findings };
               } catch (error) {
                    console.error(`Failed to fetch ${url}:`, error);
                    return { url, error: error.message };
               }
          })
     );

     const formattedResults = results
          .map(({ url, findings, error }) => {
               if (error) {
                    return `<div class="error">File: ${url}<br>Error: ${error}</div>`;
               }

               return findings
                    .map(
                         (f) =>
                              `<div class="match">
               <h3> ${f.name} </h3>
               <div><strong>[${url}]</strong>: "${f.match}"</div>
             </div>`
                    )
                    .join("");
          })
          .join("");

     // <pre class="context">${(f.context)}</pre>
     const outputHTML = `
    <html>
      <head>
        <title>JavaScript Scanner Results</title>
        <style>
          body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
          }
          h3 {
            color: #2a7ae2;
            margin-bottom: 10px;
          }
          .match {
            border: 1px solid #ddd;
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 4px;
            background: #f9f9f9;
          }
          .error {
            color: red;
            margin-bottom: 20px;
          }
          .context {
            background: #f4f4f4;
            padding: 10px;
            border-radius: 4px;
            font-family: monospace;
            white-space: pre-wrap;
            word-break: break-word;
          }
        </style>
      </head>
      <body>
        <h1>JavaScript Scanner Results</h1>
        ${formattedResults || "<p>No matches found.</p>"}
      </body>
    </html>
  `;

     const newTab = window.open();
     newTab.document.write(outputHTML);
     newTab.document.close();

     function extractContext(text, index) {
          const lines = text.split("\n");
          const lineNum = text.substring(0, index).split("\n").length - 1;
          const startLine = Math.max(0, lineNum - 10);
          const endLine = Math.min(lines.length - 1, lineNum + 10);

          return lines.slice(startLine, endLine + 1).join("\n");
     }
})();
