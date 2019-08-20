
struct no{
	char dado;
	bool fimPalavra;
	struct no *menor;
	struct no *igual;
	struct no *maior;
};
typedef struct no noTrie;
	
noTrie* insere(noTrie *raiz, char *caractere){
	if(raiz == NULL){
			raiz = (noTrie *)malloc(sizeof(noTrie));
			raiz->dado = *caractere;
			raiz->fimPalavra = false;
			raiz->menor = raiz->igual = raiz->maior = NULL;
	}
	
	if(*caractere < raiz->dado){
		raiz->menor = insere(raiz->menor,caractere);	
	}
	else if(*caractere == raiz->dado){
		if(*(caractere+1))
			raiz->igual = insere(raiz->igual, caractere+1);
		else
			raiz->fimPalavra = true;
	}
	else
		raiz->maior = insere(raiz->maior,caractere);
	return raiz;
}

int pesquisa(noTrie *raiz,char *palavra){
	while(raiz!=NULL){
		if(raiz->dado > *palavra)
			raiz = raiz->menor;
			
		else if(raiz->dado == *palavra){
			if((raiz->fimPalavra) && (*(palavra+1) == '\0'))
				return 1;
			palavra++;
			raiz = raiz->igual;
		}
		else
			raiz = raiz->maior;
	}
	return 0;
}


main()
{
	char palavra[100];
	noTrie *ARVORE = NULL;
	int encerra = 1;
	
	while(encerra){
		printf("Digite 0 para encerrar ou 1 para pesquisar e inserir na arvore!\n");
		scanf("%d", &encerra);
		switch(encerra){
			case 0: return 0; 
				break;
				
			case 1:		
				printf("Digite a palavra para buscar ou inserir na Trie: ");
				fflush(stdin);
				gets(palavra);
	
				if(pesquisa(ARVORE,palavra)){
					printf("%s esta na arvore!\n",palavra);
					break;
				}
				else{
					ARVORE = insere(ARVORE,palavra);
					printf("%s nao esta na arvore! Palavra foi inserida com sucesso!\n",palavra);	
					break;
				}
	}

}
}
