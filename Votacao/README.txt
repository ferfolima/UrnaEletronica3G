- Votacao
	- gerenciar.py		//talvez mudar o nome para gerenciar.py
		gerar chaves	//botao utilizado para gerar chave de seguranca para a votacao
		ler codigo	//botam que chama leitor de qr para ler voto e contabilizar
		gerar boletim	//botao parar gerar arquivo pdf com boletim de urna
	- incrementar.py	//classe chamada pera classe apuracao para incrementar votos
	- main.py		//classe utilizada para iniciar a votacao
		votar		//botao que chama classe votar.py
	- votar.py		//classe chamada pela classe main para iniciar a votacao
	- verificar.py		//classe utilizada para verificar o voto
		verificar	//botao chama leitor de qr code para verificar o voto
	- file.py		//classe temporaria para ler arquivo/pasta
