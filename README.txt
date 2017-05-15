

1. COMMENT DEMARRER

    Le projet contient un mini shel capable d’exécuter des commandes sur le sytème. Les commandes du shell sont disponible via la commande ‘help’ et sont listé si dessous.

	COMMANDES :
		1. help
			Liste toutes les commandes disponible
		2. compile
			Permet le compilation d’un fichier. Nécéssaire pour run.
		3. run
			Permet l’exécution du programme compilé.
		4. debug
			Affiche les informations d’exécutions (Flags, Current Input, Memory, Regiters)
			ATTENTION : Le fait d’afficher le current input le vide.
		5. keyboard
			Démarre/Arrête l’écoute du clavier. (Confirmer avant de run)
		6. input
			Simuler une entrée clavier. Ajouter le text dans l’input courante.
		7. exit
			Quit le shell

	EXEMPLE :
		Exemple d’exécution du programme input-on-screen.txt (les programmes sont détaillé plus bas)

		$ python main.py
		Enter 'help' for more informations.
		-Cmd : compile
		  file name : prog/input-on-screen.txt
		-Cmd : run
		  Keyboard listening stopped. Start ? (Y)Y

		=== PROGRAMME EXECUTION ===
		-Cmd : exit
		$

2. PROGRAMMES DISPONIBLES

	Le projet contient de programmes tests. Ils sont disponibles dans le dossier prog. Vous pouvez les charger à la compilation en entrant : prog/programName.txt

	1. boucle.txt
		Ce programme met en place une simple de boucle. Tant que B <= A, on increment B. Au debut on fait A = 10 et B = 0, on a donc 11 tour de boucle. Avec un ‘debug’ après l’exécution du programme, on voit le que le registre B(2) = 11, le programme à donc bien réalisé la boucle.

	2. functions.txt
		Ce programme utilise une fonctionnalité implémenter permettant de créer des fonctions plus facilement. En effet, il set la valeur de différents registre dans les functions, on peut alors savoir si cette dernière à été appelé ou non. De plus, on remarque que la dernière instruction n’est pas exécuté puisque l’on qui le programme avec l’instruction HLT avant.
		Les functions utilisent une sauvegarde automatique du pc courant lors d’un JMP. Ceci permet alors à l’instruction HFT de remonter automatique la stack d’appel.
		Cette fonctionnalité supporte également les appels en série. En effet, la function 2 est appelé dans la function 1 elle même appelé dans le main.

	3. input-on-screen.txt
		Ce programme utilise l’écoute du clavier et l’affichage de l’écran. Le programme écoute le clavier, des qu’une touche est enfoncé, il l’affiche sur l’écran. A chaque affiche, il décale le pixel. Si la touche ‘q’ est enfoncé, le programme quit.
		ASTUCE : Afin de ne pas avoir a appuyer sur le clavier à chaque test, il est possible de simuler une entrée avec la commande ‘input’.

	4. letter-select.txt
		Ce programme utilise l’écoute du clavier et l’affichage de l’écran.
		Il permet d’écrire un mot en sélectionnant des lettres. Si vous pressez la touche ’n’ (next) vous aurez la lettre suivante, si vous pressez la touche ‘p’ (previous) vous aurez la touche précédente. Pour sélectionner la lettre, pressez la touche ’s’.
		Une fois la touche sélectionnez, le programme passe automatiquement à la lettre suivant et donc ce décale sur l’écran.
		Pour quitter le programme, sélectionnez la lettre ‘q’.
		ATTENTION : le programme a un comportement indéfini si une touche autre que ’n’, ‘p’, ’s’ est pressez.


3. INFORMATION D’EXECUTION

	RETURN CODE
		FINISH : -1
			Le programme s’est terminé avec succès.
		ER_FINISH_OP : -2
			Une erreur est survenue lors de l’obtention de l’instruction suivante. Généralement lorsque la dernière instruction n’est pas HLT.
		ER_EMPTY_REGITER : -3
			Le programme essaye d’accéder à la valeur d’un registre qui n’a pas encore été initialisé.

4. INFORMATION SUR LE LANGUAGE ASSEMBLEUR

	Le language suit une structure strict : OP REGISTER VALUE
	Il est possible de mettre des commentaires : OP. REGISTER VALUE # COMMENT
	Il est possible de laisser des ligne vide ou des ligne qui commence par des commentaire : # COMMENT
	Pour les opération qui ne nécessite pas de registre (ex: JMP), le registre peut être nul avec Z

	• OP :
	    - doit être dans la liste [NOP, JMP, JMZ, JMO, JMC, SET, LD, ST, MV, ADD, SUB, MUL, DIV, OR, AND, XOR, NOT, HLT, HFT, LT, GT, LE, GE, EQ, EZ, NZ] 
	• REGISTER :
	    - peut être un char de A à I
	    - peut être le pc courant (Y)
	    - peut être l'address parente de la dernière fonction (X)
	    - peut être null (Z)
	• VALUE
    	    - peut être de l'hexadecimal (0x[0-9]+)
	    - peut être du binaire (0b[0-9]+)
	    - peut être decimal ([0-9]+)
	    - peut être la valeur stocké dans un registre ([A-I])
	    - peut être le pc courant (Y)
	    - peut être un code ascii (ASCII([A-I]))
	    - peut être null (Z)
