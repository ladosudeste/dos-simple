import asyncio
import aiohttp
import threading
import time

def start_event_loop(url, thread_id):
    """Cria um loop de eventos isolado para cada thread."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    async def request_worker():
        # Cada thread gerencia sua própria sessão (obrigatório para segurança de threads)
        async with aiohttp.ClientSession() as session:
            print(f"[Thread {thread_id}] Iniciada.")
            while True:
                try:
                    async with session.get(url) as response:
                        await response.read() # Consome a resposta
                        print(f"[Thread {thread_id}] Request OK - Status: {response.status}")
                except Exception as e:
                    print(f"[Thread {thread_id}] Erro: {e}")
                
                # Pequena pausa para não estourar o limite de conexões local
                await asyncio.sleep(0.1)

    loop.run_until_complete(request_worker())

if __name__ == "__main__":
    target_url = input("URL de destino: ").strip()
    num_threads = int(input("Número de Threads: "))

    if not target_url.startswith("http"):
        target_url = "http://" + target_url

    threads = []

    for i in range(num_threads):
        # Criação dinâmica conforme o input do usuário
        t = threading.Thread(target=start_event_loop, args=(target_url, i), daemon=True)
        threads.append(t)
        t.start()

    print(f"\nDisparadas {num_threads} threads em paralelo.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nParando tudo...")
