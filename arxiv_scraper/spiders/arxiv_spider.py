import scrapy
from datetime import datetime, date
from urllib.parse import urlencode

ATOM_NS = {"a": "http://www.w3.org/2005/Atom"}


class ArxivSpider(scrapy.Spider):
    name = "arxiv"

    def __init__(
        self,
        query,
        start_date,
        end_date,
        max_items=0,
        page_size=100,
        max_empty_pages=5,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        # -------- user params --------
        self.query = query
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        self.page_size = int(page_size)

        self.max_items = int(max_items) if str(max_items).strip() else 0

        # -------- internal state --------
        self.start_index = 0
        self.emitted = 0

        self.empty_pages = 0
        self.max_empty_pages = int(max_empty_pages)

        self._logged_sample = False

        # -------- strategy decision --------
        # If crawling old data (end_date well before today),
        # go OLD -> NEW to avoid scanning tons of new papers.
        self.archival = self.end_date < date.today().replace(month=1, day=1)

        self.logger.warning(
            f"SMART SPIDER ACTIVE | archival={self.archival} | "
            f"window={self.start_date}..{self.end_date}"
        )

    # -----------------------------------------------------

    def start_requests(self):
        yield self._make_request()

    def _make_request(self):
        params = {
            "search_query": self.query,
            "start": self.start_index,
            "max_results": self.page_size,
            "sortBy": "submittedDate",
            "sortOrder": "ascending" if self.archival else "descending",
        }
        url = "https://export.arxiv.org/api/query?" + urlencode(params)
        self.logger.info(
            f"Requesting start={self.start_index} "
            f"(emitted={self.emitted}, empty_pages={self.empty_pages})"
        )
        return scrapy.Request(url, callback=self.parse, dont_filter=True)

    # -----------------------------------------------------

    def parse(self, response):
        entries = response.xpath("//a:entry", namespaces=ATOM_NS)
        self.logger.info(f"Received {len(entries)} entries")

        if not entries:
            self.logger.info("No entries. Stopping.")
            self.crawler.engine.close_spider(self, "no_entries")
            return

        yielded_this_page = 0

        for entry in entries:
            # -------- stop if enough papers --------
            if self.max_items > 0 and self.emitted >= self.max_items:
                self.logger.info(f"Stopping: reached max_items={self.max_items}")
                self.crawler.engine.close_spider(self, "max_items_reached")
                return

            published = entry.xpath("a:published/text()", namespaces=ATOM_NS).get()
            if not published:
                continue

            pub_date = datetime.strptime(published[:10], "%Y-%m-%d").date()

            if not self._logged_sample:
                self._logged_sample = True
                self.logger.info(
                    f"Sample published={published} (pub_date={pub_date})"
                )

            # -------- date window logic --------
            if self.archival:
                # OLD -> NEW
                if pub_date < self.start_date:
                    continue
                if pub_date > self.end_date:
                    self.logger.info(
                        f"Stopping: passed end_date ({self.end_date}) in archival mode"
                    )
                    self.crawler.engine.close_spider(self, "end_date_reached")
                    return
            else:
                # NEW -> OLD
                if pub_date > self.end_date:
                    continue
                if pub_date < self.start_date:
                    self.logger.info(
                        f"Stopping: passed start_date ({self.start_date}) in recent mode"
                    )
                    self.crawler.engine.close_spider(self, "start_date_reached")
                    return

            # -------- emit paper --------
            self.emitted += 1
            yielded_this_page += 1

            yield {
                "id": entry.xpath("a:id/text()", namespaces=ATOM_NS).get(),
                "title": (
                    entry.xpath("a:title/text()", namespaces=ATOM_NS).get() or ""
                )
                .strip()
                .replace("\n", " "),
                "authors": entry.xpath(
                    "a:author/a:name/text()", namespaces=ATOM_NS
                ).getall(),
                "published": published,
                "summary": (
                    entry.xpath("a:summary/text()", namespaces=ATOM_NS).get() or ""
                )
                .strip()
                .replace("\n", " "),
            }

        # -------- sparse detection --------
        if yielded_this_page == 0:
            self.empty_pages += 1
        else:
            self.empty_pages = 0

        self.logger.info(
            f"Yielded {yielded_this_page} items on start={self.start_index} "
            f"(emitted={self.emitted})"
        )

        if self.empty_pages >= self.max_empty_pages:
            self.logger.info(
                f"Stopping: {self.empty_pages} consecutive empty pages "
                f"(date window likely too sparse)"
            )
            self.crawler.engine.close_spider(self, "too_sparse")
            return

        # -------- pagination --------
        if len(entries) < self.page_size:
            self.logger.info(
                f"Stopping: last page (<page_size) at start={self.start_index}"
            )
            self.crawler.engine.close_spider(self, "last_page")
            return

        self.start_index += self.page_size
        yield self._make_request()
