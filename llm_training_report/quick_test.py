#!/usr/bin/env python3
"""
精简版 LLM 训练环境测试
专注于本地可用功能，快速验证
"""

import os
import sys
import time
import json
import torch
import psutil
from datetime import datetime

REPORT_DIR = "/Users/hans/.openclaw/workspace/llm_training_report"

def log(msg):
    print(f"⏰ {datetime.now().strftime('%H:%M:%S')} | {msg}")

def get_mem():
    return psutil.Process().memory_info().rss / (1024**3)

# ============================================================================
# 测试 1: PyTorch MPS 基础功能
# ============================================================================
def test_pytorch_mps():
    log("🔧 测试 1: PyTorch MPS 基础功能")
    start_mem = get_mem()
    
    # 检查 MPS
    assert torch.backends.mps.is_available(), "MPS 不可用"
    assert torch.backends.mps.is_built(), "MPS 未构建"
    log("  ✅ MPS 可用")
    
    # 张量运算
    x = torch.randn(1000, 1000, device='mps')
    y = torch.matmul(x, x)
    log(f"  ✅ 张量运算 (1000x1000): {y.shape}")
    
    # 梯度计算
    x = torch.randn(100, 100, device='mps', requires_grad=True)
    y = x.sum()
    y.backward()
    log("  ✅ 自动微分正常")
    
    # 混合精度
    x = torch.randn(100, 100, device='mps', dtype=torch.float16)
    log(f"  ✅ FP16 支持: {x.dtype}")
    
    mem = get_mem()
    return {
        "status": "success",
        "mps_available": True,
        "operations": ["matmul", "autograd", "fp16"],
        "memory_gb": mem,
        "elapsed_sec": 0
    }

# ============================================================================
# 测试 2: 简单神经网络训练
# ============================================================================
def test_simple_training():
    log("🔧 测试 2: 简单神经网络训练")
    start_mem = get_mem()
    start_time = time.time()
    
    class TinyNet(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.layers = torch.nn.ModuleList([
                torch.nn.Linear(128, 256),
                torch.nn.ReLU(),
                torch.nn.Linear(256, 128),
                torch.nn.ReLU(),
                torch.nn.Linear(128, 64),
                torch.nn.Linear(64, 10)
            ])
        
        def forward(self, x):
            for layer in self.layers:
                x = layer(x)
            return x
    
    model = TinyNet().to('mps')
    optimizer = torch.optim.Adam(model.parameters())
    criterion = torch.nn.CrossEntropyLoss()
    
    # 训练循环
    losses = []
    for i in range(100):
        x = torch.randn(32, 128, device='mps')
        y = torch.randint(0, 10, (32,), device='mps')
        
        optimizer.zero_grad()
        pred = model(x)
        loss = criterion(pred, y)
        loss.backward()
        optimizer.step()
        losses.append(loss.item())
        
        if (i + 1) % 25 == 0:
            log(f"    迭代 {i+1}: loss={loss.item():.4f}")
    
    elapsed = time.time() - start_time
    mem = get_mem()
    
    return {
        "status": "success",
        "model": "TinyNet",
        "parameters": sum(p.numel() for p in model.parameters()),
        "iterations": 100,
        "final_loss": losses[-1],
        "avg_loss": sum(losses) / len(losses),
        "memory_gb": mem,
        "elapsed_sec": elapsed
    }

# ============================================================================
# 测试 3: Transformers 加载
# ============================================================================
def test_transformers():
    log("🔧 测试 3: Transformers 模型加载")
    start_mem = get_mem()
    start_time = time.time()
    
    from transformers import GPT2LMHeadModel, GPT2Tokenizer
    
    # 加载 GPT-2 (124M)
    log("  📦 加载 GPT-2 (124M)...")
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    tokenizer.pad_token = tokenizer.eos_token
    
    model = GPT2LMHeadModel.from_pretrained('gpt2')
    model = model.to('mps')
    
    # 生成测试
    log("  🎯 测试文本生成...")
    input_ids = tokenizer.encode("Hello, I am", return_tensors='pt').to('mps')
    with torch.no_grad():
        output = model.generate(input_ids, max_length=20, do_sample=True)
    generated = tokenizer.decode(output[0], skip_special_tokens=True)
    
    mem = get_mem()
    elapsed = time.time() - start_time
    
    log(f"  📝 生成示例: {generated[:50]}...")
    
    return {
        "status": "success",
        "model": "GPT-2",
        "parameters": model.num_parameters(),
        "memory_gb": mem,
        "elapsed_sec": elapsed,
        "sample_output": generated[:100]
    }

# ============================================================================
# 测试 4: PEFT LoRA 配置
# ============================================================================
def test_peft_lora():
    log("🔧 测试 4: PEFT LoRA 配置")
    start_mem = get_mem()
    start_time = time.time()
    
    from transformers import AutoModelForCausalLM
    from peft import LoraConfig, get_peft_model, TaskType
    
    # 使用小模型测试
    model_name = "gpt2"  # 使用 GPT-2 作为测试
    
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model = model.to('mps')
    
    # 配置 LoRA
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=8,
        lora_alpha=16,
        lora_dropout=0.05,
        target_modules=["c_attn", "c_proj", "c_fc"]
    )
    
    lora_model = get_peft_model(model, lora_config)
    lora_model.print_trainable_parameters()
    
    # 简单训练测试
    optimizer = torch.optim.Adam(lora_model.parameters())
    
    for i in range(20):
        x = torch.randint(0, 50257, (4, 32), device='mps')
        y = x.clone()
        
        optimizer.zero_grad()
        outputs = lora_model(input_ids=x, labels=y)
        loss = outputs.loss
        
        if loss.item() > 0 and i < 20:
            loss.backward()
            optimizer.step()
        
        if (i + 1) % 10 == 0:
            log(f"    迭代 {i+1}: loss={loss.item():.4f}")
    
    mem = get_mem()
    elapsed = time.time() - start_time
    
    return {
        "status": "success",
        "base_model": "GPT-2",
        "lora_r": 8,
        "trainable_params": lora_model.num_parameters(only_trainable=True),
        "total_params": model.num_parameters(),
        "memory_gb": mem,
        "elapsed_sec": elapsed
    }

