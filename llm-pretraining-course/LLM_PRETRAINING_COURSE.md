# 🤖 大模型预训练完整课程体系

> 基于"低成本预训练经验"理念的系统化学习路径
> 目标：具备大厂面试官问不倒的预训练能力
> 
> **硬件方案**：Mac Studio (M2 Ultra 64GB) 本地学习 + 云端GPU训练

---

## 🎯 课程说明

### 本地 vs 云端分工

| 环境 | 用途 | 框架 |
|------|------|------|
| **Mac Studio本地** | 学习PyTorch框架、跑通代码逻辑、小batch实验 | PyTorch (CPU模式) |
| **云端GPU** | 大模型预训练（1B+参数）、分布式训练 | PyTorch + DeepSpeed + CUDA |

### M2 Ultra 64GB 本地训练说明

```bash
# Mac Studio上PyTorch的行为：
# 1. 不支持CUDA（NVIDIA GPU）
# 2. 支持MPS（Metal Performance Shaders），但加速有限
# 3. 建议：学习用CPU跑通代码，训练用云端GPU

# 本地验证安装
python << 'EOF'
import torch
print(f"PyTorch版本: {torch.__version__}")
print(f"CUDA可用: {torch.cuda.is_available()}")
print(f"MPS可用: {torch.backends.mps.is_available()}")
print(f"运行设备: {'CUDA GPU' if torch.cuda.is_available() else 'CPU/MPS'}")
EOF
```

> **核心原则**：本课程所有代码都基于PyTorch，经验可直接迁移到企业级NVIDIA GPU训练环境。

---

## 📋 课程概述

| 项目 | 内容 |
|------|------|
| **总时长** | 12-16 周（每天 2-3 小时） |
| **前置要求** | Python 基础 + 深度学习基础 |
| **核心理念** | 以小见大、成本可控、面试导向 |
| **最终目标** | 能独立完成预训练项目 + 应对高级面试 |

---

## 🗓️ 完整课程大纲

### 第一阶段：预训练基础认知（1-2 周）

#### Week 1: 大模型全景图

**周一至周二：宏观理解**
- [ ] 理解大模型发展历程（Transformer → GPT → LLaMA → GPT-4）
- [ ] 掌握主流模型架构（Encoder-only, Decoder-only, Encoder-Decoder）
- [ ] 了解模型规模参数（7B, 13B, 70B, 405B）

**周三至周四：预训练本质**
- [ ] 为什么需要预训练？（预训练 vs 微调的本质区别）
- [ ] 预训练的目标函数是什么？
- [ ] Next Token Prediction 的数学原理

**周五至周日：面试准备**
- ❓ **思考题 1**：为什么decoder-only架构成为主流？encoder-decoder有什么劣势？
- ❓ **思考题 2**：预训练为什么要用next token prediction，而不是其他任务？

**周末实践：**
```bash
# 安装环境
conda create -n pretrain python=3.10
conda activate pretrain
pip install torch transformers accelerate
```

---

#### Week 2: 数据工程基础

**周一至周二：数据采集**
- [ ] Common Crawl 数据处理流程
- [ ] 为什么要做数据清洗？（色情、暴力、低质量过滤）
- [ ] 常用数据集（The Pile, RefinedWeb, SlimPajama）

**周三至周四：数据质量**
- [ ] 数据去重策略（MinHash, SimHash）
- [ ] 语言识别与过滤
- [ ] 质量评分模型（Perplexity-based filtering）

**周五至周日：面试准备**
- ❓ **思考题 3**：如果训练数据中有大量重复，会导致什么问题？
- ❓ **思考题 4**：为什么高质量数据比大数据更重要？

**周末实践：**
```bash
# 下载示例数据（可选）
git clone https://github.com/EleutherAI/the-pile.git

# 数据质量检查示例
python << 'EOF'
import re
from collections import Counter

# 简单质量检查
def quality_check(text):
    lines = text.split('\n')
    avg_line_len = sum(len(l) for l in lines) / len(lines)
    char_ratio = len(re.findall(r'[a-zA-Z]', text)) / len(text)
    return {
        'avg_line_len': avg_line_len,
        'char_ratio': char_ratio,
        'is_english': 0.3 < char_ratio < 0.7
    }
EOF
```

---

### 第二阶段：核心训练技术（3-5 周）

