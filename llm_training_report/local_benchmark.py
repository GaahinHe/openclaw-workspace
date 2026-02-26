#!/usr/bin/env python3
"""
本地基准测试 - 无需下载大模型
测试计算性能、内存带宽等
"""

import os
import time
import json
import torch
import psutil
import numpy as np
from datetime import datetime

REPORT_DIR = "/Users/hans/.openclaw/workspace/llm_training_report"

def log(msg):
    print(f"⏰ {datetime.now().strftime('%H:%M:%S')} | {msg}")

def get_mem():
    return psutil.Process().memory_info().rss / (1024**3)

# ============================================================================
# 基准 1: 张量运算性能
# ============================================================================
def benchmark_matmul():
    log("📊 基准 1: 矩阵乘法性能")
    
    sizes = [512, 1024, 2048]
    results = []
    
    for size in sizes:
        # 准备数据
        a = torch.randn(size, size, device='mps')
        b = torch.randn(size, size, device='mps')
        
        # 预热
        for _ in range(3):
            _ = torch.matmul(a, b)
        
        # 计时
        torch.mps.synchronize()
        start = time.perf_counter()
        
        for _ in range(10):
            _ = torch.matmul(a, b)
        
        torch.mps.synchronize()
        end = time.perf_counter()
        
        elapsed = (end - start) / 10
        flops = (size ** 3 * 2) / elapsed / 1e9  # GFLOPS
        
        results.append({
            "size": size,
            "time_ms": elapsed * 1000,
            "gflops": flops
        })
        log(f"  {size}x{size}: {elapsed*1000:.2f}ms, {flops:.1f} GFLOPS")
    
    return {"status": "success", "results": results}

# ============================================================================
# 基准 2: 内存带宽
# ============================================================================
def benchmark_memory():
    log("📊 基准 2: 内存带宽测试")
    
    sizes = [1024, 2048, 4096]
    results = []
    
    for size in sizes:
        # 创建大张量
        a = torch.randn(size, size, device='mps')
        
        # 预热
        for _ in range(3):
            _ = a * 2
        
        # 测试赋值操作
        torch.mps.synchronize()
        start = time.perf_counter()
        
        for _ in range(100):
            a = a * 2
            a = a / 2
        
        torch.mps.synchronize()
        end = time.perf_counter()
        
        elapsed = (end - start) / 100
        bandwidth_gbps = (size ** 2 * 4 * 2) / elapsed / 1e9  # GB/s (float32 = 4 bytes)
        
        results.append({
            "size": size,
            "time_ms": elapsed * 1000,
            "gbps": bandwidth_gbps
        })
        log(f"  {size}x{size}: {elapsed*1000:.2f}ms, {bandwidth_gbps:.1f} GB/s")
    
    return {"status": "success", "results": results}

# ============================================================================
# 基准 3: 神经网络 Forward Pass
# ============================================================================
def benchmark_forward():
    log("📊 基准 3: 神经网络 Forward Pass")
    
    configs = [
        {"layers": 3, "hidden": 256, "batch": 32},
        {"layers": 6, "hidden": 512, "batch": 16},
        {"layers": 12, "hidden": 768, "batch": 8},
    ]
    results = []
    
    for cfg in configs:
        layers = []
        in_dim = 128
        for i in range(cfg["layers"]):
            layers.append(torch.nn.Linear(in_dim, cfg["hidden"]))
            layers.append(torch.nn.ReLU())
            in_dim = cfg["hidden"]
        layers.append(torch.nn.Linear(in_dim, 10))
        
        model = torch.nn.Sequential(*layers).to('mps')
        x = torch.randn(cfg["batch"], 128, device='mps')
        
        # 预热
        for _ in range(3):
            _ = model(x)
        
        torch.mps.synchronize()
        start = time.perf_counter()
        
        for _ in range(50):
            _ = model(x)
        
        torch.mps.synchronize()
        end = time.perf_counter()
        
        elapsed = (end - start) / 50 * 1000  # ms
        
        results.append({
            "config": f"{cfg['layers']}L-{cfg['hidden']}H",
            "batch": cfg["batch"],
            "time_ms": elapsed
        })
        log(f"  {cfg['layers']}层/{cfg['hidden']}隐藏: {elapsed:.2f}ms/batch")
    
    return {"status": "success", "results": results}

