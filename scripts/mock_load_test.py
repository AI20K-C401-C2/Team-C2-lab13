import random
import time
import httpx

BASE_URL = "http://127.0.0.1:8000"

FEATURES = ["bao_hanh", "gia_xe", "tra_gop", "pin_sac", "dich_vu"]

MESSAGES = [
    "Chinh sach bao hanh VinFast la bao lau?",
    "VinFast VF8 co nhung mau nao?",
    "Thu tuc mua xe VinFast tra gop nhu the nao?",
    "Pin xe dien VinFast bao hanh bao nhieu nam?",
    "Co the doi pin VinFast VF e34 khong?",
    "Chinh sach thu cu doi moi VinFast 2024?",
    "VinFast VF9 gia bao nhieu tien hien tai?",
    "Co tram sac VinFast o Da Nang khong?",
    "VinFast Lux SA2.0 con duoc san xuat khong?",
    "Chinh sach uu dai cho khach hang mua VF5?",
    "Xe VinFast co ho tro lai tu dong khong?",
    "Thu tuc dang ky bien so xe VinFast?",
    "VinFast co showroom o Ha Noi khong?",
    "Bao duong dinh ky VinFast VF8 bao nhieu tien?",
    "VinFast co chinh sach doi tra xe trong 7 ngay khong?",
    "Mua xe VinFast co duoc tang kem sac khong?",
    "Chinh sach ho tro lai suat 0% khi mua VinFast?",
    "Thoi gian giao xe VinFast VF8 la bao lau?",
    "VinFast co chuong trinh gioi thieu ban be khong?",
    "Bao hiem xe VinFast bao nhieu tien mot nam?",
]


def random_payload():
    return {
        "user_id": f"user_{random.randint(1, 100)}",
        "feature": random.choice(FEATURES),
        "session_id": f"sess_{random.randint(1000, 9999)}",
        "message": random.choice(MESSAGES),
    }


def main() -> None:
    print("Mock Load Test - Dashboard Data Generator")
    print("=" * 50)
    print("Chay moi 30 giay, nhan Ctrl+C de dung\n")

    with httpx.Client() as client:
        batch_num = 1
        while True:
            # Random so request moi batch (5-25 request)
            batch_size = random.randint(5, 25)
            
            # Random delay giua cac request trong batch
            delay = random.uniform(0.05, 0.3)
            
            print(f"[Batch {batch_num}] Gui {batch_size} request...")
            
            for i in range(batch_size):
                payload = random_payload()
                try:
                    r = client.post(f"{BASE_URL}/chat", json=payload, timeout=30.0)
                    print(f"  [{r.status_code}] {payload['feature']} | {payload['message'][:35]}...")
                except Exception as e:
                    print(f"  Error: {e}")
                
                # Delay ngau nhien giua cac request
                if i < batch_size - 1:
                    time.sleep(delay)
            
            # Random: doi khi gay loi (30% chance - cao hon de error breakdown nhay)
            if random.random() < 0.3:
                print("  -> Injecting error request...")
                try:
                    # Gui request voi payload loi
                    client.post(f"{BASE_URL}/chat", json={"invalid": "data"}, timeout=5.0)
                except Exception:
                    pass  # Expected error
            
            # Random: doi khi gay timeout (20% chance)
            if random.random() < 0.2:
                print("  -> Injecting timeout request...")
                try:
                    # Gui request voi message rat dai de gay delay
                    client.post(
                        f"{BASE_URL}/chat",
                        json={
                            "user_id": "user_slow",
                            "feature": "rag",
                            "session_id": "sess_slow",
                            "message": "A" * 5000,  # Message qua dai
                        },
                        timeout=0.001,  # Timeout cuc nhanh
                    )
                except Exception:
                    pass  # Expected timeout
            
            # Random: doi khi gay validation error (15% chance)
            if random.random() < 0.15:
                print("  -> Injecting validation error...")
                try:
                    # Thieu required field
                    client.post(
                        f"{BASE_URL}/chat",
                        json={"message": "Missing other fields"},
                        timeout=5.0,
                    )
                except Exception:
                    pass  # Expected error
            
            # Random thoi gian cho lan chay tiep theo (1s - 20s)
            wait_time = random.randint(1, 20)
            print(f"[Batch {batch_num}] Hoan thanh. Doi {wait_time}s...\n")
            batch_num += 1
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDa dung mock load test.")