#### Week 3: 分布式训练基础

**周一至周二：并行策略**
- [ ] 数据并行（Data Parallel, DP）
- [ ] 模型并行（Tensor Parallel, TP）
- [ ] 流水线并行（Pipeline Parallel, PP）

**周三至周四：ZeRO优化器**
- [ ] ZeRO Stage 1, 2, 3 的区别
- [ ] 为什么ZeRO能节省显存？
- [ ] 混合精度训练（FP16/BF16）

**周五至周日：面试准备**
- ❓ **思考题 5**：如果GPU显存不够，优先用TP还是PP？为什么？
- ❓ **思考题 6**：ZeRO Stage 2和Stage 3的本质区别是什么？

**周末实践（本地小规模）：**
```bash
# 测试你的Mac Studio能否进行小规模训练
python << 'EOF'
import torch
print(f"PyTorch版本: {torch.__version__}")
print(f"CUDA可用: {torch.cuda.is_available()}")
print(f"CUDA可用: {torch.cuda.is_available()}")
print(f"设备数量: {torch.cuda.device_count()}")
print(f"设备: {'CUDA' if torch.cuda.is_available() else 'CPU'}")

# 测试显存
if torch.cuda.is_available():
    print(f"GPU显存: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    print(f"GPU型号: {torch.cuda.get_device_name(0)}")
else:
    print("使用CPU训练（Mac Studio本地学习用，云端需CUDA环境）")
EOF

# 安装DeepSpeed
pip install deepspeed
```

---

#### Week 4: 训练稳定性

**周一至周二：Loss发散问题**
- [ ] 梯度爆炸/消失的识别与解决
- [ ] 学习率warmup的原理
- [ ] Gradient Clipping

**周三至周四：优化器与超参**
- [ ] Adam vs AdamW
- [ ] 学习率调度器（Cosine Annealing, Linear Warmup）
- [ ] Batch Size的选择策略

**周五至周日：面试准备**
- ❓ **思考题 7**：为什么预训练需要warmup？直接用固定学习率会怎样？
- ❓ **思考题 8**：如果Loss突然飙升，可能是什么原因？怎么排查？

**周末实践：**
```python
# 完整训练脚本框架
import torch
import torch.nn as nn
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineWarmupScheduler

class Trainer:
    def __init__(self, model, train_loader, args):
        self.model = model
        self.train_loader = train_loader
        self.args = args

        # 使用混合精度
        self.scaler = torch.cuda.amp.GradScaler()

        # 优化器
        self.optimizer = AdamW(
            model.parameters(),
            lr=args.learning_rate,
            weight_decay=args.weight_decay
        )

        # 学习率调度
        self.scheduler = CosineWarmupScheduler(
            self.optimizer,
            warmup_epochs=args.warmup_epochs,
            total_epochs=args.total_epochs
        )

    def train_epoch(self, epoch):
        self.model.train()
        total_loss = 0

        for step, batch in enumerate(self.train_loader):
            self.optimizer.zero_grad()

            # 混合精度训练
            with torch.cuda.amp.autocast():
                loss = self.model(**batch).loss
                loss = loss / self.args.gradient_accumulation_steps

            # 反向传播
            self.scaler.scale(loss).backward()

            # Gradient Clipping
            self.scaler.unscale_(self.optimizer)
            torch.nn.utils.clip_grad_norm_(
                self.model.parameters(),
                self.args.max_grad_norm
            )

            self.scaler.step(self.optimizer)
            self.scaler.update()

            total_loss += loss.item()

        return total_loss / len(self.train_loader)
```

---

#### Week 5: 高效训练技术

**周一至周二：显存优化**
- [ ] Gradient Checkpointing（以计算换显存）
- [ ] 混合精度训练深入
- [ ] 优化器状态分片

**周三至周四：高效注意力**
- [ ] Flash Attention原理与实现
- [ ] KV Cache优化
- [ ] 分组查询注意力（GQA）

**周五至周日：面试准备**
- ❓ **思考题 9**：Flash Attention相比标准Attention快在哪里？
- ❓ **思考题 10**：为什么LLaMA-2/3使用GQA？相比MHA有什么优势？

