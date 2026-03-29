import fasttext
import jarowinkler
import np.linalg.norm
import pandas as pd


def set_dist(x: str, y: str) -> float:
    """Return the fraction of words that overlap relative to the shorter
    string.

    Args:
        x (str): string 1
        y (str): string 2

    Returns:
        float: fraction of overlap
    """
    words1 = x.replace(" ", ",").split(",")
    words2 = y.replace(" ", ",").split(",")
    words1 = set([word for word in words1 if len(word) > 0])
    words2 = set([word for word in words2 if len(word) > 0])

    denom = min(len(words1), len(words2))
    numer = len(words1.intersection(words2))
    return numer / denom


class EntityResolutionFeatures:
    def features(self, comb_df: pd.DataFrame) -> pd.DataFrame:
        """ Get features from data

        Args: comb_df: combined dataframe (authors and grantees)
        """
        # For each character slot, is it the same character?
        comb_df["jw_fn_dist"] = comb_df.apply(
            lambda row: jarowinkler.jaro_similarity(
                row["forename_x"], row["forename_y"]
            ),
            axis=1,
        )
        comb_df["jw_sn_dist"] = comb_df.apply(
            lambda row: jarowinkler.jaro_similarity(row["surname_x"], row["surname_y"]),
            axis=1,
        )

        comb_df["set_aff_dist"] = comb_df.apply(
            lambda row: set_dist(row["affiliation_x"], row["affiliation_y"]), axis=1
        )

        comb_df["ft_fn_dist"] = comb_df.apply(
            lambda row: np.linalg.norm(
                row["ft_forename_vec_x"] - row["ft_forename_vec_y"]
            ),
            axis=1,
        )
        comb_df["ft_sn_dist"] = comb_df.apply(
            lambda row: np.linalg.norm(
                row["ft_surname_vec_x"] - row["ft_surname_vec_y"]
            ),
            axis=1,
        )

        return comb_df[
            [
                "jw_fn_dist",
                "jw_sn_dist",
                "set_aff_dist",
                "ft_fn_dist",
                "ft_surname_dist",
            ]
        ]