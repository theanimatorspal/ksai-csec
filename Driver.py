import globals
from testing import http_methods
from testing import cross_site_tracing
from testing import http_method_override
from testing import ria_cross_domain_policy
from testing import forced_browsing
from testing import subdomain_enumeration
from testing import android_manifest
from testing import port_scan


def GeneralRecon(inFolder, inDomain):
     # port_scan.Run(ip=inDomain, output_file=inFolder + "open_ports.txt")
     # subdomain_enumeration.RunSubfinder(inDomain, inFolder + "subdomains.txt")
     # subdomain_enumeration.RunFindAlive(inFolder + "subdomains.txt", inFolder + "alive_subdomains.txt")
     forced_browsing.RunGobuster(inDomain, inFolder + "forced.txt")

GeneralRecon("targets/quixel/", "quixel.com")