**周末实践：**
```bash
# 安装Flash Attention（仅CUDA环境支持）
# Mac Studio本地学习可跳过，云端训练必须安装
pip install flash-attn --no-build-isolation

# 测试（如果你的设备支持CUDA）
python << 'EOF'
import torch
if torch.cuda.is_available():
    try:
        import flash_attn
        print("Flash Attention 可用 ✓")
    except ImportError:
        print("Flash Attention 不可用（需重新安装CUDA版本）")
else:
    print("使用CPU/MPS，Flash Attention不可用（需云端CUDA环境）")

# 使用替代方案：PyTorch Native Attention
python << 'EOF'
import torch.nn.functional as F

def scaled_dot_product_attention(query, key, value):
    """PyTorch原生的高效注意力实现"""
    # Q @ K^T / sqrt(d_k)
    scores = torch.matmul(query, key.transpose(-2, -1)) / math.sqrt(key.size(-1))
    # Softmax
    attn_weights = F.softmax(scores, dim=-1)
    # @ V
    output = torch.matmul(attn_weights, value)
    return output
EOF
```

---

### 第三阶段：完整实战项目（6-9 周）

#### Week 6-7: 小模型预训练（GPT-2级别）

**项目目标**：从头预训练一个100M-300M参数的GPT模型

**周一至周二：项目规划**
- [ ] 确定模型规模（层数、隐藏层维度、头数）
- [ ] 设计数据pipeline
- [ ] 配置训练超参数

**周三至周四：代码实现**
- [ ] 实现GPT模型架构
- [ ] 实现数据预处理
- [ ] 搭建训练循环

**周五至周日：面试准备**
- ❓ **思考题 11**：模型规模如何影响训练稳定性？
- ❓ **思考题 12**：如何判断模型是否欠拟合/过拟合？

**完整代码框架：**
```python
# pretrain_gpt.py - 完整预训练脚本
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import GPT2Config, GPT2LMHeadModel
from deepspeed.ops.adam import FusedAdam
import math

class PretrainConfig:
    # 模型参数
    n_layer = 12
    n_head = 12
    n_embd = 768
    vocab_size = 50257
    seq_len = 1024

    # 训练参数
    batch_size = 8
    learning_rate = 6e-4
    min_lr = 6e-5
    warmup_steps = 2000
    max_steps = 100000
    gradient_accumulation_steps = 4
    max_grad_norm = 1.0

    # 优化器参数
    weight_decay = 0.1
    betas = (0.9, 0.95)

class TextDataset(Dataset):
    def __init__(self, file_path, tokenizer, seq_len):
        with open(file_path, 'r') as f:
            self.texts = f.readlines()
        self.tokenizer = tokenizer
        self.seq_len = seq_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        encoding = self.tokenizer(
            self.texts[idx],
            truncation=True,
            max_length=self.seq_len,
            padding='max_length',
            return_tensors='pt'
        )
        input_ids = encoding['input_ids'].squeeze()
        return {'input_ids': input_ids}

class GPTPreTrainer:
    def __init__(self, config):
        self.config = config

        # 初始化模型
        self.model = GPT2LMHeadModel(GPT2Config(
            n_layer=config.n_layer,
            n_head=config.n_head,
            n_embd=config.n_embd,
            vocab_size=config.vocab_size,
            n_positions=config.seq_len,
        ))

        # 优化器
        self.optimizer = FusedAdam(
            self.model.parameters(),
            lr=config.learning_rate,
            betas=config.betas,
            weight_decay=config.weight_decay
        )

        # 学习率调度
        self.scheduler = self._create_scheduler()

        # 混合精度
        self.scaler = torch.cuda.amp.GradScaler()

    def _create_scheduler(self):
        def lr_lambda(step):
            if step < self.config.warmup_steps:
                return float(step) / float(max(1, self.config.warmup_steps))
            else:
                progress = float(step - self.config.warmup_steps) / float(
                    max(1, self.config.max_steps - self.config.warmup_steps)
                )
                return max(
                    0.0,
                    0.5 * (1.0 + math.cos(math.pi * progress))
                ) * (self.config.min_lr / self.config.learning_rate)

        return torch.optim.lr_scheduler.LambdaLR(
            self.optimizer,
            lr_lambda
        )

    def train(self, train_loader):
        self.model.train()

        for step, batch in enumerate(train_loader):
            input_ids = batch['input_ids'].cuda()

            with torch.cuda.amp.autocast():
                outputs = self.model(input_ids=input_ids)
                loss = outputs.loss / self.config.gradient_accumulation_steps

            self.scaler.scale(loss).backward()

            if (step + 1) % self.config.gradient_accumulation_steps == 0:
                self.scaler.unscale_(self.optimizer)
                torch.nn.utils.clip_grad_norm_(
                    self.model.parameters(),
                    self.config.max_grad_norm
                )

                self.scaler.step(self.optimizer)
                self.scaler.update()
                self.optimizer.zero_grad()
                self.scheduler.step()

            if step % 100 == 0:
                print(f"Step {step}, Loss: {loss.item():.4f}")

            if step >= self.config.max_steps:
                break

        # 保存模型
        self.model.save_pretrained(f"gpt-pretrain-step-{step}")
```

