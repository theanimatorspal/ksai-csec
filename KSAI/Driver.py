import globals
import os
from testing import http_methods
from testing import cross_site_tracing
from testing import http_method_override
from testing import ria_cross_domain_policy
from testing import forced_browsing
from testing import subdomain_enumeration
from testing import android_manifest
from testing import port_scan
from testing import wayback_urls
from testing import subdomain_takeover
from testing import crt_sh

def GeneralRecon(crt_keyword, inFolder, inDomain):
     crt_sh.Run(crt_keyword, inFolder + "crtsh.txt")
     # os.makedirs(inFolder, exist_ok=True)
     # port_scan.Run(ip=inDomain, output_file=inFolder + "open_ports.txt")
     # subdomain_enumeration.RunSubfinder(inDomain, inFolder + "subdomains.txt")
     # subdomain_enumeration.RunFindAlive(inFolder + "subdomains.txt", inFolder + "alive_subdomains.txt")
     # wayback_urls.Run(inFolder + "alive_subdomains.txt", inFolder + "wayback.txt")
     # ShouldOutputOnlyMatched = False
     # wayback_urls.ExtractParameters(inFolder + "wayback.txt", inFolder + "wayback_parameters.txt", ShouldOutputOnlyMatched)
     # wayback_urls.ExtractJSLinks(inFolder + "wayback.txt", inFolder + "wayback_js_links.txt", ShouldOutputOnlyMatched)
     # wayback_urls.ExtractPHPLinks(inFolder + "wayback.txt", inFolder + "wayback_php_links.txt", ShouldOutputOnlyMatched)
     # wayback_urls.ExtractSuspiciousEndpoints(inFolder + "wayback.txt", inFolder + "wayback_suspicious_endpoints.txt", ShouldOutputOnlyMatched)
     # wayback_urls.ExtractFileLeaks(inFolder + "wayback.txt", inFolder + "wayback_file_leaks.txt", ShouldOutputOnlyMatched)
     # wayback_urls.ExtractSensitiveKeywordsLinks(inFolder + "wayback.txt", inFolder + "wayback_sensitive_keywords.txt", ShouldOutputOnlyMatched)
     # wayback_urls.ExtractAPIEndpoints(inFolder + "wayback.txt", inFolder + "wayback_api_endpoints.txt", ShouldOutputOnlyMatched)
     # wayback_urls.ExtractDebugInfoURLs(inFolder + "wayback.txt", inFolder + "wayback_debug_info.txt", ShouldOutputOnlyMatched)
     # wayback_urls.ExtractOldVersionFiles(inFolder + "wayback.txt", inFolder + "wayback_old_versions.txt", ShouldOutputOnlyMatched)
     # wayback_urls.ExtractWordPressLinks(inFolder + "wayback.txt", inFolder + "wayback_wordpress_links.txt", ShouldOutputOnlyMatched)
     # subdomain_takeover.Run(inFolder + "subdomains.txt", "takeovers.txt")
     # os.makedirs(inFolder + "forced_browsing/", exist_ok=True)
     # forced_browsing.RunFeroxbusterFromFile(inDomain, inFolder + "forced_browsing/", "lists/content_discovery.txt")

#GeneralRecon("targets/forumsepic/", "forums.unrealengine.com")
#GeneralRecon("targets/artstation/", "artstation.com")
# GeneralRecon("targets/quixel/", "quixel.com")
# GeneralRecon("targets/fab/", "fab.com")
# GeneralRecon("targets/epic/", "epicgames.dev")
# GeneralRecon("targets/unreal/", "unrealengine.com")
#GeneralRecon("targets/devepic/", "dev.epicgames.com")
# GeneralRecon("targets/square", "square.com")
# GeneralRecon("targets/squareup", "squareup.com")
# GeneralRecon("targets/weebly", "weebly.com")
#GeneralRecon("targets/rapyd/", "rapyd.net")
#GeneralRecon("targets/porche/", "www.porsche.com")
#GeneralRecon("targets/northwestmutual/", "northwesternmutual.com")
# GeneralRecon("targets/nml/", "nml.com")
# GeneralRecon("targets/nmfn/", "nmfn.com")
GeneralRecon("Paytm Payments", "targets/sophos/", "sophos.com")