import fasttext as ft
import hnswlib
import numpy as np

from entity_resolution.readers import grants_reader


class GranteeNNIndex:
    def __init__(
        self,
        ft_path: str = "data/cc.en.50.bin",
        default_grant_path: str = "data/RePORTER_PRJ_C_FY2025.zip",
    ):
        """
        Args: ft_path (str)
              default_grant_path (str)
              
        """
        self.idx = hnswlib.Index(space="l2", dim=50)
        self.grantee_ids = []
        self.grantee_df = None
        self.ft_model = ft.load_model(ft_path)
        self._generate(default_grant_path)

    def _generate(self, default_grant_path: str):
        """Load in every grantee to put in the index
        
        Args: default_grant_path (str)

        """
        greader = grants.Grants(default_grant_path)
        grantees = greader.get_all_grantees_from_db()
        self.grantee_df = grantees
        self.idx.init_index(max_elements=len(grantees), ef_construction=200, M=16)
        self.grantee_ids = grantees["id"].to_numpy()
        grantees["vec"] = grantees.apply(
            lambda row: self.ft_model.get_sentence_vector(
                (row["forename"] + " " + row["surname"]).lower()
            ),
            axis=1,
        )
        vecs = grantees["vec"].apply(lambda x: np.array(x).flatten())
        self.idx.add_items(np.vstack(vecs))

    def query(self, forename: str, surname: str, affiliation: str):
        """Returns potential matches
        
        Args: forename (str): first name of entity
              surname (str): last name of entity
              affilliation (str): affiliation of entity

        """
        vec = self.ft_model.get_sentence_vector(
            forename.lower() + " " + surname.lower()
        )
        positions, dists = self.idx.knn_query(vec, k=100)
        return self.grantee_df.iloc[positions[0]], dists


if __name__ == "__main__":
    nnidx = GranteeNNIdx()
    print(
        nnidx.query("jack", "smith", "duquesne university pittsburgh pa 15206")[0][
            ["forename", "surname", "affiliation"]
        ]
    )