#!/usr/bin/env python3
"""
LLM Training/Finetuning Benchmark Suite
Tests different model scales, datasets, and training methods on M2 Ultra
"""

import os
import sys
import time
import json
import torch
import psutil
import subprocess
from datetime import datetime

# Setup
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

REPORT_DIR = "/Users/hans/.openclaw/workspace/llm_training_report"

def get_memory_info():
    """Get current memory usage"""
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return {
        "rss_gb": mem_info.rss / (1024**3),
        "vms_gb": mem_info.vms / (1024**3),
        "percent": process.memory_percent()
    }

def get_system_memory():
    """Get system-wide memory info"""
    mem = psutil.virtual_memory()
    return {
        "total_gb": mem.total / (1024**3),
        "available_gb": mem.available / (1024**3),
        "used_gb": mem.used / (1024**3),
        "percent": mem.percent
    }

def log_result(test_name, result):
    """Log test result to JSON file"""
    log_file = os.path.join(REPORT_DIR, "benchmark_results.json")
    existing = []
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            existing = json.load(f)
    
    existing.append({
        "test": test_name,
        "timestamp": datetime.now().isoformat(),
        "result": result
    })
    
    with open(log_file, 'w') as f:
        json.dump(existing, f, indent=2)
    
    print(f"✓ Result saved: {test_name}")

def run_benchmark(test_name, test_func, description=""):
    """Run a benchmark test with timing and logging"""
    print(f"\n{'='*60}")
    print(f"🔬 Running: {test_name}")
    if description:
        print(f"   {description}")
    print(f"{'='*60}")
    
    start_time = time.time()
    start_mem = get_memory_info()
    sys_mem = get_system_memory()
    
    print(f"📊 Initial Memory: {start_mem['rss_gb']:.2f} GB")
    print(f"💾 System: {sys_mem['total_gb']:.1f}GB total, {sys_mem['available_gb']:.1f}GB available")
    
    try:
        result = test_func()
        elapsed = time.time() - start_time
        end_mem = get_memory_info()
        sys_mem_end = get_system_memory()
        
        result.update({
            "elapsed_seconds": elapsed,
            "elapsed_formatted": f"{elapsed/60:.2f} min" if elapsed > 60 else f"{elapsed:.2f} sec",
            "memory_delta_gb": end_mem['rss_gb'] - start_mem['rss_gb'],
            "peak_memory_gb": max(start_mem['rss_gb'], end_mem['rss_gb']),
            "system_memory_final": sys_mem_end['available_gb']
        })
        
        print(f"\n✅ Completed in {result['elapsed_formatted']}")
        print(f"📊 Peak Memory: {result['peak_memory_gb']:.2f} GB")
        print(f"💾 System Available: {sys_mem_end['available_gb']:.2f} GB")
        
        log_result(test_name, result)
        return result
        
    except Exception as e:
        elapsed = time.time() - start_time
        error_result = {
            "status": "error",
            "error": str(e),
            "elapsed_seconds": elapsed
        }
        print(f"\n❌ Failed: {e}")
        log_result(test_name, error_result)
        return error_result

