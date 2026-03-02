更高级的思维方式通常在这些维度上突破：

前瞻性（lookahead / planning depth）
目标导向（goal reasoning 而非 rule following）
不确定性建模（probabilistic / utility scoring）
自适应/学习（incorporate ML / self-improvement）
多智能体协作（orchestration across agents）


BT = 优秀的前线士兵：每秒看一眼情况，选最高优先任务执行（reactive checklist）。
Utility AI = 更聪明的参谋：给每个选项打分（e.g. “逃跑 utility=0.9 因为血低”），选最高分的（context-sensitive scoring）。
GOAP / HTN = 战略家：不是选当前动作，而是“目标是活下去 → 我要先找掩体 → 再射击 → 最后撤退”，自动搜路径（deliberative planning）。
MCTS = 赌徒+棋手：脑补几百次未来模拟，“这条路赢面大就多走这条”（handling uncertainty via simulation）。
Agentic / Multi-Agent = CEO + 团队：不只自己干活，还能“反思我刚才计划错了吗”“叫其他 agent 来帮忙”“用工具查信息再决定”（goal-directed, reflective, collaborative）。

中断/并行/优先级/调试都变得更麻烦

AI具备“响应性”的关键机制

必须是条件节点才能监听状态变化来打断别人

库名成熟度/社区异步支持可视化工具ROS/机器人友好LLM 集成推荐场景
py_trees★★★★★部分优秀★★★★★一般机器人、主流选择
BehaviorTree.py★★★★否Groot★★★★一般与 C++ 风格一致的项目
async-btree★★★是一般★★★一般异步/并发代理
Dendron★★★是一般★★★★★★★LLM 驱动的智能代理

Behavior Tree 的全部“智能”和流程控制都建立在节点 tick 后返回的 SUCCESS / FAILURE / RUNNING 这三个状态上

prompt

## Conda


在 base（根）环境中安装 nb_conda_kernels（只需一次）：text

conda install nb_conda_kernels
对于每个你想用的 Conda 环境：text 
conda create -n myenv python=3.11          # 创建环境（如果还没有）
conda activate myenv
conda install ipykernel                     # 安装 kernel 支持
启动 Jupyter（从 base 环境启动即可）：text
conda activate base
jupyter lab    # 或 jupyter notebook

conda config --set proxy_servers.http http://127.0.0.1:7890
conda config --set proxy_servers.https http://127.0.0.1:7890

jupyter kernelspec list

conda env list

jupyter lab --no-browser

conda remove -n 环境名 --all

conda deactivate

jupyter notebook

# 方法A：最常用（带 GPU 支持，如果有 NVIDIA 显卡）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126

# 方法B：只用 CPU（笔记本没独显或服务器无 GPU 时用这个）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu