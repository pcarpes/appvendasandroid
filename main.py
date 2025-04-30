from kivy.app import App
from kivy.lang import Builder
from telas import *
from butoes import *
from bannervenda import *
import requests
import os
from functools import partial
from myfirebase import MyFirebase
from bannervendedor import BannerVendedor
from datetime import date



GUI = Builder.load_file("main.kv")
class MainApp(App):
    cliente = None
    produto = None
    unidade = None

    def build(self):
        self.firebase = MyFirebase()
        return GUI

    def on_start(self):
        #carregar fotos de perfil
        arquivos = os.listdir("icones/fotos_perfil")
        pagina_fotoperfil = self.root.ids["fotoperfilpage"]
        lista_fotos = pagina_fotoperfil.ids["lista_fotos_perfil"]
        for foto in arquivos:
            imagem = ImageButton(source=f"icones/fotos_perfil/{foto}", on_release= partial(self.mudar_foto_perfil, foto))
            lista_fotos.add_widget(imagem)

        #carregar fotos dos clientes
        arquivos = os.listdir("icones/fotos_clientes")
        pagina_adicionarvendas = self.root.ids["adicionarvendaspage"]
        lista_clientes = pagina_adicionarvendas.ids["lista_clientes"]
        for foto_cliente in arquivos:
            imagem = ImageButton(source=f"icones/fotos_clientes/{foto_cliente}",
                                 on_release=partial(self.selecionar_cliente, foto_cliente))
            label = LabelButton(text=foto_cliente.replace(".png","").capitalize(),
                                on_release=partial(self.selecionar_cliente, foto_cliente))
            lista_clientes.add_widget(imagem)
            lista_clientes.add_widget(label)

        #carregar fotos dos produtos
        arquivos = os.listdir("icones/fotos_produtos")
        pagina_adicionarvendas = self.root.ids["adicionarvendaspage"]
        lista_produtos = pagina_adicionarvendas.ids["lista_produtos"]
        for foto_produto in arquivos:
            imagem = ImageButton(source=f"icones/fotos_produtos/{foto_produto}",
                                 on_release=partial(self.selecionar_produto, foto_produto))
            label = LabelButton(text=foto_produto.replace(".png", "").capitalize(),
                                on_release=partial(self.selecionar_produto, foto_produto))
            lista_produtos.add_widget(imagem)
            lista_produtos.add_widget(label)

        #carregar data
        pagina_adicionarvendas = self.root.ids["adicionarvendaspage"]
        label_data = pagina_adicionarvendas.ids["label_data"]
        label_data.text = f"Dia: {date.today().strftime('%d/%m/%Y')}"


        self.carregar_infos_usuario()

    def carregar_infos_usuario(self):
        try:
            with open("refreshtoken.txt", "r") as arquivo:
                refresh_token = arquivo.read()
            local_id, id_token = self.firebase.trocar_token(refresh_token)
            self.local_id = local_id
            self.id_token = id_token

            #pegar informacoes de usuario
            requisicao = requests.get(f"https://aplicativovendashash-e2261-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}")
            requisicao_dic = requisicao.json()

            #preencher foto de perfil
            avatar = requisicao_dic["avatar"]
            self.avatar = avatar
            foto_perfil = self.root.ids["foto_perfil"]
            foto_perfil.source = f"icones/fotos_perfil/{avatar}"

            #preencher ID unico
            id_vendedor = requisicao_dic['id_vendedor']
            self.id_vendedor = id_vendedor
            pagina_ajustes = self.root.ids["ajustespage"]
            pagina_ajustes.ids["id_vendedor"].text = f"Seu ID unico: {id_vendedor}"

            #preencher total vendas
            total_vendas = requisicao_dic['total_vendas']
            self.total_vendas = total_vendas
            homepage = self.root.ids["homepage"]
            homepage.ids["label_total_vendas"].text = f"[color=#000000]Total de vendas:[/color] [b]R$ {total_vendas}[/b]"

            #preencher equipe
            self.equipe = requisicao_dic["equipe"]

            #preencher lista de vendas
            try:
                vendas = requisicao_dic["vendas"]
                self.vendas = vendas
                pagina_homepage = self.root.ids["homepage"]
                lista_vendas = pagina_homepage.ids["lista_vendas"]
                for id_venda in vendas:
                    venda = vendas[id_venda]
                    banner = BannerVenda(cliente=venda["cliente"], foto_cliente=venda["foto_cliente"],
                                         produto=venda["produto"], foto_produto=venda["foto_produto"],
                                         data=venda["data"], preco=venda["preco"], unidade=venda["unidade"],
                                         quantidade=venda["quantidade"])
                    lista_vendas.add_widget(banner)
            except Exception as e:
                print(e)

            #preencher equipe vendedores
            try:
                equipe = requisicao_dic["equipe"]
                lista_equipe = equipe.split(",")
                paginalistarvendas = self.root.ids["listarvendaspage"]
                lista_vendedores = paginalistarvendas.ids["lista_vendedores"]

                for id_vendedor_equipe in lista_equipe:
                    if id_vendedor_equipe != "":
                        banner_vendedor = BannerVendedor(id_vendedor=id_vendedor_equipe)
                        lista_vendedores.add_widget(banner_vendedor)

                self.mudar_tela("homepage")
            except Exception as e:
                print(f'Erro: {e}')

        except:
                pass

    def mudar_tela(self, id_tela):
        gerenciador_telas = self.root.ids["screen_manager"]
        gerenciador_telas.current = id_tela

    def mudar_foto_perfil(self, foto, *args):
        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/{foto}"

        info = f'{{"avatar": "{foto}"}}'
        requisicao = requests.patch(f"https://aplicativovendashash-e2261-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}",
                                    data=info)
        self.mudar_tela("ajustespage")

    def adicionar_vendedor(self, id_vendedor_adicionado):
        link = f'https://aplicativovendashash-e2261-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"&equalTo="{id_vendedor_adicionado}"'
        requisicao = requests.get(link)
        requisicao_dic = requisicao.json()

        pagina_adicionarvendedor = self.root.ids["adicionarvendedorpage"]
        mensagem_texto = pagina_adicionarvendedor.ids["mensagem_outrovendedor"]
        if requisicao_dic == {}:
            mensagem_texto.text = "Vendedor nao encontrado"
        else:
            equipe = self.equipe.split(",")
            if id_vendedor_adicionado in equipe:
                mensagem_texto.text = "Vendedor ja faz parte da equipe"
            else:
                self.equipe = self.equipe + f",{id_vendedor_adicionado}"
                info = f'{{"equipe": "{self.equipe}"}}'
                requests.patch(f"https://aplicativovendashash-e2261-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}",
                               data=info)
                mensagem_texto.text = "Vendedor adicionado com sucesso"
                #adicionar novo banner na lista de vendedores da equipe
                paginalistarvendas = self.root.ids["listarvendaspage"]
                lista_vendedores = paginalistarvendas.ids["lista_vendedores"]
                banner_vendedor = BannerVendedor(id_vendedor=id_vendedor_adicionado)
                lista_vendedores.add_widget(banner_vendedor)

    def selecionar_cliente(self, foto, *args):
        self.cliente = foto.replace(".png", "")
        #Pintar de branco todas os textos
        pagina_adicionarvendas = self.root.ids["adicionarvendaspage"]
        lista_clientes = pagina_adicionarvendas.ids["lista_clientes"]

        for item in list(lista_clientes.children):
            item.color = (1,1,1,1)
            #pintar de azul o texto do item selecionado
            #foto=carrefour.png / Label: Carrefour -> carrefour -> carrefour.png
            try:
                texto = item.text
                texto = texto.lower() + ".png"
                if foto == texto:
                    item.color = (0, 207/255, 219/255, 1)
            except:
                pass

    def selecionar_produto(self, foto, *args):
        self.produto = foto.replace(".png", "")
        #Pintar de branco todas os textos
        pagina_adicionarvendas = self.root.ids["adicionarvendaspage"]
        lista_produtos = pagina_adicionarvendas.ids["lista_produtos"]

        for item in list(lista_produtos.children):
            item.color = (1,1,1,1)
            #pintar de azul o texto do item selecionado
            #foto=arroz.png / Label: Arroz -> arroz -> arroz.png
            try:
                texto = item.text
                texto = texto.lower() + ".png"
                if foto == texto:
                    item.color = (0, 207/255, 219/255, 1)
            except:
                pass

    def selecionar_unidade(self, id_label, *args):
        pagina_adicionarvendas = self.root.ids["adicionarvendaspage"]
        self.unidade = id_label.replace("unidades_", "")
        #pintar todos de branco
        pagina_adicionarvendas.ids["unidades_kg"].color = (1,1,1,1)
        pagina_adicionarvendas.ids["unidades_unidades"].color = (1, 1, 1, 1)
        pagina_adicionarvendas.ids["unidades_litros"].color = (1, 1, 1, 1)

        #pintar o texto selecionado de azul
        pagina_adicionarvendas.ids[id_label].color = (0, 207/255, 219/255, 1)

    def adicionar_venda(self):
        cliente = self.cliente
        produto = self.produto
        unidade = self.unidade
        pagina_adicionarvendas = self.root.ids["adicionarvendaspage"]
        data = pagina_adicionarvendas.ids["label_data"].text.replace("Data: ", "")
        preco = pagina_adicionarvendas.ids["preco_total"].text
        quantidade = pagina_adicionarvendas.ids["quantidade"].text

        if not cliente:
            pagina_adicionarvendas.ids["label_selecione_cliente"].color = (1,0,0,1)
        if not produto:
            pagina_adicionarvendas.ids["label_selecione_produto"].color = (1, 0, 0, 1)
        if not unidade:
            pagina_adicionarvendas.ids["unidades_kg"].color = (1, 0, 0, 1)
            pagina_adicionarvendas.ids["unidades_unidades"].color = (1, 0, 0, 1)
            pagina_adicionarvendas.ids["unidades_litros"].color = (1, 0, 0, 1)
        if not preco:
            pagina_adicionarvendas.ids["label_preco"].color = (1, 0, 0, 1)
        else:
            try:
                preco = float(preco)
            except:
                pagina_adicionarvendas.ids["label_preco"].color = (1, 0, 0, 1)
        if not quantidade:
            pagina_adicionarvendas.ids["label_quantidade"].color = (1, 0, 0, 1)
        else:
            try:
                quantidade = float(quantidade)
            except:
                pagina_adicionarvendas.ids["label_quantidade"].color = (1, 0, 0, 1)

        #verifica se tudo foi preenchido corretamente e executa a funcao de adicionar venda no banco de dados
        if cliente and produto and unidade and preco and quantidade and (type(preco)==float) and (type(quantidade==float)):
            foto_cliente = cliente + ".png"
            foto_produto = produto + ".png"

            info = (f'{{"cliente": "{cliente}", "produto": "{produto}", "foto_cliente": "{foto_cliente}", '
                    f'"foto_produto": "{foto_produto}", "data": "{data}", "unidade": "{unidade}", '
                    f'"preco": "{preco}", "quantidade": "{quantidade}"}}')

            requests.post(f"https://aplicativovendashash-e2261-default-rtdb.firebaseio.com/{self.local_id}/vendas.json?auth={self.id_token}", data=info)

            banner = BannerVenda(cliente=cliente, produto=produto, foto_cliente=foto_cliente, foto_produto=foto_produto,
                                 data=data, preco=preco, quantidade=quantidade, unidade=unidade)

            pagina_homepage = self.root.ids["homepage"]
            lista_vendas = pagina_homepage.ids["lista_vendas"]
            lista_vendas.add_widget(banner)

            requisicao = requests.get(f"https://aplicativovendashash-e2261-default-rtdb.firebaseio.com/{self.local_id}/total_vendas.json?auth={self.id_token}")
            total_vendas = float(requisicao.json())
            total_vendas += preco
            info = f'{{"total_vendas":"{total_vendas}"}}'
            requests.patch(f"https://aplicativovendashash-e2261-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}", data=info)

            homepage = self.root.ids["homepage"]
            homepage.ids["label_total_vendas"].text = f"[color=#000000]Total de vendas:[/color] [b]R$ {total_vendas}[/b]"

            self.mudar_tela("homepage")


        self.cliente = None
        self.produto = None
        self.unidade = None

    def carregar_todas_vendas(self):
        pagina_todasvendas = self.root.ids["todasvendaspage"]
        lista_vendas = pagina_todasvendas.ids["lista_vendas"]
        total_vendas = 0

        for item in list(lista_vendas.children):
            lista_vendas.remove_widget(item)

        #preencher a pagina todasvendaspage
        # pegar informacoes da empresa
        requisicao = requests.get(
            f'https://aplicativovendashash-e2261-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"')
        requisicao_dic = requisicao.json()

        # preencher foto de perfil
        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/hash.png"

        # preencher lista de vendas
        for local_id_usuario in requisicao_dic:
            try:
                vendas = requisicao_dic[local_id_usuario]["vendas"]
                for id_venda in vendas:
                    venda = vendas[id_venda]
                    total_vendas += float(venda["preco"])
                    banner = BannerVenda(cliente=venda["cliente"], foto_cliente=venda["foto_cliente"],
                                         produto=venda["produto"], foto_produto=venda["foto_produto"],
                                         data=venda["data"], preco=venda["preco"], unidade=venda["unidade"],
                                         quantidade=venda["quantidade"])
                    lista_vendas.add_widget(banner)
            except:
                pass

        # preencher total vendas
        pagina_todasvendas.ids["label_total_vendas"].text = f"[color=#000000]Total de vendas:[/color] [b]R$ {total_vendas}[/b]"


        #redirecionar para todasvendaspage
        self.mudar_tela("todasvendaspage")

    def sair_todas_vendas(self, id_tela):
        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/{self.avatar}"

        self.mudar_tela(id_tela)

    def carregar_vendas_vendedor(self, dic_info_vendedor, *args):
        try:
            vendas = dic_info_vendedor["vendas"]
            pagina_vendasoutrovendedor = self.root.ids["vendasoutrovendedorpage"]
            lista_vendas = pagina_vendasoutrovendedor.ids["lista_vendas"]
            #limpar vendas anteriores
            for item in list(lista_vendas.children):
                lista_vendas.remove_widget(item)

            for id_venda in vendas:
                venda = vendas[id_venda]
                banner = BannerVenda(cliente=venda["cliente"], foto_cliente=venda["foto_cliente"],
                                     produto=venda["produto"], foto_produto=venda["foto_produto"],
                                     data=venda["data"], preco=venda["preco"], unidade=venda["unidade"],
                                     quantidade=venda["quantidade"])
                lista_vendas.add_widget(banner)
        except:
            pass

        total_vendas = dic_info_vendedor["total_vendas"]
        # preencher total vendas
        pagina_vendasoutrovendedor.ids[
            "label_total_vendas"].text = f"[color=#000000]Total de vendas:[/color] [b]R$ {total_vendas}[/b]"

        # preencher foto de perfil
        foto_perfil = self.root.ids["foto_perfil"]
        avatar = dic_info_vendedor["avatar"]
        foto_perfil.source = f"icones/fotos_perfil/{avatar}"

        self.mudar_tela("vendasoutrovendedorpage")

MainApp().run()