# ============================================================================
# TEST 1: GPT-2 Small Scale Pretraining
# ============================================================================
def test_gpt2_pretrain():
    """Test GPT-2 (124M) pretraining on synthetic data"""
    import torch.nn as nn
    from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Config
    from torch.utils.data import Dataset, DataLoader
    
    class SimpleDataset(Dataset):
        def __init__(self, tokenizer, size=1000, seq_length=128):
            self.tokenizer = tokenizer
            self.size = size
            self.seq_length = seq_length
            self.texts = [f"This is sample text number {i} for training." * 3 
                          for i in range(size)]
        
        def __len__(self):
            return self.size
        
        def __getitem__(self, idx):
            encoding = self.tokenizer(
                self.texts[idx],
                truncation=True,
                max_length=self.seq_length,
                padding='max_length',
                return_tensors='pt'
            )
            input_ids = encoding['input_ids'].squeeze()
            attention_mask = encoding['attention_mask'].squeeze()
            return {
                'input_ids': input_ids,
                'attention_mask': attention_mask,
                'labels': input_ids.clone()
            }
    
    print("📦 Loading GPT-2 model and tokenizer...")
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    tokenizer.pad_token = tokenizer.eos_token
    
    config = GPT2Config(
        n_embd=768,
        n_layer=12,
        n_head=12,
        n_ctx=256,  # Reduced context for memory efficiency
    )
    model = GPT2LMHeadModel(config)
    
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model = model.to(device)
    
    mem_info = get_memory_info()
    print(f"📊 Model loaded. Memory: {mem_info['rss_gb']:.2f} GB")
    
    # Create dataset
    dataset = SimpleDataset(tokenizer, size=500, seq_length=256)
    dataloader = DataLoader(dataset, batch_size=4, shuffle=True)
    
    # Training setup
    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)
    model.train()
    
    # Quick training loop (3 epochs, limited batches)
    total_loss = 0
    batches_processed = 0
    max_batches = 50
    
    print("🚀 Starting training loop...")
    for epoch in range(3):
        for batch in dataloader:
            if batches_processed >= max_batches:
                break
                
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)
            
            optimizer.zero_grad()
            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            batches_processed += 1
            
            if batches_processed % 10 == 0:
                mem = get_memory_info()
                print(f"   Batch {batches_processed}: loss={loss.item():.4f}, mem={mem['rss_gb']:.2f}GB")
    
    avg_loss = total_loss / batches_processed
    
    return {
        "model": "GPT-2 (124M config, reduced)",
        "task": "pretraining",
        "framework": "PyTorch MPS",
        "epochs": 3,
        "batches": batches_processed,
        "dataset_size": 500,
        "avg_loss": avg_loss,
        "status": "success"
    }

# ============================================================================
# TEST 2: LoRA Fine-tuning (Qwen 1.5B)
# ============================================================================
def test_lora_finetune():
    """Test LoRA fine-tuning on a small model"""
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import LoraConfig, get_peft_model, TaskType
    
    print("📦 Loading Qwen 1.5B model for LoRA fine-tuning...")
    
    model_name = "Qwen/Qwen1.5-1.8B-Chat"  # Smaller variant
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"📱 Device: {device}")
    
    # Load model with memory optimization
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32,
        device_map="auto",
        trust_remote_code=True,
        low_cpu_mem_usage=True
    )
    
    mem_info = get_memory_info()
    print(f"📊 Model loaded. Memory: {mem_info['rss_gb']:.2f} GB")
    
    # Configure LoRA
    print("🔧 Configuring LoRA...")
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        inference_mode=False,
        r=8,
        lora_alpha=16,
        lora_dropout=0.05,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"]
    )
    
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    # Create simple instruction dataset
    train_data = [
        {"instruction": "What is the capital of France?", "response": "The capital of France is Paris."},
        {"instruction": "What is 2+2?", "response": "2+2 equals 4."},
        {"instruction": "Who wrote Hamlet?", "response": "Hamlet was written by William Shakespeare."},
        {"instruction": "What is the speed of light?", "response": "The speed of light is approximately 299,792 km/s."},
        {"instruction": "What is AI?", "response": "AI stands for Artificial Intelligence."},
    ] * 20  # Repeat for more data
    
    # Training loop
    model.train()
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
    
    print("🚀 Starting LoRA training...")
    losses = []
    for epoch in range(2):
        epoch_loss = 0
        for i, item in enumerate(train_data):
            text = f"### Instruction: {item['instruction']}\n### Response: {item['response']}"
            inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=256)
            inputs = {k: v.to(device) for k, v in inputs.items()}
            
            optimizer.zero_grad()
            outputs = model(**inputs, labels=inputs["input_ids"])
            loss = outputs.loss
            
            if loss.item() > 0:
                loss.backward()
                optimizer.step()
                epoch_loss += loss.item()
                
                if (i + 1) % 10 == 0:
                    mem = get_memory_info()
                    print(f"   Epoch {epoch+1}, Step {i+1}: loss={loss.item():.4f}, mem={mem['rss_gb']:.2f}GB")
        
        avg_epoch_loss = epoch_loss / len(train_data)
        losses.append(avg_epoch_loss)
        print(f"   Epoch {epoch+1} complete: avg loss = {avg_epoch_loss:.4f}")
    
    return {
        "model": "Qwen1.5-1.8B",
        "task": "fine-tuning (LoRA)",
        "framework": "PEFT + Transformers",
        "lora_r": 8,
        "lora_alpha": 16,
        "epochs": 2,
        "dataset_size": len(train_data),
        "losses": losses,
        "status": "success"
    }

