import pandas as pd
import sqlalchemy


class GrantsReader:
    def __init__(self, path: str | None = None, load_db: bool = False):
        """Create and parse a Grants file

        Args:
            path (str): 
                if empty, defaults to pulling from the database

            load_db (bool): if True, load the entire dataset from the database
        """
        if path is None and load_db:
            self.df, self.grantee_df = self._from_db()

        self.path = path
        self.df, self.grantee_df = self._parse(path)

    def _parse(self, path: str):
        """Parse a grants file"""
        df = pd.read_csv(path, compression="zip")

        mapper = {
            "APPLICATION_ID": "application_id",  # _id means an id
            "BUDGET_START": "start_at",  #  _at means a date
            "ACTIVITY": "grant_type",
            "TOTAL_COST": "total_cost",
            "PI_NAMEs": "pi_names",
            "ORG_NAME": "organization",
            "ORG_CITY": "city",
            "ORG_STATE": "state",
            "ORG_COUNTRY": "country",
        }

        df = df.rename(columns=mapper)[mapper.values()]

        df["affiliation"] = df.apply(
            lambda row: ", ".join(
                [
                    v
                    for v in [
                        row["organization"],
                        row["city"],
                        row["state"],
                        row["country"],
                    ]
                    if not pd.isna(v)
                ]
            ),
            axis=1
        ).str.lower()

        grantees = df[["application_id", "pi_names", "affiliation"]].dropna(how="any")
        grantees["pi_name"] = grantees["pi_names"].str.split(";")
        grantees = grantees.explode("pi_name").reset_index(drop=True)

        grantees["pi_name"] = (
            grantees["pi_name"].str.lower().str.replace("(contact)", "").str.strip()
        )
        names = grantees["pi_name"].apply(lambda x: x.split(","))
        grantees["surname"] = names.apply(lambda x: x[0]).str.strip()
        grantees["forename"] = (
            names.apply(lambda x: x[1]).str.replace(".", "").str.strip()
        )
        grantees["initials"] = grantees["forename"].apply(
            lambda x: "".join([v[0] for v in x.split(" ") if len(v) > 0])
        )

        return (
            df.drop(columns=["pi_names"]),
            grantees[["surname", "forename", "initials", "affiliation", "application_id"]]
        )

    def to_db(self, path:str = 'data/article_grant_db.sqlite'):
        """Send the read-in data to the sqlite database

        Args: 
            path(str): location of sqlite file
        """
        # Define the connection
        engine = sqlalchemy.create_engine("sqlite:///data/article_grant_db.sqlite")
        connection = engine.connect()

        self.df[['applicaiton_id', 'start_at', 'grant_type', 'total_cost']].to_sql(
            'grants', connection, if_exists='append', index=False
        )
        self.get_grantees().to_sql(
            'grantees', connection, if_exists='append', index=False
        )


    def get_grants(self):
        """Get parsed grants"""
        return self.df

    def get_grantees(self):
        """Get parsed grantees"""
        return self.grantee_df.rename(
            {
                "LastName": "surname",
                "ForeName": "forename",
                "Initials": "initials",
                "Affiliation": "affiliation",
            }
        )

    def get_all_grantees_from_db(self):
        engine = sqlalchemy.create_engine("sqlite:///data/article_grant_db.sqlite")
        connection = engine.connect()
        return pd.read_sql(
            'SELECT id, forename, surname, initials, affiliation FROM grantees',
            connection
        )

    def _from_db(self):
        """Load the data from the database"""
        engine = sqlalchemy.create_engine("sqlite:///data/article_grant_db.sqlite")
        connection = engine.connect()
        df = pd.read_sql("SELECT * FROM grants", connection)
        grantee_df = pd.read_sql('SELECT * FROM grantees')
        return df, grantee_df


if __name__ == "__main__":
    # This is for debugging
    grants_reader = GrantsReader("data/RePORTER_PRJ_C_FY2025.zip")
    grants_reader.to_db()