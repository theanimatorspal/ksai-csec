import globals
from testing import http_methods
from testing import cross_site_tracing
from testing import http_method_override
from testing import ria_cross_domain_policy
from testing import forced_browsing
from testing import subdomain_enumeration
from testing import android_manifest

folder = "targets/ring/"
domain = "https://ring.com"

# subdomain_enumeration.RunAmass(
#                     domain,
#                     globals.all_subdomains_list,
#                     folder + "subdomains.txt"
#           )

forced_browsing.Run(domain,
                    folder + "forced_browsing.txt",
                    globals.all_content_discovery)

# android_manifest.Run(folder + "AndroidManifestimm.xml", folder + "imm_manifest.txt")