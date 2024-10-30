from bs4 import BeautifulSoup
from uk_bin_collection.uk_bin_collection.common import *
from uk_bin_collection.uk_bin_collection.get_bin_data import AbstractGetBinDataClass

import re
from datetime import datetime

# Regex to match orindal days (1st, 2nd, 3rd, 4th, .. 31st)
ordinal = re.compile(r'(\d+)(st|nd|rd|th)')


class CouncilClass(AbstractGetBinDataClass):
    def parse_data(self, page: str, **kwargs) -> dict:
        # Make a BS4 object
        soup = BeautifulSoup(page.text, features="html.parser")
        soup.prettify()
        print(soup)

        data = {"bins": []}

        # Iterate over next collection date tags
        for bin_tag in soup.find(id="results").find_all("h3"):
            # Get bin type from image alt text
            bin_type = bin_tag.img["alt"]
            # Get collection date
            next_collection_date = bin_tag.get_text(strip=True)
            # Strip ordinal suffixes from date
            next_collection_date = ordinal.sub(
                r"\1",
                next_collection_date
            )

            data["bins"].append(
                {
                    "type": bin_type,
                    "collectionDate": datetime.strptime(
                        next_collection_date,
                        "%A, %d %B %Y"
                    )
                }
            )

        return data
