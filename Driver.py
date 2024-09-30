from scrapping import metadata_extractor
from scrapping import sourcemap_identifier

#metadata_extractor.ExtractAllMetaDataFrom("http://127.0.0.1:3000/#/", 2, "comments.txt")

sourcemap_identifier.identify_sourcemaps("http://127.0.0.1:3000/#/")