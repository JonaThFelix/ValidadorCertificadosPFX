import os
from datetime import datetime
from tkinter import Tk, Label, Button, messagebox, filedialog
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

class VerificadorICPBrasil:
    def __init__(self, master):
        self.master = master
        master.title("Verificador de Certificados ICP-Brasil")

        self.label = Label(master, text="Selecione o certificado ICP-Brasil para verificar:")
        self.label.pack()

        self.selecionar_certificado_button = Button(master, text="Selecionar Certificado", command=self.selecionar_certificado)
        self.selecionar_certificado_button.pack()

    def verifica_validade_certificado(self, caminho_certificado):
        try:
            with open(caminho_certificado, 'rb') as cert_file:
                cert_data = cert_file.read()

            cert_priv_key = serialization.load_pem_private_key(
                cert_data,
                password=None,
                backend=default_backend()
            )

            cert = cert_priv_key.public_key().certificate

            data_validade = cert.not_valid_after
            data_atual = datetime.utcnow()
            diferenca_tempo = data_validade - data_atual

            dias_limite_perto_vencimento = 30

            if diferenca_tempo.days <= 0:
                messagebox.showinfo("Status do Certificado", "O certificado está vencido.")
            elif diferenca_tempo.days <= dias_limite_perto_vencimento:
                messagebox.showinfo("Status do Certificado", "O certificado está perto de vencer.")
            else:
                messagebox.showinfo("Status do Certificado", "O certificado ainda está válido.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao verificar o certificado:\n{str(e)}")

    def selecionar_certificado(self):
        caminho_certificado = filedialog.askopenfilename(title="Selecione o Certificado ICP-Brasil", filetypes=[("Certificados ICP-Brasil", "*.pfx;*.p12"), ("Todos os arquivos", "*.*")])
        if caminho_certificado:
            self.verifica_validade_certificado(caminho_certificado)

if __name__ == "__main__":
    root = Tk()
    app = VerificadorICPBrasil(root)
    root.mainloop()
