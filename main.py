from csv import excel
from kivy.app import App
from kivy.lang import Builder
from myfirebase import MyFirebase
from telas import *
from botoes import *
import requests
from bannervenda import BannerVenda
import os
from functools import partial
from myfirebase import MyFirebase


GUI = Builder.load_file("main.kv")


class MainApp(App):

    def build(self):
        self.firebase = MyFirebase()
        return GUI

    def on_start(self):
        # carregar as fotos de perfil
        arquivos = os.listdir("icones/fotos_perfil/")
        pagina_foto_perfil = self.root.ids["fotoperfilpage"]
        lista_fotos = pagina_foto_perfil.ids["lista_fotos_perfil"]
        for foto in arquivos:
            imagem = ImageButton(
                source=f"icones/fotos_perfil/{foto}", on_release=partial(self.mudar_foto_perfil, foto))
            lista_fotos.add_widget(imagem)

        # carrega as infos dos usuários
        self.carregar_infos_usuario()

    def carregar_infos_usuario(self):
        try:
            # pegar informacoes do usuario
            requisicao = requests.get(
                f"https://aplicativovendashash-ac1e8-default-rtdb.firebaseio.com/{self.local_id}.json")
            requisicao_dic = requisicao.json()

            # preencher foto de perfil
            avatar = requisicao_dic['avatar']
            foto_perfil = self.root.ids["foto_perfil"]
            foto_perfil.source = f"icones/fotos_perfil/{avatar}"

            # preencher lista de vendas
            try:
                vendas = requisicao_dic['vendas'][1:]
                for venda in vendas:
                    banner = BannerVenda(cliente=venda["cliente"], foto_cliente=venda["foto_cliente"],
                                         produto=venda["produto"], foto_produto=venda["foto_produto"],
                                         data=venda["data"], preco=venda["preco"],
                                         unidade=venda["unidade"], quantidade=venda["quantidade"])
                    pagina_homepage = self.root.ids["homepage"]
                    lista_vendas = pagina_homepage.ids["lista_vendas"]
                    lista_vendas.add_widget(banner)
            except:
                pass
        except:
            pass

    def mudar_tela(self, id_tela):
        # print(id_tela)
        gerenciador_telas = self.root.ids["screen_manager"]
        gerenciador_telas.current = id_tela

    def mudar_foto_perfil(self, foto, *args):
        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/{foto}"

        info = f'{{"avatar": "{foto}"}}'
        requests.patch(f'https://aplicativovendashash-ac1e8-default-rtdb.firebaseio.com/{self.local_id}.json',
                       data=info)

        self.mudar_tela("ajustespage")


MainApp().run()
