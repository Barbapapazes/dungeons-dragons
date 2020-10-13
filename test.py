 
class Article:
	"""Représente un article du stock avec pour paramètre :
        - son code article
        - sa référence 
        - sa désignation
        - sa marque
        - sa famille
        - sa quantité
        - son stock minimum
        - sa quantité à commander
        """
 
	def __init__(self, code_article, reference, designation, marque, famille, quantite, mini, a_cmd):
		"""constructeur de la classe article avec pour attribut : code_article = code article, reference = référence, désignation = designation, 
                famille = famille, quantité en stock = quantité, stock minimum = mini, sa quantité à commander = a_cmd"""
		self.code_article = code_article
		self.reference = reference
		self.designation = designation
		self.marque = marque
		self.famille = famille
		self.quantite = quantite
		self.mini = mini
		self.a_cmd = a_cmd
		self.art = [self.code_article, self.reference, self.designation, self.marque, self.famille, self.quantite, self.mini, self.a_cmd]
 
	def __str__(self):
		"""fonction pour passer l'article en chaine de caractère"""
		str_article = list(self.art)
		"""copie de la liste sans référence de l'une à l'autre"""
		c = 0
		for x in str_article: 
			"""permet de passer les éléments de la liste en chaine"""
			str_article[c] = str(x)
			c+=1
		txt = " - ".join(str_article)
		return txt
 
	def ajouter_bdd(self):
		""" permet d'ajouter l'article à la base de donnée """
		conn = sqlite3.connect(fichierBDD)
		cur = conn.cursor()
		data = [(self.code_article, self.reference, self.designation, self.marque, self.famille, self.quantite, self.mini, self.a_cmd)]
		for tu in data:
			cur.execute("INSERT INTO article(code_article, reference, designation, marque, famille, quantite, mini, a_cmd) VALUES(?,?,?,?,?,?,?,?)", tu)
		conn.commit()
		cur.close()
		conn.close()