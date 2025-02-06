import requests
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

class DemoExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or ""
        if not query:
            return RenderResultListAction([
                ExtensionResultItem(icon='images/icon.png',
                                    name='Nenhuma pesquisa fornecida',
                                    description='Digite um termo para buscar.',
                                    on_enter=HideWindowAction())
            ])
        
        url = f"http://192.168.15.10:5001?q={query}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            results = response.json()
        except requests.RequestException as e:
            return RenderResultListAction([
                ExtensionResultItem(icon='images/icon.png',
                                    name='Erro na consulta',
                                    description=str(e),
                                    on_enter=HideWindowAction())
            ])
        
        items = []
        for item in results.get("data", []):  # Ajuste conforme o formato da resposta JSON
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name=item.get("title", "Sem título"),
                                             description=item.get("description", "Sem descrição"),
                                             on_enter=HideWindowAction()))
        
        if not items:
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name='Nenhum resultado encontrado',
                                             description=f'Nenhum dado disponível para "{query}".',
                                             on_enter=HideWindowAction()))
        
        return RenderResultListAction(items)

if __name__ == '__main__':
    DemoExtension().run()
