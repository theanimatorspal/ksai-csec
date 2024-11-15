from testing.require import *

def Run(inDomainsTxtFile, outWaybackTxtFile):
    command = f"cat {inDomainsTxtFile} | waybackurls > {outWaybackTxtFile}"
    RunCommand(command, "Wayback URLs saved successfully.", "Failed waybackurls command.")

def RunUrlRegex(inDomainsTxtFile, outWaybackTxtFile):
    command = f"cat {inDomainsTxtFile} | waybackurls | grep -Eo '(http|https)://[a-zA-Z0-9./?=_%:-]*' | sort -u > {outWaybackTxtFile}"
    RunCommand(command, "Filtered URLs saved successfully.", "Failed URL regex extraction.")

def RunExcludeUrls(inDomainsTxtFile, excludeFile, outWaybackTxtFile):
    command = f"cat {inDomainsTxtFile} | waybackurls -exclude {excludeFile} > {outWaybackTxtFile}"
    RunCommand(command, "Excluded URLs saved successfully.", "Failed to exclude URLs.")

def RunStatusCode200(inDomainsTxtFile, outWaybackTxtFile):
    command = f"cat {inDomainsTxtFile} | waybackurls | grep -E 'status_code:200' | sort -u > {outWaybackTxtFile}"
    RunCommand(command, "200 status code URLs saved successfully.", "Failed status code filtering.")

def RunPathFrequency(inDomainsTxtFile, outWaybackTxtFile):
    command = f"cat {inDomainsTxtFile} | waybackurls | unfurl paths | sort | uniq -c | sort -rn > {outWaybackTxtFile}"
    RunCommand(command, "Path frequency saved successfully.", "Failed to extract path frequency.")

def RunHeaderCheck(inDomainsTxtFile, outWaybackTxtFile):
    command = f"cat {inDomainsTxtFile} | waybackurls | xargs -I{{}} curl -s -L -I -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0' {{}} | grep -iE 'x-frame-options|content-security-policy' > {outWaybackTxtFile}"
    RunCommand(command, "Header checks saved successfully.", "Failed to check headers.")

def ExtractParameters(inLinksFile, outParametersFile, inShouldOutputOnlyMatched=False):
    if inShouldOutputOnlyMatched:
        command = rf"grep -oP '(?<=\?|&)\w+(?==|&)' {inLinksFile} | sort -u | tee {outParametersFile}"
    else:
        command = rf"grep -P '(?<=\?|&)\w+(?==|&)' {inLinksFile} | sort -u | tee {outParametersFile}"

    RunCommand(command, "Parameters extracted successfully.", "Failed extracting parameters.")

def ExtractJSLinks(inLinksFile, outJSLinksFile, inShouldOutputOnlyMatched=False):
    if inShouldOutputOnlyMatched:
        command = rf"grep -oP '(https?://[^\s\"'\''<>]*\.js(\?\S*)?)' {inLinksFile} | sort -u | tee {outJSLinksFile}"
    else:
        command = rf"grep -P '(https?://[^\s\"'\''<>]*\.js(\?\S*)?)' {inLinksFile} | sort -u | tee {outJSLinksFile}"
    
    RunCommand(command, "JavaScript links extracted successfully.", "Failed extracting JavaScript links.")

def ExtractPHPLinks(inLinksFile, outPHPLinksFile, inShouldOutputOnlyMatched=False):
    if inShouldOutputOnlyMatched:
        command = rf"grep -oP '(https?://[^\s\"'\''<>]*\.php(\?\S*)?)' {inLinksFile} | sort -u | tee {outPHPLinksFile}"
    else:
        command = rf"grep -P '(https?://[^\s\"'\''<>]*\.php(\?\S*)?)' {inLinksFile} | sort -u | tee {outPHPLinksFile}"
    
    RunCommand(command, "PHP links extracted successfully.", "Failed extracting PHP links.")

def ExtractSuspiciousEndpoints(inLinksFile, outSuspiciousFile, inShouldOutputOnlyMatched=False):
    if inShouldOutputOnlyMatched:
        command = rf"grep -oP '(https?://[^\s\"'\''<>]*/(admin|login|signup|dashboard)[^\s\"'\''<>]*)' {inLinksFile} | sort -u | tee {outSuspiciousFile}"
    else:
        command = rf"grep -P '(https?://[^\s\"'\''<>]*/(admin|login|signup|dashboard)[^\s\"'\''<>]*)' {inLinksFile} | sort -u | tee {outSuspiciousFile}"
    
    RunCommand(command, "Suspicious endpoints extracted successfully.", "Failed extracting suspicious endpoints.")

