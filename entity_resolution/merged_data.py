import fasttext
import pandas as pd

from dtsc330_26.readers import articles, grants


class MergedData:
    def __init__(
        self,
        grant_path: str = "data/RePORTER_PRJ_C_FY2025.zip",
        article_path: str = "data/pubmed25n1275.xml.gz",
        ft_path: str = "data/cc.en.50.bin",
    ):
        self.ft_model = fasttext.load_model(ft_path)
        art = articles.Articles(article_path)
        self.auth_df = art.get_authors().iloc[0:100]

        grant = grants.Grants(grant_path)
        self.grant_df = grant.get_grantees().iloc[0:100]

    def get_merged_data(self) -> pd.DataFrame:
        # TEMPORARILY
        # Before we cluster possible matches together
        # I'm going to limit to only 100 entries from each dataframe

        self.auth_df["ft_forename_vec"] = self.auth_df["forename"].apply(
            self.ft_model.get_sentence_vector
        )
        self.auth_df["ft_surname_vec"] = self.auth_df["surname"].apply(
            self.ft_model.get_sentence_vector
        )
        self.grants_df["ft_forename_vec"] = self.grants_df["forename"].apply(
            self.ft_model.get_sentence_vector
        )
        self.grants_df["ft_surname_vec"] = self.grants_df["surname"].apply(
            self.ft_model.get_sentence_vector
        )

        for i in range(0, len(self.auth_df), 100):
            for j in range(0, len(self.grant_df), 100):
                comb_df = self.auth_df.iloc[i : i + 100].merge(
                    self.grant_df.iloc[i : i + 100], how="cross"
                )
                # What the heck is yield?
                # Return halfway through
                # Take a pause, return part, then keep going
                yield comb_df


if __name__ == "__main__":
    x = get_merged_data()