# ============================================================================
# 测试 5: MLX 原生框架
# ============================================================================
def test_mlx():
    log("🔧 测试 5: MLX 原生框架")
    start_mem = get_mem()
    start_time = time.time()
    
    import mlx.core as mx
    import mlx.nn as nn
    import mlx.optimizers as optim
    
    # 检查设备
    devices = mx.list_devices()
    log(f"  📱 MLX 设备: {devices}")
    
    # 简单 MLP
    class MLXNet(nn.Module):
        def __init__(self):
            super().__init__()
            self.layers = [
                nn.Linear(128, 256),
                nn.ReLU(),
                nn.Linear(256, 128),
                nn.ReLU(),
                nn.Linear(128, 10)
            ]
        
        def __call__(self, x):
            for layer in self.layers:
                x = layer(x)
            return x
    
    model = MLXNet()
    num_params = sum(v.size for _, v in model.parameters().items())
    log(f"  📊 模型参数量: {num_params:,}")
    
    # 训练
    optimizer = optim.Adam(learning_rate=1e-3)
    loss_fn = nn.losses.cross_entropy
    
    losses = []
    for i in range(50):
        x = mx.random.normal((32, 128))
        y = mx.random.randint(0, 10, (32,))
        
        logits = model(x)
        loss = loss_fn(logits, y)
        
        grad = mx.grad(loss, model.parameters())
        optimizer.update(model, grad)
        
        losses.append(float(loss))
        
        if (i + 1) % 25 == 0:
            log(f"    迭代 {i+1}: loss={float(loss):.4f}")
    
    elapsed = time.time() - start_time
    mem = get_mem()
    
    return {
        "status": "success",
        "framework": "MLX",
        "parameters": num_params,
        "iterations": 50,
        "final_loss": losses[-1],
        "devices": [str(d) for d in devices],
        "memory_gb": mem,
        "elapsed_sec": elapsed
    }

# ============================================================================
# 测试 6: 量化推理测试
# ============================================================================
def test_quantization():
    log("🔧 测试 6: 量化推理测试")
    start_mem = get_mem()
    start_time = time.time()
    
    from transformers import GPT2LMHeadModel
    import torch.quantization
    
    # 加载模型
    model = GPT2LMHeadModel.from_pretrained('gpt2')
    model = model.to('mps')
    
    # 动态量化 (int8)
    log("  📦 应用动态量化...")
    quantized_model = torch.quantization.quantize_dynamic(
        model,
        {torch.nn.Linear},
        dtype=torch.qint8
    )
    
    # 推理测试
    log("  🎯 量化推理测试...")
    input_ids = torch.randint(0, 50257, (1, 32), device='mps')
    
    with torch.no_grad():
        output = quantized_model(input_ids)
    
    mem = get_mem()
    elapsed = time.time() - start_time
    
    return {
        "status": "success",
        "method": "Dynamic Quantization (int8)",
        "model": "GPT-2",
        "memory_gb": mem,
        "elapsed_sec": elapsed
    }

# ============================================================================
# 主程序
# ============================================================================
def main():
    print("\n" + "="*70)
    print("    🚀 LLM 训练环境精简测试")
    print("    Apple M2 Ultra (64GB) - macOS")
    print("="*70 + "\n")
    
    results = {}
    tests = [
        ("PyTorch_MPS", test_pytorch_mps),
        ("Simple_Training", test_simple_training),
        ("Transformers", test_transformers),
        ("PEFT_LoRA", test_peft_lora),
        ("MLX_Native", test_mlx),
        ("Quantization", test_quantization),
    ]
    
    for name, test_func in tests:
        try:
            log(f"\n{'='*50}")
            result = test_func()
            results[name] = result
            log(f"✅ {name} 完成 | 内存: {result.get('memory_gb', 'N/A'):.2f}GB | 时间: {result.get('elapsed_sec', 0):.2f}s")
        except Exception as e:
            log(f"❌ {name} 失败: {e}")
            results[name] = {"status": "error", "error": str(e)}
    
    # 汇总报告
    print("\n" + "="*70)
    print("    📊 测试结果汇总")
    print("="*70)
    
    success = [k for k, v in results.items() if v.get("status") == "success"]
    failed = [k for k, v in results.items() if v.get("status") != "success"]
    
    print(f"\n✅ 通过: {len(success)}/{len(tests)}")
    for k in success:
        r = results[k]
        print(f"   • {k}: {r.get('elapsed_sec', 0):.2f}s, {r.get('memory_gb', 0):.2f}GB")
    
    if failed:
        print(f"\n❌ 失败: {len(failed)}/{len(tests)}")
        for k in failed:
            print(f"   • {k}: {results[k].get('error', 'Unknown')}")
    
    # 保存结果
    output_file = os.path.join(REPORT_DIR, "quick_test_results.json")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n📁 结果保存: {output_file}")
    
    return results

if __name__ == "__main__":
    main()
