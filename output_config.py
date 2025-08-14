from pydantic import BaseModel, Field
from typing import Literal  

# Configuration de l'output "Mon profile"

class UserProfile(BaseModel):
    caractere: Literal["Nerveux", "Sentimental", "Colérique", "Passionné", "Sanguin", "Flegmatique", "Amorphique", "Apathique"] = Field(description="Type caractérologique de l'utilisateur")
    emotivite: Literal["Oui", "Non"] = Field(description="Si l'utilisateur est émotif ou non")
    activite: Literal["Oui", "Non"] = Field(description="Si l'utilisateur est actif ou non")
    retentissement: Literal["Primaire", "Secondaire"] = Field(description="Si l'utilisateur a un retentissement primaire ou secondaire")
    