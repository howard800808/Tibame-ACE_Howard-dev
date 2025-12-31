import time
import requests
import psutil
import csv
import threading
import argparse
import statistics
from datetime import datetime
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# 確保安裝了 psutil
try:
    import psutil
except ImportError:
    print("請先安裝 psutil: pip install psutil")
    sys.exit(1)

class SystemMonitor:
    def __init__(self, interval=1.0):
        self.interval = interval
        self.running = False
        self.metrics = []
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def _monitor_loop(self):
        while self.running:
            cpu_percent = psutil.cpu_percent(interval=None)
            memory = psutil.virtual_memory()
            net_connections = len(psutil.net_connections())
            
            self.metrics.append({
                'timestamp': datetime.now().isoformat(),
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_used_mb': memory.used / (1024 * 1024),
                'net_connections': net_connections
            })
            time.sleep(self.interval)

    def get_latest_metrics(self):
        if not self.metrics:
            return None
        return self.metrics[-1]

class LoadTester:
    def __init__(self, url, max_workers=100, step_duration=10, step_size=10):
        self.url = url
        self.max_workers = max_workers
        self.step_duration = step_duration
        self.step_size = step_size
        self.results = []
        self.monitor = SystemMonitor()

    def send_request(self):
        start_time = time.time()
        try:
            response = requests.get(self.url, timeout=5)
            elapsed = time.time() - start_time
            return {
                'success': 200 <= response.status_code < 300,
                'elapsed': elapsed,
                'status_code': response.status_code
            }
        except Exception as e:
            return {
                'success': False,
                'elapsed': time.time() - start_time,
                'error': str(e)
            }

    def run_step(self, concurrent_users):
        print(f"正在測試 {concurrent_users} 個併發連線...")
        
        step_results = []
        start_time = time.time()
        
        # 在 step_duration 內持續發送請求
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            while time.time() - start_time < self.step_duration:
                futures = [executor.submit(self.send_request) for _ in range(concurrent_users)]
                
                for future in as_completed(futures):
                    step_results.append(future.result())
                
                # 簡單的速率限制，避免過度轟炸導致測試腳本本身崩潰
                time.sleep(0.1)

        # 計算統計數據
        if not step_results:
            return None

        success_count = sum(1 for r in step_results if r['success'])
        total_count = len(step_results)
        avg_time = statistics.mean([r['elapsed'] for r in step_results])
        
        sys_metrics = self.monitor.get_latest_metrics()
        
        return {
            'concurrent_users': concurrent_users,
            'total_requests': total_count,
            'success_rate': (success_count / total_count) * 100,
            'avg_response_time': avg_time,
            'cpu_percent': sys_metrics['cpu_percent'] if sys_metrics else 0,
            'memory_percent': sys_metrics['memory_percent'] if sys_metrics else 0,
            'net_connections': sys_metrics['net_connections'] if sys_metrics else 0
        }

    def run(self):
        print(f"開始壓力測試: 目標 {self.url}")
        print(f"最大併發: {self.max_workers}, 每階段持續: {self.step_duration}秒")
        
        self.monitor.start()
        
        try:
            current_users = self.step_size
            while current_users <= self.max_workers:
                result = self.run_step(current_users)
                if result:
                    self.results.append(result)
                    print(f"結果: Users={result['concurrent_users']}, "
                          f"CPU={result['cpu_percent']}%, "
                          f"RAM={result['memory_percent']}%, "
                          f"AvgTime={result['avg_response_time']:.3f}s, "
                          f"Success={result['success_rate']:.1f}%")
                
                current_users += self.step_size
                time.sleep(2) # 冷卻時間
                
        except KeyboardInterrupt:
            print("\n測試被使用者中斷")
        finally:
            self.monitor.stop()
            self.save_results()

    def save_results(self):
        if not self.results:
            print("沒有結果可儲存")
            return

        filename = f"benchmark_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        keys = self.results[0].keys()
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.results)
            
        print(f"\n測試報告已儲存至: {filepath}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="網站壓力測試與系統監控工具")
    parser.add_argument("--url", default="http://127.0.0.1:8000", help="測試目標 URL")
    parser.add_argument("--max_users", type=int, default=100, help="最大併發使用者數")
    parser.add_argument("--step_duration", type=int, default=10, help="每個併發階段的持續時間(秒)")
    parser.add_argument("--step_size", type=int, default=10, help="每次增加的使用者數")
    
    args = parser.parse_args()
    
    tester = LoadTester(
        url=args.url,
        max_workers=args.max_users,
        step_duration=args.step_duration,
        step_size=args.step_size
    )
    tester.run()
