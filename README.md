# entity_resolution

### Purpose
This repository serves as a demonstration of a full entity resolution pipeline. It contains data science tools applied to a specific problem.

In seperate datasets, human entities' names can be listed differently. One dataset could say "Alexander D. Smith, Duquesne University" and the other "Alex Smith, Duquesne University" for example. These differences are small, but with hundreds of thousands of entities, machine learning can be a powerful tool in reconsiling them.

### Description and overview
Entity resolution is the process of relating and linking data between one or more datasets using machine learning to ultimately create a single profile for each individual entity. 

The specific entity resolution problem I solve here in this repository is linking PubMed article authors and grant recipients.

Attributes used to match author/grantee entities are forename, surname, and affiliation (university, company, etc.)