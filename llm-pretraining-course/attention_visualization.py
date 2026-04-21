#!/usr/bin/env python3
"""
注意力机制可视化示例
帮助理解 Self-Attention 如何实现"理解"
"""

import torch
import torch.nn.functional as F

def visualize_attention():
    """
    简化版 Self-Attention 可视化
    展示模型如何处理句子中的词关系
    """
    
    # 示例句子
    sentence = "The cat sat on the mat because it was tired"
    words = sentence.split()
    n_words = len(words)
    
    print("=" * 60)
    print("Self-Attention 可视化示例")
    print("=" * 60)
    print(f"\n句子：{sentence}\n")
    
    # 模拟 Query 和 Key（简化版，实际是学习得到的）
    # 这里用随机向量模拟
    torch.manual_seed(42)  # 固定随机种子
    d_model = 64  # 向量维度
    
    Q = torch.randn(n_words, d_model)  # Query 矩阵
    K = torch.randn(n_words, d_model)  # Key 矩阵
    
    # 计算注意力分数：Q · K^T
    attention_scores = torch.matmul(Q, K.transpose(0, 1)) / (d_model ** 0.5)
    
    # Softmax 归一化
    attention_weights = F.softmax(attention_scores, dim=1)
    
    # 可视化注意力矩阵
    print("注意力权重矩阵（每个词对其他词的关注度）:\n")
    
    # 打印表头
    print("        ", end="")
    for word in words:
        print(f"{word[:6]:<8}", end="")
    print()
    print("-" * 60)
    
    # 打印每一行
    for i, word in enumerate(words):
        print(f"{word[:6]:<8}", end="")
        for j in range(n_words):
            weight = attention_weights[i, j].item()
            # 用颜色深浅表示权重（终端显示）
            if weight > 0.15:
                print(f"\033[91m{weight:.2f}   \033[0m", end="")  # 红色高亮
            elif weight > 0.10:
                print(f"{weight:.2f}   ", end="")
            else:
                print(f"{weight:.2f}   ", end="")
        print()
    
    print("\n" + "=" * 60)
    print("关键观察：")
    print("1. 每个词都会关注与之相关的其他词")
    print("2. 权重高的词对表示当前词更重要")
    print("3. 这就是模型'理解'上下文的数学实现")
    print("=" * 60)
    
    # 特别分析 "it" 的注意力
    it_idx = words.index("it")
    print(f"\n深入分析 'it' 的注意力分布：")
    print("-" * 60)
    
    sorted_indices = torch.argsort(attention_weights[it_idx], descending=True)
    
    for rank, idx in enumerate(sorted_indices[:5]):
        word = words[idx]
        weight = attention_weights[it_idx, idx].item()
        bar = "█" * int(weight * 50)
        print(f"{rank+1}. {word:<10} {weight:.3f} {bar}")
    
    print("\n💡 在真实模型中，'it' 应该高度关注 'cat'（指代关系）")
    print("   这就是模型理解代词指代的机制！")

if __name__ == "__main__":
    visualize_attention()