**运行命令：**
```bash
# 单机单卡训练
deepspeed pretrain_gpt.py \
    --deepspeed \
    --ds_config ds_config.json

# 如果没有DeepSpeed，用普通模式
python pretrain_gpt.py
```

---

#### Week 8-9: 继续预训练（Continued Pre-training）

**项目目标**：在现有模型上继续预训练特定领域数据

**技术要点：**
- [ ] 领域数据混合比例（通常95%通用 + 5%领域）
- [ ] 学习率调整（通常降低）
- [ ] 防止灾难性遗忘

**面试问题准备：**
- ❓ **思考题 13**：如何衡量灾难性遗忘的程度？
- ❓ **思考题 14**：继续预训练时，学习率应该如何调整？

---

### 第四阶段：高级主题（10-12 周）

#### Week 10: RLHF与对齐

**周一至周二：RLHF基础**
- [ ] 为什么需要RLHF？
- [ ] SFT（监督微调）vs RLHF
- [ ] PPO算法核心原理

**周三至周四：实践RLHF**
- [ ] Reward Model训练
- [ ] PPO训练循环
- [ ] KL散度约束

**周五至周日：面试准备**
- ❓ **思考题 15**：RLHF为什么比SFT更难训练？
- ❓ **思考题 16**：PPO中的KL散度项起什么作用？

---

#### Week 11: 高效微调技术

**周一至周二：LoRA系列**
- [ ] LoRA原理与实现
- [ ] QLoRA（4-bit量化 + LoRA）
- [ ] 其他高效微调方法（Prefix Tuning, Adapter）

**周三至周四：量化与部署**
- [ ] 4-bit/8-bit量化
- [ ] GGUF格式转换
- [ ] 推理优化（vLLM, TensorRT）

**周五至周日：面试准备**
- ❓ **思考题 17**：LoRA为什么能保持全量微调的效果？
- ❓ **思考题 18**：QLoRA的显存节省原理是什么？

---

#### Week 12: 面试冲刺与项目总结

**周一至周三：高频面试题**
- [ ] 预训练相关面试题整理
- [ ] 系统设计题准备
- [ ] 项目经验复盘

**周四至周六：项目整合**
- [ ] 完成完整项目文档
- [ ] 准备项目展示材料
- [ ] 模拟面试练习

---

## 💻 你的实操环境配置

### 硬件环境

| 组件 | 本地配置（Mac Studio） | 云端配置（训练用） |
|------|----------------------|-------------------|
| **CPU** | Apple Silicon (M系列) | x86_64 (Intel/AMD) |
| **GPU** | 集成GPU（MPS加速有限） | NVIDIA A100/4090 (CUDA) |
| **内存** | 建议16GB+ | 建议64GB+ |
| **存储** | 建议50GB+ | 建议200GB+ |
| **用途** | 代码学习、小规模实验 | 大模型预训练/微调 |

> **说明**：Mac Studio本地主要用于学习PyTorch框架、跑通代码逻辑。真正的大模型训练（1B+参数）需要在云端GPU上进行。

### 本地环境配置

```bash
# 1. 安装Miniconda
cd /tmp
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh
bash Miniconda3-latest-MacOSX-arm64.sh

# 2. 创建虚拟环境
conda create -n pretrain python=3.10 -y
conda activate pretrain

# 3. 安装PyTorch（云端GPU训练用CUDA版本）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 验证安装
python << 'EOF'
import torch
print(f"PyTorch: {torch.__version__}")
print(f"CUDA可用: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA版本: {torch.version.cuda}")
    print(f"GPU显存: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
else:
    print("使用CPU训练（Mac Studio本地学习用，云端需CUDA环境）")
EOF

# 4. 安装核心依赖
pip install \
    transformers \
    datasets \
    accelerate \
    tiktoken \
    numpy \
    tqdm

# 5. 安装DeepSpeed（有限支持）
pip install deepspeed

# 6. 安装可视化工具
pip install \
    tensorboard \
    wandb
```