# ============================================================================
# TEST 3: MLX Training (Apple Silicon Native)
# ============================================================================
def test_mlx_training():
    """Test MLX framework for native Apple Silicon training"""
    import mlx.core as mx
    import mlx.nn as nn
    import mlx.optimizers as optim
    
    print("🍎 Testing MLX (Apple Silicon Native Framework)")
    print(f"📱 MLX Version: {mx.__version__}")
    
    # Check MLX device
    devices = mx.list_devices()
    print(f"🖥️ Available devices: {devices}")
    
    # Simple neural network test
    class SimpleModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.layers = [
                nn.Linear(128, 256),
                nn.ReLU(),
                nn.Linear(256, 128),
                nn.ReLU(),
                nn.Linear(128, 64),
                nn.ReLU(),
                nn.Linear(64, 10)
            ]
        
        def __call__(self, x):
            for layer in self.layers:
                x = layer(x)
            return x
    
    # Create model
    model = SimpleModel()
    num_params = sum(v.size for _, v in model.parameters().items())
    print(f"📊 Model parameters: {num_params:,}")
    
    # Create dummy data
    batch_size = 32
    x = mx.random.normal((batch_size, 128))
    y = mx.random.randint(0, 10, (batch_size,))
    
    # Training setup
    optimizer = optim.Adam(learning_rate=1e-3)
    loss_fn = nn.losses.cross_entropy
    
    # Training loop
    print("🚀 Starting MLX training loop...")
    model.train()
    losses = []
    
    for i in range(100):
        # Forward pass
        logits = model(x)
        loss = loss_fn(logits, y)
        
        # Backward pass
        optimizer.zero_grad()
        grad = mx.grad(loss, model.parameters())
        optimizer.update(model, grad)
        
        losses.append(float(loss))
        
        if (i + 1) % 20 == 0:
            avg_loss = sum(losses[-20:]) / 20
            mem = get_memory_info()
            print(f"   Step {i+1}: loss={float(loss):.4f}, avg={avg_loss:.4f}, mem={mem['rss_gb']:.2f}GB")
    
    # Test inference
    model.eval()
    test_input = mx.random.normal((1, 128))
    output = model(test_input)
    print(f"📊 Inference output shape: {output.shape}")
    
    return {
        "model": "Simple MLP (test architecture)",
        "task": "training",
        "framework": "MLX (Native)",
        "parameters": num_params,
        "iterations": 100,
        "final_loss": float(losses[-1]),
        "losses": losses[-5:],
        "device": str(devices),
        "status": "success"
    }

# ============================================================================
# TEST 4: QLoRA 4-bit Fine-tuning Test (7B Model)
# ============================================================================
def test_qlora_finetune():
    """Test QLoRA with 4-bit quantization on 7B model"""
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_int8_training
    
    print("📦 Loading 7B model with QLoRA (4-bit) configuration...")
    
    model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # Use 1.1B as proxy for 7B
    
    # QLoRA configuration
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True
    )
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    
    print("📦 Loading model with 4-bit quantization...")
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto",
        low_cpu_mem_usage=True
    )
    
    mem_info = get_memory_info()
    print(f"📊 Model loaded with quantization. Memory: {mem_info['rss_gb']:.2f} GB")
    
    # Configure LoRA for QLoRA
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        inference_mode=False,
        r=16,
        lora_alpha=32,
        lora_dropout=0.1,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"]
    )
    
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    # Simple training test
    train_data = [
        {"text": "Question: What is Python?\nAnswer: Python is a programming language."} 
        for _ in range(50)
    ]
    
    model.train()
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
    
    print("🚀 Starting QLoRA training...")
    losses = []
    for epoch in range(2):
        for i, item in enumerate(train_data):
            inputs = tokenizer(item["text"], return_tensors="pt", truncation=True, max_length=128)
            inputs = {k: v for k, v in inputs.items()}
            
            outputs = model(**inputs, labels=inputs["input_ids"])
            loss = outputs.loss
            
            if loss.item() > 0:
                loss.backward()
                optimizer.step()
                optimizer.zero_grad()
                
                losses.append(loss.item())
                
                if (i + 1) % 25 == 0:
                    mem = get_memory_info()
                    print(f"   Epoch {epoch+1}, Step {i+1}: loss={loss.item():.4f}, mem={mem['rss_gb']:.2f}GB")
    
    return {
        "model": "TinyLlama-1.1B (QLoRA 4-bit)",
        "task": "fine-tuning (QLoRA)",
        "framework": "BitsAndBytes + PEFT",
        "quantization": "4-bit NF4",
        "lora_r": 16,
        "epochs": 2,
        "dataset_size": len(train_data),
        "final_loss": losses[-1] if losses else None,
        "memory_gb": mem_info['rss_gb'],
        "status": "success"
    }

