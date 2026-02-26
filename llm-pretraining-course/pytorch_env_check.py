#!/usr/bin/env python3
"""
PyTorch 预训练环境验证脚本（简化版）
不下载大模型，只验证核心组件
"""

import torch
import time

print("=" * 60)
print("🎯 PyTorch 预训练环境验证")
print("=" * 60)

# 1. PyTorch信息
print(f"\n📦 PyTorch版本: {torch.__version__}")

# 2. 设备检测
print(f"\n🖥️ 设备检测:")
if torch.cuda.is_available():
    print(f"  ✅ CUDA可用")
    print(f"  GPU数量: {torch.cuda.device_count()}")
    for i in range(torch.cuda.device_count()):
        props = torch.cuda.get_device_properties(i)
        print(f"  GPU {i}: {props.name}")
        print(f"    显存: {props.total_memory / 1e9:.1f} GB")
elif torch.backends.mps.is_available():
    print(f"  ⚠️ MPS可用（Apple Silicon加速）")
    print(f"  说明: 本地学习用，生产训练需云端NVIDIA GPU")
else:
    print(f"  ❌ 使用CPU")
    print(f"  说明: Mac Studio本地仅供学习，生产训练需云端GPU")

# 3. 核心库导入测试
print(f"\n✅ 核心库状态:")
libs = [
    ("torch", torch.__version__),
]

try:
    import transformers
    libs.append(("transformers", transformers.__version__))
except:
    print("  transformers: 未安装 ❌")

try:
    import datasets
    libs.append(("datasets", datasets.__version__))
except:
    print("  datasets: 未安装 ❌")

try:
    import tiktoken
    libs.append(("tiktoken", tiktoken.__version__))
except:
    print("  tiktoken: 未安装 ❌")

for name, version in libs:
    print(f"  {name}: {version}")

# 4. 简单计算测试
print(f"\n🧮 计算性能测试:")
x = torch.randn(1000, 1000)
y = torch.randn(1000, 1000)

start = time.time()
z = torch.matmul(x, y)
elapsed = time.time() - start
print(f"  CPU矩阵乘法 (1000x1000): {elapsed:.3f}s")

if torch.cuda.is_available():
    x_gpu = x.cuda()
    y_gpu = y.cuda()
    start = time.time()
    z_gpu = torch.matmul(x_gpu, y_gpu)
    torch.cuda.synchronize()
    elapsed_gpu = time.time() - start
    print(f"  GPU矩阵乘法: {elapsed_gpu:.4f}s")
    print(f"  加速比: {elapsed/elapsed_gpu:.1f}x")

# 5. PyTorch训练框架测试
print(f"\n🔧 训练框架测试:")
try:
    import torch.nn as nn
    model = nn.Linear(100, 100)
    x = torch.randn(4, 100)
    y = model(x)
    print(f"  ✅ nn.Module: 正常")
    print(f"     Forward形状: {y.shape}")
except Exception as e:
    print(f"  ❌ nn.Module: 失败 - {e}")

try:
    from torch.optim import Adam
    model = nn.Linear(100, 100)
    optimizer = Adam(model.parameters(), lr=1e-3)
    print(f"  ✅ Adam优化器: 正常")
except Exception as e:
    print(f"  ❌ Adam优化器: 失败 - {e}")

try:
    from torch.utils.data import DataLoader, Dataset
    class DummyDataset(Dataset):
        def __len__(self): return 100
        def __getitem__(self, i): return torch.randn(10), torch.randint(0, 10, (1,))
    loader = DataLoader(DummyDataset(), batch_size=4)
    batch = next(iter(loader))
    print(f"  ✅ DataLoader: 正常")
except Exception as e:
    print(f"  ❌ DataLoader: 失败 - {e}")

try:
    from torch.optim.lr_scheduler import CosineAnnealingLR
    model = nn.Linear(100, 100)
    optimizer = Adam(model.parameters(), lr=1e-3)
    scheduler = CosineAnnealingLR(optimizer, T_max=100)
    print(f"  ✅ 学习率调度器: 正常")
except Exception as e:
    print(f"  ❌ 学习率调度器: 失败 - {e}")

# 6. Hugging Face transformers测试（轻量级）
print(f"\n🤗 Hugging Face生态:")
try:
    from transformers import GPT2Config
    config = GPT2Config()
    params = config.vocab_size * config.n_embd  # embedding
    params += config.n_layer * (config.n_embd * config.n_embd * 4 * 3)  # attention
    params += config.n_layer * (config.n_embd * config.n_embd * 4)  # FFN
    params += config.n_embd * config.vocab_size  # lm_head
    print(f"  ✅ transformers配置加载: 正常")
    print(f"     GPT-2参数量: ~{params/1e6:.0f}M (近似)")
except Exception as e:
    print(f"  ❌ transformers配置加载: 失败 - {e}")

try:
    import tiktoken
    enc = tiktoken.get_encoding("gpt2")
    text = "Hello, world!"
    tokens = enc.encode(text)
    decoded = enc.decode(tokens)
    print(f"  ✅ tiktoken分词: 正常")
    print(f"     '{text}' -> {len(tokens)} tokens")
except Exception as e:
    print(f"  ❌ tiktoken分词: 失败 - {e}")

# 7. 总结
print(f"\n" + "=" * 60)
print("✅ PyTorch 环境验证完成！")
print("=" * 60)
print("""
📋 后续步骤:
   1. ✅ 本地学习PyTorch框架
   2. ⏳ 租用云端GPU（如AutoDL A100）
   3. ⏳ 开始大模型预训练实践

💡 提示:
   - Mac Studio本地用CPU/MPS跑通代码
   - 1B+模型训练使用云端NVIDIA GPU
   - 经验可直接迁移到企业级训练

🎯 课程文档: LLM_PRETRAINING_COURSE.md
""")
