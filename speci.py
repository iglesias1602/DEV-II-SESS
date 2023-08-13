class Produit:
    def __init__(self, nom, prix):
        """
        Initialisation d'un produit avec un nom et un prix.

        PRE: nom est un string , prix est un float .
        POST: self.nom est initialisé avec le nom spécifié. self.prix est initialisé avec le prix spécifié.

        """
        if not nom:
            raise ValueError("Le nom du produit ne peut pas être vide.")
        if prix <= 0:
            raise ValueError("Le prix du produit doit être positif.")

        self.nom = nom
        self.prix = prix

    def __str__(self):
        """
        Renvoie une représentation en chaîne du produit.

        :return: La représentation en chaîne du produit.
        :rtype: str
        """
        return f"{self.nom} - {self.prix} €"


class Inventory:
    def __init__(self):
        self.stock = {
            "Sandwich au poulet": 10,
            "Chips Paprika": 20,
            "Barre Chocolatée": 15,
            "Bonbons": 25,
            "Ice Tea": 30,
            "Limonade": 30,
        }

    def get_stock_quantity(self, produit):
        """
        Obtient la quantité en stock d'un produit.
        PRE: produit est un string qui représente le nom du produit.
        POST: retourne la quantité en stock du produit.
        """
        return self.stock.get(produit, 0)

    def enlever_stock(self, produit, quantite):
        if produit in self.stock:
            self.stock[produit] -= quantite
            if self.stock[produit] <= 0:
                del self.stock[produit]

    def est_disponible(self, produit, quantite):
        """
              Vérifie si une certaine quantité d'un produit est disponible en stock.

        PRE: produit est un str qui represente le nom de produit et quantite est un entier qui représente la quantité a vérifier .
        POST: retourne True si la quantité est disponible, sinon False .

        """
        return self.get_stock_quantity(produit) >= quantite

    def ajouter_stock(self, produit, quantite):

        """
        Ajoute la quantité spécifiée au stock pour un produit donné.

        PRE: produit est un str qui represente le nom de produit et quantite est un entier qui représente la quantité a ajouter .
        POST: self.stock[produit] est la quantité total du stock.

        """

        if quantite < 0:
            raise ValueError("La quantité doit être positive.")

        self.stock.setdefault(produit, 0)
        self.stock[produit] += quantite

    def retirer_stock(self, produit, quantite):
        """
        Retire la quantité spécifiée du stock pour un produit donné.

        PRE: produit est un str qui represente le nom de produit et quantite est un entier qui représente la quantité a retirer .
        POST: self.stock[produit] est la quantité total du stock pour un produit donné.
        """
        if produit in self.stock:
            if quantite < 0:
                raise ValueError("La quantité doit être positive.")
            if quantite > self.stock[produit]:
                raise ValueError("La quantité demandée est supérieure au stock disponible.")

            self.stock[produit] -= quantite
            if self.stock[produit] <= 0:
                del self.stock[produit]
        else:
            raise KeyError("Le produit spécifié n'est pas dans le stock.")
        quantite_restante = self.stock.get(produit, 0)
        print(f"Quantité restante de {produit} : {quantite_restante}")


class Distributeur:
    def __init__(self):
        self.produits = [
            Produit("Sandwich au poulet", 4.90),
            Produit("Chips Paprika", 2.50),
            Produit("Barre Chocolatée", 2.00),
            Produit("Bonbons", 3.30),
            Produit("Ice Tea", 2.20),
            Produit("Limonade", 1.90),
        ]
        self.inventory = Inventory()

    def afficher_menu(self):
        """
        Affichage du menu du distributeur avec les produits disponibles.

        PRE:
        POST: Le menu est affiché.
        """
        print("Bienvenue ! Voici notre sélection de produits :")
        for i, produit in enumerate(self.produits, start=1):
            quantite = self.inventory.get_stock_quantity(produit.nom)
            print(f"{i}: {produit} - Quantité en stock : {quantite}")
        print("7: Ajouter un produit au stock")
        print("8: Retirer un produit du stock")
        print("---------------------------------------------------------------")

    def get_produit_by_index(self, index):
        """
        Récupère un produit à partir de l'index donné.

        PRE:index est un entier qui représente l'index du produit dans la liste.
        POST: Retourne le produit correspondant à l'index.
        """
        if 0 <= index < self.get_produit_count():
            return self.produits[index]
        else:
            raise IndexError("Index invalide pour récupérer le produit.")

    def get_produit_count(self):
        """
        Obtient le nombre total de produits disponibles.

        PRE:
        POST: Retourne le nombre total de produits.
        """
        return len(self.produits)


class Client:
    def __init__(self):
        self.argent = 0.0

    def inserer_argent(self, montant):
        """
        Insère de l'argent dans le portefeuille du client.

        PRE: montant est un float qui représente le montant à insérer.
        POST: retourne le montant inséré.
        """
        if montant < 0:
            raise ValueError("Le montant inséré doit être positif.")
        self.argent += montant

    def recuperer_argent(self):
        """
        Récupère l'argent du portefeuille du client et le remet à zéro.

        PRE:
        POST: retourne le montant d'argent récupéré.
        """
        argent_a_rendre = self.argent
        self.argent = 0.0
        return argent_a_rendre


class Transaction:
    def __init__(self, produit, argent, inventory):
        self.produit = produit
        self.argent = argent
        self.inventory = inventory

    def effectuer(self):
        """
        Effectue la transaction en fonction de l'argent inséré et du produit sélectionné.

        PRE:
        POST: Si la transaction est réussie et aucun argent n'est rendu,
               le stock du produit est réduit de 1.
             Si la transaction est réussie et de l'argent est rendu,
               le stock du produit est réduit de 1, et l'argent rendu est disponible pour le client.
        """
        if not self.inventory.est_disponible(self.produit.nom, 1):
            print("Le produit sélectionné n'est plus disponible.")
            print("Veuillez récupérer votre monnaie :", self.argent, "€")
            return

        if self.argent < self.produit.prix:
            print(self.produit.nom)
            print("Transaction annulée")
            print("Montant insuffisant")
            print("Veuillez récupérer votre monnaie")
        elif self.argent == self.produit.prix:
            print(self.produit.nom)
            print("Transaction acceptée")
            self.inventory.enlever_stock(self.produit.nom, 1)
            print("Bon appétit !")
        else:
            print(self.produit.nom)
            print("Transaction acceptée")
            monnaie = self.argent - self.produit.prix
            self.inventory.enlever_stock(self.produit.nom, 1)
            print("Veuillez récupérer le reste", monnaie, "€")
            print("Bon appétit !")


def main():
    distributeur = Distributeur()

    while True:
        distributeur.afficher_menu()

        choix = input("Veuillez faire un choix : ")

        if choix == "7":
            produit = input("Nom du produit à ajouter : ")
            quantite = int(input("Quantité à ajouter : "))
            distributeur.inventory.ajouter_stock(produit, quantite)
            print(f"{quantite} {produit} ont été ajoutés au stock.")
        elif choix == "8":
            produit = input("Nom du produit à retirer : ")
            quantite = int(input("Quantité à retirer : "))
            distributeur.inventory.retirer_stock(produit, quantite)
            print(f"{quantite} {produit} ont été retirés du stock.")
        else:
            if not choix.isdigit():
                print("Vous devez entrer un nombre.")
                continue

            index_choix = int(choix) - 1
            if 0 <= index_choix < distributeur.get_produit_count():
                produit_selectionne = distributeur.get_produit_by_index(index_choix)

                argent_insere = float(input("Veuillez insérer votre monnaie : "))
                client = Client()
                client.inserer_argent(argent_insere)

                transaction = Transaction(produit_selectionne, client.argent, distributeur.inventory)
                print("---------------------------------------------------------------")
                transaction.effectuer()
                argent_rendu = client.recuperer_argent()
                if argent_rendu > 0:
                    print("Veuillez récupérer votre monnaie :", argent_rendu, "€")
                print("---------------------------------------------------------------")
            else:
                print("Vous avez entré un choix qui ne figure pas dans le menu")
                continue


if __name__ == "__main__":
    main()