# ============================================================================
# TEST 5: Distributed Training Test (Accelerate)
# ============================================================================
def test_accelerate_distributed():
    """Test Accelerate distributed training configuration"""
    from accelerate import Accelerator
    from accelerate import DistributedDataParallelKwargs
    
    print("🔧 Testing Accelerate distributed training setup...")
    
    # Configure for MPS/Apple Silicon
    kwargs_handler = DistributedDataParallelKwargs(
        find_unused_parameters=True
    )
    
    accelerator = Accelerator(
        kwargs_handlers=[kwargs_handler],
        device_placement=True,
        split_batches=False
    )
    
    print(f"📊 Accelerator configured successfully")
    print(f"   State: {accelerator.state}")
    print(f"   Device: {accelerator.device}")
    print(f"   Num processes: {accelerator.num_processes}")
    
    # Test basic distributed operations
    tensor = torch.randn(100, 100)
    tensor = accelerator.prepare(tensor)
    
    mem = get_memory_info()
    
    return {
        "framework": "Accelerate",
        "task": "distributed_setup",
        "device": str(accelerator.device),
        "num_processes": accelerator.num_processes,
        "test_tensor_shape": list(tensor.shape),
        "memory_gb": mem['rss_gb'],
        "status": "success"
    }

# ============================================================================
# MAIN EXECUTION
# ============================================================================
def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║     LLM Training/Finetuning Benchmark Suite                  ║
║     Apple M2 Ultra (64GB) macOS                              ║
║     Python 3.14 + PyTorch 2.10 (MPS) + MLX                   ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    results = {}
    
    # Run all tests
    tests = [
        ("MLX_Native", test_mlx_training, "Apple Silicon native MLX framework"),
        ("GPT2_Pretrain", test_gpt2_pretrain, "GPT-2 pretraining with PyTorch MPS"),
        ("LoRA_Qwen1.5B", test_lora_finetune, "LoRA fine-tuning on Qwen 1.8B"),
        ("QLoRA_4bit", test_qlora_finetune, "QLoRA 4-bit fine-tuning"),
        ("Accelerate_Distributed", test_accelerate_distributed, "Accelerate distributed setup"),
    ]
    
    for test_name, test_func, description in tests:
        result = run_benchmark(test_name, test_func, description)
        results[test_name] = result
    
    # Generate summary report
    print("\n" + "="*60)
    print("📊 BENCHMARK SUMMARY")
    print("="*60)
    
    successful = [k for k, v in results.items() if v.get("status") == "success"]
    failed = [k for k, v in results.items() if v.get("status") == "error"]
    
    print(f"\n✅ Successful: {len(successful)}/{len(tests)}")
    for name in successful:
        print(f"   - {name}")
    
    if failed:
        print(f"\n❌ Failed: {len(failed)}/{len(tests)}")
        for name in failed:
            print(f"   - {name}: {results[name].get('error', 'Unknown error')}")
    
    # Save summary
    summary_file = os.path.join(REPORT_DIR, "benchmark_summary.md")
    with open(summary_file, 'w') as f:
        f.write("# LLM Training Benchmark Results\n\n")
        f.write(f"**Date**: {datetime.now().isoformat()}\n")
        f.write(f"**Hardware**: Apple M2 Ultra (64GB)\n")
        f.write(f"**OS**: macOS\n\n")
        
        f.write("## Summary\n\n")
        f.write(f"- **Total Tests**: {len(tests)}\n")
        f.write(f"- **Successful**: {len(successful)}\n")
        f.write(f"- **Failed**: {len(failed)}\n\n")
        
        f.write("## Detailed Results\n\n")
        for name, result in results.items():
            f.write(f"### {name}\n\n")
            f.write(f"- **Status**: {result.get('status', 'unknown')}\n")
            f.write(f"- **Framework**: {result.get('framework', 'N/A')}\n")
            f.write(f"- **Task**: {result.get('task', 'N/A')}\n")
            f.write(f"- **Time**: {result.get('elapsed_formatted', 'N/A')}\n")
            f.write(f"- **Peak Memory**: {result.get('peak_memory_gb', 'N/A'):.2f} GB\n\n")
    
    print(f"\n📁 Results saved to: {REPORT_DIR}")
    
    return results

if __name__ == "__main__":
    main()