def ExtractFileLeaks(inLinksFile, outFileLeaksFile, inShouldOutputOnlyMatched=False):
    if inShouldOutputOnlyMatched:
        command = rf"grep -oP '(https?://[^\s\"'\''<>]*\.(env|git|bak|zip|tar|sql)[^\s\"'\''<>]*)' {inLinksFile} | sort -u | tee {outFileLeaksFile}"
    else:
        command = rf"grep -P '(https?://[^\s\"'\''<>]*\.(env|git|bak|zip|tar|sql)[^\s\"'\''<>]*)' {inLinksFile} | sort -u | tee {outFileLeaksFile}"
    
    RunCommand(command, "Potential file leaks extracted successfully.", "Failed extracting file leaks.")

def ExtractSensitiveKeywordsLinks(inLinksFile, outSensitiveKeywordsFile, inShouldOutputOnlyMatched=False):
    if inShouldOutputOnlyMatched:
        command = rf"grep -oP '(https?://[^\s\"'\''<>]*\b(password|secret|token|key|auth|config)\b[^\s\"'\''<>]*)' {inLinksFile} | sort -u | tee {outSensitiveKeywordsFile}"
    else:
        command = rf"grep -P '(https?://[^\s\"'\''<>]*\b(password|secret|token|key|auth|config)\b[^\s\"'\''<>]*)' {inLinksFile} | sort -u | tee {outSensitiveKeywordsFile}"
    
    RunCommand(command, "Links with sensitive keywords extracted successfully.", "Failed extracting sensitive keywords links.")

def ExtractAPIEndpoints(inLinksFile, outAPIEndpointsFile, inShouldOutputOnlyMatched=False):
    if inShouldOutputOnlyMatched:
        command = rf"grep -oP '(https?://[^\s\"'\''<>]*/(api|v1|v2|graphql)[^\s\"'\''<>]*)' {inLinksFile} | sort -u | tee {outAPIEndpointsFile}"
    else:
        command = rf"grep -P '(https?://[^\s\"'\''<>]*/(api|v1|v2|graphql)[^\s\"'\''<>]*)' {inLinksFile} | sort -u | tee {outAPIEndpointsFile}"
    
    RunCommand(command, "API endpoints extracted successfully.", "Failed extracting API endpoints.")

def ExtractDebugInfoURLs(inLinksFile, outDebugInfoFile, inShouldOutputOnlyMatched=False):
    if inShouldOutputOnlyMatched:
        command = rf"grep -oP '(https?://[^\s\"'\''<>]*\b(debug|error|test|trace|log)\b[^\s\"'\''<>]*)' {inLinksFile} | sort -u | tee {outDebugInfoFile}"
    else:
        command = rf"grep -P '(https?://[^\s\"'\''<>]*\b(debug|error|test|trace|log)\b[^\s\"'\''<>]*)' {inLinksFile} | sort -u | tee {outDebugInfoFile}"
    
    RunCommand(command, "Debug information URLs extracted successfully.", "Failed extracting debug information URLs.")

def ExtractOldVersionFiles(inLinksFile, outOldVersionsFile, inShouldOutputOnlyMatched=False):
    if inShouldOutputOnlyMatched:
        command = rf"grep -oP '(https?://[^\s\"'\''<>]*\.(old|backup|bak|orig|~)[^\s\"'\''<>]*)' {inLinksFile} | sort -u | tee {outOldVersionsFile}"
    else:
        command = rf"grep -P '(https?://[^\s\"'\''<>]*\.(old|backup|bak|orig|~)[^\s\"'\''<>]*)' {inLinksFile} | sort -u | tee {outOldVersionsFile}"
    
    RunCommand(command, "Old version files extracted successfully.", "Failed extracting old version files.")

def ExtractWordPressLinks(inLinksFile, outWordPressFile, inShouldOutputOnlyMatched=False):
    if inShouldOutputOnlyMatched:
        command = rf"grep -oP '(https?://[^\s\"'\''<>]*wp-(content|admin|includes)[^\s\"'\''<>]*)' {inLinksFile} | sort -u | tee {outWordPressFile}"
    else:
        command = rf"grep -P '(https?://[^\s\"'\''<>]*wp-(content|admin|includes)[^\s\"'\''<>]*)' {inLinksFile} | sort -u | tee {outWordPressFile}"
    
    RunCommand(command, "WordPress links extracted successfully.", "Failed extracting WordPress links.")

def MakeReadyForDalfox(inLinksFile, outFile):
    command = rf"cat {inLinksFile} | grep -E '(\?|&)([^=]+)=' | sed 's/=.*/=/' | sed 's/URL: //' | tee {outFile}"
    RunCommand(command, "Made Urls Dalfox Ready", "Failed to make URls dalfox ready")

def DalfoxTestXSS(inDalfoxReadyFile, outFile):
    command = f"dalfox file {inDalfoxReadyFile} pipe | tee {outFile} "
    RunCommand(command, "Dalfox Test XSS Complete", "Dalfox XSS Failed")