# ============================================================================
# 基准 4: 神经网络 Backward Pass
# ============================================================================
def benchmark_backward():
    log("📊 基准 4: 神经网络训练 (Forward + Backward)")
    
    class SimpleNet(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.layers = torch.nn.ModuleList([
                torch.nn.Linear(256, 512),
                torch.nn.ReLU(),
                torch.nn.Linear(512, 256),
                torch.nn.ReLU(),
                torch.nn.Linear(256, 128),
                torch.nn.Linear(128, 10)
            ])
        
        def forward(self, x):
            for layer in self.layers:
                x = layer(x)
            return x
    
    model = SimpleNet().to('mps')
    optimizer = torch.optim.Adam(model.parameters())
    criterion = torch.nn.CrossEntropyLoss()
    
    batch_sizes = [8, 16, 32]
    results = []
    
    for batch_size in batch_sizes:
        x = torch.randn(batch_size, 256, device='mps')
        y = torch.randint(0, 10, (batch_size,), device='mps')
        
        # 预热
        for _ in range(3):
            optimizer.zero_grad()
            out = model(x)
            loss = criterion(out, y)
            loss.backward()
        
        torch.mps.synchronize()
        start = time.perf_counter()
        
        for _ in range(20):
            optimizer.zero_grad()
            out = model(x)
            loss = criterion(out, y)
            loss.backward()
            optimizer.step()
        
        torch.mps.synchronize()
        end = time.perf_counter()
        
        elapsed = (end - start) / 20 * 1000  # ms
        
        results.append({
            "batch_size": batch_size,
            "time_ms": elapsed,
            "samples_per_sec": batch_size / (elapsed / 1000)
        })
        log(f"  Batch {batch_size}: {elapsed:.2f}ms, {batch_size/(elapsed/1000):.1f} samples/s")
    
    return {"status": "success", "results": results}

# ============================================================================
# 基准 5: 激活函数性能
# ============================================================================
def benchmark_activations():
    log("📊 基准 5: 激活函数性能")
    
    size = 2048
    x = torch.randn(32, size, size, device='mps')
    
    activations = [
        ("ReLU", torch.nn.ReLU()),
        ("GELU", torch.nn.GELU()),
        ("SiLU", torch.nn.SiLU()),
        ("Softmax", torch.nn.Softmax(dim=-1)),
    ]
    results = []
    
    for name, act in activations:
        # 预热
        for _ in range(3):
            _ = act(x)
        
        torch.mps.synchronize()
        start = time.perf_counter()
        
        for _ in range(50):
            _ = act(x)
        
        torch.mps.synchronize()
        end = time.perf_counter()
        
        elapsed = (end - start) / 50 * 1000
        
        results.append({
            "function": name,
            "time_ms": elapsed
        })
        log(f"  {name}: {elapsed:.2f}ms")
    
    return {"status": "success", "results": results}

# ============================================================================
# 基准 6: 混合精度测试
# ============================================================================
def benchmark_fp16():
    log("📊 基准 6: 混合精度 (FP16 vs FP32)")
    
    size = 1024
    results = []
    
    # FP32
    a32 = torch.randn(size, size, device='mps', dtype=torch.float32)
    b32 = torch.randn(size, size, device='mps', dtype=torch.float32)
    
    torch.mps.synchronize()
    start = time.perf_counter()
    for _ in range(20):
        _ = torch.matmul(a32, b32)
    torch.mps.synchronize()
    time32 = (time.perf_counter() - start) / 20 * 1000
    
    # FP16
    a16 = a32.half()
    b16 = b32.half()
    
    torch.mps.synchronize()
    start = time.perf_counter()
    for _ in range(20):
        _ = torch.matmul(a16, b16)
    torch.mps.synchronize()
    time16 = (time.perf_counter() - start) / 20 * 1000
    
    speedup = time32 / time16
    
    results.append({"dtype": "FP32", "time_ms": time32})
    results.append({"dtype": "FP16", "time_ms": time16})
    results.append({"speedup": speedup})
    
    log(f"  FP32: {time32:.2f}ms")
    log(f"  FP16: {time16:.2f}ms")
    log(f"  加速比: {speedup:.2f}x")
    
    return {"status": "success", "results": results}

# ============================================================================
# 主程序
# ============================================================================
def main():
    print("\n" + "="*70)
    print("    🚀 LLM 训练环境本地基准测试")
    print("    Apple M2 Ultra (64GB) - MPS 性能测试")
    print("="*70 + "\n")
    
    results = {}
    
    # 检查 MPS
    log(f"🔧 MPS 状态: {torch.backends.mps.is_available()}")
    log(f"🔧 设备: mps (Apple Silicon)\n")
    
    # 运行基准测试
    benchmarks = [
        ("MatMul", benchmark_matmul),
        ("Memory", benchmark_memory),
        ("Forward", benchmark_forward),
        ("Backward", benchmark_backward),
        ("Activations", benchmark_activations),
        ("FP16", benchmark_fp16),
    ]
    
    for name, func in benchmarks:
        try:
            log(f"\n{'='*50}")
            result = func()
            results[name] = result
        except Exception as e:
            log(f"❌ {name} 失败: {e}")
            results[name] = {"status": "error", "error": str(e)}
    
    # 汇总
    print("\n" + "="*70)
    print("    📊 基准测试结果汇总")
    print("="*70)
    
    for name, result in results.items():
        status = "✅" if result.get("status") == "success" else "❌"
        print(f"{status} {name}")
    
    # 保存
    output_file = os.path.join(REPORT_DIR, "local_benchmark_results.json")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n📁 结果保存: {output_file}")
    
    return results

if __name__ == "__main__":
    main()
