import gzip
import xml.etree.ElementTree as ET

import pandas as pd
import sqlalchemy


class ArticlesReader:
    def __init__(self, path: str):
        """Read in a pubmed articles XML file that is gzipped

        Args:
            path (str)
        """
        self.article_df = None
        self.author_df = None
        self._parse(path)

    def _parse(self, path: str):
        """Parse the Pubmed file"""
        articles = []
        authors = []

        with gzip.open(path, "rb") as fp:
            for _, article in ET.iterparse(fp, events=("end",)):
                if article.tag == "PubmedArticle":
                    article_row, article_authors = self._parse_article(article)
                    articles.append(article_row)
                    authors.extend(article_authors)
                    # append: [[auth1, auth2], [auth3, auth4, auth5]]
                    # extend: [auth1, auth2, ..., auth5]
                    article.clear()

        self.article_df = pd.DataFrame(articles)
        self.author_df = pd.DataFrame(authors)

    def _parse_article(self, article: ET.Element):
        """Parse an XML PubmedArticle element"""
        row = {}
        tags = [
            "PMID",
            "ArticleTitle",
            "PubDate",
            "DateCompleted",
            "Affiliation",
            "Year",
            "Month",
            "Day",
        ]
        # XML Tag format for reference:
        # <PubDate>
        #   <Year>2001</Year>
        #   <Month>2</Month>
        #   <Day>28</Day>
        #   <Hour>10</Hour>
        #   <Minute>0</Minute>
        # </PubDate>
        for el in article.iter():
            if el.tag in tags:
                if el.tag.find("Date") > -1:
                    for el2 in el.iter():
                        if el2.tag in tags:
                            row[el2.tag] = el2.text
                row[el.tag] = el.text

        if "PMID" not in row.keys():
            return {}, {}

        authors = []
        tags = ["LastName", "ForeName", "Initials", "Affiliation"]
        for author in article.findall(".//Author"):
            auth_row = {"PMID": row["PMID"]}
            for el in author.iter():
                if el.tag in tags:
                    auth_row[el.tag] = el.text.lower().strip()
            authors.append(auth_row)

        return row, authors

    def get_authors(self):
        """Get parsed article authors"""
        return self.author_df.rename(
            columns={
                "LastName": "surname",
                "ForeName": "forename",
                "Initials": "initials",
                "Affiliation": "affiliation",
                "PMID": "pmid"
            }
        )

    def get_entries(self):
        """Get parsed articles"""
        return self.article_df.rename(
            columns={'PMID':'pmid', 'ArticleTitle':'title'}
        )

    def to_db(self, path:str = 'data/article_grant_db.sqlite'):
        """Send the read-in data to sqlite database

        Args: path (str)
        """
        # Define the connection
        engine = sqlalchemy.create_engine("sqlite:///data/article_grant_db.sqlite")
        connection = engine.connect

        self.article_df.dropna().to_sql('articles', connection, if_exists='append', index=False)
        self.get_authors().dropna(subset=['pmid', 'surname']).to_sql(
            'authors', connection, if_exists='append', index=False
        )

    def batch_from_db(self):
        """Load teh data from the sqlite database"""
        engine = sqlalchemy.create_engine("sqlite:///data/article_grant_db.sqlite")
        connection = engine.connect()
        return pd.read_sql(
            f"SELECT id, forename, surname, affiliation FROM authors",
            connection,
            chunksize=100
        )

if __name__ == "__main__":
    articles_reader = ArticlesReader("data/pubmed25n1275.xml.gz")
    articles_reader.to_db()
    