import requests
from kivy.app import App


class MyFirebase():
    API_KEY = "AIzaSyBqE-vOonYSj-aHy2vOpazcLk21uBYUyZ0"

    def criar_conta(self, email, senha):
        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.API_KEY}"
        print(email, senha)
        info = {"email": email,
                "password": senha,
                "returnSecureToken": True}
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()

        if requisicao.ok:
            print("Usuário Criado")
            # requisicao_dic["idToken"] -> autenticacao
            # requisicao_dic["refreshToken"] -> token que mantem o usuario logado
            # requisicao_dic["localId"] -> id_usuario
            refresh_token = requisicao_dic["refreshToken"]
            local_id = requisicao_dic["localId"]
            id_token = requisicao_dic["idToken"]      
            
            meu_aplicativo = App.get_running_app()
            meu_aplicativo.local_id = local_id
            meu_aplicativo.id_token = id_token
            
            with open("refreshtoken.txt", "w") as arquivo:
                arquivo.write(refresh_token)          
                
            link = f'https://aplicativovendashash-ac1e8-default-rtdb.firebaseio.com/{local_id}.json'
            info_usuario = '{"avatar": "foto1.png", "equipe": "", "total_vendas": "0", "vendas": ""}'            
            requisicao_usuario = requests.patch(link, data=info_usuario)
            meu_aplicativo.carregar_infos_usuario()
            meu_aplicativo.mudar_tela("homepage")
                           
        else:
            mensagem_erro = requisicao_dic["error"]["message"]
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids["loginpage"]
            pagina_login.ids["mensagem_login"].text = mensagem_erro
            pagina_login.ids["mensagem_login"].color = (1, 0, 0, 1)           
        print(requisicao_dic)

    def fazer_login(self, email, senha):
        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.API_KEY}"
        info = {"email": email,
                "password": senha,
                "returnSecureToken": True}
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()
         
        if requisicao.ok:
            # requisicao_dic["idToken"] -> autenticacao
            # requisicao_dic["refreshToken"] -> token que mantem o usuario logado
            # requisicao_dic["localId"] -> id_usuario
            refresh_token = requisicao_dic["refreshToken"]
            local_id = requisicao_dic["localId"]
            id_token = requisicao_dic["idToken"]      
            
            meu_aplicativo = App.get_running_app() 
            meu_aplicativo.local_id = local_id
            meu_aplicativo.id_token = id_token
            
            with open("refreshtoken.txt", "w") as arquivo:
                arquivo.write(refresh_token)          
                      
            meu_aplicativo.carregar_infos_usuario()
            meu_aplicativo.mudar_tela("homepage")
                           
        else:
            mensagem_erro = requisicao_dic["error"]["message"]
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids["loginpage"]
            pagina_login.ids["mensagem_login"].text = mensagem_erro
            pagina_login.ids["mensagem_login"].color = (1, 0, 0, 1)  
            
    def trocar_token(self, refresh_token):
        link = f"https://securetoken.googleapis.com/v1/token?key={self.API_KEY}"
        
        info = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token            
        }
        
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()
        local_id = requisicao_dic["user_id"]
        id_token = requisicao_dic["id_token"]
        return local_id, id_token