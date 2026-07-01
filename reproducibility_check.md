# 复现检查说明

## 1. 项目信息

- GitHub 仓库：https://github.com/sucGavin/HJZ-intership.git
- 当前 commit hash：`ac3c1d0df6789a0a57dfd166f9e37fadd00431b1`
- 当前分支：`main`
- 项目用途：基于文献公开参数构建源网荷储一体化园区仿真数据，比较逻辑判断基准策略、PSO 和 DE 的调度效果。
- 数据性质：合成仿真数据，不是实际工程原始数据。

## 2. 推荐复现环境

当前归档服务器环境如下：

- 操作系统：Ubuntu 22.04.5 LTS
- Python 版本：Python 3.12.3
- pip 版本：pip 24.0，路径为 `/root/miniconda3/lib/python3.12/site-packages/pip`
- 依赖安装命令：

```bash
python -m pip install -r requirements.txt
```

`requirements.txt` 中列出的依赖如下，当前文件未固定具体版本号：

```text
numpy
pandas
matplotlib
scipy
python-docx
tabulate
```

当前服务器中这些依赖的实际安装版本如下，仅作为复现环境参考：

```text
numpy==2.3.2
pandas==3.0.3
matplotlib==3.10.5
scipy==1.18.0
python-docx==1.2.0
tabulate==0.10.0
```

## 3. 复现步骤

在新电脑或服务器上可按以下步骤复现实验：

```bash
git clone https://github.com/sucGavin/HJZ-intership.git
cd HJZ-intership
python -m pip install -r requirements.txt
python scripts/run_dispatch_simulation.py
python scripts/run_multi_day_runtime_comparison.py
```

如果仓库是私有仓库，需要先配置 GitHub HTTPS token 或 SSH key，确保当前机器有权限 clone 仓库。

## 4. 预期输出文件

运行后应生成或更新以下文件：

- `data/simulated_dispatch_data.csv`
- `results/core_results.csv`
- `results/algorithm_5run_stats.csv`
- `results/multi_day_runtime_comparison.csv`
- `results/validation_report.md`
- `figures/`
- `paper/`

## 5. 预期核心结果

以下结果读取自当前归档版本中的结果文件。

### 5.1 典型日核心调度结果

来源：`results/core_results.csv`

| 算法 | 风电最大可发电量/MWh | 光伏最大可发电量/MWh | 余热发电量/MWh | 计划负荷用电量/MWh | 购电成本/万元 | 综合运行成本/万元 | 算法运行时间/s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 逻辑判断基准策略 | 2360.0419 | 284.2062 | 547.2327 | 5537.5653 | 77.079 | 77.3168 | 0.0 |
| PSO | 2360.0419 | 284.2062 | 547.2327 | 5537.5653 | 76.1393 | 76.6853 | 1.739 |
| DE | 2360.0419 | 284.2062 | 547.2327 | 5537.5653 | 77.2607 | 77.7295 | 6.973 |

### 5.2 PSO 与 DE 的 5 次运行统计结果

来源：`results/algorithm_5run_stats.csv`

| 算法 | 最优综合运行成本/万元 | 平均综合运行成本/万元 | 标准差 | 平均运行时间/s |
| --- | ---: | ---: | ---: | ---: |
| PSO | 76.6853 | 76.822 | 0.1097 | 1.6974 |
| DE | 77.7295 | 77.8939 | 0.1576 | 6.9302 |

### 5.3 多典型日运行时间对比汇总

来源：`results/multi_day_runtime_comparison.csv`

| 样本编号 | 起始时间 | 结束时间 | PSO运行时间/s | DE运行时间/s | DE/PSO时间比 |
| ---: | --- | --- | ---: | ---: | ---: |
| 1 | 2026-01-01 00:00:00 | 2026-01-01 23:45:00 | 1.6477 | 6.8296 | 4.1448 |
| 2 | 2026-01-02 00:00:00 | 2026-01-02 23:45:00 | 1.6756 | 6.8113 | 4.0649 |
| 3 | 2026-01-03 00:00:00 | 2026-01-03 23:45:00 | 1.6556 | 6.8794 | 4.1552 |
| 4 | 2026-01-04 00:00:00 | 2026-01-04 23:45:00 | 1.6595 | 6.9671 | 4.1983 |
| 5 | 2026-01-05 00:00:00 | 2026-01-05 23:45:00 | 1.6423 | 6.7751 | 4.1254 |
| 6 | 2026-01-06 00:00:00 | 2026-01-06 23:45:00 | 1.6356 | 6.6701 | 4.0781 |
| 7 | 2026-01-07 00:00:00 | 2026-01-07 23:45:00 | 1.625 | 6.7926 | 4.18 |

多典型日运行时间汇总：

- PSO 平均运行时间：1.6488 s
- DE 平均运行时间：6.8179 s
- DE 平均耗时约为 PSO 的 4.1352 倍

当前归档结果显示：

- PSO 综合运行成本低于 DE。
- PSO 平均运行时间低于 DE。
- PSO 标准差低于 DE。
- 多典型日运行时间中，DE 平均耗时约为 PSO 的 4.1352 倍。

## 6. 复现一致性检查方法

复现完成后，应重点检查以下文件是否与本文档记录一致：

- `results/core_results.csv`
- `results/algorithm_5run_stats.csv`
- `results/multi_day_runtime_comparison.csv`

建议检查方式：

1. 对照 `results/core_results.csv`，确认三种策略的购电成本、综合运行成本和主要调度结果与本文档一致。
2. 对照 `results/algorithm_5run_stats.csv`，确认 PSO 与 DE 的最优综合运行成本、平均综合运行成本和标准差与本文档一致。
3. 对照 `results/multi_day_runtime_comparison.csv`，确认多典型日样本数量、日期范围和 DE/PSO 时间比量级一致。

不同机器的运行时间可能因硬件性能、系统负载、Python/依赖版本和后台任务而略有差异，这是正常现象；但综合运行成本和主要调度结果应保持一致。

## 7. 注意事项

- 结果依赖当前仿真数据生成逻辑、算法参数和随机种子。
- 不应将结果表述为真实工程实测结论。
- 不同机器的运行时间可能不同，比较时应以同一机器上的相对耗时为准。
- 复现时如需更新依赖版本，应记录 Python、pip 和依赖版本，便于解释运行时间差异。
