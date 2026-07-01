# 源网荷储一体化园区多时间尺度经济调度仿真复现

## 项目说明

本项目用于归档和复现源网荷储一体化园区多时间尺度经济调度仿真实验。项目基于文献公开参数构建仿真数据，比较逻辑判断基准策略、粒子群优化算法（PSO）和差分进化算法（DE）在典型日调度场景下的经济性、运行时间和稳定性。

## 数据说明

`data/` 中的数据为合成仿真数据，不是实际工程原始数据。实验结果依赖当前仿真数据生成逻辑、算法参数和随机种子，不应表述为真实工程实测结论。

## 环境安装

```bash
python -m pip install -r requirements.txt
```

## 实验复现

主实验复现命令：

```bash
python scripts/run_dispatch_simulation.py
```

多典型日运行时间实验命令：

```bash
python scripts/run_multi_day_runtime_comparison.py
```

## 主要输出文件

- `results/core_results.csv`
- `results/algorithm_5run_stats.csv`
- `results/multi_day_runtime_comparison.csv`
- `results/validation_report.md`
- `figures/`
- `paper/`

## 核心结论

在当前仿真算例和参数设置下，PSO 的综合运行成本、平均运行时间和稳定性优于 DE。

## 目录说明

- `scripts/`：实验复现脚本。
- `data/`：合成仿真数据。
- `results/`：实验结果、统计结果和校验报告。
- `figures/`：实验图表。
- `paper/`：论文材料和写作材料。
- `requirements.txt`：Python 依赖列表。

## 注意事项

归档版本未修改调度模型、算法、随机种子、仿真数据生成逻辑或已有实验结果数值。复现实验时应保持当前脚本、数据和参数设置一致。
