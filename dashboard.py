import os
import tkinter as tk
from tkinter import filedialog, messagebox
import random
import string
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore, storage

# ==========================================
# CONFIGURAÇÕES INICIAIS E SEGURANÇA
# ==========================================
USUARIOS = {
    "1": "123",
    "manutencao": "manut123"
}
LINK_PORTAL = "https://adtec-vistorias.web.app"

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ADTEC CloudVistoria - Dashboard")
        self.root.geometry("550x500")
        self.root.configure(bg="#0a192f")
        
        self.pasta_selecionada = ""
        self.logado = False
        self.db = None
        self.bucket = None
        
        # Inicializa a conexão com a Nuvem
        self.inicializar_firebase()
        self.tela_login()

    def inicializar_firebase(self):
        """Conecta o script Python ao Firebase usando o arquivo JSON de credenciais"""
        try:
            # Verifica se o arquivo de credenciais existe na pasta
            if os.path.exists("credenciais.json"):
                cred = credentials.Certificate("credenciais.json")
                # Substitua 'seu-projeto.appspot.com' pelo link do seu bucket no Firebase Storage
                firebase_admin.initialize_app(cred, {
                    'storageBucket': 'seu-projeto.appspot.com' 
                })
                self.db = firestore.client()
                self.bucket = storage.bucket()
                print("[NUVEM]: Conectado ao Firebase com sucesso.")
            else:
                print("[AVISO]: Arquivo 'credenciais.json' não encontrado. O app rodará em modo de simulação local.")
        except Exception as e:
            print(f"[ERRO NUVEM]: Falha ao conectar na nuvem: {e}")

    def tela_login(self):
        self.limpar_tela()
        lbl_titulo = tk.Label(self.root, text="Acesso Restrito - ADTEC", font=("Arial", 16, "bold"), bg="#0a192f", fg="#ffffff")
        lbl_titulo.pack(pady=30)
        
        frame_card = tk.Frame(self.root, bg="#ffffff", padx=20, pady=20)
        frame_card.pack(pady=10, padx=50, fill="both")
        
        tk.Label(frame_card, text="Usuário:", font=("Arial", 11, "bold"), bg="#ffffff", fg="#0052cc").pack(anchor="w")
        self.ent_usuario = tk.Entry(frame_card, font=("Arial", 12), bd=2, relief="groove")
        self.ent_usuario.pack(fill="x", pady=5)
        
        tk.Label(frame_card, text="Senha:", font=("Arial", 11, "bold"), bg="#ffffff", fg="#0052cc").pack(anchor="w", pady=(10,0))
        self.ent_senha = tk.Entry(frame_card, font=("Arial", 12), show="*", bd=2, relief="groove")
        self.ent_senha.pack(fill="x", pady=5)
        
        btn_logar = tk.Button(frame_card, text="Entrar no Painel", font=("Arial", 12, "bold"), bg="#0052cc", fg="white", bd=0, command=self.autenticar)
        btn_logar.pack(fill="x", pady=15)

    def autenticar(self):
        usuario = self.ent_usuario.get().strip()
        senha = self.ent_senha.get().strip()
        if usuario in USUARIOS and USUARIOS[usuario] == senha:
            self.logado = True
            self.tela_principal()
        else:
            messagebox.showerror("Erro de Autenticação", "Usuário ou senha incorretos!")

    def tela_principal(self):
        self.limpar_tela()
        lbl_welcome = tk.Label(self.root, text="Painel de Controle de Vistorias", font=("Arial", 14, "bold"), bg="#0a192f", fg="#ffffff")
        lbl_welcome.pack(pady=20)
        
        frame_acoes = tk.Frame(self.root, bg="#0a192f")
        frame_acoes.pack(pady=10, padx=20, fill="x")
        
        btn_selecionar = tk.Button(frame_acoes, text="1. Selecionar Pasta Base (Ex: Fotos de entrada 2026)", font=("Arial", 10, "bold"), bg="#b3d4ff", fg="#0033aa", command=self.selecionar_pasta)
        btn_selecionar.pack(fill="x", pady=5)
        
        self.lbl_pasta = tk.Label(frame_acoes, text="Nenhuma pasta selecionada", font=("Arial", 9, "italic"), bg="#0a192f", fg="#b3d4ff", wraplength=400)
        self.lbl_pasta.pack(pady=5)
        
        self.btn_sincronizar = tk.Button(self.root, text="🔄 Executar Backup e Sincronismo Manual", font=("Arial", 12, "bold"), bg="#28a745", fg="white", state="disabled", command=self.executar_backup)
        self.btn_sincronizar.pack(pady=20, padx=40, fill="x")
        
        tk.Label(self.root, text="Logs do Sistema:", font=("Arial", 10, "bold"), bg="#0a192f", fg="#ffffff").pack(anchor="w", padx=40)
        self.txt_logs = tk.Text(self.root, height=10, font=("Courier New", 9), bg="#000000", fg="#00ff00")
        self.txt_logs.pack(pady=5, padx=40, fill="x")

    def selecionar_pasta(self):
        caminho = filedialog.askdirectory()
        if caminho:
            self.pasta_selecionada = caminho
            self.lbl_pasta.config(text=caminho, fg="#ffffff")
            self.btn_sincronizar.config(state="normal")
            self.log_mensagem(f"Pasta selecionada: {caminho}")

    def log_mensagem(self, msg):
        self.txt_logs.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        self.txt_logs.see(tk.END)

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def gerar_credenciais(self):
            sufixo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            login = f"ADTEC-{sufixo}"
            senha = ''.join(random.choices(string.digits, k=6))
            return login, senha

    def executar_backup(self):
        self.log_mensagem("Iniciando varredura inteligente em profundidade...")
        
        if not self.pasta_selecionada:
            self.log_mensagem("Erro: Nenhuma pasta base foi selecionada.")
            return

        PREFIXOS_VALIDOS = ["rua", "r.", "avenida", "av.", "praça", "pç", "alameda", "al."]
        ELEMENTOS_VALIDOS = ["centro", "bairro", "loja", "fundos", "parque", "vilela", "jardim"]

        pastas_de_imoveis_encontradas = []

        try:
            # 1. Primeiro nível: Varre tudo o que está dentro da pasta selecionada (Ex: Fotos de Vistoria de Entrada)
            itens_raiz = os.listdir(self.pasta_selecionada)
            
            for item in itens_raiz:
                caminho_item = os.path.join(self.pasta_selecionada, item)
                
                if os.path.isdir(caminho_item):
                    # Se for uma pasta de ano (Ex: 'Fotos de Vistoria 2026')
                    if "fotos de vistoria" in item.lower():
                        self.log_mensagem(f"📁 Entrando na pasta de ano: '{item}'")
                        
                        # 2. Segundo nível: Entra na pasta do ano e pega os imóveis lá dentro
                        sub_itens = os.listdir(caminho_item)
                        for sub_item in sub_itens:
                            caminho_sub_item = os.path.join(caminho_item, sub_item)
                            
                            if os.path.isdir(caminho_sub_item):
                                nome_minusculo = sub_item.lower()
                                tem_prefixo = any(prefixo in nome_minusculo for prefixo in PREFIXOS_VALIDOS)
                                tem_elemento = any(elemento in nome_minusculo for elemento in ELEMENTOS_VALIDOS)
                                
                                # Aplica a pergunta chave do Gilberto apenas nos endereços reais
                                if tem_prefixo or tem_elemento:
                                    # Guarda o caminho completo da pasta do imóvel e o nome dela
                                    pastas_de_imoveis_encontradas.append((caminho_sub_item, sub_item))
                                else:
                                    self.log_mensagem(f"   [Ignorado]: '{sub_item}' não é um endereço.")
                    
                    # Caso o usuário já selecione direto a pasta do ano (Ex: Selecionou direto a 'Fotos de Vistoria 2026')
                    else:
                        nome_minusculo = item.lower()
                        tem_prefixo = any(prefixo in nome_minusculo for prefixo in PREFIXOS_VALIDOS)
                        tem_elemento = any(elemento in nome_minusculo for elemento in ELEMENTOS_VALIDOS)
                        if tem_prefixo or tem_elemento:
                            pastas_de_imoveis_encontradas.append((caminho_item, item))

        except Exception as e:
            self.log_mensagem(f"Erro ao ler diretórios: {e}")
            return

        if not pastas_de_imoveis_encontradas:
            self.log_mensagem("Nenhum endereço válido foi localizado nas subpastas.")
            return

        # 3. Processamento final estritamente dentro das pastas de endereços validadas
        for caminho_absoluto_imovel, imovel in pastas_de_imoveis_encontradas:
            caminho_txt_estrito = os.path.join(caminho_absoluto_imovel, "Acesso Online.txt")
            
            login_imovel = ""
            senha_imovel = ""
            
            # RESPOSTA SIM: Cria o arquivo TXT rigorosamente dentro da pasta do respectivo imóvel
            if not os.path.exists(caminho_txt_estrito):
                login_imovel, senha_imovel = self.gerar_credenciais()
                conteudo = (
                    f"ADTEC IMÓVEIS - DADOS DE ACESSO À VISTORIA\n"
                    f"=========================================\n"
                    f"Endereço: {imovel}\n"
                    f"Link do Portal: {LINK_PORTAL}\n"
                    f"Login: {login_imovel}\n"
                    f"Senha: {senha_imovel}\n"
                    f"=========================================\n"
                    f"Copie os dados acima para enviar ao inquilino."
                )
                try:
                    with open(caminho_txt_estrito, "w", encoding="utf-8") as f:
                        f.write(conteudo)
                    self.log_mensagem(f"✨ [TXT CRIADO] em: .../{imovel[:25]}")
                except Exception as e:
                    self.log_mensagem(f"❌ Erro ao criar TXT em {imovel[:20]}: {e}")
            else:
                self.log_mensagem(f"✅ [TXT JÁ EXISTIA] em: .../{imovel[:25]}")
                try:
                    with open(caminho_txt_estrito, "r", encoding="utf-8") as f:
                        for linha in f:
                            if "Login:" in linha:
                                login_imovel = linha.split("Login:")[1].strip()
                            if "Senha:" in linha:
                                senha_imovel = linha.split("Senha:")[1].strip()
                except Exception as e:
                    self.log_mensagem(f"⚠️ Erro ao ler TXT existente: {e}")

            # Contagem de fotos
            try:
                arquivos = os.listdir(caminho_absoluto_imovel)
                fotos = [arq for arq in arquivos if arq.lower().endswith(('.png', '.jpg', '.jpeg'))]
                self.log_mensagem(f"   └─► Imagens encontradas: {len(fotos)}")
            except Exception as e:
                self.log_mensagem(f"   └─► Erro ao listar fotos: {e}")
                continue

            # Conectando e subindo dados para o banco na nuvem
            if self.db and login_imovel and senha_imovel:
                try:
                    doc_ref = self.db.collection("vistorias").document(login_imovel)
                    doc_ref.set({
                        "login": login_imovel,
                        "senha": senha_imovel,
                        "endereco_completo": imovel,
                        "quantidade_fotos": len(fotos),
                        "data_sincronismo": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }, merge=True)
                    self.log_mensagem(f"   └─► Nuvem Sincronizada com Sucesso!")
                except Exception as e:
                    self.log_mensagem(f"   └─► Erro de persistência em nuvem: {e}")
            
        messagebox.showinfo("Sucesso", "Filtro de árvore aplicado! Arquivos TXT gerados nos destinos corretos.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()