### 云端资源（用于大规模训练）

由于Mac Studio显存有限，大规模预训练需要云GPU：

| 服务商 | GPU选择 | 价格参考 | 适用场景 |
|--------|---------|----------|----------|
| **阿里云** | A10 (24GB) / A100 (40GB) | ¥10-30/小时 | 100M-1B模型训练 |
| **腾讯云** | GN10 (32GB) | ¥15/小时 | 中等规模训练 |
| **AutoDL** | 4090 (24GB) | ¥2-4/小时 | 性价比最高 |
| **Lambda Labs** | A100 (80GB) | $1-2/小时 | 大规模训练 |

**推荐方案：**
- **Week 1-5**：Mac Studio本地实验（小batch、小模型）
- **Week 6-12**：AutoDL租GPU（RTX 4090，¥2.5/小时）

### 本地 vs 云端任务分配

| 周次 | 任务 | 本地/云端 | 时长 |
|------|------|----------|------|
| Week 1-2 | 数据处理、模型理解 | 本地 | 每天2小时 |
| Week 3-5 | 小规模训练实验 | 本地（减小batch） | 每天2小时 |
| Week 6 | GPT-2规模训练 | 云端（1周） | 每天1小时+ |
| Week 7-9 | 继续预训练实战 | 云端（2周） | 每天1小时+ |
| Week 10-12 | RLHF、高阶实验 | 云端（2周） | 每天1小时+ |

---

## 📚 学习资源推荐

### 必读论文

| 论文 | 主题 | 重要性 |
|------|------|--------|
| Attention Is All You Need | Transformer基础 | ⭐⭐⭐ |
| GPT-3 Paper | Scaling Law | ⭐⭐⭐ |
| LLaMA: Open and Efficient | 公开模型训练 | ⭐⭐⭐ |
| Flash Attention | 高效注意力 | ⭐⭐⭐ |
| LoRA | 高效微调 | ⭐⭐⭐ |
| DeepSpeed & ZeRO | 分布式训练 | ⭐⭐ |
| RLHF Paper (PPO) | 对齐技术 | ⭐⭐ |

### 优质课程

1. **Stanford CS229** - Machine Learning（基础）
2. **Stanford CS224N** - NLP with Deep Learning
3. **Hugging Face Course** - NLP with Transformers
4. **DeepLearning.AI** - LLMs专题课程

### 实战项目参考

1. **TinyStories** - 100M参数模型预训练
2. **RedPajama** - 开源预训练数据集
3. **OpenLLaMA** - 复现LLaMA训练

---

## 📊 面试Checklist

### 基础知识

- [ ] 理解Transformer各层作用
- [ ] 能解释Next Token Prediction
- [ ] 掌握Attention计算复杂度
- [ ] 理解位置编码原理
- [ ] 了解主流模型架构区别

### 训练经验

- [ ] 能配置分布式训练
- [ ] 知道如何调试Loss发散
- [ ] 了解混合精度训练细节
- [ ] 掌握学习率调度策略
- [ ] 理解数据质量的重要性

### 高级话题

- [ ] 能解释LoRA原理
- [ ] 了解RLHF训练流程
- [ ] 知道如何进行模型量化
- [ ] 能设计预训练数据pipeline
- [ ] 了解Scaling Law

---

## 🎯 每周Check-in问题

在每周结束时，问自己：

1. **这周学到的最重要的概念是什么？**
2. **有没有不理解的地方需要再深入？**
3. **代码实践遇到了什么问题？**
4. **下周需要重点加强什么？**
5. **这个知识在实际项目中怎么用？**

---

**文档版本**: v1.0
**创建日期**: 2026-02-07
**最后更新**: 2026-02-07

---

## 下一步

1. ✅ 阅读此课程大纲
2. ⬜ 从Week 1开始执行
3. ⬜ 配置本地环境
4. ⬜ 租用云GPU（如需要）

准备好了就告诉我，我们从Week 1开始！
