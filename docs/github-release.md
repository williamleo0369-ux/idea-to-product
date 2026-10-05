# GitHub 发布说明

建议仓库名：`idea-to-product`。简介：`成器｜idea-to-product：整合策划、设计、开发与内容反馈的 Agent 技能包。`

建议标签：`agent-skills`、`codex`、`ai-workflow`、`product-development`、`design`、`content-strategy`。

## 当前发布包

四个技能、中文 README、独立使用示例、方法来源说明、MIT（仅原创内容）、安装器与验证脚本。发布本仓库即可，不需要上传个人业务项目、技能全集或运行记录。

## 发布操作

在本仓库目录执行。下面命令用于创建公开仓库并推送，执行前应已有发布授权且 `gh auth status` 成功。

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
git status --short
git add README.md SOURCES.md LICENSE .gitignore skills scripts tests examples docs
git commit -m "Release idea-to-product skills v0.3.0"
gh repo create idea-to-product --public --source=. --remote=origin --push
```

若已有同名仓库，先核实归属、内容与 remote，勿重复创建或覆盖。创建结果不确定时查询仓库再重试。首版可建立 `v0.3.0` Release，说明独立技能包、简化校准边界与验证范围。

后续把真实使用发现写成具体问题：输入、预期、实际、相关产物。修改技能后重新检查引用和结构；不能仅凭格式通过宣称流程效果通过实战验证。
