from scrapping import metadata_extractor
from scrapping import sourcemap_identifier
from testing import http_methods
from testing import cross_site_tracing
from testing import http_method_override
from testing import ria_cross_domain_policy

url = "https://www.nba.com/"

metadata_extractor.Run(url, 2, "nba/comments.txt")
# sourcemap_identifier.Run("http://127.0.0.1:3000/#/")
# http_methods.Run("http://127.0.0.1:3000/test.html", "<html>HTTP PUT Method is Enabled</html>")
# cross_site_tracing.Run("http://127.0.0.1:3000")
# http_method_override.Run("http://127.0.0.1:3000")
# ria_cross_domain_policy.Run("127.0.0.1:3000", "jshop/")