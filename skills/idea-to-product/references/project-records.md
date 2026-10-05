# 项目记录契约

文件位于用户当前项目 `.idea-to-product/`，仅在持续追踪有价值时创建。

- `brief.md`：用户原话、目标用户与场景、问题证据、替代方案、价值、范围与不做项、验收标准、验证指标、事实/假设。
- `design.md`：主要任务路径、信息结构、视觉依据、关键状态、平台约束、预览入口、给开发的交接与缺口。
- `delivery.md`：运行方式、配置字段名称（无秘密值）、功能状态、测试命令与结果、外部依赖、交付限制。
- `status.json`：`schema_version`（1）、`project`、`phase`（plan/design/develop/validate）、`updated_at`（含时区）、`artifacts`（相对路径）、`decisions`、`open_questions`、`next_action`。这是 idea-to-product 的状态，不修改 `.cheat-state.json`。

文件创建时间和指标不是示例数据；缺失值写未提供。读取已有状态后保留未知字段，不把“写完文件”当成阶段通过。验收失败时记录具体阻塞和可继续工作，不把状态标为完成。

## 实验状态

`status.json` 可增加 `experiments` 数组：id、phase、prediction_path（回顾可为空）、retro_paths、status（planned/running/supported/contradicted/inconclusive/pending）、window、next_action。保留旧字段，不覆写已有状态。

`experiments/predictions/` 存事前记录和 SHA-256，`experiments/retros/` 存独立复盘，`decisions.md` 存回流决定。内容复用原 content 或上游 cheat 目录，不重复登记。
