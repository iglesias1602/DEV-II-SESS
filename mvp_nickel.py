
    class Produit:
    def __init__(self, nom, prix):
        self.nom = nom
        self.prix = prix

    def __str__(self):
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
        return self.stock.get(produit, 0)

    def enlever_stock(self, produit, quantite):
        if produit in self.stock:
            self.stock[produit] -= quantite
            if self.stock[produit] <= 0:
                del self.stock[produit]

    def est_disponible(self, produit, quantite):
        return self.get_stock_quantity(produit) >= quantite

    def ajouter_stock(self, produit, quantite):
        if produit in self.stock:
            self.stock[produit] += quantite
        else:
            self.stock[produit] = quantite

    def retirer_stock(self, produit, quantite):
        if produit in self.stock:
            self.stock[produit] -= quantite
            if self.stock[produit] <= 0:
                del self.stock[produit]
        else:
            print("Le produit spécifié n'est pas dans le stock.")
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
        print("Bienvenue ! Voici notre sélection de produits :")
        for i, produit in enumerate(self.produits, start=1):
            quantite = self.inventory.get_stock_quantity(produit.nom)
            print(f"{i}: {produit} - Quantité en stock : {quantite}")
        print("7: Ajouter un produit au stock")
        print("8: Retirer un produit du stock")
        print("---------------------------------------------------------------")

    def get_produit_by_index(self, index):
        return self.produits[index]

    def get_produit_count(self):
        return len(self.produits)


class Client:
    def __init__(self):
        self.argent = 0.0

    def inserer_argent(self, montant):
        self.argent += montant

    def recuperer_argent(self):
        argent_a_rendre = self.argent
        self.argent = 0.0
        return argent_a_rendre


class Transaction:
    def __init__(self, produit, argent, inventory):
        self.produit = produit
        self.argent = argent
        self.inventory = inventory

    def effectuer(self):
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
            print("Bonne appétit !")
        else:
            print(self.produit.nom)
            print("Transaction acceptée")
            monnaie = self.argent - self.produit.prix
            self.inventory.enlever_stock(self.produit.nom, 1)
            print("Veuillez récupérer le reste", monnaie, "€")
            print("Bonne appétit !")




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



